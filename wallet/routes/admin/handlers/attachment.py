import logging
import os

import aiofiles  # type: ignore[import-untyped]
from aiofiles.os import path  # type: ignore[import-untyped]
from fastapi import UploadFile

# from PIL import Image, ImageOps
from wallet.errors import APIException
from wallet.models.attachment import Attachment

# from .storage import copy_upload_file_stream
from .storage import copy_uploadfile

# try:
#     from preview_generator.manager import PreviewManager
#
#     preview_generator = True
# except ModuleNotFoundError:
#     preview_generator = False
#     logging.warning("No preview generator")

STRETCH_THUMB_SIZE = (615, 500)

STORAGE_URL = os.getenv("STORAGE_URL", "/storage")
STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")


async def upload_attachment(file: UploadFile):
    if file is None:
        return None
    try:
        upload_file_path = f"{STORAGE_PATH}/orig/{file.filename}"
        upload_file_extention = os.path.splitext(file.filename)[1].lower()
        file_hash = await copy_uploadfile(upload_file_path, file, 1024 * 1024 * 2)
        upload_file_path_hash = f"{STORAGE_PATH}/orig/{file_hash}{upload_file_extention}"
        if upload_file_path_hash != upload_file_path:
            if await path.exists(upload_file_path_hash):
                await aiofiles.os.remove(upload_file_path_hash)
            await aiofiles.os.rename(upload_file_path, upload_file_path_hash)
        return upload_file_path_hash.lower()
    except Exception as error:
        logging.exception(error)
        raise APIException("storage_upload_error", 400) from error


async def create_attachment(
    file: UploadFile,
    upload_file_path_hash: str,
    title=None,
    description=None,
) -> Attachment:
    filename = os.path.basename(upload_file_path_hash)
    attachment = await Attachment.get_or_none(filename=filename)
    if attachment is None:
        attachment = await Attachment.create(
            title=title,
            description=description,
            origin_filename=file.filename,
            content_type=file.content_type,
            filename=filename,
            filesize=os.stat(upload_file_path_hash).st_size,
            file_type="orig",
            status="uploaded",
        )
    else:
        attachment.title = title
        attachment.description = description
        await attachment.save()
    return attachment


# async def update_pdf_content(attachment: Attachment):
#     content = get_content_type(attachment.content_type)
#     if content == AttachmentContentType.pdf:
#         main_path = attachment.filepath(AttachmentFileType.main, is_exist=False)
#         try:
#             orig_path = attachment.filepath(AttachmentFileType.orig)
#             attachment.preview_ext = ".jpeg"
#             thumb_path = attachment.filepath(AttachmentFileType.thumb, is_exist=False)
#
#             attachment.status = FileStatus.processing
#             await copy_file(main_path, orig_path)
#             if preview_generator:
#                 if orig_path is None:
#                     raise APIException(ErrorCode.storage_upload_error)
#                 manager = PreviewManager(os.path.dirname(thumb_path))
#                 path_to_preview_image = manager.get_jpeg_preview(orig_path)
#                 attachment.preview_ext = os.path.splitext(path_to_preview_image)[1]
#                 await aiofiles.os.rename(path_to_preview_image, thumb_path)
#                 await attachment.save(update_fields=["preview_ext"])
#             attachment.status = (
#                 FileStatus.approved if STRETCH_AUTO_APPROVE else FileStatus.review
#             )
#             await attachment.save(update_fields=["status"])
#             return attachment
#         except Exception as e:
#             logging.error(e)
#             await attachment.remove()
#
#
# async def update_image_content(attachment: Attachment):
#     content = get_content_type(attachment.content_type)
#     size = STRETCH_THUMB_SIZE
#     if content == AttachmentContentType.image:
#         orig_path = attachment.filepath(AttachmentFileType.orig)
#         thumb_path = attachment.filepath(AttachmentFileType.thumb, is_exist=False)
#         main_path = attachment.filepath(AttachmentFileType.main, is_exist=False)
#         attachment.status = FileStatus.processing
#         try:
#             with Image.open(orig_path) as im:
#                 im = ImageOps.exif_transpose(im)
#                 ext = os.path.splitext(main_path)[1]
#                 im = scale_to_height(im)
#                 im.save(main_path, format=ext[1:], optimize=True, quality=80)
#                 attachment.filename = os.path.basename(main_path)
#                 img = crop_to_aspect(im, size[0], size[1])
#                 img.thumbnail(size, Image.Resampling.LANCZOS)
#                 img.save(thumb_path)
#                 attachment.preview_ext = os.path.splitext(thumb_path)[1]
#             attachment.status = (
#                 FileStatus.approved if STRETCH_AUTO_APPROVE else FileStatus.review
#             )
#             await attachment.save()
#             return attachment
#         except OSError as e:
#             logging.error("cannot convert", orig_path, e)
#             await attachment.remove()
#
#
# async def update_video_content(attachment: Attachment):
#     if attachment.content == AttachmentContentType.video:
#         try:
#             attachment.duration = get_video_duration(
#                 attachment.filepath(AttachmentFileType.orig)
#             )
#             if attachment.duration > 180:
#                 attachment.duration = 180
#             await attachment.save(update_fields=["duration"])
#             if attachment.status == FileStatus.uploaded:
#                 attachment.status = FileStatus.processing
#                 await attachment.save(update_fields=["status"])
#                 asyncio.ensure_future(create_attachment_view_video(attachment))
#             return attachment
#         except Exception as e:
#             logging.error(e)
#             await attachment.remove()
#
#
# async def update_content(attachment: Attachment):
#     if attachment.content == AttachmentContentType.image:
#         return await update_image_content(attachment)
#     elif attachment.content == AttachmentContentType.pdf:
#         return await update_pdf_content(attachment)
#     elif attachment.content == AttachmentContentType.video:
#         return await update_video_content(attachment)
#     return attachment
