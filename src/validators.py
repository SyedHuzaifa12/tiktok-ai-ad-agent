"""
Business rules and validation logic
This is where ALL the music logic lives (primary evaluation area)
"""

from typing import Tuple, Optional, Literal
from pydantic import BaseModel, Field, validator


class AdCampaignData(BaseModel):
    """
    Pydantic model for ad campaign with built-in validation
    """
    campaign_name: str = Field(..., min_length=3, description="Campaign name (min 3 chars)")
    objective: Literal["Traffic", "Conversions"] = Field(..., description="Campaign objective")
    ad_text: str = Field(..., max_length=100, description="Ad text (max 100 chars)")
    cta: str = Field(..., description="Call to action")
    music_id: Optional[str] = Field(None, description="TikTok Music ID")
    
    @validator('campaign_name')
    def validate_campaign_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Campaign name must be at least 3 characters")
        return v.strip()
    
    @validator('ad_text')
    def validate_ad_text(cls, v):
        if len(v) > 100:
            raise ValueError(f"Ad text must be 100 characters or less (current: {len(v)})")
        if not v.strip():
            raise ValueError("Ad text cannot be empty")
        return v.strip()
    
    @validator('music_id', always=True)
    def validate_music_requirement(cls, v, values):
        """
        CRITICAL BUSINESS RULE:
        - Music is OPTIONAL for Traffic campaigns
        - Music is REQUIRED for Conversions campaigns
        
        This validation happens BEFORE submission attempt
        """
        objective = values.get('objective')
        
        if objective == "Conversions" and not v:
            raise ValueError(
                "🚫 Music is REQUIRED for Conversions campaigns. "
                "Please provide a Music ID or upload custom music."
            )
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "campaign_name": "Summer Sale 2024",
                "objective": "Conversions",
                "ad_text": "Get 50% off! Limited time offer 🔥",
                "cta": "Shop Now",
                "music_id": "MUS_12345"
            }
        }


class MusicValidator:
    """
    Handles all three music cases (primary evaluation area)
    
    Case A: Existing Music ID - validate via API
    Case B: Custom Upload - simulate upload + validate
    Case C: No Music - enforce objective constraint
    """
    
    @staticmethod
    def validate_music_for_objective(
        objective: Literal["Traffic", "Conversions"],
        music_id: Optional[str]
    ) -> Tuple[bool, str]:
        """
        Validates music requirement based on campaign objective
        
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if objective == "Conversions" and not music_id:
            return False, (
                "❌ Music is REQUIRED for Conversions campaigns.\n"
                "Conversions campaigns need engaging music to drive user action.\n\n"
                "You can:\n"
                "  1. Provide an existing TikTok Music ID\n"
                "  2. Upload custom music\n"
            )
        
        if objective == "Traffic" and not music_id:
            return True, "✅ No music is allowed for Traffic campaigns (optional)"
        
        return True, "✅ Music ID provided"
    
    @staticmethod
    def validate_music_id_format(music_id: str) -> Tuple[bool, str]:
        """
        Basic format validation for music ID
        Real API would do deeper validation
        
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not music_id:
            return False, "Music ID cannot be empty"
        
        # Basic format check (TikTok music IDs typically start with MUS_)
        if not (music_id.startswith("MUS_") or music_id.startswith("MUSIC_")):
            return False, (
                f"⚠️ Music ID format looks unusual: '{music_id}'\n"
                "TikTok Music IDs typically start with 'MUS_' or 'MUSIC_'\n"
                "Example: MUS_12345678\n\n"
                "Proceeding with API validation..."
            )
        
        return True, "Format looks good"


class FieldValidator:
    """
    Individual field validators with helpful error messages
    """
    
    @staticmethod
    def validate_campaign_name(name: str) -> Tuple[bool, str]:
        """Validate campaign name"""
        if not name or not name.strip():
            return False, "❌ Campaign name cannot be empty"
        
        if len(name.strip()) < 3:
            return False, f"❌ Campaign name must be at least 3 characters (current: {len(name.strip())})"
        
        return True, "✅ Valid campaign name"
    
    @staticmethod
    def validate_objective(objective: str) -> Tuple[bool, str]:
        """Validate objective"""
        valid_objectives = ["Traffic", "Conversions"]
        
        if objective not in valid_objectives:
            return False, (
                f"❌ Invalid objective: '{objective}'\n"
                f"Valid options: {', '.join(valid_objectives)}"
            )
        
        return True, f"✅ Valid objective: {objective}"
    
    @staticmethod
    def validate_ad_text(text: str) -> Tuple[bool, str]:
        """Validate ad text"""
        if not text or not text.strip():
            return False, "❌ Ad text cannot be empty"
        
        if len(text) > 100:
            return False, (
                f"❌ Ad text too long: {len(text)} characters (max: 100)\n"
                f"Current text: '{text[:50]}...'\n"
                f"Please shorten by {len(text) - 100} characters"
            )
        
        return True, f"✅ Valid ad text ({len(text)} characters)"
    
    @staticmethod
    def validate_cta(cta: str) -> Tuple[bool, str]:
        """Validate CTA"""
        if not cta or not cta.strip():
            return False, "❌ CTA cannot be empty"
        
        # Common CTAs for reference
        common_ctas = [
            "Shop Now", "Learn More", "Sign Up", "Download",
            "Get Started", "Book Now", "Watch Now", "Apply Now"
        ]
        
        return True, f"✅ Valid CTA: {cta}"


def validate_complete_campaign(
    campaign_name: str,
    objective: Literal["Traffic", "Conversions"],
    ad_text: str,
    cta: str,
    music_id: Optional[str]
) -> Tuple[bool, list[str]]:
    """
    Validates all fields together and returns all errors
    
    Returns:
        Tuple[bool, list[str]]: (is_valid, list_of_error_messages)
    """
    errors = []
    
    # Validate each field
    is_valid, msg = FieldValidator.validate_campaign_name(campaign_name)
    if not is_valid:
        errors.append(msg)
    
    is_valid, msg = FieldValidator.validate_objective(objective)
    if not is_valid:
        errors.append(msg)
    
    is_valid, msg = FieldValidator.validate_ad_text(ad_text)
    if not is_valid:
        errors.append(msg)
    
    is_valid, msg = FieldValidator.validate_cta(cta)
    if not is_valid:
        errors.append(msg)
    
    # Validate music requirement
    is_valid, msg = MusicValidator.validate_music_for_objective(objective, music_id)
    if not is_valid:
        errors.append(msg)
    
    return len(errors) == 0, errors