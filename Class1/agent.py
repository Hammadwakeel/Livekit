import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# 1. Setup Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            Your responses are concise, to the point, and without complex formatting.
            You are curious, friendly, and have a sense of humor.""",
        )

server = AgentServer()

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    logger.info(f"Starting agent for room: {ctx.room.name}")

    session = AgentSession(
        stt="deepgram/nova-3:multi",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # 2. Add Event Listeners for Logging
    @session.on("user_started_speaking")
    def on_user_speech_start():
        logger.info("User started speaking...")

    @session.on("user_stopped_speaking")
    def on_user_speech_stop():
        logger.info("User stopped speaking. Processing...")

    @session.on("agent_started_speaking")
    def on_agent_speech_start():
        logger.info("Agent is responding...")

    @session.on("metrics_collected")
    def on_metrics(metrics):
        # This is great for SEO/Performance tracking!
        logger.info(f"Metrics Collected: {metrics}")

    await ctx.connect()

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

    logger.info("Agent session started successfully.")

    await session.generate_reply(
        instructions="Greet the user warmly and offer your assistance."
    )

if __name__ == "__main__":
    cli.run_app(server)