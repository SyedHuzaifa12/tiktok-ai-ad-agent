"""
Conversation state management
Single source of truth for ad campaign data
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum


class ConversationStage(str, Enum):
    """Tracks where we are in the conversation"""
    GREETING = "greeting"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_OBJECTIVE = "collecting_objective"
    COLLECTING_AD_TEXT = "collecting_ad_text"
    COLLECTING_CTA = "collecting_cta"
    HANDLING_MUSIC = "handling_music"
    VALIDATING_MUSIC = "validating_music"
    FINALIZING = "finalizing"
    SUBMITTING = "submitting"
    COMPLETE = "complete"
    ERROR = "error"


class MusicChoice(str, Enum):
    """User's music selection"""
    EXISTING_ID = "existing_id"
    CUSTOM_UPLOAD = "custom_upload"
    NO_MUSIC = "no_music"
    NOT_DECIDED = "not_decided"


class AdCampaignState(BaseModel):
    """
    Central state object for the entire conversation
    All validations happen here
    """
    
    # Conversation management
    stage: ConversationStage = ConversationStage.GREETING
    conversation_history: list[dict] = Field(default_factory=list)
    
    # Campaign data
    campaign_name: Optional[str] = None
    objective: Optional[Literal["Traffic", "Conversions"]] = None
    ad_text: Optional[str] = None
    cta: Optional[str] = None
    
    # Music handling
    music_choice: MusicChoice = MusicChoice.NOT_DECIDED
    music_id: Optional[str] = None
    
    # Validation and errors
    validation_errors: list[str] = Field(default_factory=list)
    last_api_error: Optional[str] = None
    
    def is_ready_for_submission(self) -> bool:
        """Check if all required fields are collected and valid"""
        if not all([self.campaign_name, self.objective, self.ad_text, self.cta]):
            return False
        
        # Music validation based on objective
        if self.objective == "Conversions" and not self.music_id:
            return False
        
        return True
    
    def to_payload(self) -> dict:
        """Convert to TikTok API payload format"""
        return {
            "campaign_name": self.campaign_name,
            "objective": self.objective,
            "creative": {
                "text": self.ad_text,
                "cta": self.cta,
                "music_id": self.music_id
            }
        }