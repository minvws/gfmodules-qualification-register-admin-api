from _typeshed import Incomplete
from gfmodules_python_shared.session.db_session import DbSession as DbSession
from sqlalchemy import Engine as Engine

class DbSessionFactory:
    engine: Incomplete
    def __init__(self, engine: Engine) -> None: ...
    def create(self) -> DbSession: ...
