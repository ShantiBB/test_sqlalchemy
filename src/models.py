import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import Table, Column, Integer, String, ForeignKey, text, \
    MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

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
    pass


class WorkersOrm(Base):
    __tablename__ = 'workers'
    id: Mapped[intpk]
    username: Mapped[str]


class WorkLoad(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'


class ResumesOrm(Base):
    __tablename__ = 'resumes'
    id: Mapped[intpk]
    tittle: Mapped[str_256]
    compensation: Mapped[Optional[str]]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(
        ForeignKey('workers.id', ondelete='CASCADE')
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)