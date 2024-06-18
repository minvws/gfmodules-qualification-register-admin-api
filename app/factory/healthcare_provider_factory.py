from app.db.entities.healthcare_provider import HealthcareProvider


class HealthcareProviderFactory:
    @staticmethod
    def create_instance(
        ura_code: str, agb_code: str, trade_name: str, statutory_name: str
    ) -> HealthcareProvider:
        return HealthcareProvider(
            ura_code=ura_code,
            agb_code=agb_code,
            trade_name=trade_name,
            statutory_name=statutory_name,
        )
