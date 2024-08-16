from typing import List
from uuid import UUID

from fastapi import APIRouter

from wallet.models.apps import AppMarketing
from wallet.view.app.marketing import AppMarketingCreateIn, AppMarketingOut

router = APIRouter()


@router.post("", response_model=AppMarketingOut)
async def post_create_marketing(marketing_in: AppMarketingCreateIn):

    marketing_data = {
        "title": marketing_in.title,
        "url": marketing_in.url,
        "image_id": marketing_in.image_id,
    }
    marketing = await AppMarketing.create(**marketing_data)
    await marketing.fetch_related("image")
    return marketing


@router.delete("/{marketing_id}")
async def delete_marketing(marketing_id: UUID):
    marketing = await AppMarketing.get(id=marketing_id)
    await marketing.delete()
    return {"status": "deleted", "total": 1}


@router.get("s", response_model=List[AppMarketingOut])
async def get_app_categories():
    return await AppMarketing.all().order_by("order").prefetch_related("image")
