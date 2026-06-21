import asyncio
from google.adk.sessions import InMemorySessionService

async def test():
    s = InMemorySessionService()
    res = await s.get_session(app_name='test', user_id='test', session_id='test')
    print('Result:', res)

asyncio.run(test())
