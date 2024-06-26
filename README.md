# Wallet API

Welcome to the repository for our backend API project, built with FastAPI. This API is designed to serve as the backbone for our wallet application, handling tasks such as user authentication, data management, and server-side logic.

---

### Installation

Clone this repository to set up the project locally, then proceed to the next instructions:

```bash
docker build . -t <container_name>
docker run <container_name>
```

---

### Project Structure

```bash
	    └── wallet/
        ├── auth/      # contains logic related to user authentication and authorization
        ├── models/    # describes data structures and interaction with the database
        ├── routes/    # routes, defines URLs and associated handlers
        ├── view/      # the definitions and annotations of entities' fields
        ├── app.py     # contains the creation and configuration of the application instance
        ├── errors.py  # manages custom exceptions and error handling
        └── main.py    # entry point to the application

```

---

### Project Resources

[Russian Telegram channel](https://t.me/architecton_tech)

[English Telegram channel](https://t.me/architecton_eu)

[Chat for dicsussions](https://t.me/architec_ton)
