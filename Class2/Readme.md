# 🎙️ LiveKit Voice AI Agent: Lesson 2 — Natural Interactions

### **Developed by [Hammad Wakeel**](https://www.google.com/search?q=https://github.com/Hammadwakeel)

This repository contains the implementation for **Lesson 2: Mastering Natural Interactions**. Building upon the basic pipeline from Lesson 1, this class focuses on "Social Intelligence"—specifically how an AI agent handles turn-taking, interruptions, and low-latency thinking.

---

## 🚀 Advanced Features in Class 2

To make the AI feel less like a machine and more like a human, we have implemented three critical features:

### **1. Semantic Turn Detection**

Standard Voice Activity Detection (VAD) only detects silence. If you pause to think, the AI might interrupt you.

* **The Solution:** We integrated the **Multilingual Semantic Turn Detector**. This local transformer model analyzes the transcript to see if your sentence is actually finished or if you are just pausing mid-thought.

### **2. Interruption Handling (`allow_interruptions`)**

One of the biggest pain points in Voice AI is the agent "talking over" the user.

* **The Solution:** By enabling `allow_interruptions=True`, the agent instantly kills its audio output stream the moment it detects your voice, allowing for natural, fluid conversation.

### **3. Preemptive Generation**

Waiting for the user to finish speaking before "thinking" adds unnecessary latency.

* **The Solution:** With `preemptive_generation=True`, the LLM starts processing a potential response *while you are still speaking*. This shaves hundreds of milliseconds off the response time.

---

## 💻 The Source Code: `agent.py`

This version of the agent is optimized for the **2026 LiveKit SDK** and includes professional logging.

```python
import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Professional logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent-class2")

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful and natural voice AI assistant.
            Keep responses concise and conversational. 
            If the user interrupts you, stop immediately and listen.""",
        )

server = AgentServer()

@server.rtc_session(agent_name="class2-agent")
async def my_agent(ctx: agents.JobContext):
    logger.info(f"Connecting to room: {ctx.room.name}")

    # Initializing the session with Class 2 Intelligence
    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm="openai/gpt-4o-mini",
        tts="cartesia/sonic-3",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(), # Semantic Turn Detection
        allow_interruptions=True,           # Instant response to user voice
        preemptive_generation=True,         # Zero-latency thinking
    )

    await ctx.connect()

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(instructions="Greet the user warmly.")

if __name__ == "__main__":
    cli.run_app(server)

```

---

## 🔍 Why This Matters

| Feature | Without It | With Class 2 |
| --- | --- | --- |
| **Interruptions** | Agent ignores you and keeps talking. | Agent stops immediately when you speak. |
| **Pausing** | Agent interrupts your mid-sentence pause. | Agent waits for you to finish your thought. |
| **Latency** | Noticeable gap before AI starts talking. | Near-instant response via preemptive logic. |

---

## 🛠️ Setup & Execution

1. **Navigate to Folder:**
```bash
cd Class2

```


2. **Activate Environment:**
```bash
source .venv/bin/activate

```


3. **Download Model Weights:**
The Turn Detector requires local weights (~135MB).
```bash
uv run agent.py download-files

```


4. **Launch Agent:**
```bash
uv run agent.py console

```



---

## 🧠 Learnings by Hammad Wakeel

* **NLP for Turn-Taking:** Implemented local transformer models to handle conversational nuances.
* **State Management:** Learned how to handle session-level interruptions in the LiveKit 2026 SDK.
* **UX Design:** Focused on the "human feel" of AI, moving beyond just accuracy to focus on rhythm and flow.
