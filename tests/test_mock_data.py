import pytest
from aiohttp import JsonPayload
from aioresponses import aioresponses  # type: ignore
from aionexusmods.nexusmods import *
from aionexusmods.schemas import *

MOCK_API_KEY = ""

MOCK_GAME_DOMAIN_NAME = "morrowind"

MOCK_MOD_ID = 49565

MOCK_FILE_ID = 1000023992

MOCK_MD5_HASH = "76cdb2bad9582d23c1f6f4d868218d6c"

MOCK_USER = {
    "user_id": 64030,
    "key": "",
    "name": "Greatness7",
    "is_premium?": True,
    "is_supporter?": True,
    "email": "greatness7@gmail.com",
    "profile_url": "https://forums.nexusmods.com/uploads/profile/photo-64030.png",
    "is_supporter": True,
    "is_premium": True,
}

MOCK_GAME = {
    "id": 100,
    "name": "Morrowind",
    "forum_url": "https://forums.nexusmods.com/index.php?/forum/111-morrowind/",
    "nexusmods_url": "https://nexusmods.com/morrowind",
    "genre": "RPG",
    "file_count": 22236,
    "downloads": 29702839,
    "domain_name": "morrowind",
    "approved_date": 1,
    "file_views": 135082400,
    "authors": 2546,
    "file_endorsements": 997932,
    "mods": 7956,
    "categories": [
        {"category_id": 1, "name": "Morrowind", "parent_category": False},
        {"category_id": 2, "name": "Buildings", "parent_category": 1},
    ],
}

MOCK_MOD_USER = {
    "member_id": 64030,
    "member_group_id": 27,
    "name": "Greatness7",
}

MOCK_ENDORSEMENT_STATUS = {
    "endorse_status": "Undecided",
    "timestamp": None,
    "version": None,
}

MOCK_MOD = {
    "name": "Nexus Mods API Test",
    "summary": "Brief overview",
    "description": "Detailed description",
    "picture_url": "https://staticdelivery.nexusmods.com/mods/100/images/49565/49565-1618581763-530333594.jpeg",
    "uid": 429496779165,
    "mod_id": 49565,
    "game_id": 100,
    "allow_rating": False,
    "domain_name": "morrowind",
    "category_id": 15,
    "version": "0.1.0",
    "endorsement_count": 0,
    "created_timestamp": 1618587177,
    "created_time": "2021-04-16T15:32:57.000+00:00",
    "updated_timestamp": 1618587177,
    "updated_time": "2021-04-16T15:32:57.000+00:00",
    "author": "Greatness7",
    "uploaded_by": "Greatness7",
    "uploaded_users_profile_url": "https://nexusmods.com/games/users/64030",
    "contains_adult_content": False,
    "status": "published",
    "available": True,
    "user": MOCK_MOD_USER,
    "endorsement": MOCK_ENDORSEMENT_STATUS,
}

MOCK_FILE = {
    "id": [1000023992, 100],
    "uid": 430496753592,
    "file_id": 1000023992,
    "name": "Nexus Mods API Test",
    "version": "0.1.0",
    "category_id": 4,
    "category_name": "OLD_VERSION",
    "is_primary": False,
    "size": 0,
    "file_name": "Nexus Mods API Test-49565-0-1-0-1618582484.zip",
    "uploaded_timestamp": 1618582484,
    "uploaded_time": "2021-04-16T14:14:44.000+00:00",
    "mod_version": "0.1.0",
    "external_virus_scan_url": "https://www.virustotal.com/gui/file/8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85/detection/f-8739c76e681f900923b900c9df0ef75cf421d39cabb54650c4b9ad19b6a76d85-1618577779",
    "description": "File description",
    "size_kb": 0,
    "changelog_html": "Version 0.1.0",
    "content_preview_link": "https://file-metadata.nexusmods.com/file/nexus-files-s3-meta/100/49565/Nexus Mods API Test-49565-0-1-0-1618582484.zip.json",
}

MOCK_SEARCH_RESULT = {
    "mod": MOCK_MOD,
    "file_details": MOCK_FILE,
}

MOCK_FILE_UPDATE = {
    "old_file_id": 1000023992,
    "new_file_id": 1000023994,
    "old_file_name": "Nexus Mods API " "Test-49565-0-1-0-1618582484.zip",
    "new_file_name": "Nexus Mods API " "Test-49565-0-2-0-1618592285.zip",
    "uploaded_timestamp": 1618592286,
    "uploaded_time": "2021-04-16T16:58:06.000+00:00",
}


