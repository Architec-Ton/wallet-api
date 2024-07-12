import asyncio
import logging
import random
import uuid
from typing import List
from faker import Faker

from wallet.auth import get_user
from wallet.models import AppCategory, App, AppMarketing
from wallet.view.app.app import AppsCategoriesOut, AppDetailOut, AppsOut
from wallet.view.auth.user import UserOut

fake = Faker()

from fastapi import APIRouter, Query, Depends

from wallet.view.game.games import GameCategoryOut

router = APIRouter()


@router.get("s", response_model=AppsOut)
async def get_apps(
    search: str | None = Query(default=None),
    categoryId: str | None = Query(default=None),
    # user: UserOut = Depends(get_user),
):
    if categoryId is None and search is None:
        # logging.info(f"u2: {user}")
        categories_with_apps, marketings = await asyncio.gather(
            AppCategory.all().order_by("order").prefetch_related("apps", "apps__icon"),
            AppMarketing.all().order_by("order").prefetch_related("image"),
        )
    else:
        marketings = []
        categories_with_apps = (
            await AppCategory.filter(id=categoryId)
            .order_by("order")
            .prefetch_related("apps", "apps__icon")
        )
        logging.info(categories_with_apps)

    return AppsOut(categories=categories_with_apps, marketings=marketings)


@router.get("/{app_id}", response_model=AppDetailOut)
async def get_app(app_id: uuid.UUID):
    app = await App.get(id=app_id).prefetch_related(
        "icon", "attachments", "resources", "resources__icon"
    )
    return app
