"""
ARYA Prototype - AI Career Counselor Voice Agent
Entry point for the AI Telephony Agent using Sarvam STT + Gemini LLM + Sarvam TTS
"""

import asyncio
import traceback
import os
import logging
import sys
from dotenv import load_dotenv

# Fix Unicode issue on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from videosdk.agents import (
    AgentSession,
    CascadingPipeline,
    JobContext,
    RoomOptions,
    WorkerJob,
    Options,
    ConversationFlow,
    InterruptConfig,
)
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.sarvamai import SarvamAISTT, SarvamAITTS
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector

from agent import ARYAAgent
from config.settings import settings

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

AGENT_ID = os.getenv("AGENT_ID", "ARYA_Careers360")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "8081"))
MAX_PROCESSES = int(os.getenv("MAX_PROCESSES", "10"))


async def start_session(context: JobContext):
    """Start the ARYA agent session."""
    logger.info("Starting ARYA agent session...")
    
    session = None
    
    try:
        logger.info("Initializing Sarvam STT for Indian languages...")
        stt = SarvamAISTT(
            model="saarika:v2.5",
            language="en-IN",
        )
        logger.info("Sarvam STT initialized successfully")
        
        logger.info("Initializing OpenRouter LLM (free tier)...")
        llm = OpenAILLM(
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            api_key=settings.openrouter_api_key,
            temperature=0.7,
        )
        logger.info("Gemini LLM initialized successfully")
        
        logger.info("Initializing Sarvam TTS for Indian languages...")
        tts = SarvamAITTS(
            model="bulbul:v2",
            speaker="anushka",
            language="en-IN",
        )
        logger.info("Sarvam TTS initialized successfully")
        
        logger.info("Creating CascadingPipeline...")
        pipeline = CascadingPipeline(
            stt=stt,
            llm=llm,
            tts=tts,
            vad=SileroVAD(threshold=0.35),
            turn_detector=TurnDetector(threshold=0.8),
            interrupt_config=InterruptConfig(
                mode="NONE",  # Disable interruption handling to fix LLM cancellation error
            ),
        )
        logger.info("Pipeline created successfully")
        
        logger.info("Creating ARYAAgent...")
        agent = ARYAAgent()
        logger.info("Agent created successfully")
        
        logger.info("Creating ConversationFlow...")
        conversation_flow = ConversationFlow(agent)
        logger.info("ConversationFlow created successfully")
        
        logger.info("Creating AgentSession...")
        session = AgentSession(agent=agent, pipeline=pipeline, conversation_flow=conversation_flow)
        logger.info("Session created successfully")
        
        logger.info("Connecting to VideoSDK...")
        await context.connect()
        logger.info("Connected to VideoSDK")
        
        logger.info("Starting agent session...")
        await session.start()
        logger.info("Agent session started - waiting for calls...")
        
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Error in start_session: {e}")
        traceback.print_exc()
        raise
    finally:
        logger.info("Shutting down session...")
        try:
            if session is not None:
                await session.close()
            await context.shutdown()
            logger.info("Session shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


def make_context() -> JobContext:
    """Create the job context with room options."""
    room_options = RoomOptions(
        background_audio=True,
    )
    return JobContext(room_options=room_options)


def main():
    """Main entry point."""
    try:
        print("\n" + "="*60)
        print("ARYA Career Counselor Agent")
        print("Careers360 AI Voice Assistant")
        print("Architecture: Sarvam STT + Gemini LLM + Sarvam TTS")
        print("="*60 + "\n")
        
        print("Configuration:")
        print(f"  Agent ID: {AGENT_ID}")
        print(f"  Host: {HOST}:{PORT}")
        print(f"  Max Processes: {MAX_PROCESSES}")
        print(f"  STT: Sarvam AI (saarika:v2.5)")
        print(f"  LLM: Gemini 2.5 Flash Native Audio (TEXT mode)")
        print(f"  TTS: Sarvam AI (bulbul:v2, anushka)")
        print("")
        
        if not os.getenv("VIDEOSDK_AUTH_TOKEN"):
            print("[ERROR] VIDEOSDK_AUTH_TOKEN not set!")
            print("Please add your token to the .env file")
            return 1
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("[ERROR] GOOGLE_API_KEY not set!")
            print("Please add your API key to the .env file")
            return 1
        
        if not os.getenv("SARVAMAI_API_KEY"):
            print("[ERROR] SARVAMAI_API_KEY not set!")
            print("Please add your API key to the .env file")
            return 1
        
        print("[OK] Environment variables configured")
        print("")
        
        options = Options(
            agent_id=AGENT_ID,
            register=True,
            max_processes=MAX_PROCESSES,
            host=HOST,
            port=PORT,
        )
        
        job = WorkerJob(
            entrypoint=start_session,
            jobctx=make_context,
            options=options,
        )
        
        print("Starting worker...")
        print("Waiting for incoming calls...")
        print("\n" + "="*60 + "\n")
        
        job.start()
        
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Received keyboard interrupt")
        return 0
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
