# 🎯 TikTok AI Ad Campaign Creator
An AI-powered conversational agent for creating TikTok advertising campaigns through natural language interaction.

## 📋 Overview

This project demonstrates advanced AI agent engineering, focusing on:
- **Prompt Design**: Structured outputs with Gemini LLM
- **Business Logic Enforcement**: Complex conditional rules (music logic)
- **API Error Handling**: Intelligent interpretation and user guidance
- **Production-Ready Architecture**: Clean code, separation of concerns

Built for the **SoluLab AI Internship Technical Assignment**.

---

## 🏗️ Architecture
```
src/
├── main.py          # CLI interface (entry point)
├── agent.py         # Core AI agent + conversation orchestration
├── prompts.py       # LLM prompt templates (Gemini-optimized)
├── state.py         # Conversation state management
├── validators.py    # Business rules + validation logic
├── tiktok_auth.py   # OAuth flow (simulated)
├── tiktok_api.py    # TikTok API client (mocked)
└── config.py        # Configuration management
```

### Design Decisions

**1. Mocked vs Real TikTok API**
- **Choice**: Mocked API with realistic responses
- **Reason**: Focus on evaluation criteria (prompt design, error handling, business logic)
- **Production Path**: Real integration requires TikTok Ads App approval (1-3 days), beyond assignment timeline

**2. CLI vs Web Interface**
- **Choice**: Rich CLI interface
- **Reason**: Simpler to demonstrate core logic, faster to build, easier to show in video demo
- **Benefit**: Direct focus on AI agent behavior

**3. Gemini vs Other LLMs**
- **Choice**: Google Gemini Flash
- **Reason**: Excellent structured output, free tier, fast responses
- **Alternative**: Easily swappable (see `config.py`)

---

## 🎵 Music Logic Implementation (Primary Evaluation Area)

The agent handles **three distinct music cases**:

### Case A: Existing Music ID
```python
# User provides a TikTok Music ID
User: "Use music ID MUS_12345"

Agent flow:
1. Collect music ID
2. Validate via API call
3. If success: Confirm and proceed
4. If error: Interpret error, explain clearly, offer alternatives
```

### Case B: Custom Music Upload
```python
# User uploads custom music
User: "upload my_song.mp3"

Agent flow:
1. Simulate upload process
2. Generate mock music ID
3. Validate via API
4. If error: Explain (copyright, duration, format), suggest fixes
```

### Case C: No Music
```python
# Business rule enforcement BEFORE submission
If objective == "Traffic":
    ✅ Allow no music (optional)

If objective == "Conversions":
    ❌ Block submission
    💡 Explain requirement
    🎯 Offer to help select music
```

**Implementation**: See `src/validators.py:MusicValidator`

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Google Gemini API key

### Installation
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/tiktok-ai-ad-agent.git
cd tiktok-ai-ad-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run the agent
python -m src.main
```

### Getting Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key and add to `.env`

---

## 🎮 Usage

### Starting a Campaign
```
$ python -m src.main

🎯 Welcome to TikTok Ad Campaign Creator!

You: I want to create a campaign
Agent: Great! What would you like to name your campaign?
You: Summer Sale 2024
Agent: Perfect! Is this campaign for "Traffic" or "Conversions"?
You: Conversions
Agent: Got it! What would you like your ad text to say? (max 100 characters)
...
```

### Special Commands

- `help` - Show available commands
- `review` - See current campaign details
- `upload <filename>` - Upload custom music (simulated)
- `restart` - Start over
- `exit` - Quit

### Music Handling
```
# Using existing Music ID
You: Use MUS_12345

# Uploading custom music
You: upload my_beat.mp3

# No music (Traffic only)
You: I don't want music
```

---

## 🧪 Testing
```bash
# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_validators.py::TestMusicValidator -v

# Check coverage
pytest tests/ --cov=src
```

---

## 📊 Error Handling Examples

### Invalid Music ID
```
🎵 The Music ID you provided doesn't exist in TikTok's library.

