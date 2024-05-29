import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import DatabaseError
from app.db.decorator import repository
from app.db.entities.vendor import Vendor
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(Vendor)
class VendorsRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> Vendor | None:
        try:
            db_vendor = self.session.scalars(
                select(Vendor)
                .options(
                    selectinload(Vendor.applications),
                )
                .filter_by(**kwargs)
            ).first()
            return db_vendor
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_all(self) -> Sequence[Vendor]:
        db_vendors = self.session.scalars(select(Vendor)).all()
        return db_vendors

    def create(self, new_vendor: Vendor) -> None:
        try:
            self.session.add(new_vendor)
            self.session.commit()
            self.session.refresh(new_vendor)

        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()

    def update(self, vendor: Vendor) -> None:
        try:
            self.session.commit()
            self.session.refresh(vendor)
        except DatabaseError as e:
            logger.error(e)

    def delete(self, vendor: Vendor) -> None:
        try:
            self.session.delete(vendor)
            self.session.commit()
        except DatabaseError as e:
            logger.error(e)
