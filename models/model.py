from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, TIMESTAMP, Float

metadata = MetaData()

stat = Table(
    "stats",
    metadata,
    Column("id", Integer, nullable=False),
    Column("x", Float, nullable=False),
    Column("y", Float, nullable=False),
    Column("z", Float, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
)
