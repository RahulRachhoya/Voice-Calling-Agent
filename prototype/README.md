# ARYA Prototype - Minimal Working Version

AI Career Counselor Voice Agent for Careers360

## Quick Start

### 1. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 2. Configure API Keys

Edit `.env` and add your API keys:
```
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token_here
GOOGLE_API_KEY=your_google_api_key_here
VIDEOSDK_OUTBOUND_GATEWAY_ID=gw_xxxxx
```

**Get API Keys:**
- VideoSDK: https://app.videosdk.live/api-keys
- Google: https://aistudio.google.com/apikey

**Get Outbound Gateway ID:**
1. Go to VideoSDK Dashboard > Telephony > Outbound Gateways
2. Create an outbound gateway with your Twilio SIP credentials
3. Copy the Gateway ID (starts with `gw_`)
4. Add it to `.env` file

### 3. Run the Agent

```bash
python main.py
```

## Project Structure

```
arya-prototype/
├── main.py              # Entry point - WorkerJob registration
├── agent.py             # ARYAAgent class
├── prompts.py           # System prompts
├── outbound_call.py     # Script to trigger outbound calls
├── transcripts/         # Call transcripts (auto-created)
├── audio/               # Hold music directory
│   └── hold_music.mp3   # (add your file here)
├── .env                 # API keys (configure this)
├── .env.example         # Template
└── requirements.txt     # Dependencies
```

## Twilio SIP Configuration (+1 Region)

### Step 1: Twilio Setup
1. Purchase US (+1) phone number in Twilio Console
2. Create SIP Trunk in Voice section
3. Note the Termination SIP URI

### Step 2: VideoSDK Dashboard
1. **Inbound Gateway**: Add your Twilio number
2. **Outbound Gateway**: Add Twilio termination credentials
3. **Routing Rule**: Link to agent ID `ARYA-Agent`

### Step 3: Test Calls

#### Inbound Calls:
- Dial your Twilio +1 number
- ARYA will answer with the greeting

#### Outbound Calls:
Run the outbound call script:
```bash
python outbound_call.py
```

Or provide phone number directly:
```bash
python outbound_call.py +14155551234
```

**Prerequisites for outbound calls:**
1. Agent must be running (`python main.py`)
2. Outbound Gateway configured in VideoSDK Dashboard
3. Twilio SIP Trunk with termination URI

## Next Steps

After minimal version works:
1. Add Sarvam STT/TTS for Hindi/Hinglish support
2. Add Tavily MCP for college search
3. Add language detection (FastText)
4. Implement hold flow with music

## Requirements

- Python 3.12+
- VideoSDK Account
- Google API Key
- Twilio Account (for telephony)
