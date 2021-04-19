from pathlib import Path

import pytest
from aionexusmods import NexusMods
from aionexusmods.nexusmods import USER_AGENT

API_KEY = Path("secrets/API_KEY").read_text()
GAME = "Morrowind"


def test_user_agent() -> None:
    assert USER_AGENT.startswith("aionexusmods/0.1")


@pytest.mark.asyncio
async def test_user_details() -> None:
    async with NexusMods(API_KEY, GAME) as nexusmods:
        assert await nexusmods.get_user_details()


@pytest.mark.asyncio
async def test_latest_added() -> None:
    async with NexusMods(API_KEY, GAME) as nexusmods:
        latest_added = await nexusmods.get_latest_added()
        assert len(latest_added) == 10


@pytest.mark.asyncio
async def test_session_closed() -> None:
    async with NexusMods(API_KEY, GAME) as nexusmods:
        assert nexusmods._session.closed == False  # type: ignore[union-attr]
    assert nexusmods._session.closed == True  # type: ignore[union-attr]


@pytest.mark.asyncio
async def test_sequential_sessions() -> None:
    nexusmods = NexusMods(API_KEY, GAME)
    async with nexusmods:
        pass
    async with nexusmods:
        pass


@pytest.mark.asyncio
async def test_session_not_started() -> None:
    nexusmods = NexusMods(API_KEY, GAME)
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user_details()
    assert str(e.value) == "attempted to use a session before it was started"


@pytest.mark.asyncio
async def test_session_used_after_closed() -> None:
    async with NexusMods(API_KEY, GAME) as nexusmods:
        pass
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user_details()
    assert str(e.value) == "attempted to use a session after it was closed"


@pytest.mark.asyncio
async def test_overlapping_sessions_started() -> None:
    with pytest.raises(RuntimeError) as e:
        nexus_mods = NexusMods(API_KEY, GAME)
        async with nexus_mods:
            async with nexus_mods:
                pass
    assert str(e.value) == "attemped to start a new session before closing the previous one"
