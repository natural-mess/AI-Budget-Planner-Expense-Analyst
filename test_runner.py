import asyncio
from app.agent import app as adk_app
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService

async def main():
    runner = Runner(
        app=adk_app,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService()
    )
    async for event in runner.run_async('Hello'):
        print(event)

asyncio.run(main())
