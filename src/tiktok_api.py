"""
Mocked TikTok Ads API client

IMPORTANT: This is a simulation for demonstration purposes.
All responses, including campaign IDs and dashboard URLs, are mocked.

In production, this would:
- Call real TikTok API endpoints
- Return actual campaign IDs
- Generate working dashboard URLs
- Use authenticated requests

This mock maintains the same structure and error handling
patterns as the real API would require.
"""

import random
import time
from typing import Dict, Optional, Tuple, Literal
from dataclasses import dataclass


@dataclass
class APIResponse:
    """Standard API response structure"""
    success: bool
    data: Optional[Dict] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    suggestion: Optional[str] = None


class TikTokAPIError(Exception):
    """Custom exception for TikTok API errors"""
    def __init__(self, error_code: str, message: str, suggestion: str = None):
        self.error_code = error_code
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)


class TikTokAPI:
    """
    Mocked TikTok Ads API
    
    Simulates:
    - Music validation with realistic responses
    - Campaign submission
    - Various error scenarios
    - Rate limiting behavior
    """
    
    # Simulate a database of valid music IDs
    VALID_MUSIC_IDS = {
        "MUS_12345": {"title": "Trending Beat 2024", "artist": "DJ Fresh", "duration": 30},
        "MUS_67890": {"title": "Viral Dance Track", "artist": "Sound Wave", "duration": 25},
        "MUS_11111": {"title": "Chill Vibes", "artist": "Ambient Artists", "duration": 45},
        "MUSIC_99999": {"title": "Popular Song", "artist": "Top Charts", "duration": 35},
    }
    
    # Error scenarios with realistic messages
    ERROR_SCENARIOS = {
        "invalid_music_id": {
            "message": "Music ID does not exist in TikTok's music library",
            "suggestion": "Please check the Music ID and try again, or choose from our music library",
            "recoverable": True
        },
        "copyright_claim": {
            "message": "This music has active copyright restrictions and cannot be used in ads",
            "suggestion": "Choose royalty-free music or upload original content",
            "recoverable": True
        },
        "geo_restricted": {
            "message": "Music is not available in your target advertising region",
            "suggestion": "Select music that's available globally or change your target region",
            "recoverable": True
        },
        "duration_invalid": {
            "message": "Music duration exceeds the maximum allowed for TikTok ads (60 seconds)",
            "suggestion": "Choose a shorter track or trim your music to under 60 seconds",
            "recoverable": True
        }
    }
    
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self.request_count = 0
        self.last_request_time = 0
    
    def _simulate_network_delay(self):
        """Simulate API network latency"""
        if self.mock_mode:
            time.sleep(random.uniform(0.3, 0.8))  # 300-800ms delay
    
    def _check_rate_limit(self):
        """Simulate rate limiting"""
        self.request_count += 1
        current_time = time.time()
        
        # Simulate rate limit: max 10 requests per minute
        if current_time - self.last_request_time < 60 and self.request_count > 10:
            raise TikTokAPIError(
                error_code="rate_limit_exceeded",
                message="Too many requests. Rate limit: 10 requests per minute",
                suggestion="Please wait before making more requests"
            )
        
        if current_time - self.last_request_time >= 60:
            self.request_count = 0
            self.last_request_time = current_time
    
    def validate_music(self, music_id: str) -> APIResponse:
        """
        Validates a music ID against TikTok's music library
        
        This method simulates three music cases:
        - Case A: Existing valid music ID
        - Case A (error): Invalid/non-existent music ID
        - Random failures to test error handling
        
        Args:
            music_id: TikTok Music ID to validate
            
        Returns:
            APIResponse with validation result
        """
        print(f"🔍 Validating Music ID: {music_id}")
        
        self._simulate_network_delay()
        self._check_rate_limit()
        
        # Case 1: Valid music ID (80% chance if in database)
        if music_id in self.VALID_MUSIC_IDS:
            # 80% success, 20% random failure for testing
            if random.random() < 0.8:
                music_data = self.VALID_MUSIC_IDS[music_id]
                return APIResponse(
                    success=True,
                    data={
                        "music_id": music_id,
                        "title": music_data["title"],
                        "artist": music_data["artist"],
                        "duration": music_data["duration"],
                        "status": "approved"
                    }
                )
            else:
                # Random failure scenario
                error_type = random.choice(["copyright_claim", "geo_restricted"])
                error_info = self.ERROR_SCENARIOS[error_type]
                return APIResponse(
                    success=False,
                    error_code=error_type,
                    error_message=error_info["message"],
                    suggestion=error_info["suggestion"]
                )
        
        # Case 2: Invalid music ID
        else:
            return APIResponse(
                success=False,
                error_code="invalid_music_id",
                error_message=f"Music ID '{music_id}' does not exist in TikTok's music library",
                suggestion="Please verify the Music ID or choose from our music catalog"
            )
    
    def simulate_music_upload(self, file_name: str) -> APIResponse:
        """
        Simulates uploading custom music
        
        This simulates Case B: Custom music upload
        
        Args:
            file_name: Name of the music file being uploaded
            
        Returns:
            APIResponse with generated music ID or error
        """
        print(f"📤 Uploading custom music: {file_name}")
        
        self._simulate_network_delay()
        self._check_rate_limit()
        
        # 90% success rate for uploads
        if random.random() < 0.9:
            # Generate mock music ID
            mock_music_id = f"MUS_CUSTOM_{random.randint(10000, 99999)}"
            
            return APIResponse(
                success=True,
                data={
                    "music_id": mock_music_id,
                    "file_name": file_name,
                    "status": "processing",
                    "message": "Music uploaded successfully. Processing may take 1-2 minutes."
                }
            )
        else:
            # Simulate upload failure
            error_type = random.choice(["duration_invalid", "copyright_claim"])
            error_info = self.ERROR_SCENARIOS[error_type]
            return APIResponse(
                success=False,
                error_code=error_type,
                error_message=error_info["message"],
                suggestion=error_info["suggestion"]
            )
    
    def submit_campaign(self, campaign_data: Dict) -> APIResponse:
        """
        Submits ad campaign to TikTok Ads API
        
        Args:
            campaign_data: Complete campaign payload
            
        Returns:
            APIResponse with submission result
        """
        print(f"📤 Submitting campaign: {campaign_data.get('campaign_name')}")
        
        self._simulate_network_delay()
        self._check_rate_limit()
        
        # 95% success rate for well-formed campaigns
        if random.random() < 0.95:
            campaign_id = f"CAMP_{random.randint(100000, 999999)}"
            
            return APIResponse(
                success=True,
                data={
                    "campaign_id": campaign_id,
                    "campaign_name": campaign_data.get("campaign_name"),
                    "status": "active",
                    "message": "Campaign created successfully!",
                    "dashboard_url": f"https://ads.tiktok.com/campaigns/{campaign_id}",
                    "note": "Mocked URL - in production, this would link to actual TikTok Ads dashboard"
                }
            )
        else:
            # Random submission failure
            return APIResponse(
                success=False,
                error_code="validation_failed",
                error_message="Campaign validation failed. Please review your inputs.",
                suggestion="Check all required fields and try again"
            )


