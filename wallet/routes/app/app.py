import logging
import random
import uuid
from typing import List
from faker import Faker

from wallet.auth import get_user
from wallet.models import AppCategory
from wallet.view.app.app import AppsCategoriesOut
from wallet.view.auth.user import UserOut

fake = Faker()

from fastapi import APIRouter, Query, Depends

from wallet.view.game.games import GameCategoryOut

router = APIRouter()


@router.get("s", response_model=List[AppsCategoriesOut])
async def get_apps(
    search: str | None = Query(default=None),
    categoryId: str | None = Query(default=None),
    # user: UserOut = Depends(get_user),
):
    # logging.info(f"u2: {user}")
    categories_with_apps = (
        await AppCategory.all().order_by("order").prefetch_related("apps", "apps__icon")
    )
    return categories_with_apps
