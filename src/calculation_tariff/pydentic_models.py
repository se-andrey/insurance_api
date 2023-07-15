from datetime import date
from decimal import Decimal

from fastapi import Header
from pydantic import BaseModel


class CalcRequest(BaseModel):
    date_tariff: date
    cargo_type: str
    price: Decimal


def get_calc(
        date_tariff: date = Header(..., alias='Api-Date-Tariff.YYYY-MM-DD'),
        cargo_type: str = Header(..., alias='Api-Cargo-Type'),
        price: Decimal = Header(..., alias='Api-Price')
):
    return CalcRequest(
        date_tariff=date_tariff,
        cargo_type=cargo_type,
        price=price
    )
