from __future__ import annotations

import platform
from os import PathLike
from typing import AsyncIterator, ClassVar, Optional, Union

from aiohttp import ClientSession, TCPConnector
from aiolimiter import AsyncLimiter
from pydantic import parse_raw_as

import aionexusmods

from .models import *

__all__ = ["NexusMods"]

_JsonDict = dict[str, Union[str, int]]


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

    async def get_mod_updates(self, period: str) -> list[ModUpdate]:
        """
        Returns a list of mods that have been updated in a given period, with timestamps of their last update.
        Cached for 5 minutes.
        The only accepted periods are '1d', '1w' and '1m' (1 day, 1 week and 1 month).
        """
        json: _JsonDict = {"period": period}
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/updated.json", json=json)
        return parse_raw_as(list[ModUpdate], result)

    async def get_mod_changelogs(self, mod_id: int) -> dict[str, list[str]]:
        """
        Returns a list of changelogs for the specified mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/changelogs.json")
        return parse_raw_as(dict[str, list[str]], result)

    async def get_latest_added_mods(self) -> list[Mod]:
        """
        Returns the 10 latest added mods.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/latest_added.json")
        return parse_raw_as(list[Mod], result)

    async def get_latest_updated_mods(self) -> list[Mod]:
        """
        Returns the 10 latest updated mods.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/latest_updated.json")
        return parse_raw_as(list[Mod], result)

    async def get_trending_mods(self) -> list[Mod]:
        """
        Returns 10 trending mods.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/trending.json")
        return parse_raw_as(list[Mod], result)

    async def get_mod(self, mod_id: int) -> Mod:
        """
        Returns a specified mod. Cached for 5 minutes.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}.json")
        return parse_raw_as(Mod, result)

    async def get_md5_search(self, md5_hash: str) -> list[tuple[Mod, File]]:
        """
        Returns a list of mod files for the given MD5 file hash.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/md5_search/{md5_hash}.json")
        parsed = parse_raw_as(list[SearchResult], result)
        return [(p.mod, p.file_details) for p in parsed]

    async def set_endorsed(self, mod_id: int, version: str, endorsed: bool) -> Status:
        """Endorse or unendorse a mod."""
        json: _JsonDict = {"version": version}
        if endorsed:
            result = await self._post(
                f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/endorse.json",
                json=json,
            )
        else:
            result = await self._post(
                f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/abstain.json",
                json=json,
            )
        return parse_raw_as(Status, result)

    #
    # Nexus Mods Public Api - Mod Files
    #

    async def get_files_and_updates(self, mod_id: int) -> tuple[list[File], list[FileUpdate]]:
        """
        Returns a list of files for the specified mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files.json")
        parsed = parse_raw_as(FilesResult, result)
        return parsed.files, parsed.file_updates

    async def get_file(self, mod_id: int, file_id: int) -> File:
        """
        Returns the specified file for the specified mod.
        """
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}.json")
        return parse_raw_as(File, result)

    async def get_download_links(self, mod_id: int, file_id: int) -> list[DownloadLink]:
        """
        Returns a generated download link for the specified mod file.
        """
        result = await self._get(
            f"{self.BASE_URL}/games/{self.game_domain_name}/mods/{mod_id}/files/{file_id}/download_link.json"
        )
        return parse_raw_as(list[DownloadLink], result)

    #
    # Nexus Mods Public Api - Games
    #

    async def get_games(self) -> list[Game]:
        """Returns a list of all games."""
        result = await self._get(f"{self.BASE_URL}/games.json")
        return parse_raw_as(list[Game], result)

    async def get_game(self) -> Game:
        """Returns the specified game."""
        result = await self._get(f"{self.BASE_URL}/games/{self.game_domain_name}.json")
        return parse_raw_as(Game, result)

    #
    # Nexus Mods Public Api - User
    #

    async def get_user(self) -> User:
        """Returns the current user."""
        result = await self._get(f"{self.BASE_URL}/users/validate.json")
        return parse_raw_as(User, result)

    async def get_tracked_mods(self) -> list[TrackedMod]:
        """Returns all the mods being tracked by the current user."""
        result = await self._get(f"{self.BASE_URL}/user/tracked_mods.json")
        return parse_raw_as(list[TrackedMod], result)

    async def set_tracked(self, mod_id: int, tracked: bool) -> Message:
        """Track or untrack a mod."""
        json: _JsonDict = {"domain_name": self.game_domain_name, "mod_id": mod_id}
        if tracked:
            result = await self._post(f"{self.BASE_URL}/user/tracked_mods.json", json=json)
        else:
            result = await self._delete(f"{self.BASE_URL}/user/tracked_mods.json", json=json)
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
        """
        Returns the results from the specified content preview link.
        """
        result = await self._get(content_preview_link)
        return parse_raw_as(ContentPreview, result)

    async def download(self, download_link: str, path: Union[str, PathLike[str]]) -> None:
        """
        Downloads the contents from the specified download link to the specified path.
        """
        from os.path import dirname
        from aiofiles.os import mkdir
        from aiofiles import open

        try:
            await mkdir(dirname(path))
        except (FileExistsError, FileNotFoundError):
            pass
        async with open(path, "wb") as f:
            async for chunk in self._get_iter_chunks(download_link):
                await f.write(chunk)

    #
    # Implementation Details
    #
    _api_key: str
    _session: Optional[ClientSession]
    _limiter: ClassVar[AsyncLimiter] = AsyncLimiter(3600 / 28)  # limit to 28 per sec

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
            connector=TCPConnector(limit_per_host=28),
        )
        return self

    async def __aexit__(self, *args):  # type: ignore[no-untyped-def]
        await self._active_session().close()

    async def _get(self, url: str, json: Optional[_JsonDict] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().get(url, json=json) as response:
                return await response.read()

    async def _post(self, url: str, json: Optional[_JsonDict] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().post(url, json=json) as response:
                return await response.read()

    async def _delete(self, url: str, json: Optional[_JsonDict] = None) -> bytes:
        async with self._limiter:
            async with self._active_session().delete(url, json=json) as response:
                return await response.read()

    async def _get_iter_chunks(self, url: str) -> AsyncIterator[bytes]:
        async with self._limiter:
            async with self._active_session().get(url) as response:
                while True:
                    chunk = await response.content.read(1024 * 1024 * 12)  # 12 MB
                    if chunk:
                        yield chunk
                    else:
                        break
