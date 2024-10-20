from sqlalchemy import select, func, cast, Integer, and_, insert
from sqlalchemy.orm import aliased, joinedload, selectinload

from src.database import (sync_engine, session_factory,
                          async_session_factory)
from src.models import WorkersOrm, Base, ResumesOrm, Workload


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            bobr = WorkersOrm(username='Bobr')
            volk = WorkersOrm(username='Volk')
            session.add_all([bobr, volk])
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.all()
            print(f'{workers=}')

    @staticmethod
    def update_workers(
        worker_id: int = 1,
        new_username: str = 'Misha'
    ):
        with session_factory() as session:
            worker = session.get(WorkersOrm, worker_id)
            worker.username = new_username
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000,
                workload=Workload.fulltime, worker_id=1)
            resume_jack_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000,
                workload=Workload.fulltime, worker_id=1)
            resume_michael_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000,
                workload=Workload.parttime, worker_id=2)
            resume_michael_2 = ResumesOrm(
                title="Data Scientist", compensation=300000,
                workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2,
                             resume_michael_1, resume_michael_2])
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_languages: str = 'Python'):
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer)
                    .label('avg_compensation')
                )
                .select_from(ResumesOrm)
                .filter(
                    and_(
                        ResumesOrm.title.contains(like_languages),
                        ResumesOrm.compensation > 40000,
                    )
                )
                .group_by(ResumesOrm.workload)
                .having(
                    cast(func.avg(ResumesOrm.compensation), Integer)
                    > 70000
                )
            )
            print(query.compile(compile_kwargs={'literal_binds': True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},  # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000,
                 "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer",
                 "compensation": 70000, "workload": "parttime",
                 "worker_id": 3},
                {"title": "Python Data Scientist",
                 "compensation": 80000, "workload": "parttime",
                 "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000,
                 "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer",
                 "compensation": 100000, "workload": "fulltime",
                 "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func():
        with session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)
                    .over(partition_by=r.workload)
                    .cast(Integer).label('avg_workload_compensation'),
                )
                .join(r, r.worker_id == w.id).subquery('helper1')
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation
                     - subq.c.avg_workload_compensation)
                    .label('compensation_diff')
                )
                .cte('helper2')
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            res = session.execute(query)
            result = res.all()
            cnt = 1
            for item in result:
                print(cnt, item)
                cnt += 1

    @staticmethod
    def select_workers_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
            )

            res = session.execute(query)
            result = res.scalars().all()
            worker_1 = result[0].resumes
            print(worker_1)
            worker_2 = result[1].resumes
            print(worker_2)

    @staticmethod
    def select_workers_joined_relationship():
        sync_engine.echo = True
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            worker_1 = result[0].resumes
            print(worker_1)
            worker_2 = result[1].resumes
            print(worker_2)

    @staticmethod
    def select_workers_selectin_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            worker_1 = result[0].resumes
            print(worker_1)
            worker_2 = result[1].resumes
            print(worker_2)
















def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


async def insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkersOrm(username='Bobr')
        worker_volk = WorkersOrm(username='Volk')
        session.add_all((worker_bobr, worker_volk))
        await session.commit()
