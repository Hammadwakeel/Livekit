import asyncio
import logging
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli, function_tool, RunContext
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("class4-faiss-agent")

load_dotenv()

# --- 🧠 DATA PREPARATION & FAISS SETUP ---
logger.info("Initializing Local FAISS Vector Index (Zero API Keys)...")

# Excerpts from "Attention Is All You Need"
paper_chunks = [
    "The Transformer is a novel network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
    "Scaled Dot-Product Attention is computed as the softmax of the dot product of the query and key, divided by the square root of the dimension of the key, multiplied by the value.",
    "Multi-Head Attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.",
    "Positional Encoding is added to the input embeddings at the bottoms of the encoder and decoder stacks to inject some information about the relative or absolute position of the tokens in the sequence."
]

# Load a small, extremely fast local embedding model (Runs on CPU)
logger.info("Loading SentenceTransformer model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 1. Convert text chunks to vector embeddings locally
raw_embeddings = embedding_model.encode(paper_chunks)

# 2. FAISS requires data to be in a float32 numpy array
embedding_matrix = np.array(raw_embeddings).astype('float32')
dimension = embedding_matrix.shape[1] # 384 for all-MiniLM-L6-v2

# 3. Create the FAISS Index
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embedding_matrix)

logger.info(f"FAISS index built with {faiss_index.ntotal} vectors of dimension {dimension}.")

# --- 🛠️ THE RAG TOOL ---
@function_tool
async def search_transformer_paper(
    context: RunContext,
    query: str,
):
    """
    Called when the user asks questions about the 'Attention Is All You Need' paper, Transformers, or AI architecture.
    Args:
        query: The specific question or concept to search for in the paper.
    """
    logger.info(f"FAISS Tool Triggered: Searching for '{query}'")
    
    try:
        # 1. Embed the user's voice query LOCALLY (Running in asyncio to not block the audio stream)
        query_vector = await asyncio.to_thread(embedding_model.encode, [query])
        query_vector = np.array(query_vector).astype('float32')

        # 2. Search the FAISS index for the top 1 closest match
        distances, indices = faiss_index.search(query_vector, k=1)
        
        match_index = indices[0][0]
        match_distance = distances[0][0]
        
        logger.info(f"FAISS Match Found (Index: {match_index}, L2 Distance: {match_distance})")
        
        if match_index != -1:
            retrieved_text = paper_chunks[match_index]
            return f"According to the paper: {retrieved_text}"
        else:
            return "I couldn't find anything relevant in the paper."
            
    except Exception as e:
        logger.error(f"RAG Search failed: {e}")
        return "I had trouble accessing the vector index."

# --- 🎙️ THE AGENT SESSION ---
server = AgentServer()

@server.rtc_session(agent_name="class4-faiss-rag")
async def my_agent(ctx: agents.JobContext):
    logger.info(f"Connecting to room: {ctx.room.name}")

    # These models run entirely through LiveKit Inference using your LIVEKIT_API_KEY
    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm="openai/gpt-4o-mini",
        tts="cartesia/sonic-3",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        allow_interruptions=True,
        preemptive_generation=True, 
    )

    agent = Agent(
        instructions="""You are an AI research assistant. 
        You have access to a FAISS vector index containing the 'Attention Is All You Need' paper.
        Whenever the user asks about the paper, transformers, or attention mechanisms, use the search_transformer_paper tool.
        Keep your spoken responses natural, concise, and academic.""",
        tools=[search_transformer_paper], 
    )

    await ctx.connect()
    await session.start(room=ctx.room, agent=agent)
    await session.generate_reply(instructions="Introduce yourself as an AI research assistant and ask what they want to know about the Transformer architecture.")

if __name__ == "__main__":
    cli.run_app(server)