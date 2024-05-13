from typing import List

from fastapi import APIRouter, Depends

from app.schemas.application.mapper import map_application_entity_to_dto
from app.schemas.application.schema import ApplicationDTO
from app.schemas.vendor.mapper import map_vendor_entity_to_dto
from app.schemas.vendor.schema import VendorDTO, VendorCreate, VendorApplicationCreate
from app.services.vendors_service import VendorService
from app.services.vendor_application_service import VendorApplicationService
from app.container import (
    get_vendors_service,
    get_vendor_application_service,
)

router = APIRouter(prefix="/administration/vendors", tags=["Vendors"])


@router.get("", response_model=List[VendorDTO])
def get_all_vendors(
    vendor_service: VendorService = Depends(get_vendors_service),
) -> list[VendorDTO]:
    result = vendor_service.get_all_vendors()
    return [map_vendor_entity_to_dto(vendor) for vendor in result]


@router.get("/{kvk_number}", response_model=VendorDTO)
def get_one_vendor(
    kvk_number: str, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    result = vendor_service.get_one_vendor(kvk_number)
    return map_vendor_entity_to_dto(result)


@router.post("/", response_model=None)
def add_one_vendor(
    data: VendorCreate, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    results = vendor_service.add_one_vendor(
        kvk_number=data.kvk_number,
        trade_name=data.trade_name,
        statutory_name=data.statutory_name,
    )
    return map_vendor_entity_to_dto(results)


@router.delete("/{kvk_number}", response_model=None)
def delete_one_vendor(
    kvk_number: str, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:

    result = vendor_service.delete_one_vendor(kvk_number)
    return map_vendor_entity_to_dto(result)


@router.get("/{kvk_number}/applications")
def get_all_vendor_applications(
    kvk_number: str,
    vendor_application_service: VendorApplicationService = Depends(
        get_vendor_application_service
    ),
) -> list[ApplicationDTO]:
    results = vendor_application_service.get_all_vendor_applications(kvk_number)
    return [map_application_entity_to_dto(result) for result in results]


@router.get("/{kvk_number}/applications/{application_name}")
def get_one_vendor_application(
    kvk_number: str,
    application_name: str,
    service: VendorApplicationService = Depends(get_vendor_application_service),
) -> ApplicationDTO:
    results = service.get_one_vendor_application(
        kvk_number=kvk_number, application_name=application_name
    )
    return map_application_entity_to_dto(results)


@router.post("/{kvk_number}/application")
def register_one_vendor_application(
    kvk_number: str,
    data: VendorApplicationCreate,
    service: VendorApplicationService = Depends(get_vendor_application_service),
) -> VendorDTO:
    result = service.register_one_application(
        kvk_number=kvk_number,
        application_name=data.name,
        application_version=data.version,
    )
    return map_vendor_entity_to_dto(result)


@router.delete("/{kvk_number}/applications/{application_name}")
def deregister_one_vendor_application(
    kvk_number: str,
    application_name: str,
    service: VendorApplicationService = Depends(get_vendor_application_service),
) -> VendorDTO:
    results = service.deregister_one_vendor_application(
        kvk_number=kvk_number, application_name=application_name
    )
    return map_vendor_entity_to_dto(results)
