import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Professional logging
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

    # CLASS 2: Moved allow_interruptions and added preemptive_generation
    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm="openai/gpt-4o-mini",
        tts="cartesia/sonic-3",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        allow_interruptions=True, # MOVED HERE
        preemptive_generation=True, 
    )

    await ctx.connect()

    # Cleaned up start call
    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(instructions="Greet the user warmly.")

if __name__ == "__main__":
    cli.run_app(server)