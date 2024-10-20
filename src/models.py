import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import (Table, Column, Integer, String, ForeignKey,
                        text, MetaData)

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, \
    relationship

metadata_obj = MetaData()

str_256 = Annotated[str, 256]
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
]
updated_at = Annotated[
    datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )
]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class WorkersOrm(Base):
    __tablename__ = 'workers'
    id: Mapped[intpk]
    username: Mapped[str]
    resumes: Mapped[list['ResumesOrm']] = relationship()


class Workload(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'


class ResumesOrm(Base):
    __tablename__ = 'resumes'
    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(
        ForeignKey('workers.id', ondelete='CASCADE')
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    worker: Mapped['WorkersOrm'] = relationship()

    repr_cols_num = 4
    repr_cols = ('created_at',)



workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