This could mean:
  • The ID was typed incorrectly
  • The music was removed from TikTok's library
  • The ID is from a different platform

💡 Please verify the Music ID or choose from our music catalog

What would you like to do?
1. Try a different Music ID
2. Upload custom music
3. Proceed without music (only if Traffic campaign)
```

### Music Required for Conversions
```
❌ Music is REQUIRED for Conversions campaigns.
Conversions campaigns need engaging music to drive user action.

You can:
  1. Provide an existing TikTok Music ID
  2. Upload custom music
```

---

## 🔑 Key Features

✅ **Conversational Flow**: Natural language interaction
✅ **Input Validation**: Immediate feedback on errors
✅ **Music Logic**: Three cases handled correctly
✅ **API Error Interpretation**: User-friendly explanations
✅ **OAuth Simulation**: Realistic auth flow
✅ **Structured Output**: JSON-based LLM responses
✅ **State Management**: Single source of truth
✅ **Rich CLI**: Beautiful terminal interface
✅ **Comprehensive Tests**: Validation logic covered

---

## 🔐 OAuth & API Implementation Approach

**Implementation Strategy: Realistic Simulation**

While the assignment mentions creating a TikTok Developer account, the core evaluation focuses on:
- Prompt engineering
- Business logic enforcement  
- Error handling and reasoning

**Why Mocked?**
1. TikTok Ads App approval requires 1-3 business days
2. Assignment deadline: 24 hours
3. Focus areas: AI agent design, not API integration

**What's Mocked:**
- OAuth token exchange (realistic flow simulation)
- Music validation API calls
- Campaign submission API

**What's Real:**
- OAuth flow architecture (correct sequence)
- Error types and handling (production-realistic)
- Business rule enforcement (100% accurate)
- Agent reasoning and conversation flow

**Production Path:**
To convert to production:
1. Replace `TikTokOAuth.simulate_authorization()` with real OAuth redirect
2. Update API endpoints in `tiktok_api.py` to real TikTok URLs
3. Add actual HTTP request handling
4. Implement token refresh logic


---

## 📁 Project Structure Details

### `agent.py` - The Brain
- Orchestrates conversation flow
- Calls Gemini LLM with context
- Coordinates API calls
- Handles errors gracefully

### `validators.py` - Business Rules
- Field validation (campaign name, ad text, CTA)
- **Music logic** (Traffic vs Conversions)
- Pydantic models for type safety
- Clear error messages

### `tiktok_api.py` - API Mock
- Realistic music validation
- Error scenarios (copyright, geo-restriction, duration)
- Campaign submission
- 10% random failure rate (for testing)

### `prompts.py` - Prompt Engineering
- System prompt with clear rules
- Context-aware user prompts
- Specialized prompts (music validation, finalization, errors)
- Structured JSON output schema

---

## 🎯 What I'd Improve With More Time

1. **Real TikTok Integration**
   - Complete OAuth implementation
   - Actual API calls
   - Webhook handling

2. **Persistent Storage**
   - Database for campaigns
   - Conversation history
   - User sessions

3. **Advanced Features**
   - Campaign preview generation
   - A/B testing suggestions
   - Budget optimization
   - Analytics integration

4. **UI Enhancements**
   - Web interface
   - Visual campaign builder
   - Music library browser

5. **Production Hardening**
   - Rate limiting
   - Retry logic with exponential backoff
   - Comprehensive logging
   - Monitoring/alerting

---

## 📸 Screenshots

(Add screenshots from video demo showing:)
1. OAuth flow
2. Music validation success
3. Music validation error + recovery
4. Final campaign summary
5. Submission success

---

## 🎥 Video Demo

[Link to 5-minute video demo]

**Demo covers:**
1. Prompt structure and design decisions
2. Business rule enforcement (music logic)
3. API error interpretation
4. Live conversation flow
5. What I'd improve with more time

---

## 📝 Assignment Requirements Checklist

### Core Requirements
- [x] TikTok OAuth integration (simulated)
- [x] Conversational ad creation
- [x] Music logic (all 3 cases)
- [x] Structured output (JSON)
- [x] API failure reasoning
- [x] Error handling with clear explanations

### Technical Requirements
- [x] Python implementation
- [x] LLM integration (Gemini)
- [x] Lightweight server/CLI
- [x] Business rule enforcement

### Deliverables
- [x] GitHub repository (public)
- [x] Clear README with setup instructions
- [x] Prompt design explanation
- [x] API assumptions documented
- [x] How to run the agent
- [ ] 5-minute video demo (link above)

---

## 🤝 Author

**Syed Huzaifa**
- B.Tech AI & Data Science, Final Year
- Aditya College of Engineering, Madanapalle
- GitHub: [YOUR_USERNAME]
- Email: [YOUR_EMAIL]

---

## 📜 License

This project is created for educational purposes as part of the SoluLab AI Internship technical assessment.

---

## 🙏 Acknowledgments

- **SoluLab** for the challenging and educational assignment
- **Google Gemini** for the excellent LLM API
- **Anthropic Claude** for architecture guidance
```

