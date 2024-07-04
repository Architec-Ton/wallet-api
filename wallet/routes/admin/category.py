import logging
from typing import List
from uuid import UUID

from wallet.view.category.category import (
    CategoryCreateIn,
    CategoryDetailOut,
    CategoryUpdateIn,
)

from fastapi import APIRouter
from wallet.models.apps import AppCategory

from slugify import slugify

router = APIRouter()


@router.post("y", response_model=CategoryDetailOut)
async def post_create_app_category(category_in: CategoryCreateIn):

    category_data = {
        "title_en": category_in.title_en,
        "payload": {"translation": category_in.translation},
        "slug": slugify(category_in.title_en),
    }
    return await AppCategory.create(**category_data)


@router.put("y/{category_id}", response_model=CategoryDetailOut)
async def post_update_app_category(category_id: UUID, category_in: CategoryUpdateIn):
    category = await AppCategory.get(id=category_id)
    category_data = category_in.model_dump(exclude_unset=True, exclude_none=True)
    if "translation" in category_data:
        category.payload["translation"] = category_data["translation"]
        del category_data["translation"]
    await category.update_from_dict(category_data).save()
    return category


@router.delete("y/{category_id}")
async def delete_app_category(category_id: UUID):
    category = await AppCategory.get(id=category_id)
    await category.delete()
    return {"status": "deleted", "total": 1}


@router.get("ies", response_model=List[CategoryDetailOut])
async def get_app_categories():
    return await AppCategory.all().order_by("order")
