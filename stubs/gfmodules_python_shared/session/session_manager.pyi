from gfmodules_python_shared.repository.repository_base import RepositoryBase as RepositoryBase
from gfmodules_python_shared.repository.repository_factory import RepositoryFactory as RepositoryFactory
from gfmodules_python_shared.session.session_factory import DbSessionFactory as DbSessionFactory
from typing import Any, Callable, ParamSpec, TypeVar

T = TypeVar('T')
P = ParamSpec('P')

def get_repository() -> Any: ...
def session_manager(func: Callable[P, T]) -> Callable[P, T]: ...
