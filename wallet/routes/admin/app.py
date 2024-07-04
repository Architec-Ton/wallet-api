import logging
from typing import List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from wallet.models import AppCategory
from wallet.models.apps import App
from wallet.view.app.app import (
    AppCreateIn,
    AppUpdateIn,
    AppDetailOut,
    AppsByCategoriesOut,
)

from wallet.errors import APIException

from fastapi import APIRouter

from slugify import slugify

router = APIRouter()


@router.post("", response_model=AppDetailOut)
async def post_create_app(app_in: AppCreateIn):

    app_data = jsonable_encoder(
        {
            "url": app_in.url,
            "title_en": app_in.title_en,
            "subtitle_en": app_in.subtitle_en,
            "description_en": app_in.description_en,
            "payload": {"translation": app_in.translation},
            "icon_id": app_in.icon_id,
            "category_id": app_in.category_id,
            "slug": slugify(app_in.title_en),
        }
    )
    app = await App.create(**app_data)
    await app.update_attachments(app_in.attachments_ids)
    await app.fetch_related("icon", "attachments")
    return app


@router.put("/{app_id}", response_model=AppDetailOut)
async def post_update_app_category(app_id: UUID, app_in: AppUpdateIn):
    app = await App.get(id=app_id)
    app_data = app_in.model_dump(exclude_unset=True, exclude_none=True)
    if "translation" in app_data:
        app.payload["translation"] = app_data["translation"]
        del app_data["translation"]

    await app.verify_attachments(app_in.attachments_ids)
    await app.update_from_dict(app_data).save()
    await app.update_attachments(app_in.attachments_ids)
    await app.fetch_related("icon", "attachments")
    return app


@router.delete("/{app_id}")
async def delete_app_category(app_id: UUID):
    app = await App.get(id=app_id)
    await app.delete()
    return {"status": "deleted", "total": 1}


@router.get("s", response_model=List[AppDetailOut])
async def get_apps():
    return await App.all().order_by("order").prefetch_related("icon", "attachments")


@router.get("s/preview", response_model=List[AppsByCategoriesOut])
async def get_apps_by_cat():

    categories_with_apps = (
        await AppCategory.all()
        .order_by("order")
        .prefetch_related("apps", "apps__icon", "apps__attachments")
    )

    return categories_with_apps
