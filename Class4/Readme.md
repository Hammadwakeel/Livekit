# LiveKit Voice AI Agent: Lesson 4 — Voice RAG & Local Memory
### **Developed by [Hammad Wakeel](https://github.com/Hammadwakeel)**

This repository contains the implementation for **Lesson 4: Retrieval-Augmented Generation (RAG)**. In this class, we solved the biggest problem with LLMs—hallucinations—by giving the Voice Agent a "Photographic Memory" using a local Vector Database.

The agent can now accurately answer questions about private, domain-specific data (in this case, the *"Attention Is All You Need"* research paper) without relying on general internet knowledge.

---

## Architectural Breakthroughs in Class 4

To build a secure, fast, and cost-effective RAG pipeline, this project implements several advanced engineering techniques:

### **1. 100% Local Vector Embeddings (Zero Cost)**
Instead of sending private data to OpenAI's embedding API and paying per token, this agent uses Hugging Face's `sentence-transformers` (`all-MiniLM-L6-v2`). 
* **The Result:** Text is converted to high-dimensional vectors directly on the local CPU. Maximum privacy, zero API costs.

### **2. FAISS Vector Database**
We replaced standard databases with **FAISS (Facebook AI Similarity Search)**. 
* **The Result:** By using `numpy` and `IndexFlatL2`, the agent performs lightning-fast Euclidean distance calculations to find the exact paragraph needed to answer the user's question in milliseconds.

### **3. LiveKit Cloud Inference**
We streamlined the environment by routing all STT (Deepgram), LLM (GPT-4o-mini), and TTS (Cartesia) requests through LiveKit's Inference API.
* **The Result:** No need to manage multiple API keys. A single LiveKit connection handles the entire voice pipeline.

---

## The Tech Stack

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LiveKit Agents SDK | Handles the WebRTC audio stream and agent state. |
| **Vector Engine** | FAISS & Numpy | High-performance C++ matrix math for similarity search. |
| **Embeddings** | `sentence-transformers` | Runs local AI models to map text into vector space. |
| **Intelligence** | GPT-4o-mini (via LiveKit) | Evaluates the retrieved FAISS data to speak a natural response. |

---

## Setup & Execution

### **1. Environment Setup**
Ensure you have `uv` installed. Navigate to the `Class4` folder and run:
```bash
uv venv
source .venv/bin/activate
uv add livekit-agents livekit-plugins-silero livekit-plugins-turn-detector python-dotenv faiss-cpu numpy sentence-transformers
```

### **2. Configure Keys**
Create a `.env` file in the root of `Class4`. Because we use local embeddings and LiveKit Inference, you **only** need your LiveKit credentials:
```env
LIVEKIT_URL=wss://your-url.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```

### **3. Run the Agent**
The first time you run this, it will take a few seconds to download the local `all-MiniLM-L6-v2` model to your machine.
```bash
# Download required local assets (Turn Detector & Embeddings)
uv run agent.py download-files

# Start the interactive console
uv run agent.py console
```

---

## How to Test the RAG Memory

Once the agent introduces itself, ask it questions specifically about the embedded data to trigger the FAISS search tool:
* *"What is the Transformer architecture based on?"*
* *"Why do we use Positional Encoding?"*
* *"Can you explain how Scaled Dot-Product Attention is computed?"*

Watch your terminal—you will see the exact `L2 Distance` and `Index` of the vector match before the AI speaks!

---

## Learnings by Hammad Wakeel
* **Vector Math:** Mastered the integration of `numpy` arrays `astype('float32')` to interact with low-level FAISS C++ bindings.
* **Async Threading:** Utilized `asyncio.to_thread()` to ensure the CPU-heavy local embedding process does not block the real-time WebRTC audio stream.
* **Cost Optimization:** Successfully bypassed paid embedding APIs in favor of open-source Hugging Face models.
```
