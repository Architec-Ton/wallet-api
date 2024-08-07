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

TON_CLIENT_API_URL = os.getenv(
    "TON_CLIENT_API_URL", "https://testnet.toncenter.com/api/v2"
)

TON_CLIENT_API_URL_PREFIX = os.getenv("TON_CLIENT_API_URL_PREFIX", "/api/v2")


TON_CLIENT_API_GET_URL = os.getenv(
    "TON_CLIENT_API_GET_URL", "https://ton.architecton.site"
)

ADMIN_AUTH_KEY = os.getenv("ADMIN_AUTH_KEY", "")