MOCK_FILES_RESULT = {
    "files": [MOCK_FILE],
    "file_updates": [MOCK_FILE_UPDATE],
}

MOCK_MOD_UPDATE = {
    "mod_id": 49565,
    "latest_file_update": 1618587177,
    "latest_mod_activity": 1618587177,
}

MOCK_DOWNLOAD_LINK = {
    "name": "Nexus Global Content Delivery Network",
    "short_name": "Nexus CDN",
    "URI": "https://cf-files.nexusmods.com/cdn/100/49565/Nexus Mods API Test-49565-0-1-0-1618582484.zip?md5=V_BnIzJ3Weh-App8Zrb-9A&expires=1618620510&user_id=64030",
}

MOCK_COLOUR_SCHEME = {
    "id": 1,
    "name": "ReskinOrange",
    "primary_colour": "#da8e35",
    "secondary_colour": "#b4762c",
    "darker_colour": "#815316",
}

MOCK_TRACKED_MOD = {
    "mod_id": 49565,
    "domain_name": "morrowind",
}

MOCK_ENDORSEMENT = {
    "mod_id": 49565,
    "domain_name": "morrowind",
    "date": 1618592286,
    "version": "0.1.0",
    "status": "Endorsed",
}

MOCK_ENDORSED_MESSAGE = {"message": "Updated to: Endorsed", "status": "Endorsed"}
MOCK_ABSTAINED_MESSAGE = {"message": "Updated to: Abstained", "status": "Abstained"}
MOCK_TRACKED_MESSAGE = {"message": "User 64030 is now Tracking Mod: 49565"}
MOCK_UNTRACKED_MESSAGE = {"message": "User 64030 is no longer tracking 49565"}
MOCK_CHANGELOGS = {"0.1.0": ["Version 0.1.0"], "0.2.0": ["Version 0.2.0"]}

# -----------

MOCK_GET = [
    # nexusmods.get_updated("1d")
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/updated.json",
        {"body": JsonPayload({"period": "1d"})},
        [MOCK_MOD_UPDATE],
    ),
    # nexusmods.get_changelogs(MOCK_MOD_ID)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/changelogs.json",
        {},
        MOCK_CHANGELOGS,
    ),
    # nexusmods.get_latest_added()
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/latest_added.json",
        {},
        [MOCK_MOD],
    ),
    # nexusmods.get_latest_updated()
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/latest_updated.json",
        {},
        [MOCK_MOD],
    ),
    # nexusmods.get_trending()
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/trending.json",
        {},
        [MOCK_MOD],
    ),
    # nexusmods.get_mod(MOCK_MOD_ID)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}.json",
        {},
        MOCK_MOD,
    ),
    # nexusmods.get_md5_search(MOCK_MD5_HASH)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/md5_search/{MOCK_MD5_HASH}.json",
        {},
        [MOCK_SEARCH_RESULT],
    ),
    # nexusmods.get_files(MOCK_MOD_ID)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/files.json",
        {},
        MOCK_FILES_RESULT,
    ),
    # nexusmods.get_file(MOCK_MOD_ID, MOCK_FILE_ID)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/files/{MOCK_FILE_ID}.json",
        {},
        MOCK_FILE,
    ),
    # nexusmods.get_download_link(MOCK_MOD_ID, MOCK_FILE_ID)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/files/{MOCK_FILE_ID}/download_link.json",
        {},
        [MOCK_DOWNLOAD_LINK],
    ),
    # nexusmods.get_games()
    (
        f"{BASE_URL}/games.json",
        {},
        [MOCK_GAME],
    ),
    # nexusmods.get_game(GAME)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}.json",
        {},
        MOCK_GAME,
    ),
    # nexusmods.get_user_details()
    (
        f"{BASE_URL}/users/validate.json",
        {},
        MOCK_USER,
    ),
    # nexusmods.get_tracked_mods()
    (
        f"{BASE_URL}/user/tracked_mods.json",
        {},
        [MOCK_TRACKED_MOD],
    ),
    # nexusmods.get_endorsements()
    (
        f"{BASE_URL}/user/endorsements.json",
        {},
        [MOCK_ENDORSEMENT],
    ),
    # nexusmods.get_colour_schemes()
    (
        f"{BASE_URL}/colourschemes.json",
        {},
        [MOCK_COLOUR_SCHEME],
    ),
]

