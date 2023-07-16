from fastapi import APIRouter, Depends, HTTPException

from src.api.models import Tariff
from src.calculation_tariff.pydentic_models import CalcRequest, get_calc
from src.logger import logger

router = APIRouter()


@router.get("/", tags=["calculate"])
async def calculate_tariff(calc_request: CalcRequest = Depends(get_calc)):

    # Проверяем существование тарифа
    tariff = await Tariff.filter(date_tariff=calc_request.date_tariff, cargo_type=calc_request.cargo_type).first()
    if not tariff:
        logger.error("Tariff not found")
        raise HTTPException(status_code=404, detail="Tariff not found")

    # Расчет стоимости страхования
    insurance_cost = calc_request.price * tariff.rate
    logger.info(
        f"Calculate insurance {insurance_cost} for {calc_request.price} on {tariff.rate} with {tariff.date_tariff}"
    )

    return {"insurance_cost": insurance_cost}
