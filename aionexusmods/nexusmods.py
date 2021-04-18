from __future__ import annotations

import platform
from typing import Dict, List, Optional

from aiohttp import ClientSession

from .schemas import *

BASE_URL = "https://api.nexusmods.com/v1"

USER_AGENT = "{}/{} ({}; {}) {}/{}".format(
    __package__,
    "0.1.1",  # importlib.metadata.version(__package__)
    platform.platform(),
    platform.architecture()[0],
    platform.python_implementation(),
    platform.python_version(),
)


class NexusMods:
    """
    Nexus Mods Public API Documentation:
    https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0
    """

    api_key: str
    game_domain_name: str

    def __init__(self, api_key: str, game_domain_name: str):
        self.game_domain_name = game_domain_name
        self.api_key = api_key
        self._session = None

    #
    # Nexus Mods Public Api - Mods
    #

    async def get_updated(self, period: str) -> List[ModUpdate]:
        """
        Returns a list of mods that have been updated in a given period, with timestamps of their last update.
        Cached for 5 minutes.
        The only accepted periods are '1d', '1w' and '1m' (1 day, 1 week and 1 month).
        """
        json = dict(period=period)
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/updated.json", json=json)
        return ModUpdateSchema.load(result, many=True)

    async def get_changelogs(self, mod_id: int) -> Dict[str, List[str]]:
        """
        Returns list of changelogs for mod.
        """
        return await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/changelogs.json")

    async def get_latest_added(self) -> List[Mod]:
        """
        Retrieve 10 latest added mods for a specified game.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/latest_added.json")
        return ModSchema.load(result, many=True)

    async def get_latest_updated(self) -> List[Mod]:
        """
        Retrieve 10 latest updated mods for a specified game.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/latest_updated.json")
        return ModSchema.load(result, many=True)

    async def get_trending(self) -> List[Mod]:
        """
        Retrieve 10 trending mods for a specified game.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/trending.json")
        return ModSchema.load(result, many=True)

    async def get_mod(self, mod_id: int) -> Mod:
        """
        Retrieve specified mod, from a specified game. Cached for 5 minutes.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}.json")
        return ModSchema.load(result)

    async def get_md5_search(self, md5_hash: str) -> List[SearchResult]:
        """
        Looks up a file MD5 file hash.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/md5_search/{md5_hash}.json")
        return SearchResultSchema.load(result, many=True)

    async def set_endorsed(self, mod_id: int, version: str, endorsed: bool) -> Status:
        """Endorse or unendorse a mod."""
        json = dict(version=version)
        if endorsed:
            result = await self._post(
                f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/endorse.json",
                json=json,
            )
        else:
            result = await self._post(
                f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/abstain.json",
                json=json,
            )
        return StatusSchema.load(result)

    #
    # Nexus Mods Public Api - Mod Files
    #

    async def get_files(self, mod_id: int) -> FilesResult:
        """
        Retrieve a list of files for the specified mod.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files.json")
        return FilesResultSchema.load(result)

    async def get_file(self, mod_id: int, file_id: int) -> File:
        """
        View a specified mod file, using a specified game and mod.
        """
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}.json")
        return FileSchema.load(result)

    async def get_download_link(self, mod_id: int, file_id: int) -> List[DownloadLink]:
        """
        Retrieve a generated download link for the specified mod file.
        """
        result = await self._get(
            f"{BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}/download_link.json"
        )
        return DownloadLinkSchema.load(result, many=True)

    #
    # Nexus Mods Public Api - Games
    #

    async def get_games(self) -> List[Game]:
        """Retrieve a list of all games."""
        result = await self._get(f"{BASE_URL}/games.json")
        return GameSchema.load(result, many=True)

    async def get_game(self) -> Game:
        """Retrieve specified game, along with download count, file count and categories."""
        result = await self._get(f"{BASE_URL}/games/{self.game_domain_name}.json")
        return GameSchema.load(result)

    #
    # Nexus Mods Public Api - User
    #

    async def get_user_details(self) -> User:
        """Checks an API key is valid and returns the user's details."""
        result = await self._get(f"{BASE_URL}/users/validate.json")
        return UserSchema.load(result)

    async def get_tracked_mods(self) -> List[TrackedMod]:
        """Fetch all the mods being tracked by the current user."""
        result = await self._get(f"{BASE_URL}/user/tracked_mods.json")
        return TrackedModSchema.load(result, many=True)

    async def set_tracked(self, mod_id: int, tracked: bool) -> Message:
        """Track or untrack a mod."""
        json = dict(mod_id=mod_id, domain_name=self.game_domain_name)
        if tracked:
            result = await self._post(f"{BASE_URL}/user/tracked_mods.json", json=json)
        else:
            result = await self._delete(f"{BASE_URL}/user/tracked_mods.json", json=json)
        return MessageSchema.load(result)

    async def get_endorsements(self) -> List[Endorsement]:
        """Returns a list of all endorsements for the current user."""
        result = await self._get(f"{BASE_URL}/user/endorsements.json")
        return EndorsementSchema.load(result, many=True)

    #
    # Nexus Mods Public Api - Colour Schemes
    #

    async def get_colour_schemes(self) -> List[ColourScheme]:
        """
        Returns list of all colour schemes, including the primary, secondary and 'darker' colours.
        """
        result = await self._get(f"{BASE_URL}/colourschemes.json")
        return ColourSchemeSchema.load(result, many=True)

    #
    # Implementation Details
    #

    _session: Optional[ClientSession]

    def _active_session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("attempted to use a session before it was started")
        if self._session.closed:
            raise RuntimeError("attempted to use a session after it was closed")
        return self._session

    async def __aenter__(self) -> NexusMods:
        if self._session and not self._session.closed:
            raise RuntimeError("attemped to start a new session before closing the previous one")

        self._session = ClientSession(
            headers={
                "apikey": self.api_key,
                "user-agent": USER_AGENT,
                "content-type": "application/json",
            },
            raise_for_status=True,
        )

        return self

    async def __aexit__(self, *args):
        await self._active_session().close()

    async def _get(self, url, **kwargs) -> dict:
        async with self._active_session().get(url, **kwargs) as response:
            return await response.json()

    async def _post(self, url, **kwargs) -> dict:
        async with self._active_session().post(url, **kwargs) as response:
            return await response.json()

    async def _delete(self, url, **kwargs) -> dict:
        async with self._active_session().delete(url, **kwargs) as response:
            return await response.json()
