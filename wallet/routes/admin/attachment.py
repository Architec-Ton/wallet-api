import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, File, Form, Query, UploadFile
from slugify import slugify

from wallet.models import Attachment
from wallet.models.apps import AppCategory
from wallet.routes.admin.handlers.attachment import create_attachment, upload_attachment
from wallet.view.attachment.attachment import AttachmentOut
from wallet.view.category.category import CategoryCreateIn, CategoryDetailOut, CategoryUpdateIn

router = APIRouter()


@router.post("", response_model=AttachmentOut)
async def post_upload_attachment(
    file: UploadFile = File(...),
    title: Optional[str] = Form(default=None),
    description: Optional[str] = Form(default=None),
):
    orig_file = await upload_attachment(file)

    attachment = await create_attachment(file, orig_file, title, description)

    return attachment


@router.delete("/{attachment_id}")
async def delete_attachment(attachment_id: UUID):
    attachment = await Attachment.get(id=attachment_id)
    await attachment.delete()
    return {"status": "deleted", "total": 1}


@router.get("s", response_model=List[AttachmentOut])
async def get_attachments(search=Query(default=None)):
    if search is None:
        return await Attachment.all()
    else:
        return await Attachment.filter(title__icontains=search)
    # return [await AppCategory.all().order_by("order")]
