from enum import Enum


class AttachmentFileType(str, Enum):
    orig = "orig"
    icon = "icon"
    view = "view"
    thumb = "thumb"
    promo = "promo"


class AttachmentContentType(str, Enum):
    image = "image"
    video = "video"
    undefined = "undefined"
