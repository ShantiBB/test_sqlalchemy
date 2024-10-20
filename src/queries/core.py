from sqlalchemy import URL, create_engine, text, select, insert, update

from src.database import sync_engine, async_engine, \
    async_session_factory

from src.models import metadata_obj, workers_table, WorkersOrm


class SyncCore:
    @staticmethod
    def create_tables():
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {'username': 'Jack'},
                    {'username': 'Michael'}
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all()
            print(f'{workers=}')

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = 'Misha'):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username "
            #             "WHERE id=:id")
            stmt = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)

    @staticmethod
    async def insert_workers():
        async with async_engine.connect() as conn:
            bobr = WorkersOrm(username='Bobr')
            volk = WorkersOrm(username='Volk')
            conn.execute(bobr)
            await conn.commit()