def interpret_api_error(response: APIResponse) -> str:
    """
    Interprets API errors and provides user-friendly explanations
    
    This is a key part of the evaluation - showing we can translate
    technical errors into actionable guidance
    
    Args:
        response: API response with error
        
    Returns:
        User-friendly error explanation with next steps
    """
    if response.success:
        return "✅ Success - no errors"
    
    error_explanations = {
        "invalid_music_id": (
            "🎵 The Music ID you provided doesn't exist in TikTok's library.\n\n"
            "This could mean:\n"
            "  • The ID was typed incorrectly\n"
            "  • The music was removed from TikTok's library\n"
            "  • The ID is from a different platform\n\n"
            f"💡 {response.suggestion}"
        ),
        "copyright_claim": (
            "⚠️ Copyright Issue Detected\n\n"
            "This music has copyright restrictions and cannot be used in advertisements.\n"
            "Using copyrighted music without permission can result in your ad being rejected.\n\n"
            f"💡 {response.suggestion}"
        ),
        "geo_restricted": (
            "🌍 Geographic Restriction\n\n"
            "This music is not available in all regions where you're targeting your ads.\n"
            "TikTok requires music to be licensed in all target markets.\n\n"
            f"💡 {response.suggestion}"
        ),
        "duration_invalid": (
            "⏱️ Music Duration Issue\n\n"
            "TikTok ads have a maximum music duration of 60 seconds.\n"
            "Longer tracks may cause playback issues.\n\n"
            f"💡 {response.suggestion}"
        ),
        "rate_limit_exceeded": (
            "⏸️ Too Many Requests\n\n"
            "You've exceeded the API rate limit.\n"
            "This is a temporary restriction to prevent system overload.\n\n"
            f"💡 {response.suggestion}"
        )
    }
    
    explanation = error_explanations.get(
        response.error_code,
        f"❌ Error: {response.error_message}\n\n💡 {response.suggestion}"
    )
    
    return explanation