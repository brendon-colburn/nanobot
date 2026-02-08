<div align="center">
  <img src="aegis_logo.png" alt="AEGIS" width="500">
  <h1>AEGIS: Autonomous Evolving General Intelligence System</h1>
  <p>
    <a href="https://pypi.org/project/aegis-ai/"><img src="https://img.shields.io/pypi/v/aegis-ai" alt="PyPI"></a>
    <a href="https://pepy.tech/project/aegis-ai"><img src="https://static.pepy.tech/badge/aegis-ai" alt="Downloads"></a>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/Feishu-Group-E9DBFC?style=flat&logo=feishu&logoColor=white" alt="Feishu"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/WeChat-Group-C5EAB4?style=flat&logo=wechat&logoColor=white" alt="WeChat"></a>
    <a href="https://discord.gg/MnCvHqpUGB"><img src="https://img.shields.io/badge/Discord-Community-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"></a>
  </p>
</div>

🛡️ **AEGIS** (Autonomous Evolving General Intelligence System) is an identity-based AI agent framework that goes beyond task execution to develop preferences, learn from consequences, and form genuine partnerships with operators. 

⚡️ Delivers core agent functionality in just **~4,000** lines of code — **99% smaller** than Clawdbot's 430k+ lines.

📏 Real-time line count: **3,422 lines** (run `bash core_agent_lines.sh` to verify anytime)

## 📢 News

