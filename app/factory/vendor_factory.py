from app.db.entities.vendor import Vendor


class VendorFactory:

    @staticmethod
    def create_instance(
        kvk_number: str, trade_name: str, statutory_name: str
    ) -> Vendor:
        return Vendor(
            kvk_number=kvk_number, trade_name=trade_name, statutory_name=statutory_name
        )
