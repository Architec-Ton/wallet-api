import asyncio
import logging
import random
import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from tortoise.queryset import Q

from wallet.auth import get_user
from wallet.models import App, AppCategory, AppMarketing
from wallet.view.app.app import AppDetailOut, AppsCategoriesOut, AppsFilterIn, AppsOut
from wallet.view.auth.user import UserOut
from wallet.view.game.games import GameCategoryOut

router = APIRouter()


@router.get("s", response_model=AppsOut)
async def get_apps(
    filter_in: AppsFilterIn = Depends(AppsFilterIn),
    user: UserOut = Depends(get_user),
):
    if filter_in.search is None and filter_in.category_id is None:
        logging.info(f"u2: {user}")
        categories_with_apps, marketings = await asyncio.gather(
            AppCategory.filter(active=True).order_by("order").prefetch_related("apps", "apps__icon"),
            AppMarketing.all().order_by("order").prefetch_related("image"),
        )
    else:
        marketings = []
        query = Q()
        if filter_in.category_id is not None:
            query = Q(id=filter_in.category_id, active=True)
        if filter_in.search is not None:
            query = query & Q(apps__title_en__icontains=filter_in.search)
        categories_with_apps = await AppCategory.filter(query).order_by("order").prefetch_related("apps", "apps__icon")
        # r = AppsOut(categories=categories_with_apps, marketings=marketings).model_dump()
        # if filter_in.search is not None:
        #     s = filter_in.search.lower().strip()
        #     for c in r["categories"]:
        #         apps = []
        #         for a in c["apps"]:
        #             if s in a["title"].lower():
        #                 apps.append(a)
        #         c["apps"] = apps
        # await categories_with_apps.fetch_related("apps", "apps__icon")
        # logging.info(categories_with_apps)
        # return r

    return AppsOut(categories=categories_with_apps, marketings=marketings)


@router.get("/{app_id}", response_model=AppDetailOut)
async def get_app(app_id: uuid.UUID, user: UserOut = Depends(get_user)):
    app = await App.get(id=app_id).prefetch_related("icon", "attachments", "resources", "resources__icon")
    return app
