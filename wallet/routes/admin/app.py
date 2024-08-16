from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from slugify import slugify

from wallet.models import AppCategory, AppResource
from wallet.models.apps import App
from wallet.view.app.app import AppCreateIn, AppDetailOut, AppsByCategoriesOut, AppUpdateIn
from wallet.view.app.resource import AppResourceCreateIn, AppResourceOut, AppResourceUpdateIn

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
    await app.fetch_related("icon", "attachments", "resources", "resources_icon")
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
    await app.fetch_related("icon", "attachments", "resources", "resources_icon")
    return app


@router.delete("/{app_id}")
async def delete_app_category(app_id: UUID):
    app = await App.get(id=app_id)
    await app.delete()
    return {"status": "deleted", "total": 1}


@router.get("s", response_model=List[AppDetailOut])
async def get_apps():
    return (
        await App.all()
        .order_by("order")
        .prefetch_related(
            "icon",
            "attachments",
            "resources",
            "resources__icon",
        )
    )


@router.get("s/preview", response_model=List[AppsByCategoriesOut])
async def get_apps_by_cat():

    categories_with_apps = (
        await AppCategory.all()
        .order_by("order")
        .prefetch_related(
            "apps",
            "apps__icon",
            "apps__attachments",
            "apps__resources",
            "apps__resources__icon",
        )
    )

    return categories_with_apps


@router.get("/{app_id}/resources", response_model=List[AppResourceOut])
async def get_app_resources(app_id: UUID):
    return await AppResource.filter(app_id=app_id).prefetch_related("icon")


@router.post("/{app_id}/resource", response_model=AppResourceOut)
async def post_create_resource(app_id: UUID, app_resource_in: AppResourceCreateIn):
    app = await App.get(id=app_id)
    app_data = jsonable_encoder(
        {
            "url": app_resource_in.url,
            "title_en": app_resource_in.title_en,
            "app_id": app.id,
            "payload": {"translation": app_resource_in.translation},
            "icon_id": app_resource_in.icon_id,
            "type": app_resource_in.type,
        }
    )
    app_resource = await AppResource.create(**app_data)
    await app_resource.fetch_related("icon")
    return app_resource


@router.put("/{app_id}/resource/{resource_id}", response_model=AppResourceOut)
async def put_update_resource(app_id: UUID, resource_id: UUID, app_resource_in: AppResourceUpdateIn):
    app_resource = await AppResource.get(app_id=app_id, id=resource_id)
    app_data = app_resource_in.model_dump(exclude_unset=True, exclude_none=True)
    if "translation" in app_data:
        app_resource.payload["translation"] = app_data["translation"]
        del app_data["translation"]
    await app_resource.update_from_dict(app_data).save()
    await app_resource.fetch_related("icon")
    return app_resource


@router.delete("/{app_id}/resource/{resource_id}")
async def delete_app_resource(app_id: UUID, resource_id: UUID):
    app = await AppResource.get(app_id=app_id, id=resource_id)
    await app.delete()
    return {"status": "deleted", "total": 1}
