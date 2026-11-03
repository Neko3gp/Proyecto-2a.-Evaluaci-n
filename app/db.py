"""Conexión a MongoDB para la aplicación de consultas BDAutos."""

from __future__ import annotations

import os

from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGODB_DB", "bdautos")


def get_client(uri: str | None = None) -> MongoClient:
    return MongoClient(uri or DEFAULT_URI, serverSelectionTimeoutMS=5000)


def get_db(uri: str | None = None) -> Database:
    client = get_client(uri)
    client.admin.command("ping")
    return client[DB_NAME]
