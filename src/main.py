import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.orm import insert_data, SyncORM
from src.queries.core import SyncCore


def main():
    # SyncCore.create_tables()
    #
    # SyncCore.insert_workers()
    #
    # SyncCore.update_workers()
    #
    # SyncCore.select_workers()

    SyncORM.create_tables()

    SyncORM.insert_workers()

    SyncORM.insert_resumes()

    SyncORM.select_workers_selectin_relationship()

    # SyncORM.update_workers()


if __name__ == '__main__':
    main()
