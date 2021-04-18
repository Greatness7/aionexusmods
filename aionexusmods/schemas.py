__all__ = [
    "Category",
    "CategorySchema",
    "ColourScheme",
    "ColourSchemeSchema",
    "DownloadLink",
    "DownloadLinkSchema",
    "Endorsement",
    "EndorsementSchema",
    "EndorsementRef",
    "EndorsementRefSchema",
    "File",
    "FileSchema",
    "FilesResult",
    "FilesResultSchema",
    "FileUpdate",
    "FileUpdateSchema",
    "Game",
    "GameSchema",
    "Message",
    "MessageSchema",
    "Mod",
    "ModSchema",
    "ModUpdate",
    "ModUpdateSchema",
    "ModUser",
    "ModUserSchema",
    "SearchResult",
    "SearchResultSchema",
    "Status",
    "StatusSchema",
    "TrackedMod",
    "TrackedModSchema",
    "User",
    "UserSchema",
]

from typing import List, Optional, Tuple, Union, ClassVar, Type

from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow_dataclass import dataclass


class Base:
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        ordered = True


@dataclass
class User(Base):
    user_id: int
    key: str
    name: str
    email: str
    profile_url: str
    is_premium: bool
    is_supporter: bool

    # The Nexus Mods API duplicates these field with a '?' suffix.
    # We have to rebind because '?' is not allowed in field names.
    _is_supporter: bool
    _is_premium: bool

    class Meta:
        include = {
            "_is_premium": Boolean(data_key="is_premium?"),
            "_is_supporter": Boolean(data_key="is_supporter?"),
        }


@dataclass
class Category(Base):
    category_id: int
    name: str
    parent_category: Union[bool, int]


@dataclass
class Game(Base):
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
    categories: List[Category]


@dataclass
class Endorsement(Base):
    mod_id: int
    domain_name: str
    date: int
    version: str
    status: str


@dataclass
class EndorsementRef(Base):
    endorse_status: str
    timestamp: Optional[str]
    version: Optional[str]


@dataclass
class ModUser(Base):
    member_id: int
    member_group_id: int
    name: str


@dataclass
class Mod(Base):
    name: str
    summary: str
    description: str
    picture_url: str
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
    user: ModUser
    endorsement: Optional[EndorsementRef]


@dataclass
class ModUpdate(Base):
    mod_id: int
    latest_file_update: int
    latest_mod_activity: int


@dataclass
class File(Base):
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
    mod_version: str
    external_virus_scan_url: str
    description: str
    size_kb: int
    changelog_html: Optional[str]
    content_preview_link: str
    md5: Optional[str]


@dataclass
class SearchResult(Base):  # TODO Tuple
    mod: Mod
    file_details: File


@dataclass
class FileUpdate(Base):
    old_file_id: int
    new_file_id: int
    old_file_name: str
    new_file_name: str
    uploaded_timestamp: int
    uploaded_time: str


@dataclass
class FilesResult(Base):  # TODO Tuple
    files: List[File]
    file_updates: List[FileUpdate]


@dataclass
class DownloadLink(Base):
    name: str
    short_name: str
    URI: str


@dataclass
class ColourScheme(Base):
    id: int
    name: str
    primary_colour: str
    secondary_colour: str
    darker_colour: str


@dataclass
class TrackedMod(Base):
    mod_id: int
    domain_name: str


@dataclass
class Message(Base):
    message: str


@dataclass
class Status(Base):
    message: str
    status: str


CategorySchema: Schema = Category.Schema()
ColourSchemeSchema: Schema = ColourScheme.Schema()
DownloadLinkSchema: Schema = DownloadLink.Schema()
EndorsementSchema: Schema = Endorsement.Schema()
EndorsementRefSchema: Schema = EndorsementRef.Schema()
FileSchema: Schema = File.Schema()
FilesResultSchema: Schema = FilesResult.Schema()
FileUpdateSchema: Schema = FileUpdate.Schema()
GameSchema: Schema = Game.Schema()
MessageSchema: Schema = Message.Schema()
ModSchema: Schema = Mod.Schema()
ModUpdateSchema: Schema = ModUpdate.Schema()
ModUserSchema: Schema = ModUser.Schema()
SearchResultSchema: Schema = SearchResult.Schema()
StatusSchema: Schema = Status.Schema()
TrackedModSchema: Schema = TrackedMod.Schema()
UserSchema: Schema = User.Schema()
