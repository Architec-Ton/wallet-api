import logging
import random
import uuid
from typing import List

from faker import Faker

from wallet.auth import get_user
from wallet.view.auth.user import UserOut

fake = Faker()

from fastapi import APIRouter, Depends, Query

from wallet.view.game.games import GameCategoryOut

router = APIRouter()


mock = [
    {
        "title": fake.company(),
        "id": uuid.uuid4(),
        "items": [
            {
                "title": fake.catch_phrase(),
                "id": uuid.uuid4(),
                "description": fake.paragraph(nb_sentences=5),
                "thumb": "https://cdn-icons-png.freepik.com/512/1732/1732452.png",
            }
            for _ in range(random.randint(3, 16))
        ],
    }
    for _ in range(8)
]


@router.get("s", response_model=List[GameCategoryOut])
async def get_games(
    search: str | None = Query(default=None),
    categoryId: str | None = Query(default=None),
    user: UserOut = Depends(get_user),
):
    # logging.info(f"u2: {user}")
    return mock
