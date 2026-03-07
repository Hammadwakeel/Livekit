import asyncio
from dotenv import load_dotenv

from livekit import agents, rtc
# In the latest SDK, AgentServer and AgentSession are standard for Job management
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load your environment variables
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
    # Lecture 1: Defining the session with high-speed 2026 models
    session = AgentSession(
        stt="deepgram/nova-3:multi", # High speed STT
        llm="openai/gpt-4.1-mini",  # Smart Brain
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc", # Low-latency TTS
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(), # Prevents interruptions
    )

    await ctx.connect() # Ensure we are connected to the LiveKit room first

    # Setup the audio pipeline with Noise Cancellation
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

    # Trigger the first greeting
    await session.generate_reply(
        instructions="Greet the user warmly and offer your assistance."
    )

if __name__ == "__main__":
    # Use the standard CLI runner for 2026
    cli.run_app(server)