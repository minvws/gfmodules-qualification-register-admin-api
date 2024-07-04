from datetime import date

from app.db.entities.application_version import ApplicationVersion
from app.db.entities.application_version_qualification import (
    ProtocolApplicationQualification,
)
from app.db.entities.protocol_version import ProtocolVersion


class ProtocolApplicationQualificationFactory:
    @staticmethod
    def create_instance(
        protocol_version: ProtocolVersion,
        application_version: ApplicationVersion,
        qualification_date: date,
    ) -> ProtocolApplicationQualification:
        """
        Creates a rich instance of ProtocolApplicationQualification with parent ProtocolVersion and child ApplicationVersion
        """
        new_instance = ProtocolApplicationQualification(
            qualification_date=qualification_date
        )
        new_instance.protocol_version = protocol_version
        new_instance.application_version = application_version

        return new_instance
