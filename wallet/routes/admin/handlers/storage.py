import hashlib
import os
from typing import Tuple
from uuid import uuid4

import aiofiles  # type: ignore[import-untyped]
from aiofiles.os import path  # type: ignore[import-untyped]
from fastapi import UploadFile
from PIL import Image, ImageOps
from starlette.requests import Request


async def copy_upload_file_stream(file_destination: str, request: Request):
    sha256_hash = hashlib.sha256()
    with open(file_destination, "wb") as out_file:
        async for content in request.stream():
            sha256_hash.update(content)
            out_file.write(content)  # async write chunk
    return sha256_hash.hexdigest()


async def copy_uploadfile(file_destination: str, upload_file: UploadFile, chunked: int):
    sha256_hash = hashlib.sha256()
    with open(file_destination, "wb") as out_file:
        while content := await upload_file.read(chunked):  # async read chunk
            sha256_hash.update(content)
            out_file.write(content)  # async write chunk
    return sha256_hash.hexdigest()


async def copy_file(file_destination: str, file_source: str, chunked: int = 1024000):
    async with aiofiles.open(file_destination, "wb") as out_file:
        async with aiofiles.open(file_source, "rb") as in_file:
            while content := await in_file.read(chunked):  # async read chunk
                await out_file.write(content)  # async write chunk


async def get_image_path(
    user, ext: str, content: str, media_type="gallery", hash=None, global_path=False
) -> Tuple[str, str, str, str]:
    user_path = user.path if not global_path else user.global_path

    gallery_path = await user_path([media_type, content])
    gallery_thumb_path = await user_path([media_type, content, "thumb"])
    gallery_orig_path = await user_path([media_type, content, "orig"])
    filename = f"{uuid4()}{ext}" if hash is None else f"{hash}{ext}"
    fullname = os.path.join(gallery_path, filename)
    thumb = os.path.join(gallery_thumb_path, filename)
    return fullname, thumb, filename, gallery_orig_path


def scale_to_height(image, height=1920):
    """Crops an image to a given aspect ratio.
    Args:
        aspect (float): The desired aspect ratio.
        divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
        alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
        aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
    Returns:
        Image: The cropped Image object.
    """
    if image.height > height:
        newheight = height
        newwidth = int(image.width * (height / image.height))
        return image.resize((newwidth, newheight))
    return image


def crop_to_aspect(image, aspect, divisor=1, alignx=0.5, aligny=0.5):
    """Crops an image to a given aspect ratio.
    Args:
        aspect (float): The desired aspect ratio.
        divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
        alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
        aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
    Returns:
        Image: The cropped Image object.
    """
    if image.width / image.height > aspect / divisor:
        newwidth = int(image.height * (aspect / divisor))
        newheight = image.height
    else:
        newwidth = image.width
        newheight = int(image.width / (aspect / divisor))
    return image.crop(
        (
            alignx * (image.width - newwidth),
            aligny * (image.height - newheight),
            alignx * (image.width - newwidth) + newwidth,
            aligny * (image.height - newheight) + newheight,
        )
    )


async def move_media_file(
    upload_file: UploadFile,
    user,
    ext: str,
    content: str,
    media_type="gallery",
    chunked: int = 1024000,
    size=(480, 360),
    global_path=False,
) -> Tuple[str, str, str]:
    orig_ext = ext
    if content != "video":
        ext = ".webp"

    fullname, thumb, filename, file_orig = await get_image_path(
        user, ext, content, media_type=media_type, global_path=global_path
    )

    file_hash = await copy_uploadfile(fullname, upload_file, chunked)
    fullname_hash, thumb_hash, filename_hash, gallery_orig_path = await get_image_path(
        user,
        ext,
        content,
        media_type=media_type,
        hash=file_hash,
        global_path=global_path,
    )
    gallery_orig_full_path = f"{gallery_orig_path}/{file_hash}{orig_ext}"
    if await path.exists(gallery_orig_full_path):
        await aiofiles.os.remove(gallery_orig_full_path)
    await copy_file(gallery_orig_full_path, fullname)
    if not (await path.exists(fullname_hash)):
        await aiofiles.os.rename(fullname, fullname_hash)
    else:
        await aiofiles.os.remove(fullname)
    # TODO: make async image processing
    if content != "video":
        try:
            with Image.open(fullname_hash) as im:
                im = ImageOps.exif_transpose(im)
                im.save(fullname_hash, format=ext[1:], optimize=True, quality=80)
                img = crop_to_aspect(im, size[0], size[1])
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(thumb_hash)
        except OSError as e:
            print("cannot convert", fullname, e)
            await copy_file(thumb_hash, fullname_hash)

    return fullname_hash, thumb_hash, filename_hash
