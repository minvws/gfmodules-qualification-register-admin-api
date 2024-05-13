import logging
from typing import Sequence, Dict, Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import NoResultFound, DatabaseError
from app.db.decorator import repository
from app.db.entities.models import Vendor, Application
from app.db.repository.repository_base import RepositoryBase

logger = logging.getLogger(__name__)


@repository(Vendor)
class VendorsRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: str | Dict[str, Any]) -> Vendor | None:
        try:
            db_vendor = self.session.scalars(
                select(Vendor)
                .options(
                    selectinload(Vendor.applications).selectinload(
                        Application.versions
                    ),
                    selectinload(Vendor.applications).selectinload(Application.roles),
                )
                .filter_by(**kwargs)
            ).first()
            return db_vendor
        except NoResultFound as e:
            logger.error(e)
            return None

    def find_all(self) -> Sequence[Vendor]:
        db_vendors = self.session.scalars(select(Vendor)).all()
        return db_vendors

    def create(self, new_vendor: Vendor) -> Vendor:
        self.session.add(new_vendor)
        self.session.commit()
        self.session.refresh(new_vendor)

        return new_vendor

    def update(self, vendor: Vendor) -> None:
        try:
            self.session.commit()
            self.session.refresh(vendor)
        except DatabaseError as e:
            logger.error(e)

    def delete(self, vendor: Vendor) -> None:
        self.session.delete(vendor)
        self.session.commit()
