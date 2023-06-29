#!/usr/bin/env python
import os
from pathlib import Path

from psycopg.conninfo import make_conninfo
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

DB_HOST = os.getenv("PGHOST", "database")
DB_NAME = os.getenv("PGDATABASE", "pgstac")
DB_PORT = os.getenv("PGPORT", 5432)
DB_USER = os.getenv("PGUSER", "username")
DB_PASS = os.getenv("PGPASSWORD", "password")

STAC_DIR = Path("/app/STAC/")
ADDED_ITEMS_FILE = STAC_DIR / "added_items.txt"


def main():
    conninfo = make_conninfo(
        "postgres://u@h/d",
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        password=DB_PASS,
    )

    print(f"CONNINFO, {conninfo}")

    db = PgstacDB(conninfo)

    print("Updating pgstac role settings")
    loader = Loader(db)

    all_items = [str(path) for path in STAC_DIR.glob("S2*.json")]

    added_items = read_added_items()

    new_items = [i for i in all_items if i not in added_items]

    print("Loading collections...")

    loader.load_collections(
        str(STAC_DIR / 'collection.json'),
        insert_mode=Methods.upsert,
    )

    print("Loading items...")
    print(f"Total items: {len(new_items)}")

    for item_path in new_items:
        print(f"Loading {item_path}")

        loader.load_items(
            str(item_path),
            insert_mode=Methods.upsert,
        )

        add_item_to_added_items(item_path)

    print("Finished loading data.")


def read_added_items():
    if not ADDED_ITEMS_FILE.is_file():
        ADDED_ITEMS_FILE.write_text("")

    with ADDED_ITEMS_FILE.open() as f:
        return f.read().splitlines()


def add_item_to_added_items(item_path):
    with ADDED_ITEMS_FILE.open("a") as f:
        f.write(f"{item_path}\n")


if __name__ == "__main__":
    main()
