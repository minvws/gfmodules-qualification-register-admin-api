from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams
from app.schemas.vendor.mapper import map_vendor_entity_to_dto
from app.schemas.vendor.schema import VendorDTO, VendorCreateDTO
from app.db.services.vendors_service import VendorService
from app.container import (
    get_vendors_service,
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("")
def get_vendors(
    query: Annotated[PaginationQueryParams, Depends()],
    vendor_service: VendorService = Depends(get_vendors_service),
) -> Page[VendorDTO]:
    return vendor_service.get_paginated(limit=query.limit, offset=query.offset)


@router.post("", response_model=None)
def add_one_vendor(
    data: VendorCreateDTO, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    results = vendor_service.add_one(
        kvk_number=data.kvk_number,
        trade_name=data.trade_name,
        statutory_name=data.statutory_name,
    )
    return map_vendor_entity_to_dto(results)


@router.get("/{vendor_id}", response_model=VendorDTO)
def get_vendor_by_id(
    vendor_id: UUID, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    vendor = vendor_service.get_one(vendor_id=vendor_id)
    return map_vendor_entity_to_dto(vendor)


@router.delete("/{vendor_id}")
def delete_vendor_by_id(
    vendor_id: UUID, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    deleted_vendor = vendor_service.remove_one(vendor_id=vendor_id)
    return map_vendor_entity_to_dto(deleted_vendor)


@router.get("/kvk_number/{kvk_number}", response_model=VendorDTO)
def get_one_vendor_by_kvk_number(
    kvk_number: str, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDTO:
    result = vendor_service.get_one_by_kvk_number(kvk_number)
    return map_vendor_entity_to_dto(result)
