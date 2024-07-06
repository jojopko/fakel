from typing import List, Optional
from pydantic import BaseModel, field_validator

from fakel.const import APP_SECRET


class DonutModel(BaseModel):
    is_donut: bool


class CommentsModel(BaseModel):
    count: int


class PhotoSizeModel(BaseModel):
    height: int
    type: str
    width: int
    url: str


class PhotoModel(BaseModel):
    album_id: int
    date: int
    id: int
    owner_id: int
    access_key: str
    sizes: List[PhotoSizeModel]
    text: str
    user_id: int
    web_view_token: str
    has_tags: bool


class VideoImageModel(BaseModel):
    url: str
    width: int
    height: int
    with_padding: Optional[int] = None


class VideoModel(BaseModel):
    response_type: str
    access_key: str
    can_comment: int
    can_like: int
    can_repost: int
    can_subscribe: int
    can_add_to_faves: int
    can_add: int
    comments: int
    date: int
    description: str
    duration: int
    image: List[VideoImageModel]
    first_frame: List[VideoImageModel]
    width: int
    height: int
    id: int
    owner_id: int
    title: str
    is_favorite: bool
    track_code: str
    repeat: int
    type: str
    views: int
    local_views: int
    can_dislike: int


class AttachmentModel(BaseModel):
    type: str
    photo: Optional[PhotoModel] = None
    video: Optional[VideoModel] = None
    style: Optional[str] = None


class HeaderPhotoModel(BaseModel):
    source_id: int


class HeaderTitleModel(BaseModel):
    source_id: int


class HeaderModel(BaseModel):
    photo: Optional[HeaderPhotoModel] = None
    title: HeaderTitleModel
    date: int


class AttachmentsMetaModel(BaseModel):
    primary_mode: str


class ObjectModel(BaseModel):
    inner_type: str
    can_edit: int
    created_by: int
    can_delete: int
    donut: Optional[DonutModel] = None
    comments: Optional[CommentsModel] = None
    marked_as_ads: int
    compact_attachments_before_cut: int
    hash: str
    header: Optional[HeaderModel] = None
    attachments: List[AttachmentModel] = []
    attachments_meta: Optional[AttachmentsMetaModel] = None
    date: int
    from_id: int
    id: int
    is_favorite: bool
    owner_id: int
    post_type: str
    text: str


class VKEventModel(BaseModel):
    group_id: int
    event_id: str
    v: str
    type: str
    object: Optional[ObjectModel] = None
    secret: str

    @field_validator('secret')
    def secret_must_match(cls, value):
        if value != APP_SECRET:
            raise ValueError("Поле 'secret' должно быть равно значению перменной окружения 'APP_SECRET'!")
        return value
