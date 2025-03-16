from typing import Generic, Literal, NotRequired, Optional, TypeVar, TypedDict, Union

ApiVersions = Literal[1, 2]


class SimpleLink(TypedDict):
    uri: str


class SrcLink(SimpleLink):
    rel: str


LinksList = list[SrcLink]


class NameData(TypedDict):
    international: str
    japanese: Optional[str]


class CategoryPlayersRule(TypedDict):
    value: int
    type: Literal["exactly", "up-to"]


class CategoryData(TypedDict):
    id: str
    name: str
    rules: str
    weblink: str
    miscellaneous: bool
    type: Literal["per-game", "per-level"]
    players: CategoryPlayersRule
    links: LinksList
    game: NotRequired["GameResponse"]
    variables: NotRequired["VariablesResponse"]


class GuestData(TypedDict):
    name: str
    links: LinksList


class LevelData(TypedDict):
    id: str
    name: str
    weblink: str
    rules: str
    links: LinksList
    categories: NotRequired["CategoriesResponse"]
    variables: NotRequired["VariablesResponse"]


class GameInfo(TypedDict):
    id: str
    name: str
    links: LinksList


GametypesData = GameInfo
GenresData = GameInfo
EnginesData = GameInfo
DevelopersData = GameInfo
PublishersData = GameInfo
RegionsData = GameInfo
PlatformsData = GameInfo


class GameNames(NameData):
    twitch: Optional[str]


TimeOptions = Literal["realtime", "realtime_noloads", "ingame"]

GameRuleset = TypedDict(
    "GameRuleset",
    {
        "show-milliseconds": bool,
        "require-verification": bool,
        "require-video": bool,
        "emulators-allowed": bool,
        "default-time": TimeOptions,
        "run-times": list[TimeOptions],
    },
)

ModeratorOptions = Literal["moderator", "super-moderator", "verifier"]


class ImageData(SimpleLink):
    width: int
    height: int


GameAssets = TypedDict(
    "GameAssets",
    {
        "logo": Optional[ImageData],
        "icon": Optional[ImageData],
        "trophy-1st": Optional[ImageData],
        "trophy-2nd": Optional[ImageData],
        "trophy-3rd": Optional[ImageData],
        "trophy-4th": Optional[ImageData],
        "background": Optional[ImageData],
        "foreground": Optional[ImageData],
        "cover-tiny": Optional[ImageData],
        "cover-small": Optional[ImageData],
        "cover-large": Optional[ImageData],
        "cover-medium": Optional[ImageData],
    },
)

GameData = TypedDict(
    "GameData",
    {
        "id": str,
        "weblink": str,
        "abbreviation": str,
        "release-date": str,
        "regions": Union[list[str], "RegionsResponse"],
        "platforms": Union[list[str], "PlatformsResponse"],
        "genres": Union[list[GenresData], "GenresResponse"],
        "engines": Union[list[EnginesData], "EnginesResponse"],
        "gametypes": Union[list[GametypesData], "GametypesResponse"],
        "developers": Union[list[DevelopersData], "DevelopersResponse"],
        "publishers": Union[list[PublishersData], "PublishersResponse"],
        "moderators": Union[dict[str, ModeratorOptions], "UsersResponse"],
        "names": GameNames,
        "links": LinksList,
        "assets": GameAssets,
        "ruleset": GameRuleset,
        "romhack": Optional[bool],
        "created": Optional[str],
        "released": Optional[int],
        "levels": NotRequired["LevelsResponse"],
        "categories": NotRequired["CategoriesResponse"],
        "variables": NotRequired["VariablesResponse"],
    },
)


class GameBulkData(TypedDict):
    id: str
    weblink: str
    abbreviation: str
    names: NameData


class VariablesScope(TypedDict):
    type: Literal["global", "full-game", "all-levels", "single-level"]


class VariablesValuesValuesFlags(TypedDict):
    miscellaneous: bool


class VariablesValuesValue(TypedDict):
    label: str
    rules: Optional[str]
    flags: Optional[VariablesValuesValuesFlags]