MOCK_POST = [
    # nexusmods.set_tracked(mod_id, True)
    (
        f"{BASE_URL}/user/tracked_mods.json",
        {"body": JsonPayload({"mod_id": MOCK_MOD_ID, "DOMAIN_NAME": MOCK_GAME_DOMAIN_NAME})},
        MOCK_TRACKED_MESSAGE,
    ),
    # nexusmods.set_endorsed(mod_id, True)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/endorse.json",
        {"body": JsonPayload({"version": "0.1.0"})},
        MOCK_ENDORSED_MESSAGE,
    ),
    # nexusmods.set_endorsed(mod_id, False)
    (
        f"{BASE_URL}/games/{MOCK_GAME_DOMAIN_NAME}/mods/{MOCK_MOD_ID}/abstain.json",
        {"body": JsonPayload({"version": "0.1.0"})},
        MOCK_ABSTAINED_MESSAGE,
    ),
]

MOCK_DELETE = [
    # nexusmods.set_tracked(mod_id, False)
    (
        f"{BASE_URL}/user/tracked_mods.json",
        {"body": JsonPayload({"mod_id": MOCK_MOD_ID, "DOMAIN_NAME": MOCK_GAME_DOMAIN_NAME})},
        MOCK_UNTRACKED_MESSAGE,
    ),
]


@pytest.fixture
def _aioresponse():
    with aioresponses() as mock:
        for url, kwargs, payload in MOCK_GET:
            mock.get(url, **kwargs, payload=payload)
        for url, kwargs, payload in MOCK_POST:
            mock.post(url, **kwargs, payload=payload)
        for url, kwargs, payload in MOCK_DELETE:
            mock.delete(url, **kwargs, payload=payload)
        yield mock


@pytest.mark.asyncio
async def test_mock(_aioresponse):
    async with NexusMods(MOCK_API_KEY, MOCK_GAME_DOMAIN_NAME) as nexusmods:
        mod_update = ModUpdateSchema.load(MOCK_MOD_UPDATE)
        changelogs = MOCK_CHANGELOGS
        mod = ModSchema.load(MOCK_MOD)
        search_result = SearchResultSchema.load(MOCK_SEARCH_RESULT)
        endorsed_status = StatusSchema.load(MOCK_ENDORSED_MESSAGE)
        abstained_status = StatusSchema.load(MOCK_ABSTAINED_MESSAGE)
        files_result = FilesResultSchema.load(MOCK_FILES_RESULT)
        file = FileSchema.load(MOCK_FILE)
        download_link = DownloadLinkSchema.load(MOCK_DOWNLOAD_LINK)
        game = GameSchema.load(MOCK_GAME)
        user = UserSchema.load(MOCK_USER)
        tracked_mod = TrackedModSchema.load(MOCK_TRACKED_MOD)
        tracked_message = MessageSchema.load(MOCK_TRACKED_MESSAGE)
        untracked_message = MessageSchema.load(MOCK_UNTRACKED_MESSAGE)
        endorsement = EndorsementSchema.load(MOCK_ENDORSEMENT)
        colour_scheme = ColourSchemeSchema.load(MOCK_COLOUR_SCHEME)

        assert await nexusmods.get_updated("1d") == [mod_update]
        assert await nexusmods.get_changelogs(MOCK_MOD_ID) == changelogs
        assert await nexusmods.get_latest_added() == [mod]
        assert await nexusmods.get_latest_updated() == [mod]
        assert await nexusmods.get_trending() == [mod]
        assert await nexusmods.get_mod(MOCK_MOD_ID) == mod
        assert await nexusmods.get_md5_search(MOCK_MD5_HASH) == [search_result]
        assert await nexusmods.set_endorsed(MOCK_MOD_ID, "0.1.0", True) == endorsed_status
        assert await nexusmods.set_endorsed(MOCK_MOD_ID, "0.1.0", False) == abstained_status
        assert await nexusmods.get_files(MOCK_MOD_ID) == files_result
        assert await nexusmods.get_file(MOCK_MOD_ID, MOCK_FILE_ID) == file
        assert await nexusmods.get_download_link(MOCK_MOD_ID, MOCK_FILE_ID) == [download_link]
        assert await nexusmods.get_games() == [game]
        assert await nexusmods.get_game() == game
        assert await nexusmods.get_user_details() == user
        assert await nexusmods.get_tracked_mods() == [tracked_mod]
        assert await nexusmods.set_tracked(MOCK_MOD_ID, True) == tracked_message
        assert await nexusmods.set_tracked(MOCK_MOD_ID, False) == untracked_message
        assert await nexusmods.get_endorsements() == [endorsement]
        assert await nexusmods.get_colour_schemes() == [colour_scheme]
