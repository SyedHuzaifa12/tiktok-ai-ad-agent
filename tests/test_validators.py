"""
Tests for validation logic
Demonstrates understanding of testing best practices
"""

import pytest
from src.validators import (
    FieldValidator,
    MusicValidator,
    AdCampaignData,
    validate_complete_campaign
)


class TestFieldValidators:
    """Test individual field validators"""
    
    def test_campaign_name_valid(self):
        is_valid, msg = FieldValidator.validate_campaign_name("Summer Sale")
        assert is_valid == True
        assert "✅" in msg
    
    def test_campaign_name_too_short(self):
        is_valid, msg = FieldValidator.validate_campaign_name("Hi")
        assert is_valid == False
        assert "at least 3 characters" in msg
    
    def test_campaign_name_empty(self):
        is_valid, msg = FieldValidator.validate_campaign_name("")
        assert is_valid == False
    
    def test_objective_valid_traffic(self):
        is_valid, msg = FieldValidator.validate_objective("Traffic")
        assert is_valid == True
    
    def test_objective_valid_conversions(self):
        is_valid, msg = FieldValidator.validate_objective("Conversions")
        assert is_valid == True
    
    def test_objective_invalid(self):
        is_valid, msg = FieldValidator.validate_objective("Sales")
        assert is_valid == False
    
    def test_ad_text_valid(self):
        is_valid, msg = FieldValidator.validate_ad_text("Get 50% off today!")
        assert is_valid == True
    
    def test_ad_text_too_long(self):
        long_text = "a" * 101
        is_valid, msg = FieldValidator.validate_ad_text(long_text)
        assert is_valid == False
        assert "too long" in msg.lower()
    
    def test_ad_text_empty(self):
        is_valid, msg = FieldValidator.validate_ad_text("")
        assert is_valid == False


class TestMusicValidator:
    """Test music validation logic (CRITICAL)"""
    
    def test_music_required_for_conversions(self):
        """Music is REQUIRED for Conversions campaigns"""
        is_valid, msg = MusicValidator.validate_music_for_objective(
            objective="Conversions",
            music_id=None
        )
        assert is_valid == False
        assert "REQUIRED" in msg
    
    def test_music_optional_for_traffic(self):
        """Music is OPTIONAL for Traffic campaigns"""
        is_valid, msg = MusicValidator.validate_music_for_objective(
            objective="Traffic",
            music_id=None
        )
        assert is_valid == True
    
    def test_music_allowed_with_id(self):
        """Music is allowed when ID is provided"""
        is_valid, msg = MusicValidator.validate_music_for_objective(
            objective="Conversions",
            music_id="MUS_12345"
        )
        assert is_valid == True


class TestAdCampaignData:
    """Test Pydantic model validation"""
    
    def test_valid_traffic_campaign_no_music(self):
        """Traffic campaign without music should be valid"""
        campaign = AdCampaignData(
            campaign_name="Test Campaign",
            objective="Traffic",
            ad_text="Check out our sale!",
            cta="Shop Now",
            music_id=None
        )
        assert campaign.objective == "Traffic"
        assert campaign.music_id is None
    
    def test_valid_conversions_campaign_with_music(self):
        """Conversions campaign with music should be valid"""
        campaign = AdCampaignData(
            campaign_name="Test Campaign",
            objective="Conversions",
            ad_text="Buy now!",
            cta="Shop",
            music_id="MUS_12345"
        )
        assert campaign.music_id == "MUS_12345"
    
    def test_invalid_conversions_campaign_no_music(self):
        """Conversions campaign without music should fail"""
        with pytest.raises(ValueError, match="Music"):
            AdCampaignData(
                campaign_name="Test",
                objective="Conversions",
                ad_text="Buy now!",
                cta="Shop",
                music_id=None
            )
    
    def test_campaign_name_too_short(self):
        """Campaign name under 3 chars should fail"""
        with pytest.raises(ValueError):
            AdCampaignData(
                campaign_name="Hi",
                objective="Traffic",
                ad_text="Test",
                cta="Click",
            )
    
    def test_ad_text_too_long(self):
        """Ad text over 100 chars should fail"""
        with pytest.raises(ValueError):
            AdCampaignData(
                campaign_name="Test",
                objective="Traffic",
                ad_text="a" * 101,
                cta="Click",
            )


class TestCompleteValidation:
    """Test complete campaign validation"""
    
    def test_all_valid_traffic(self):
        is_valid, errors = validate_complete_campaign(
            campaign_name="Summer Sale",
            objective="Traffic",
            ad_text="Get 50% off!",
            cta="Shop Now",
            music_id=None
        )
        assert is_valid == True
        assert len(errors) == 0
    
    def test_all_valid_conversions(self):
        is_valid, errors = validate_complete_campaign(
            campaign_name="Summer Sale",
            objective="Conversions",
            ad_text="Get 50% off!",
            cta="Shop Now",
            music_id="MUS_12345"
        )
        assert is_valid == True
        assert len(errors) == 0
    
    def test_multiple_errors(self):
        is_valid, errors = validate_complete_campaign(
            campaign_name="Hi",  # Too short
            objective="Conversions",
            ad_text="",  # Empty
            cta="",  # Empty
            music_id=None  # Missing (required for Conversions)
        )
        assert is_valid == False
        assert len(errors) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])