VariablesValuesValues = dict[str, VariablesValuesValue]


class VariablesValues(TypedDict):
    values: VariablesValuesValues
    default: str


VariablesData = TypedDict(
    "VariablesData",
    {
        "id": str,
        "name": str,
        "mandatory": bool,
        "obsoletes": bool,
        "user-defined": bool,
        "is-subcategory": bool,
        "scope": VariablesScope,
        "values": VariablesValues,
        "links": LinksList,
        "category": Optional[str],
    },
)


class RunVideos(TypedDict):
    links: list[SimpleLink]
    text: Optional[str]


class RunStatusNew(TypedDict):
    status: Literal["new"]


RunStatusVerified = TypedDict(
    "RunStatusVerified",
    {
        "examiner": str,
        "status": Literal["verified"],
        "verify-date": Optional[str],
    },
)

RunStatusRejected = TypedDict(
    "RunStatusRejected",
    {
        "reason": str,
        "examiner": str,
        "status": Literal["rejected"],
        "verify-date": Optional[str],
    },
)

RunStatus = Union[RunStatusNew, RunStatusVerified, RunStatusRejected]


class RunPlayersRegistered(SimpleLink):
    id: str
    rel: Literal["user"]


class RunPlayersGuests(SimpleLink):
    name: str
    rel: Literal["guest"]


RunPlayers = Union[RunPlayersRegistered, RunPlayersGuests]


class RunTimes(TypedDict):
    primary: str
    primary_t: float
    realtime: Optional[str]
    realtime_t: Optional[float]
    realtime_noloads: Optional[str]
    realtime_noloads_t: Optional[float]
    ingame: Optional[str]
    ingame_t: Optional[float]


class RunSystem(TypedDict):
    emulated: bool
    platform: Union[str, "PlatformResponse"]
    region: Optional[Union[str, "RegionResponse"]]


class RunData(TypedDict):
    id: str
    game: Union[str, "GameResponse"]
    weblink: str
    comment: str
    category: Union[str, "CategoryResponse"]
    status: RunStatus
    players: Union[list[RunPlayers], "UsersResponse"]
    values: dict[str, str]
    links: LinksList
    times: RunTimes
    system: RunSystem
    date: Optional[str]
    level: Optional[Union[str, "LevelResponse"]]
    submitted: Optional[str]
    videos: Optional[RunVideos]
    splits: Optional[SrcLink]


class LeaderboardRuns(TypedDict):
    place: int
    run: RunData


LeaderboardData = TypedDict(
    "LeaderboardData",
    {
        "game": Union[str, "GameResponse"],
        "weblink": str,
        "category": Union[str, "CategoryResponse"],
        "video-only": bool,
        "runs": list[LeaderboardRuns],
        "values": dict[str, str],
        "links": LinksList,
        "timing": TimeOptions,
        "level": Optional[Union[str, "LevelResponse"]],
        "region": Optional[Union[str, "RegionsResponse"]],
        "platform": Optional[Union[str, "PlatformsResponse"]],
        "emulators": Optional[bool],
        "players": NotRequired["UsersResponse"],
        "variables": NotRequired["VariablesResponse"],
    },
)


class Notification(TypedDict):
    id: str
    text: str
    created: str
    status: Literal["read", "unread"]
    item: SrcLink
    links: LinksList


class ColorData(TypedDict):
    light: str
    dark: str


class NameStyleSolid(TypedDict):
    style: Literal["solid"]
    color: ColorData


NameStyleGradient = TypedDict(
    "NameStyleGradient",
    {
        "style": Literal["gradient"],
        "color-from": ColorData,
        "color-to": ColorData,
    },
)

NameStyle = Union[NameStyleSolid, NameStyleGradient]


class UserLocationData(TypedDict):
    code: str
    names: NameData


class UserLocation(TypedDict):
    country: UserLocationData
    region: Optional[UserLocationData]


UserRoleOptions = Literal[
    "banned", "user", "trusted", "moderator", "admin", "programmer"
]

