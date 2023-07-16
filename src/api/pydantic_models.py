from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import Header, HTTPException
from pydantic import BaseModel

from src.config import SECRET
from src.logger import logger


class TariffCreate(BaseModel):
    date_tariff: date
    cargo_type: str
    rate: Decimal


class TariffPatch(BaseModel):
    date_tariff: Optional[date] = None
    cargo_type: Optional[str] = None
    rate: Optional[Decimal] = None


class TariffResponse(BaseModel):
    id: int
    date_tariff: date
    cargo_type: str
    rate: Decimal


class Token(BaseModel):
    token: str


def get_tariff_create(
        token: str = Header(..., alias='Api-Admin_Token'),
        date_tariff: date = Header(..., alias='Api-Date-Tariff.YYYY-MM-DD'),
        cargo_type: str = Header(..., alias='Api-Cargo-Type'),
        rate: Decimal = Header(..., alias='Api-Rate')
):
    validate_token(token)
    return TariffCreate(
        date_tariff=date_tariff,
        cargo_type=cargo_type,
        rate=rate
    )


def get_tariff_patch(
        token: str = Header(..., alias='Api-Admin_Token'),
        date_tariff: Optional[date] = Header(None, alias='Api-Date-Tariff.YYYY-MM-DD'),
        cargo_type: Optional[str] = Header(None, alias='Api-Cargo-Type'),
        rate: Optional[Decimal] = Header(None, alias='Api-Rate')
):
    validate_token(token)
    return TariffPatch(
        date_tariff=date_tariff,
        cargo_type=cargo_type,
        rate=rate
    )


def get_token(
    token: str = Header(..., alias='Api-Admin_Token')
):
    validate_token(token)


def validate_token(token):
    if SECRET != token:
        logger.error("Wrong token")
        raise HTTPException(status_code=401, detail='Wrong token')
