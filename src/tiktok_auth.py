"""
TikTok OAuth Integration (Mocked)

NOTE: This simulates the OAuth 2.0 Authorization Code flow.
In production, this would integrate with real TikTok OAuth endpoints.

OAuth Flow:
1. Generate authorization URL
2. User authorizes app
3. Receive authorization code
4. Exchange code for access token
5. Use token for API calls

For demonstration purposes, we mock this flow while maintaining
the correct architectural pattern.
"""

import secrets
import time
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class OAuthToken:
    """OAuth access token with metadata"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600  # 1 hour
    scope: str = "ads:read,ads:write"
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
    
    def is_expired(self) -> bool:
        """Check if token has expired"""
        age = time.time() - self.created_at
        return age >= self.expires_in
    
    def time_until_expiry(self) -> int:
        """Get seconds until token expires"""
        age = time.time() - self.created_at
        return max(0, self.expires_in - int(age))


class TikTokOAuth:
    """
    Simulated TikTok OAuth 2.0 flow
    
    In production, this would use:
    - Client ID from TikTok Developer App
    - Client Secret for token exchange
    - Real OAuth endpoints
    - Secure token storage
    """
    
    # Mock credentials (in production, these would be from env vars)
    CLIENT_ID = "mock_tiktok_client_id_12345"
    CLIENT_SECRET = "mock_tiktok_client_secret_67890"
    REDIRECT_URI = "http://localhost:8000/oauth/callback"
    
    # Mock OAuth endpoints (real ones would be from TikTok)
    AUTH_URL = "https://business-api.tiktok.com/portal/auth"
    TOKEN_URL = "https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/"
    
    def __init__(self):
        self.current_token: Optional[OAuthToken] = None
        self.auth_state = secrets.token_urlsafe(32)
    
    def generate_auth_url(self) -> str:
        """
        Generate OAuth authorization URL
        
        In production, user would visit this URL to authorize the app
        
        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "state": self.auth_state,
            "scope": "ads:read,ads:write"
        }
        
        param_string = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"{self.AUTH_URL}?{param_string}"
        
        return auth_url
    
    def simulate_authorization(self) -> str:
        """
        Simulates user authorizing the app
        
        In production, this would be a callback from TikTok after user approval
        
        Returns:
            Authorization code
        """
        # Generate mock authorization code
        auth_code = f"AUTH_{secrets.token_urlsafe(32)}"
        return auth_code
    
    def exchange_code_for_token(self, auth_code: str) -> OAuthToken:
        """
        Exchange authorization code for access token
        
        In production, this would make a POST request to TikTok's token endpoint
        
        Args:
            auth_code: Authorization code from OAuth callback
            
        Returns:
            OAuthToken object
            
        Raises:
            Exception: If token exchange fails
        """
        # Simulate token exchange
        print("🔄 Exchanging authorization code for access token...")
        time.sleep(0.5)  # Simulate network delay
        
        # In production, this would be a real API call:
        # response = requests.post(
        #     self.TOKEN_URL,
        #     data={
        #         "client_id": self.CLIENT_ID,
        #         "client_secret": self.CLIENT_SECRET,
        #         "code": auth_code,
        #         "grant_type": "authorization_code"
        #     }
        # )
        
        # Generate mock access token
        access_token = f"TT_ACCESS_{secrets.token_urlsafe(48)}"
        
        token = OAuthToken(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,
            scope="ads:read,ads:write"
        )
        
        self.current_token = token
        print(f"✅ Access token obtained (expires in {token.expires_in}s)")
        
        return token
    
    def get_valid_token(self) -> Optional[str]:
        """
        Get current valid access token
        
        Returns:
            Valid access token or None if expired/not exists
        """
        if self.current_token is None:
            return None
        
        if self.current_token.is_expired():
            print("⚠️ Access token has expired")
            return None
        
        return self.current_token.access_token
    
    def refresh_token_if_needed(self) -> bool:
        """
        Check if token needs refresh and refresh if necessary
        
        Returns:
            True if token is valid (after refresh if needed)
        """
        if self.current_token is None:
            print("❌ No token available. Please authenticate first.")
            return False
        
        if self.current_token.is_expired():
            print("🔄 Token expired. Re-authenticating...")
            auth_code = self.simulate_authorization()
            self.exchange_code_for_token(auth_code)
            return True
        
        time_left = self.current_token.time_until_expiry()
        if time_left < 300:  # Less than 5 minutes
            print(f"⚠️ Token expires soon ({time_left}s remaining). Consider refreshing.")
        
        return True
    
    def simulate_full_oauth_flow(self) -> OAuthToken:
        """
        Simulates the complete OAuth flow
        
        Steps:
        1. Generate auth URL
        2. User authorizes (simulated)
        3. Receive auth code
        4. Exchange for access token
        
        Returns:
            OAuthToken
        """
        print("\n" + "="*50)
        print("🔐 Starting TikTok OAuth Flow (Simulated)")
        print("="*50)
        
        # Step 1: Generate auth URL
        auth_url = self.generate_auth_url()
        print(f"\n1️⃣ Authorization URL generated:")
        print(f"   {auth_url[:80]}...")
        print(f"   (In production, user would visit this URL)")
        
        # Step 2: Simulate user authorization
        print(f"\n2️⃣ Simulating user authorization...")
        time.sleep(0.3)
        auth_code = self.simulate_authorization()
        print(f"   ✅ Authorization code received: {auth_code[:30]}...")
        
        # Step 3: Exchange code for token
        print(f"\n3️⃣ Exchanging authorization code for access token...")
        token = self.exchange_code_for_token(auth_code)
        
        print(f"\n✅ OAuth flow complete!")
        print(f"   Access Token: {token.access_token[:40]}...")
        print(f"   Expires In: {token.expires_in} seconds")
        print(f"   Scope: {token.scope}")
        print("="*50 + "\n")
        
        return token


class OAuthErrorHandler:
    """
    Handles OAuth-related errors with clear explanations
    """
    
    ERROR_MESSAGES = {
        "invalid_client": {
            "message": "Invalid Client ID or Client Secret",
            "explanation": "The TikTok app credentials are incorrect or the app has been deleted.",
            "action": "Verify your Client ID and Secret in the TikTok Developer Portal"
        },
        "invalid_grant": {
            "message": "Invalid or expired authorization code",
            "explanation": "The authorization code has expired or has already been used.",
            "action": "Restart the OAuth flow to get a new authorization code"
        },
        "insufficient_scope": {
            "message": "Missing required OAuth scopes",
            "explanation": "Your app doesn't have permission to access TikTok Ads API.",
            "action": "Request 'ads:read' and 'ads:write' scopes during authorization"
        },
        "access_denied": {
            "message": "User denied authorization",
            "explanation": "The user declined to grant permissions to your app.",
            "action": "User needs to approve the authorization request"
        },
        "geo_restriction": {
            "message": "Geographic restriction",
            "explanation": "TikTok Ads API is not available in your region.",
            "action": "Check if your region is supported for TikTok Ads"
        }
    }
    
    @staticmethod
    def explain_error(error_code: str) -> str:
        """
        Provides user-friendly explanation of OAuth errors
        
        Args:
            error_code: OAuth error code
            
        Returns:
            Formatted error explanation
        """
        if error_code not in OAuthErrorHandler.ERROR_MESSAGES:
            return f"Unknown OAuth error: {error_code}"
        
        error_info = OAuthErrorHandler.ERROR_MESSAGES[error_code]
        
        explanation = f"""
❌ OAuth Error: {error_info['message']}

What this means:
  {error_info['explanation']}

What to do:
  ✅ {error_info['action']}
"""
        return explanation