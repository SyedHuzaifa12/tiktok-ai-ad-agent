"""
OAuth Server for TikTok Authentication

Run this to obtain access token:
    python oauth_server.py
    
Then visit: http://localhost:8000
"""

from flask import Flask, request, redirect
import secrets
import os
from dotenv import load_dotenv, set_key

load_dotenv()

# Import after loading env
from src.tiktok_real_api import TikTokOAuth

app = Flask(__name__)

# Configuration
APP_ID = os.getenv('TIKTOK_APP_ID', '')
APP_SECRET = os.getenv('TIKTOK_APP_SECRET', '')
REDIRECT_URI = "http://localhost:8000/callback"

# OAuth handler
oauth_handler = None
oauth_state = secrets.token_urlsafe(32)


@app.route('/')
def home():
    """Home page with instructions"""
    global oauth_handler
    
    if not APP_ID or not APP_SECRET:
        return '''
        <h1>❌ Configuration Missing</h1>
        <p>Add TIKTOK_APP_ID and TIKTOK_APP_SECRET to .env file</p>
        <pre>
TIKTOK_APP_ID=your_app_id
TIKTOK_APP_SECRET=your_app_secret
        </pre>
        <p>Then restart this server</p>
        '''
    
    oauth_handler = TikTokOAuth(APP_ID, APP_SECRET, REDIRECT_URI)
    
    return f'''
    <html>
    <head><title>TikTok OAuth</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>🔐 TikTok OAuth Setup</h1>
        
        <div style="background: #f0f0f0; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3>Current Configuration:</h3>
            <p>App ID: <code>{APP_ID}</code></p>
            <p>Redirect URI: <code>{REDIRECT_URI}</code></p>
            <p><strong>⚠️ Ensure this redirect URI is in TikTok Developer Dashboard!</strong></p>
        </div>
        
        <a href="/start" style="background: #fe2c55; color: white; padding: 15px 30px; 
                                text-decoration: none; border-radius: 5px; display: inline-block;">
            🚀 Start OAuth Flow
        </a>
        
        <div style="margin-top: 30px; background: #e8f5e9; padding: 15px; border-radius: 5px;">
            <h3>Steps:</h3>
            <ol>
                <li>Click button above</li>
                <li>Login to TikTok</li>
                <li>Approve the application</li>
                <li>Redirected back with access token</li>
                <li>Token saved to .env automatically</li>
            </ol>
        </div>
    </body>
    </html>
    '''


@app.route('/start')
def start():
    """Start OAuth flow"""
    if not oauth_handler:
        return redirect('/')
    
    auth_url = oauth_handler.get_authorization_url(oauth_state)
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Handle OAuth callback"""
    auth_code = request.args.get('auth_code')
    state = request.args.get('state')
    
    if not auth_code:
        return '<h1>❌ No authorization code received</h1><a href="/">Try Again</a>'
    
    if state != oauth_state:
        return '<h1>❌ Invalid state - security error</h1><a href="/">Try Again</a>'
    
    # Exchange code for token
    success, result = oauth_handler.exchange_code_for_token(auth_code)
    
    if success:
        access_token = result['access_token']
        advertiser_ids = result.get('advertiser_ids', [])
        advertiser_id = advertiser_ids[0] if advertiser_ids else ''
        
        # Save to .env
        set_key('.env', 'TIKTOK_ACCESS_TOKEN', access_token)
        if advertiser_id:
            set_key('.env', 'TIKTOK_ADVERTISER_ID', advertiser_id)
        set_key('.env', 'TIKTOK_MOCK_MODE', 'false')
        
        return f'''
        <html>
        <body style="font-family: Arial; max-width: 800px; margin: 50px auto;">
            <h1>🎉 OAuth Successful!</h1>
            <div style="background: #e8f5e9; padding: 20px; border-radius: 5px;">
                <h3>✅ Credentials Saved</h3>
                <p>Access Token: <code>{access_token[:40]}...</code></p>
                <p>Advertiser ID: <code>{advertiser_id}</code></p>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 5px; margin-top: 20px;">
                <h3>🚀 Next Steps:</h3>
                <ol>
                    <li>Stop this server (Ctrl+C)</li>
                    <li>Run: <code>python -m src.main</code></li>
                    <li>Agent will use REAL TikTok API!</li>
                </ol>
            </div>
        </body>
        </html>
        '''
    else:
        return f'''
        <h1>❌ Token Exchange Failed</h1>
        <p>{result.get('message')}</p>
        <a href="/">Try Again</a>
        '''


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 TikTok OAuth Server")
    print("="*60)
    print("\n📍 Open browser: http://localhost:8000")
    print("\n" + "="*60 + "\n")
    
    app.run(host='localhost', port=8000, debug=False)