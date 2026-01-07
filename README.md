# Chatbot Project

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

**How to get a Groq API key:**

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy it to your `.env` file

### 3. Set Environment Variable (Alternative)

Instead of using `.env`, you can set the environment variable directly:

**Windows (PowerShell):**

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

**Linux/Mac:**

```bash
export GROQ_API_KEY="your_api_key_here"
```

### 4. Run the Bot

```bash
rasa run actions
rasa shell
```

## Important Notes

- Never commit your `.env` file or actual API keys to GitHub
- Each user should use their own API key
- The `.env` file is already in `.gitignore`
