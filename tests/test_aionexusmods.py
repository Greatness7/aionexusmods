import pytest

from aionexusmods import NexusMods
from aionexusmods.nexusmods import USER_AGENT

API_KEY = ""
GAME = ""


@pytest.mark.asyncio
async def test_user_agent():
    assert USER_AGENT.startswith("aionexusmods/0.1.0")


@pytest.mark.asyncio
async def test_session_closed():
    async with NexusMods(API_KEY, GAME) as nexusmods:
        assert nexusmods._session.closed == False
    assert nexusmods._session.closed == True


@pytest.mark.asyncio
async def test_sequential_sessions():
    nexusmods = NexusMods(API_KEY, GAME)
    async with nexusmods:
        pass
    async with nexusmods:
        pass


@pytest.mark.asyncio
async def test_session_not_started():
    nexusmods = NexusMods(API_KEY, GAME)
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user_details()
    assert str(e.value) == "attempted to use a session before it was started"


@pytest.mark.asyncio
async def test_session_used_after_closed():
    async with NexusMods(API_KEY, GAME) as nexusmods:
        pass
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user_details()
    assert str(e.value) == "attempted to use a session after it was closed"


@pytest.mark.asyncio
async def test_overlapping_sessions_started():
    with pytest.raises(RuntimeError) as e:
        nexus_mods = NexusMods(API_KEY, GAME)
        async with nexus_mods:
            async with nexus_mods:
                pass
    assert str(e.value) == "attemped to start a new session before closing the previous one"
