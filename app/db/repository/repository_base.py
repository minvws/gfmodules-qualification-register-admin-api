from typing import TypeVar, Union, Dict, Generic, Sequence, List
from uuid import UUID

from sqlalchemy import select, or_

from app.db.db_session import DbSession
from app.db.repository.exception import EntryNotFound
from app.helpers.validators import validate_sets_equal

T = TypeVar("T")

TArgs = TypeVar("TArgs", bound=Union[str, UUID, Dict[str, str]])


class RepositoryBase(Generic[T]):
    model = T  # type: ignore

    def __init__(self, session: DbSession) -> None:
        self.session = session

    def create(self, entity: T) -> None:
        return self.session.create(entity)

    def update(self, entity: T) -> None:
        return self.session.update(entity)

    def delete(self, entity: T) -> None:
        return self.session.delete(entity)

    def get(self, **kwargs: TArgs) -> T | None:
        stmt = select(self.model).filter_by(**kwargs)
        return self.session.scalars_first(stmt)

    def get_or_fail(self, **kwargs: TArgs) -> T:
        result = self.get(**kwargs)
        if result is None:
            raise EntryNotFound(self.model)

        return result

    def get_all(self, **kwargs: TArgs) -> Sequence[T]:
        stmt = select(self.model).filter_by(**kwargs)
        return self.session.scalars_all(stmt)

    def get_by_property(self, attribute: str, values: List[str]) -> Sequence[T]:
        """
        Generates a chained OR condition based on the provided attribute values:
        eg: SELECT * FROM users WHERE users.email = :email_1 OR users.email = :email_2
        """
        if attribute not in self.model.__table__.columns.keys():
            raise AttributeError(
                f"{attribute} is not a column in the {self.model.__name__}"
            )

        conditions = [getattr(self.model, attribute).__eq__(value) for value in values]
        stmt = select(self.model).where(or_(*conditions))

        return self.session.scalars_all(stmt)

    def get_by_property_exact(self, attribute: str, values: List[str]) -> Sequence[T]:
        results = self.get_by_property(attribute, values)
        result_values = [getattr(result, attribute) for result in results]
        valid_results = validate_sets_equal(result_values, values)

        if not valid_results:
            raise EntryNotFound(self.model)

        return results


TRepositoryBase = TypeVar("TRepositoryBase", bound=RepositoryBase, covariant=True)  # type: ignore
