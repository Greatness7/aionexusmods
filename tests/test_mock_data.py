import pytest
from aionexusmods import NexusMods

from .mock_data import *


@pytest.mark.asyncio
async def test_mock(mock_responses):  # type: ignore
    async with NexusMods(MOCK_API_KEY, MOCK_GAME_DOMAIN_NAME) as nexusmods:
        assert await nexusmods.get_mod_updates("1d") == [MOCK_MOD_UPDATE]
        assert await nexusmods.get_mod_changelogs(MOCK_MOD_ID) == MOCK_CHANGELOGS
        assert await nexusmods.get_latest_added_mods() == [MOCK_MOD]
        assert await nexusmods.get_latest_updated_mods() == [MOCK_MOD]
        assert await nexusmods.get_trending_mods() == [MOCK_MOD]
        assert await nexusmods.get_mod(MOCK_MOD_ID) == MOCK_MOD
        assert await nexusmods.get_md5_search(MOCK_MD5_HASH) == [(MOCK_MOD, MOCK_FILE)]
        assert await nexusmods.set_endorsed(MOCK_MOD_ID, "0.1.0", True) == MOCK_ENDORSED_MESSAGE
        assert await nexusmods.set_endorsed(MOCK_MOD_ID, "0.1.0", False) == MOCK_ABSTAINED_MESSAGE
        assert await nexusmods.get_files_and_updates(MOCK_MOD_ID) == ([MOCK_FILE], [MOCK_FILE_UPDATE])
        assert await nexusmods.get_file(MOCK_MOD_ID, MOCK_FILE_ID) == MOCK_FILE
        assert await nexusmods.get_download_links(MOCK_MOD_ID, MOCK_FILE_ID) == [MOCK_DOWNLOAD_LINK]
        assert await nexusmods.get_games() == [MOCK_GAME]
        assert await nexusmods.get_game() == MOCK_GAME
        assert await nexusmods.get_user() == MOCK_USER
        assert await nexusmods.get_tracked_mods() == [MOCK_TRACKED_MOD]
        assert await nexusmods.set_tracked(MOCK_MOD_ID, True) == MOCK_TRACKED_MESSAGE
        assert await nexusmods.set_tracked(MOCK_MOD_ID, False) == MOCK_UNTRACKED_MESSAGE
        assert await nexusmods.get_endorsements() == [MOCK_ENDORSEMENT]
        assert await nexusmods.get_colour_schemes() == [MOCK_COLOUR_SCHEME]
