import os

db_user = os.getenv("POSTGRES_USER", "wallet")
db_pass = os.getenv("POSTGRES_PASSWORD", "wallet")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_name = os.getenv("POSTGRES_DB", "wallet")
db_url = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

TORTOISE_ORM = {
    "connections": {
        "default": db_url,
    },
    "apps": {
        "models": {
            "models": ["wallet.models"],  # "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}

TON_CLIENT_API_URL = os.getenv("TON_CLIENT_API_URL", "https://testnet.toncenter.com/api/v2")

TON_CLIENT_API_URL_PREFIX = os.getenv("TON_CLIENT_API_URL_PREFIX", "/api/v2")

TON_CLIENT_NETWORK = os.getenv("TON_CLIENT_NETWORK", "mainnet")


TON_CLIENT_API_GET_URL = os.getenv("TON_CLIENT_API_GET_URL", "https://ton.architecton.site")
TON_CLIENT_API_KEY = os.getenv(
    "TON_CLIENT_API_KEY",
    "88d5912ad2394e5cbae97a351bb6a3e1174e09f7956d096beaae3acab91324da",
)

ADMIN_AUTH_KEY = os.getenv("ADMIN_AUTH_KEY", "")

MASTER_WALLET_BANK = os.getenv("MASTER_WALLET_BANK", "EQAj1qW6WZTd7sd33Uk48O3TqxNPMjYrgwRHAcBM8RcQCQAD")