- **2026-02-07** 🚀 Released v0.1.3.post5 with Qwen support & several improvements! Check [here](https://github.com/HKUDS/aegis/releases/tag/v0.1.3.post5) for details.
- **2026-02-06** ✨ Added Moonshot/Kimi provider, Discord integration, and enhanced security hardening!
- **2026-02-05** ✨ Added Feishu channel, DeepSeek provider, and enhanced scheduled tasks support!
- **2026-02-04** 🚀 Released v0.1.3.post4 with multi-provider & Docker support! Check [here](https://github.com/HKUDS/aegis/releases/tag/v0.1.3.post4) for details.
- **2026-02-03** ⚡ Integrated vLLM for local LLM support and improved natural language task scheduling!
- **2026-02-02** 🎉 aegis officially launched! Welcome to try 🐈 aegis!

## Key Features of AEGIS:

🧠 **Identity-Based**: Agent with persistent identity that evolves through experience, not just executing tasks.

🤝 **Partnership Model**: Designed around the parenting metaphor - guidance, autonomy, and genuine relationship development.

🧘 **Contemplative System**: Incorporates wisdom of non-action - not every thought becomes action, inspired by mindfulness traditions.

⚖️ **Layered Governance**: Guardrails, laws, and norms create safe autonomy that allows meaningful choices and learning.

## 🏗️ Architecture

<p align="center">
  <img src="aegis_arch.png" alt="aegis architecture" width="800">
</p>

## ✨ Features

<table align="center">
  <tr align="center">
    <th><p align="center">📈 24/7 Real-Time Market Analysis</p></th>
    <th><p align="center">🚀 Full-Stack Software Engineer</p></th>
    <th><p align="center">📅 Smart Daily Routine Manager</p></th>
    <th><p align="center">📚 Personal Knowledge Assistant</p></th>
  </tr>
  <tr>
    <td align="center"><p align="center"><img src="case/search.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/code.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/scedule.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/memory.gif" width="180" height="400"></p></td>
  </tr>
  <tr>
    <td align="center">Discovery • Insights • Trends</td>
    <td align="center">Develop • Deploy • Scale</td>
    <td align="center">Schedule • Automate • Organize</td>
    <td align="center">Learn • Memory • Reasoning</td>
  </tr>
</table>

## 📦 Install

**Install from source** (latest features, recommended for development)

```bash
git clone https://github.com/HKUDS/aegis.git
cd aegis
pip install -e .
```

**Install with [uv](https://github.com/astral-sh/uv)** (stable, fast)

```bash
uv tool install aegis-ai
```

**Install from PyPI** (stable)

```bash
pip install aegis-ai
```

## 🚀 Quick Start

> [!TIP]
> Set your API key in `~/.aegis/config.json`.
> Get API keys: [OpenRouter](https://openrouter.ai/keys) (Global) · [DashScope](https://dashscope.console.aliyun.com) (Qwen) · [Brave Search](https://brave.com/search/api/) (optional, for web search)

**1. Initialize**

```bash
aegis onboard
```

**2. Configure** (`~/.aegis/config.json`)

For OpenRouter - recommended for global users:
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

**3. Chat**

```bash
aegis agent -m "What is 2+2?"
```

That's it! You have a working AI assistant in 2 minutes.

## 🖥️ Local Models (vLLM)

Run aegis with your own local models using vLLM or any OpenAI-compatible server.

**1. Start your vLLM server**

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

**2. Configure** (`~/.aegis/config.json`)

```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

**3. Chat**

```bash
aegis agent -m "Hello from my local LLM!"
```

> [!TIP]
> The `apiKey` can be any non-empty string for local servers that don't require authentication.

## 💬 Chat Apps

Talk to your aegis through Telegram, Discord, WhatsApp, or Feishu — anytime, anywhere.

| Channel | Setup |
|---------|-------|
| **Telegram** | Easy (just a token) |
| **Discord** | Easy (bot token + intents) |
| **WhatsApp** | Medium (scan QR) |
| **Feishu** | Medium (app credentials) |

<details>
<summary><b>Telegram</b> (Recommended)</summary>

**1. Create a bot**
- Open Telegram, search `@BotFather`
- Send `/newbot`, follow prompts
- Copy the token

**2. Configure**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

> Get your user ID from `@userinfobot` on Telegram.

**3. Run**

```bash
aegis gateway
```

</details>

<details>
<summary><b>Discord</b></summary>

**1. Create a bot**
- Go to https://discord.com/developers/applications
- Create an application → Bot → Add Bot
- Copy the bot token

**2. Enable intents**
- In the Bot settings, enable **MESSAGE CONTENT INTENT**
- (Optional) Enable **SERVER MEMBERS INTENT** if you plan to use allow lists based on member data

**3. Get your User ID**
- Discord Settings → Advanced → enable **Developer Mode**
- Right-click your avatar → **Copy User ID**

**4. Configure**

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

**5. Invite the bot**
- OAuth2 → URL Generator
- Scopes: `bot`
- Bot Permissions: `Send Messages`, `Read Message History`
- Open the generated invite URL and add the bot to your server

**6. Run**

```bash
aegis gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

Requires **Node.js ≥18**.

**1. Link device**

```bash
aegis channels login
# Scan QR with WhatsApp → Settings → Linked Devices
```

**2. Configure**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. Run** (two terminals)

```bash
# Terminal 1
aegis channels login

# Terminal 2
aegis gateway
```

</details>

<details>
<summary><b>Feishu (飞书)</b></summary>

Uses **WebSocket** long connection — no public IP required.

```bash
pip install aegis-ai[feishu]
```

**1. Create a Feishu bot**
- Visit [Feishu Open Platform](https://open.feishu.cn/app)
- Create a new app → Enable **Bot** capability
- **Permissions**: Add `im:message` (send messages)
- **Events**: Add `im.message.receive_v1` (receive messages)
  - Select **Long Connection** mode (requires running aegis first to establish connection)
- Get **App ID** and **App Secret** from "Credentials & Basic Info"
- Publish the app

**2. Configure**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": []
    }
  }
}
```

> `encryptKey` and `verificationToken` are optional for Long Connection mode.
> `allowFrom`: Leave empty to allow all users, or add `["ou_xxx"]` to restrict access.

**3. Run**

```bash
aegis gateway
```

> [!TIP]
> Feishu uses WebSocket to receive messages — no webhook or public IP needed!

</details>

## ⚙️ Configuration

Config file: `~/.aegis/config.json`

### Providers

> [!NOTE]
> Groq provides free voice transcription via Whisper. If configured, Telegram voice messages will be automatically transcribed.

| Provider | Purpose | Get API Key |
|----------|---------|-------------|
| `openrouter` | LLM (recommended, access to all models) | [openrouter.ai](https://openrouter.ai) |
| `anthropic` | LLM (Claude direct) | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | LLM (GPT direct) | [platform.openai.com](https://platform.openai.com) |
| `deepseek` | LLM (DeepSeek direct) | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | LLM + **Voice transcription** (Whisper) | [console.groq.com](https://console.groq.com) |
| `gemini` | LLM (Gemini direct) | [aistudio.google.com](https://aistudio.google.com) |
| `aihubmix` | LLM (API gateway, access to all models) | [aihubmix.com](https://aihubmix.com) |
| `dashscope` | LLM (Qwen) | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |


### Security

> [!TIP]
> For production deployments, set `"restrictToWorkspace": true` in your config to sandbox the agent.

| Option | Default | Description |
|--------|---------|-------------|
| `tools.restrictToWorkspace` | `false` | When `true`, restricts **all** agent tools (shell, file read/write/edit, list) to the workspace directory. Prevents path traversal and out-of-scope access. |
| `channels.*.allowFrom` | `[]` (allow all) | Whitelist of user IDs. Empty = allow everyone; non-empty = only listed users can interact. |


## CLI Reference

| Command | Description |
|---------|-------------|
| `aegis onboard` | Initialize config & workspace |
| `aegis agent -m "..."` | Chat with the agent |
| `aegis agent` | Interactive chat mode |
| `aegis gateway` | Start the gateway |
| `aegis status` | Show status |
| `aegis channels login` | Link WhatsApp (scan QR) |
| `aegis channels status` | Show channel status |

<details>
<summary><b>Scheduled Tasks (Cron)</b></summary>

```bash
# Add a job
aegis cron add --name "daily" --message "Good morning!" --cron "0 9 * * *"
aegis cron add --name "hourly" --message "Check status" --every 3600

# List jobs
aegis cron list

# Remove a job
aegis cron remove <job_id>
```

</details>

## 🐳 Docker

> [!TIP]
> The `-v ~/.aegis:/root/.aegis` flag mounts your local config directory into the container, so your config and workspace persist across container restarts.

Build and run aegis in a container:

```bash
# Build the image
docker build -t aegis .

# Initialize config (first time only)
docker run -v ~/.aegis:/root/.aegis --rm aegis onboard

# Edit config on host to add API keys
vim ~/.aegis/config.json

# Run gateway (connects to Telegram/WhatsApp)
docker run -v ~/.aegis:/root/.aegis -p 18790:18790 aegis gateway

# Or run a single command
docker run -v ~/.aegis:/root/.aegis --rm aegis agent -m "Hello!"
docker run -v ~/.aegis:/root/.aegis --rm aegis status
```

## 📁 Project Structure

```
aegis/
├── agent/          # 🧠 Core agent logic
│   ├── loop.py     #    Agent loop (LLM ↔ tool execution)
│   ├── context.py  #    Prompt builder
│   ├── memory.py   #    Persistent memory
│   ├── skills.py   #    Skills loader
│   ├── subagent.py #    Background task execution
│   └── tools/      #    Built-in tools (incl. spawn)
├── skills/         # 🎯 Bundled skills (github, weather, tmux...)
├── channels/       # 📱 WhatsApp integration
├── bus/            # 🚌 Message routing
├── cron/           # ⏰ Scheduled tasks
├── heartbeat/      # 💓 Proactive wake-up
├── providers/      # 🤖 LLM providers (OpenRouter, etc.)
├── session/        # 💬 Conversation sessions
├── config/         # ⚙️ Configuration
└── cli/            # 🖥️ Commands
```

## 🤝 Contribute & Roadmap

PRs welcome! The codebase is intentionally small and readable. 🤗

**Roadmap** — Pick an item and [open a PR](https://github.com/HKUDS/aegis/pulls)!

- [x] **Voice Transcription** — Support for Groq Whisper (Issue #13)
- [ ] **Multi-modal** — See and hear (images, voice, video)
- [ ] **Long-term memory** — Never forget important context
- [ ] **Better reasoning** — Multi-step planning and reflection
- [ ] **More integrations** — Discord, Slack, email, calendar
- [ ] **Self-improvement** — Learn from feedback and mistakes

### Contributors

<a href="https://github.com/HKUDS/aegis/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/aegis&max=100&columns=12" />
</a>


## ⭐ Star History

<div align="center">
  <a href="https://star-history.com/#HKUDS/aegis&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/aegis&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/aegis&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/aegis&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

<p align="center">
  <em> Thanks for visiting ✨ aegis!</em><br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.aegis&style=for-the-badge&color=00d4ff" alt="Views">
</p>


<p align="center">
  <sub>aegis is for educational, research, and technical exchange purposes only</sub>
</p>
