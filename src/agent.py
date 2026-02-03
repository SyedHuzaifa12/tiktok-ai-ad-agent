"""
Core AI Agent - The Brain of the System
Handles conversation flow, LLM calls, and orchestration
"""

import json
import time
from typing import Dict, Any, Optional, Tuple
from google import genai

from .config import settings
from .state import AdCampaignState, ConversationStage, MusicChoice
from .validators import (
    FieldValidator,
    MusicValidator,
    validate_complete_campaign,
    AdCampaignData
)
from .tiktok_api import TikTokAPI, APIResponse, interpret_api_error
from .tiktok_auth import TikTokOAuth
from .prompts import (
    SYSTEM_PROMPT,
    create_user_prompt,
    MUSIC_VALIDATION_PROMPT,
    FINAL_REVIEW_PROMPT,
    SUBMISSION_RESULT_PROMPT,
    ERROR_RECOVERY_PROMPT
)


class TikTokAdAgent:
    """
    Main AI Agent for TikTok Ad Campaign Creation
    
    Responsibilities:
    - Manage conversation state
    - Call Gemini LLM for responses
    - Validate inputs using business rules
    - Coordinate with TikTok API
    - Handle errors gracefully
    """
    
    def __init__(self):
        """Initialize agent with real or mock API based on configuration"""
    
        # Initialize Gemini
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_name = settings.gemini_model
    
        # Initialize state
        self.state = AdCampaignState()
    
        # Initialize TikTok API (real or mock)
        if settings.tiktok_mock_mode:
            print("⚠️  Running in MOCK mode (no real API credentials)")
            from .tiktok_api import TikTokAPI
            self.api = TikTokAPI(mock_mode=True)
        else:
            print("✅ Running in REAL API mode")
            from .tiktok_real_api import TikTokRealAPI, TikTokConfig
        
            # Create config from settings
            config = TikTokConfig(
                app_id=settings.tiktok_app_id,
                app_secret=settings.tiktok_app_secret,
                access_token=settings.tiktok_access_token,
                advertiser_id=settings.tiktok_advertiser_id
            )
        
            # Initialize real API
            self.api = TikTokRealAPI(config)
        
            # Test connection
            success, message = self.api.test_connection()
            print(f"   {message}")
        
            if not success:
                print("   ⚠️  API connection failed - check credentials")
                print("   💡 Verify TIKTOK_ACCESS_TOKEN and TIKTOK_ADVERTISER_ID in .env")
    
        print(f"\n✅ Agent initialized")
        print(f"   Model: {self.model_name}")
        print(f"   Mode: {'MOCK' if settings.tiktok_mock_mode else 'REAL API'}\n")
    def _initialize_oauth(self):
        """Initialize OAuth authentication"""
        try:
            self.oauth.simulate_full_oauth_flow()
            self.state.conversation_history.append({
                "role": "system",
                "content": "OAuth authentication successful"
            })
        except Exception as e:
            print(f"⚠️ OAuth initialization warning: {e}")
            print("   Continuing in mock mode...")
    
    def _call_llm(self, user_message: str) -> Dict[str, Any]:
        """
        Calls Gemini LLM with structured output
        
        Args:
            user_message: User's input
            
        Returns:
            Parsed JSON response from LLM
        """
        try:
            # Build prompt with context
            prompt = create_user_prompt(
                user_message=user_message,
                current_data={
                    "campaign_name": self.state.campaign_name,
                    "objective": self.state.objective,
                    "ad_text": self.state.ad_text,
                    "cta": self.state.cta,
                    "music_id": self.state.music_id
                },
                conversation_history=self.state.conversation_history
            )
            
            # Combine system prompt with user prompt
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Task:\n{prompt}"
            
            # Call Gemini with new SDK syntax
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            parsed = json.loads(response_text)
            
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse LLM response as JSON: {e}")
            print(f"Raw response: {response_text[:200]}")
            
            # Fallback response
            return {
                "message": "I apologize, I had trouble processing that. Could you please rephrase?",
                "action": "error",
                "data": {},
                "validation_errors": ["LLM response parsing error"],
                "next_step": "retry"
            }
        
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return {
                "message": "I encountered an error. Let's try again.",
                "action": "error",
                "data": {},
                "validation_errors": [str(e)],
                "next_step": "retry"
            }
    
    def process_message(self, user_message: str) -> str:
        """
        Main entry point - processes user message and returns response
        
        Args:
            user_message: User's input message
            
        Returns:
            Agent's response message
        """
        # Add to conversation history
        self.state.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get LLM response
        llm_response = self._call_llm(user_message)
        
        # Extract components
        message = llm_response.get("message", "")
        action = llm_response.get("action", "")
        data = llm_response.get("data", {})
        
        # Update state with new data
        self._update_state_from_data(data)
        
        # Handle specific actions
        if action == "validate_music":
            message = self._handle_music_validation()
        elif action == "finalize":
            message = self._handle_finalization()
        elif action == "submit":
            message = self._handle_submission()
        
        # Add assistant response to history
        self.state.conversation_history.append({
            "role": "assistant",
            "content": message
        })
        
        return message
    
    def _update_state_from_data(self, data: Dict[str, Any]):
        """Updates state with data from LLM response"""
        if data.get("campaign_name"):
            self.state.campaign_name = data["campaign_name"]
        if data.get("objective"):
            self.state.objective = data["objective"]
        if data.get("ad_text"):
            self.state.ad_text = data["ad_text"]
        if data.get("cta"):
            self.state.cta = data["cta"]
        if data.get("music_id"):
            self.state.music_id = data["music_id"]
    
    def _handle_music_validation(self) -> str:
        """
        Handles music ID validation via API
        This is CASE A: Existing Music ID
        """
        if not self.state.music_id:
            return "⚠️ No music ID provided to validate."
        
        print(f"\n🔍 Validating music ID: {self.state.music_id}")
        
        # Call API
        response = self.api.validate_music(self.state.music_id)
        
        if response.success:
            music_data = response.data
            return (
                f"✅ Music validated successfully!\n\n"
                f"🎵 **{music_data['title']}** by {music_data['artist']}\n"
                f"   Duration: {music_data['duration']} seconds\n"
                f"   Status: {music_data['status']}\n\n"
                f"Great choice! Ready to proceed with campaign creation?"
            )
        else:
            # Interpret error
            error_explanation = interpret_api_error(response)
            
            return (
                f"{error_explanation}\n\n"
                f"What would you like to do?\n"
                f"1. Try a different Music ID\n"
                f"2. Upload custom music\n"
                f"3. Proceed without music (only if Traffic campaign)"
            )
    
    def handle_music_upload(self, file_name: str) -> str:
        """
        Handles custom music upload
        This is CASE B: Custom Upload
        """
        print(f"\n📤 Uploading custom music: {file_name}")
        
        # Simulate upload
        response = self.api.simulate_music_upload(file_name)
        
        if response.success:
            self.state.music_id = response.data['music_id']
            return (
                f"✅ Music uploaded successfully!\n\n"
                f"🎵 File: {file_name}\n"
                f"   Music ID: {response.data['music_id']}\n"
                f"   Status: {response.data['status']}\n\n"
                f"{response.data['message']}\n\n"
                f"Your music will be ready shortly. Ready to proceed?"
            )
        else:
            error_explanation = interpret_api_error(response)
            return (
                f"{error_explanation}\n\n"
                f"Would you like to:\n"
                f"1. Try uploading a different file\n"
                f"2. Use an existing Music ID instead"
            )
    
    def _handle_finalization(self) -> str:
        """Handles campaign finalization - final review before submission"""
        
        # Validate all fields
        is_valid, errors = validate_complete_campaign(
            campaign_name=self.state.campaign_name or "",
            objective=self.state.objective or "Traffic",
            ad_text=self.state.ad_text or "",
            cta=self.state.cta or "",
            music_id=self.state.music_id
        )
        
        if not is_valid:
            error_message = "\n".join(f"  • {err}" for err in errors)
            return (
                f"⚠️ Cannot proceed - some fields are invalid:\n\n"
                f"{error_message}\n\n"
                f"Please provide the missing information."
            )
        
        # Build final summary
        music_status = self.state.music_id if self.state.music_id else "No music"
        
        summary = f"""
📋 **Campaign Summary**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Campaign Name:** {self.state.campaign_name}
**Objective:** {self.state.objective}
**Ad Text:** "{self.state.ad_text}"
**CTA:** {self.state.cta}
**Music:** {music_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Everything look good? 

Reply with:
  • "yes" or "submit" to create the campaign
  • "change [field]" to modify something
  • "cancel" to start over
"""
        
        return summary
    
    def _handle_submission(self) -> str:
        """Handles campaign submission to TikTok API"""
        
        print("\n📤 Submitting campaign to TikTok Ads...")
        
        # Create payload
        try:
            campaign = AdCampaignData(
                campaign_name=self.state.campaign_name,
                objective=self.state.objective,
                ad_text=self.state.ad_text,
                cta=self.state.cta,
                music_id=self.state.music_id
            )
            
            payload = campaign.dict()
            
        except Exception as e:
            return f"❌ Validation error: {str(e)}"
        
        # Submit to API (different handling for real vs mock)
        if settings.tiktok_mock_mode:
        # Mock API
            response = self.api.submit_campaign(payload)
    
            if response.success:
                campaign_data = response.data
                self.state.stage = ConversationStage.COMPLETE
        
                return f"""
        🎉 **Campaign Created! (Mock Mode)**

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        **Campaign ID:** {campaign_data['campaign_id']}
        **Name:** {campaign_data['campaign_name']}
        **Status:** {campaign_data['status']}

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        📊 Dashboard: {campaign_data['dashboard_url']}

        ⚠️ **Note:** This is simulated. To create real campaigns:
            1. Add TikTok credentials to .env
            2. Set TIKTOK_MOCK_MODE=false
            3. Restart the agent

        Create another? Type "new campaign"!
        """
        else:
            # Real TikTok API
            success, result = self.api.create_campaign(payload)
    
            if success:
                self.state.stage = ConversationStage.COMPLETE
        
                return f"""
        🎉 **REAL Campaign Created on TikTok!**

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        **Campaign ID:** {result['campaign_id']}
        **Name:** {result['campaign_name']}
        **Status:** {result['status']}

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ✅ {result['message']}

        📊 TikTok Ads Manager: {result['dashboard_url']}

        🎯 This is a REAL campaign on TikTok!

        **Next Steps:**
        1. Visit TikTok Ads Manager
        2. Complete ad group and creative setup
        3. Set budget and schedule
        4. Launch campaign!

        Create another? Type "new campaign"!
    """
            else:
                return f"""
        ❌ **Campaign Creation Failed**

        {result.get('message', 'Unknown error')}

        **Suggestion:** {result.get('suggestion', 'Check logs for details')}

        **What to check:**
        1. Access token is valid
        2. Advertiser ID is correct
        3. API permissions granted
        4. Network connection stable

        Type "retry" to try again.
        """
    
    def get_greeting(self) -> str:
        """Returns initial greeting message"""
        return """
🎯 **Welcome to TikTok Ad Campaign Creator!**

I'll help you create a professional TikTok ad campaign step-by-step.

We'll need to collect:
  • Campaign name
  • Campaign objective (Traffic or Conversions)
  • Ad text (max 100 characters)
  • Call-to-action (CTA)
  • Music (required for Conversions, optional for Traffic)

✅ **Ready to get started?** 

What would you like to name your campaign?
"""