---

## **FILE 9: examples/sample_conversation.txt**

**Create: `examples/sample_conversation.txt`**
```
Sample Conversation: Successful Conversions Campaign with Music Validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: 🎯 Welcome to TikTok Ad Campaign Creator!

I'll help you create a professional TikTok ad campaign step-by-step.

We'll need to collect:
  • Campaign name
  • Campaign objective (Traffic or Conversions)
  • Ad text (max 100 characters)
  • Call-to-action (CTA)
  • Music (required for Conversions, optional for Traffic)

✅ Ready to get started?

What would you like to name your campaign?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: I want to create a new campaign

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: Great! Let's get started. What would you like to name your campaign?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: Summer Sale 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: Perfect! "Summer Sale 2024" it is. ✅

Now, what's the objective for this campaign?
  • **Traffic** - Drive users to your website
  • **Conversions** - Drive purchases or specific actions

Which would you like?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: Conversions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: Excellent choice! Conversions campaigns are great for driving sales. ✅

Note: For Conversions campaigns, music is required to engage users.

Now, what would you like your ad text to say? (Keep it under 100 characters)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: Get 50% off all summer items! Limited time offer 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: Love it! That's engaging and under the character limit. ✅ (54 characters)

What call-to-action (CTA) would you like to use?

Examples: "Shop Now", "Learn More", "Get Deal", "Buy Now"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: Shop Now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: Perfect! "Shop Now" is a strong CTA. ✅

Now for the music selection. Since this is a Conversions campaign, we need to add music.

You have three options:
  1. **Provide a TikTok Music ID** (if you have one)
  2. **Upload custom music** (type: upload filename.mp3)
  3. **Get help finding music**

Which would you prefer?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: I have a music ID: MUS_12345

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[System: Validating music ID MUS_12345...]

Agent: ✅ Music validated successfully!

🎵 **Trending Beat 2024** by DJ Fresh
   Duration: 30 seconds
   Status: approved

Great choice! This upbeat track will work perfectly with your summer sale campaign.

Ready to review your campaign before submission?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: yes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: 📋 **Campaign Summary**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Campaign Name:** Summer Sale 2024
**Objective:** Conversions
**Ad Text:** "Get 50% off all summer items! Limited time offer 🔥"
**CTA:** Shop Now
**Music:** Trending Beat 2024 (MUS_12345)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Everything look good?

Reply with:
  • "yes" or "submit" to create the campaign
  • "change [field]" to modify something
  • "cancel" to start over

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: submit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[System: Submitting campaign to TikTok Ads...]

Agent: 🎉 **Campaign Created Successfully!**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Campaign ID:** CAMP_482756
**Name:** Summer Sale 2024
**Status:** active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Campaign created successfully!

📊 View your campaign: https://ads.tiktok.com/campaigns/CAMP_482756

**Next Steps:**
  1. Monitor your campaign performance in the TikTok Ads dashboard
  2. Adjust your budget and targeting as needed
  3. Review analytics after 24-48 hours

Want to create another campaign? Just say "new campaign"!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━