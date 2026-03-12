import asyncio
import logging
import aiohttp
import os
from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, cli, function_tool, RunContext
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Setup professional logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("class3-tool-agent")

load_dotenv()

# --- THE UTILITY BELT (TOOLS) ---

@function_tool
async def get_weather(
    context: RunContext,
    location: str,
):
    """
    Called when the user asks about the weather.
    Args:
        location: The city or place to check the weather for.
    """
    logger.info(f"Tool Call: Fetching real-time weather for {location}")
    
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    # Using https is safer and more reliable
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']
                    return f"The weather in {location} is currently {temp}°C with {desc}."
                elif response.status == 401:
                    # This happens if the email isn't verified or the key is too new
                    logger.error("Weather API Error: 401 Unauthorized. Key might be unverified or too new.")
                    return "My weather service is still warming up. It should be ready in about an hour after email verification."
                else:
                    return f"I couldn't get the weather (Error {response.status}). Would you like to try again later?"
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return "I'm having trouble connecting to the weather service."
# --- THE AGENT SESSION ---

server = AgentServer()

@server.rtc_session(agent_name="class3-agent")
async def my_agent(ctx: agents.JobContext):
    logger.info(f"Connecting to room: {ctx.room.name}")

    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm="openai/gpt-4o-mini",
        tts="cartesia/sonic-3",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        allow_interruptions=True,
        preemptive_generation=True, 
    )

    # Initialize the Agent with the tool
    agent = Agent(
        instructions="""You are a helpful and natural voice AI assistant. 
        You have the ability to check real-time weather using the get_weather tool. 
        Keep your verbal responses short and conversational.""",
        tools=[get_weather], # Register the tool here
    )

    await ctx.connect()

    await session.start(
        room=ctx.room,
        agent=agent,
    )

    await session.generate_reply(instructions="Greet the user and mention you can check the weather for them.")

if __name__ == "__main__":
    cli.run_app(server)