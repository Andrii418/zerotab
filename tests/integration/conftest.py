from collections.abc import Iterator
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_session
from app.main import app


@dataclass(frozen=True)
class SeededGroup:
    group_id: int
    anna_id: int
    ben_id: int
    carl_id: int


@pytest.fixture
def session_factory() -> Iterator[sessionmaker[Session]]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    engine.dispose()


@pytest.fixture
def session(session_factory) -> Iterator[Session]:
    with session_factory() as db_session:
        yield db_session


@pytest.fixture
def client(session_factory) -> Iterator[TestClient]:
    def override_get_session() -> Iterator[Session]:
        with session_factory() as db_session:
            yield db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_group(client) -> SeededGroup:
    person_ids = [
        client.post("/people", json={"name": name}).json()["id"]
        for name in ("Anna", "Ben", "Carl")
    ]
    group_id = client.post(
        "/groups", json={"name": "Trip", "member_ids": person_ids}
    ).json()["id"]
    return SeededGroup(group_id, *person_ids)