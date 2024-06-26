import random
import uuid
from typing import List
from faker import Faker

from wallet.auth import get_user
from wallet.view.auth.user import UserOut
from wallet.view.game.game import GameOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()


mock = {
    "title": fake.company(),
    "description": fake.paragraph(nb_sentences=5),
    "id": uuid.uuid4(),
    "thumb": "https://cdn-icons-png.freepik.com/512/1732/1732452.png",
    "gallery": [
        "https://cdn-icons-png.freepik.com/512/1732/1732452.png",
        "https://cdn-icons-png.freepik.com/512/1732/1732452.png",
    ],
    "resources": [
        {
            "thumb": "/wallet/images/mock/game_icon.png",
            "title": fake.bs(),
            "type": "telegram",
            "description": fake.paragraph(nb_sentences=2),
            "link": "",
        }
    ],
}


@router.get("/{game_id}", response_model=GameOut)
async def get_game(
    game_id: uuid.UUID,
    # user: UserOut = Depends(get_user),
):
    return mock
