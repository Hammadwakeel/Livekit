# 🎙️ LiveKit Voice AI Agent: Lesson 1 — The Pipeline

### **Developed by [Hammad Wakeel**](https://www.google.com/search?q=https://github.com/Hammadwakeel)

This repository contains a professional-grade, real-time Voice AI Agent built using the **LiveKit Agents SDK**. This project marks the successful implementation of **Lesson 1: Mastering the Pipeline**, which focuses on creating a high-speed, "cascaded" AI architecture for seamless human-computer interaction.

---

## 🚀 Architecture Overview

To achieve a natural conversation, this agent uses a **Cascaded Pipeline** architecture. This ensures that the time between you finishing a sentence and the AI responding (TTFA) remains under **500ms**.

### **The AI Tech Stack**

* **VAD (Voice Activity Detection):** [Silero VAD](https://github.com/snakers4/silero-vad) — Detects speech locally on your CPU.
* **STT (Speech-to-Text):** [Deepgram Nova-3](https://developers.deepgram.com/) — High-speed transcription with multilingual support.
* **LLM (Large Language Model):** [OpenAI GPT-4o-mini](https://openai.com/) — Fast reasoning and conversational logic.
* **TTS (Text-to-Speech):** [Cartesia Sonic](https://cartesia.ai/) — Generative audio for realistic, low-latency voices.
* **Turn Detection:** [Multilingual Semantic Model](https://github.com/livekit/agents) — Understands sentence structure to avoid interruptions.

---

## 💻 Technical Code Breakdown

The core logic of the agent is divided into functional blocks within `agent.py`. Here is how the system is constructed:

### **1. The Brain's Personality (System Instructions)**

This block defines the "rules of engagement" for the AI. By using a class-based structure, we encapsulate the personality and conversational constraints.

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            Your responses are concise, to the point, and without any complex formatting.
            You are curious, friendly, and have a sense of humor.""",
        )

```

### **2. The Multi-Model Pipeline (The Session)**

This is the "engine room" where the STT, LLM, TTS, and VAD are wired together. We use specific model IDs to ensure the agent uses the fastest tools available.

```python
@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        stt="deepgram/nova-3:multi",
        llm="openai/gpt-4o-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(), # Semantic intelligence to wait for your thought to finish
    )

```

### **3. Audio Processing & Noise Cancellation**

This block handles "Audio I/O." It applies **BVC (Background Voice Cancellation)** to ensure the AI only hears the primary speaker, even in noisy environments.

```python
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() 
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP 
                else noise_cancellation.BVC(),
            ),
        ),
    )

```

### **4. Execution & Entry Point**

The final block connects the worker to the LiveKit server and triggers an initial proactive greeting.

```python
    await ctx.connect() 

    await session.generate_reply(
        instructions="Greet the user warmly and offer your assistance."
    )

if __name__ == "__main__":
    cli.run_app(server)

```

---

## 🛠️ Setup & Installation

1. **Clone the Repository:**
```bash
git clone https://github.com/Hammadwakeel/Livekit.git
cd Livekit/Class1

```


2. **Install Dependencies (using UV):**
```bash
uv sync

```


3. **Configure Environment Variables (`.env`):**
get your API keys from https://cloud.livekit.io/projects/p_3t2zl5b1pid/settings/keys for free
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```


4. **Download AI Models & Run:**
```bash
uv run agent.py download-files
uv run agent.py console

```



---

## 🧠 Key Learnings

* **Real-time WebRTC Streaming:** Managed bidirectional audio streams with negligible buffer.
* **Semantic Turn-Taking:** Implemented logic that differentiates between a "thoughtful pause" and a "finished sentence."
* **Hardware Optimization:** Learned how to balance local CPU usage (for VAD/Noise Cancellation) with cloud inference (STT/LLM).

---
