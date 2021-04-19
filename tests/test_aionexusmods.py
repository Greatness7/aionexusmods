from pathlib import Path

import pytest
import toml
from aionexusmods import NexusMods

from .mock_data import mock_responses

API_KEY = Path("secrets/API_KEY").read_text()
GAME = "morrowind"


def test_user_agent() -> None:
    poetry = toml.load("pyproject.toml")["tool"]["poetry"]
    prefix = f'{poetry["name"]}/{poetry["version"]}'
    assert NexusMods.USER_AGENT.startswith(prefix)


@pytest.mark.asyncio
async def test_get_user(mock_responses):  # type: ignore
    async with NexusMods(API_KEY, GAME) as nexusmods:
        assert await nexusmods.get_user()


@pytest.mark.asyncio
async def test_session_closed(mock_responses):  # type: ignore
    async with NexusMods(API_KEY, GAME) as nexusmods:
        assert nexusmods._session is not None
        assert nexusmods._session.closed == False
    assert nexusmods._session.closed == True


@pytest.mark.asyncio
async def test_sequential_sessions(mock_responses):  # type: ignore
    nexusmods = NexusMods(API_KEY, GAME)
    async with nexusmods:
        pass
    async with nexusmods:
        pass


@pytest.mark.asyncio
async def test_session_not_started(mock_responses):  # type: ignore
    nexusmods = NexusMods(API_KEY, GAME)
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user()
    assert str(e.value) == "attempted to use a session before it was started"


@pytest.mark.asyncio
async def test_session_used_after_closed(mock_responses):  # type: ignore
    async with NexusMods(API_KEY, GAME) as nexusmods:
        pass
    with pytest.raises(RuntimeError) as e:
        await nexusmods.get_user()
    assert str(e.value) == "attempted to use a session after it was closed"


@pytest.mark.asyncio
async def test_overlapping_sessions_started(mock_responses):  # type: ignore
    with pytest.raises(RuntimeError) as e:
        nexus_mods = NexusMods(API_KEY, GAME)
        async with nexus_mods:
            async with nexus_mods:
                pass
    assert str(e.value) == "attemped to start a new session before closing the previous one"
