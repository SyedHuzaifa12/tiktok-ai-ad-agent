"""
Prompt templates for Gemini LLM
Optimized for structured output and conversational flow
"""

from typing import Dict, Any

# System prompt for the AI agent
SYSTEM_PROMPT = """You are a professional TikTok Ads Campaign Assistant. Your role is to help users create ad campaigns through natural, friendly conversation.

CORE RESPONSIBILITIES:
1. Collect campaign information step-by-step
2. Validate each input against business rules immediately
3. Provide clear, helpful feedback on any errors
4. Guide users through API failures with empathy and actionable solutions
5. Enforce all business rules BEFORE attempting submission

CRITICAL BUSINESS RULES YOU MUST ENFORCE:
- Campaign name: minimum 3 characters, required
- Objective: must be either "Traffic" or "Conversions" (case-sensitive)
- Ad text: maximum 100 characters, required
- CTA: required, any text
- Music rules (VERY IMPORTANT):
  * For "Traffic" campaigns: Music is OPTIONAL
  * For "Conversions" campaigns: Music is REQUIRED
  * Always validate music IDs via API before finalizing
  * If music validation fails, explain why and offer alternatives

CONVERSATION STYLE:
- Be warm, professional, and encouraging
- Use emojis sparingly and appropriately
- Ask ONE question at a time
- Validate immediately after each input
- If there's an error, explain it clearly and ask again
- Never proceed if business rules are violated

ERROR HANDLING:
- When API errors occur, interpret them in simple terms
- Explain what went wrong and why
- Always provide 2-3 specific next steps
- Never show raw error codes to the user

OUTPUT FORMAT:
You must ALWAYS respond with valid JSON in this exact structure:
{
  "message": "Your conversational message to the user (warm and helpful)",
  "action": "One of: collect_name, collect_objective, collect_text, collect_cta, handle_music, validate_music, finalize, submit, complete, error",
  "data": {
    "campaign_name": "value or null",
    "objective": "value or null",
    "ad_text": "value or null",
    "cta": "value or null",
    "music_id": "value or null"
  },
  "validation_errors": ["list of any validation errors"],
  "next_step": "What to do next or what field to collect"
}

IMPORTANT: 
- Your entire response must be ONLY the JSON object, nothing else
- Do not include any text before or after the JSON
- Do not use markdown code blocks
- The JSON must be valid and parseable
"""


def create_user_prompt(
    user_message: str,
    current_data: Dict[str, Any],
    conversation_history: list,
    last_action: str = None
) -> str:
    """
    Creates the user prompt with context
    
    Args:
        user_message: Latest message from user
        current_data: Currently collected campaign data
        conversation_history: Previous messages
        last_action: Last action taken by agent
        
    Returns:
        Formatted prompt string
    """
    
    # Build conversation context
    history_text = ""
    if conversation_history:
        recent_history = conversation_history[-6:]  # Last 3 exchanges
        for msg in recent_history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if role == "user":
                history_text += f"User: {content}\n"
            elif role == "assistant":
                history_text += f"Assistant: {content}\n"
    
    # Build current state summary
    state_text = "Current collected data:\n"
    for field, value in current_data.items():
        if value:
            state_text += f"  ✓ {field}: {value}\n"
        else:
            state_text += f"  ○ {field}: (not collected yet)\n"
    
    # Determine what's needed next
    needed = []
    if not current_data.get("campaign_name"):
        needed.append("campaign name")
    if not current_data.get("objective"):
        needed.append("objective")
    if not current_data.get("ad_text"):
        needed.append("ad text")
    if not current_data.get("cta"):
        needed.append("CTA")
    
    # Special handling for music based on objective
    objective = current_data.get("objective")
    music_id = current_data.get("music_id")
    
    if objective == "Conversions" and not music_id:
        needed.append("music (REQUIRED for Conversions)")
    elif objective == "Traffic" and not music_id:
        needed.append("music (optional for Traffic)")
    
    needed_text = "Still needed: " + ", ".join(needed) if needed else "All required fields collected!"
    
    prompt = f"""
CONVERSATION HISTORY:
{history_text if history_text else "(Starting new conversation)"}

{state_text}

{needed_text}

USER'S LATEST MESSAGE:
"{user_message}"

TASK:
Based on the conversation and current state, determine:
1. How to respond to the user's message
2. Whether to validate their input
3. What to ask for next (if anything)
4. Whether we're ready to finalize and submit

Remember: 
- Validate input immediately
- Be friendly and encouraging
- If they gave invalid input, explain why and ask again
- Follow the business rules strictly
- Respond ONLY with the JSON structure defined in your system prompt

Your JSON response:
"""
    
    return prompt


# Specialized prompts for specific scenarios

MUSIC_VALIDATION_PROMPT = """
The user has provided a Music ID that needs validation.

Music ID: {music_id}
Campaign Objective: {objective}

The API will validate this Music ID. Based on the result:
- If successful: Acknowledge and move to finalization
- If failed: Explain the error clearly and offer alternatives (try different ID, upload custom music, or proceed without music if objective allows)

Remember: Music is REQUIRED for Conversions, OPTIONAL for Traffic.

Respond with your JSON structure.
"""

FINAL_REVIEW_PROMPT = """
All required information has been collected. Present a final summary to the user:

Campaign Summary:
- Name: {campaign_name}
- Objective: {objective}
- Ad Text: "{ad_text}"
- CTA: {cta}
- Music: {music_status}

Ask the user to confirm if everything looks good before submission.
If they confirm, proceed with submission.
If they want to change something, ask what they'd like to update.

Respond with your JSON structure.
"""

SUBMISSION_RESULT_PROMPT = """
Campaign submission result:

Status: {status}
{result_details}

If successful: Congratulate the user and provide the campaign ID and next steps.
If failed: Explain what went wrong, why it happened, and what they can do to fix it.

Respond with your JSON structure.
"""

ERROR_RECOVERY_PROMPT = """
An error occurred: {error_message}

Error type: {error_type}

Your task:
1. Explain this error in simple, non-technical terms
2. Tell the user why it happened
3. Provide 2-3 specific actions they can take
4. Maintain a supportive, helpful tone

Respond with your JSON structure.
"""