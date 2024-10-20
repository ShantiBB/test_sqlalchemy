from src.database import (sync_engine, session_factory, async_engine,
                          async_session_factory)
from src.models import WorkersOrm, Base, workers_table


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_workers():
        bobr = WorkersOrm(username='Bobr')
        volk = WorkersOrm(username='Volk')
        with session_factory() as session:
            session.add_all([bobr, volk])
            session.commit()


















def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


async def insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkersOrm(username='Bobr')
        worker_volk = WorkersOrm(username='Volk')
        session.add_all((worker_bobr, worker_volk))
        await session.commit()
