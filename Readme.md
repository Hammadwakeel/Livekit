This root **README.md** acts as the main index for your entire "LiveKit" master repository, helping anyone (or your future self) understand the structure and purpose of the project at a glance.

---

# 🎙️ LiveKit Voice AI Masterclass

### **Maintained by [Hammad Wakeel**](https://www.google.com/search?q=https://github.com/Hammadwakeel)

Welcome to the **LiveKit Voice AI Masterclass** repository. This project is a comprehensive, step-by-step collection of lessons designed to take you from a beginner to an expert in building high-performance, real-time multimodal AI agents.

---

## 📂 Repository Structure

Each folder in this repository represents a specific "Class" or "Lesson" in the journey of mastering the LiveKit Agents SDK.

| Folder | Title | Focus | Status |
| --- | --- | --- | --- |
| `Class1/` | **The Pipeline** | VAD, STT, LLM, TTS, and basic wiring. | ✅ Complete |
| `Class2/` | **Advanced Interaction** | Interruptions, Tool Calling, and RAG. | 🚧 In Progress |
| `Class3/` | **Telephony & SIP** | Connecting AI to phone lines and PSTN. | ⏳ Planned |

---

## ✨ Core Technology Stack

This master project leverages the cutting edge of AI and WebRTC technology to ensure sub-second latency and natural conversations.

* **Real-time Media:** [LiveKit](https://livekit.io/) (WebRTC Infrastructure)
* **Intelligence:** OpenAI (GPT-4o), Groq (Llama-3), Google (Gemini)
* **Audio Engines:** Deepgram (STT), Cartesia (TTS), ElevenLabs (TTS)
* **Package Management:** [UV](https://github.com/astral-sh/uv) (Extremely fast Python environment manager)

---

## 🚀 Getting Started

To explore these lessons, it is recommended to navigate into each individual class folder and follow the specific instructions in their respective README files.

### **General Setup**

1. **Clone the master repo:**
```bash
git clone https://github.com/Hammadwakeel/Livekit.git
cd Livekit

```


2. **Configure Environment Variables (`.env`):**
get your API Keys from https://cloud.livekit.io/projects/p_3t2zl5b1pid/settings/keys for free.

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

## 🛠️ Global Development Commands

If you are using **UV**, you can manage the root workspace or individual projects easily:

```bash
# Sync dependencies for the whole project (if using a workspace)
uv sync

# Run a specific agent from the root (example)
uv run Class1/agent.py console

```

---

## 🤝 About the Author

**Hammad Wakeel** is an AI Engineer and Backend Developer specializing in building agentic AI workflows and complex RAG systems.

* **GitHub:** [@Hammadwakeel](https://www.google.com/search?q=https://github.com/Hammadwakeel)
* **Portfolio:** [hammadwakeel.vercel.app](https://hammadwakeel.vercel.app)

---
