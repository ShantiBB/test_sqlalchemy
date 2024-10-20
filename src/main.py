import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.orm import insert_data, SyncORM
from src.queries.core import SyncCore


def main():
    SyncCore.create_tables()

    SyncCore.insert_workers()

    # SyncORM.select_workers()


if __name__ == '__main__':
    main()
