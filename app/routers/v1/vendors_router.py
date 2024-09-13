from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.openapi.responses import api_validation_error_response, api_conflict_response, api_not_found_response
from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams
from app.schemas.vendor.mapper import map_vendor_entity_to_dto
from app.schemas.vendor.schema import VendorDto, VendorCreateDto
from app.db.services.vendors_service import VendorService
from app.container import (
    get_vendors_service,
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("", responses={**api_validation_error_response()})
def get_vendors(
    query: Annotated[PaginationQueryParams, Depends()],
    vendor_service: VendorService = Depends(get_vendors_service),
) -> Page[VendorDto]:
    return vendor_service.get_paginated(limit=query.limit, offset=query.offset)


@router.post("", response_model=VendorDto, status_code=status.HTTP_201_CREATED, responses={**api_validation_error_response(), **api_not_found_response(), **api_conflict_response()})
def add_one_vendor(
    data: VendorCreateDto, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDto:
    results = vendor_service.add_one(
        kvk_number=data.kvk_number,
        trade_name=data.trade_name,
        statutory_name=data.statutory_name,
    )
    return map_vendor_entity_to_dto(results)


@router.get("/{vendor_id}", response_model=VendorDto, responses={**api_validation_error_response(), **api_not_found_response()})
def get_vendor_by_id(
    vendor_id: UUID, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDto:
    vendor = vendor_service.get_one(vendor_id=vendor_id)
    return map_vendor_entity_to_dto(vendor)


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT, responses={**api_validation_error_response(), **api_not_found_response()})
def delete_vendor_by_id(
    vendor_id: UUID, vendor_service: VendorService = Depends(get_vendors_service)
) -> None:
    vendor_service.remove_one(vendor_id=vendor_id)


@router.get("/kvk_number/{kvk_number}", response_model=VendorDto, responses={**api_validation_error_response(), **api_not_found_response()})
def get_one_vendor_by_kvk_number(
    kvk_number: str, vendor_service: VendorService = Depends(get_vendors_service)
) -> VendorDto:
    result = vendor_service.get_one_by_kvk_number(kvk_number)
    return map_vendor_entity_to_dto(result)
