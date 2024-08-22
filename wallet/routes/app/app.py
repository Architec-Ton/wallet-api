import asyncio
import logging
import uuid

from fastapi import APIRouter, Depends
from tortoise.queryset import Q

from wallet.auth import get_user
from wallet.models import App, AppCategory, AppMarketing
from wallet.view.app.app import AppDetailOut, AppsFilterIn, AppsOut
from wallet.view.auth.user import UserOut

router = APIRouter()


@router.get("s", response_model=AppsOut)
async def get_apps(
    filter_in: AppsFilterIn = Depends(AppsFilterIn),
    user: UserOut = Depends(get_user),
):
    query = Q(active=True)
    if filter_in.category_id is not None:
        query = Q(category_id=filter_in.category_id, active=True)
    if filter_in.search is not None:
        query = query & Q(title_en__icontains=filter_in.search)

    logging.info(f"u2: {user}")
    categories_obj, marketings, apps = await asyncio.gather(
        AppCategory.filter(active=True).order_by("order"),
        AppMarketing.all().order_by("order").prefetch_related("image"),
        App.filter(query).order_by("-is_partner", "order").prefetch_related("icon"),
    )
    categories_dict = {c.id: {"title": c.title, "id": c.id, "apps": []} for c in categories_obj}

    for a in apps:
        categories_dict[a.category_id]["apps"].append(a)

    categories_with_apps = categories_dict.values()

    return AppsOut(categories=categories_with_apps, marketings=marketings)


@router.get("/{app_id}", response_model=AppDetailOut)
async def get_app(app_id: uuid.UUID, user: UserOut = Depends(get_user)):
    app = await App.get(id=app_id).prefetch_related("icon", "attachments", "resources", "resources__icon")
    return app
