from __future__ import annotations

import platform
from typing import ClassVar, Optional

from aiohttp import ClientSession
from aiolimiter import AsyncLimiter
from pydantic import parse_raw_as

import aionexusmods

from .models import *

__all__ = ["NexusMods"]


class NexusMods:
    """
    Nexus Mods Public API Documentation:
    https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0
    """

    BASE_URL: ClassVar[str] = "https://api.nexusmods.com/v1"

    USER_AGENT: ClassVar[str] = "{}/{} ({}; {}) {}/{}".format(
        aionexusmods.__name__,
        aionexusmods.__version__,
        platform.platform(),
        platform.architecture()[0],
        platform.python_implementation(),
        platform.python_version(),
    )

    game_domain_name: str

    def __init__(self, api_key: str, game_domain_name: str):
        self.game_domain_name = game_domain_name
        self._api_key = api_key
        self._session = None

    #
    # Nexus Mods Public Api - Mods
    #

    async def get_updated_mods(self, period: str) -> list[ModUpdate]:
        """
        Returns a list of mods that have been updated in a given period, with timestamps of their last update.
        Cached for 5 minutes.
        The only accepted periods are '1d', '1w' and '1m' (1 day, 1 week and 1 month).
        """
        data = f'{{"period"={period}}}'
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/updated.json", data=data)
        return parse_raw_as(list[ModUpdate], result)

    async def get_mod_changelogs(self, mod_id: int) -> dict[str, list[str]]:
        """
        Returns list of changelogs for mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/changelogs.json")
        return parse_raw_as(dict[str, list[str]], result)

    async def get_latest_added_mods(self) -> list[Mod]:
        """
        Retrieve 10 latest added mods for a specified game.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/latest_added.json")
        return parse_raw_as(list[Mod], result)

    async def get_latest_updated_mods(self) -> list[Mod]:
        """
        Retrieve 10 latest updated mods for a specified game.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/latest_updated.json")
        return parse_raw_as(list[Mod], result)

    async def get_trending_mods(self) -> list[Mod]:
        """
        Retrieve 10 trending mods for a specified game.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/trending.json")
        return parse_raw_as(list[Mod], result)

    async def get_mod(self, mod_id: int) -> Mod:
        """
        Retrieve specified mod, from a specified game. Cached for 5 minutes.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}.json")
        return parse_raw_as(Mod, result)

    async def get_md5_search(self, md5_hash: str) -> list[tuple[Mod, File]]:
        """
        Looks up a file MD5 file hash.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/md5_search/{md5_hash}.json")
        parsed = parse_raw_as(list[SearchResult], result)
        return [(p.mod, p.file_details) for p in parsed]

    async def set_endorsed(self, mod_id: int, version: str, endorsed: bool) -> Status:
        """Endorse or unendorse a mod."""
        data = f'{{"version"="{version}"}}'
        if endorsed:
            result = await self._post(
                f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/endorse.json",
                data=data,
            )
        else:
            result = await self._post(
                f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/abstain.json",
                data=data,
            )
        return parse_raw_as(Status, result)

    #
    # Nexus Mods Public Api - Mod Files
    #

    async def get_files_and_updates(self, mod_id: int) -> tuple[list[File], list[FileUpdate]]:
        """
        Retrieve a list of files for the specified mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files.json")
        parsed = parse_raw_as(FilesResult, result)
        return parsed.files, parsed.file_updates

    async def get_file(self, mod_id: int, file_id: int) -> File:
        """
        View a specified mod file, using a specified game and mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}.json")
        return parse_raw_as(File, result)

    async def get_download_links(self, mod_id: int, file_id: int) -> list[DownloadLink]:
        """
        Retrieve a generated download link for the specified mod file.
        """
        result = await self._get(
            f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}/download_link.json"
        )
        return parse_raw_as(list[DownloadLink], result)

    #
    # Nexus Mods Public Api - Games
    #

    async def get_games(self) -> list[Game]:
        """Retrieve a list of all games."""
        result = await self._get(f"{self.BASE_URL}/games.json")
        return parse_raw_as(list[Game], result)

    async def get_game(self) -> Game:
        """Retrieve specified game, along with download count, file count and categories."""
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}.json")
        return parse_raw_as(Game, result)

    #
    # Nexus Mods Public Api - User
    #

    async def get_user(self) -> User:
        """Checks an API key is valid and returns the user's details."""
        result = await self._get(f"{self.BASE_URL}/users/validate.json")
        return parse_raw_as(User, result)

    async def get_tracked_mods(self) -> list[TrackedMod]:
        """Fetch all the mods being tracked by the current user."""
        result = await self._get(f"{self.BASE_URL}/user/tracked_mods.json")
        return parse_raw_as(list[TrackedMod], result)

    async def set_tracked(self, mod_id: int, tracked: bool) -> Message:
        """Track or untrack a mod."""
        data = f'{{"mod_id":{mod_id},"domain_name":"{self.game_domain_name}"}}'
        if tracked:
            result = await self._post(f"{self.BASE_URL}/user/tracked_mods.json", data=data)
        else:
            result = await self._delete(f"{self.BASE_URL}/user/tracked_mods.json", data=data)
        return parse_raw_as(Message, result)

    async def get_endorsements(self) -> list[Endorsement]:
        """Returns a list of all endorsements for the current user."""
        result = await self._get(f"{self.BASE_URL}/user/endorsements.json")
        return parse_raw_as(list[Endorsement], result)

    #
    # Nexus Mods Public Api - Colour Schemes
    #

    async def get_colour_schemes(self) -> list[ColourScheme]:
        """
        Returns list of all colour schemes, including the primary, secondary and 'darker' colours.
        """
        result = await self._get(f"{self.BASE_URL}/colourschemes.json")
        return parse_raw_as(list[ColourScheme], result)

    #
    # Nexus Mods Public Api - Extras
    #

    async def get_content_preview(self, content_preview_link: str) -> ContentPreview:
        result = await self._get(content_preview_link)
        return parse_raw_as(ContentPreview, result)

    async def download(self, download_link: str) -> bytes:
        return await self._get(download_link)

    #
    # Implementation Details
    #
    _api_key: str
    _session: Optional[ClientSession]
    _limiter: ClassVar[AsyncLimiter] = AsyncLimiter(100, 28)

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
                "apikey": self._api_key,
                "user-agent": self.USER_AGENT,
                "content-type": "application/json",
            },
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, *args):  # type: ignore[no-untyped-def]
        await self._active_session().close()

    async def _get(self, url: str, data: Optional[str] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().get(url, data=data) as response:
                return await response.read()

    async def _post(self, url: str, data: Optional[str] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().post(url, data=data) as response:
                return await response.read()

    async def _delete(self, url: str, data: Optional[str] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().delete(url, data=data) as response:
                return await response.read()