UserData = TypedDict(
    "UserData",
    {
        "id": str,
        "weblink": str,
        "role": UserRoleOptions,
        "names": NameData,
        "links": LinksList,
        "name-style": NameStyle,
        "signup": Optional[str],
        "twitch": Optional[SimpleLink],
        "hitbox": Optional[SimpleLink],
        "youtube": Optional[SimpleLink],
        "twitter": Optional[SimpleLink],
        "location": Optional[UserLocation],
        "speedrunslive": Optional[SimpleLink],
    },
)


class PersonalBestData(TypedDict):
    place: int
    run: RunData
    game: NotRequired["GameResponse"]
    category: NotRequired["CategoryResponse"]
    level: NotRequired["LevelResponse"]
    players: NotRequired["UserResponse"]
    region: NotRequired["RegionResponse"]
    platform: NotRequired["PlatformResponse"]


ModeratorSeriesOptions = Literal["moderator", "super-moderator"]


class SeriesData(TypedDict):
    id: str
    weblink: str
    abbreviation: str
    created: Optional[str]
    names: NameData
    links: LinksList
    assets: GameAssets
    moderators: Union[dict[str, ModeratorSeriesOptions], "UsersResponse"]


T = TypeVar("T")


class BaseResponse(TypedDict, Generic[T]):
    data: T


CategoryResponse = BaseResponse[CategoryData]
GuestResponse = BaseResponse[GuestData]
LevelResponse = BaseResponse[LevelData]
GametypeResponse = BaseResponse[GametypesData]
GenreResponse = BaseResponse[GenresData]
EngineResponse = BaseResponse[EnginesData]
DeveloperResponse = BaseResponse[DevelopersData]
PublisherResponse = BaseResponse[PublishersData]
RegionResponse = BaseResponse[RegionsData]
PlatformResponse = BaseResponse[PlatformsData]
GameResponse = BaseResponse[GameData]
VariableResponse = BaseResponse[VariablesData]
RunResponse = BaseResponse[RunData]
LeaderboardResponse = BaseResponse[LeaderboardData]
UserResponse = BaseResponse[UserData]
SerieResponse = BaseResponse[SeriesData]


class ListResponse(TypedDict, Generic[T]):
    data: list[T]


CategoriesResponse = ListResponse[CategoryData]
LevelsResponse = ListResponse[LevelData]
GametypesResponse = ListResponse[GametypesData]
GenresResponse = ListResponse[GenresData]
EnginesResponse = ListResponse[EnginesData]
DevelopersResponse = ListResponse[DevelopersData]
PublishersResponse = ListResponse[PublishersData]
RegionsResponse = ListResponse[RegionsData]
PlatformsResponse = ListResponse[PlatformsData]
GamesResponse = ListResponse[GameData]
VariablesResponse = ListResponse[VariablesData]
RunsResponse = ListResponse[RunData]
LeaderboardsResponse = ListResponse[LeaderboardData]
UsersResponse = ListResponse[UserData]
PersonalBestResponse = ListResponse[PersonalBestData]
SeriesResponse = ListResponse[SeriesData]


class NextLink(SimpleLink):
    rel: Literal["next"]


class PrevLink(SimpleLink):
    rel: Literal["prev"]


LinkPagination = Union[NextLink, PrevLink]


class PaginationData(TypedDict):
    offset: int
    max: int
    size: int
    links: list[LinkPagination]


class PaginatedResponse(TypedDict, Generic[T]):
    data: T
    pagination: PaginationData


CategoriesResponsePaginated = PaginatedResponse[CategoriesResponse]
LevelsResponsePaginated = PaginatedResponse[LevelsResponse]
PlatformsResponsePaginated = PaginatedResponse[PlatformsResponse]
GamesResponsePaginated = PaginatedResponse[GamesResponse]
RunsResponsePaginated = PaginatedResponse[RunsResponse]
UsersResponsePaginated = PaginatedResponse[UsersResponse]


class GamesBulkResponse(TypedDict):
    data: list[GameBulkData]
    pagination: PaginationData
