from __future__ import annotations

from typing import Iterator, Optional, Tuple, Union

from pydantic import BaseModel

__all__ = [
    "Category",
    "ColourScheme",
    "ContentPreview",
    "DownloadLink",
    "Endorsement",
    "EndorsementRef",
    "File",
    "FilesResult",
    "FileUpdate",
    "Game",
    "Message",
    "Mod",
    "ModUpdate",
    "ModUser",
    "SearchResult",
    "Status",
    "TrackedMod",
    "User",
]


class Category(BaseModel):
    category_id: int
    name: str
    parent_category: Union[bool, int]


class ColourScheme(BaseModel):
    id: int
    name: str
    primary_colour: str
    secondary_colour: str
    darker_colour: str


class DownloadLink(BaseModel):
    name: str
    short_name: str
    URI: str


class Endorsement(BaseModel):
    mod_id: int
    domain_name: str
    date: int
    version: str
    status: str


class EndorsementRef(BaseModel):
    endorse_status: str
    timestamp: Optional[str]
    version: Optional[str]


class File(BaseModel):
    id: Tuple[int, int]
    uid: int
    file_id: int
    name: str
    version: str
    category_id: int
    category_name: Optional[str]
    is_primary: bool
    size: int
    file_name: str
    uploaded_timestamp: int
    uploaded_time: str
    mod_version: Optional[str]
    external_virus_scan_url: Optional[str]
    description: str
    size_kb: int
    changelog_html: Optional[str]
    content_preview_link: str
    md5: Optional[str]


class FileUpdate(BaseModel):
    old_file_id: int
    new_file_id: int
    old_file_name: str
    new_file_name: str
    uploaded_timestamp: int
    uploaded_time: str


class FilesResult(BaseModel):
    files: list[File]
    file_updates: list[FileUpdate]


class Game(BaseModel):
    id: int
    name: str
    forum_url: str
    nexusmods_url: str
    genre: str
    file_count: int
    downloads: int
    domain_name: str
    approved_date: Optional[int]
    file_views: int
    authors: int
    file_endorsements: int
    mods: int
    categories: list[Category]


class Message(BaseModel):
    message: str


class ModUser(BaseModel):
    member_id: int
    member_group_id: int
    name: str


class Mod(BaseModel):
    name: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    picture_url: Optional[str]
    uid: int
    mod_id: int
    game_id: int
    allow_rating: bool
    domain_name: str
    category_id: int
    version: str
    endorsement_count: int
    created_timestamp: int
    created_time: str
    updated_timestamp: int
    updated_time: str
    author: str
    uploaded_by: str
    uploaded_users_profile_url: str
    contains_adult_content: bool
    status: str
    available: bool
    user: Optional[ModUser]
    endorsement: Optional[EndorsementRef]


class ModUpdate(BaseModel):
    mod_id: int
    latest_file_update: int
    latest_mod_activity: int


class SearchResult(BaseModel):
    mod: Mod
    file_details: File


class Status(BaseModel):
    message: str
    status: str


class TrackedMod(BaseModel):
    mod_id: int
    domain_name: str


class User(BaseModel):
    user_id: int
    key: str
    name: str
    email: str
    profile_url: str
    is_premium: bool
    is_supporter: bool


class ContentPreview(BaseModel):
    path: Optional[str]
    name: Optional[str]
    type: Optional[str]
    children: Optional[list[ContentPreview]]
    size: Optional[str]

    def children_recursive(self) -> Iterator[ContentPreview]:
        for child in self.children or ():
            yield child
            yield from child.children_recursive()


ContentPreview.update_forward_refs()
