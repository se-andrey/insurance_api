import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.logger import logger

from .models import Tariff
from .pydantic_models import (TariffCreate, TariffPatch, TariffResponse, Token,
                              get_tariff_create, get_tariff_patch, get_token)

router = APIRouter()


@router.get("/tariff", tags=["tariff"])
async def get_tariff(token: Token = Depends(get_token)):
    tariffs = await Tariff.all()
    logger.info("Send all tariffs")
    return tariffs


@router.post("/tariff", tags=["tariff"])
async def create_tariff(tariff: TariffCreate = Depends(get_tariff_create)):
    tariff_check = await Tariff.filter(date_tariff=tariff.date_tariff, cargo_type=tariff.cargo_type).first()
    if tariff_check:
        logger.error("Try to add already exists tariff")
        raise HTTPException(status_code=409, detail="Tariff already exists")
    tariff_orm = await Tariff.create(
        date_tariff=tariff.date_tariff,
        cargo_type=tariff.cargo_type,
        rate=tariff.rate
    )
    tariff_dict = {
        "id": tariff_orm.id,
        "date_tariff": tariff_orm.date_tariff,
        "cargo_type": tariff_orm.cargo_type,
        "rate": tariff_orm.rate
    }
    logger.info("Add new tariff from json request")
    return TariffResponse(**tariff_dict)


@router.post("/tariff/upload", tags=["tariff"])
async def upload_tariffs(file: UploadFile = File(...), token: Token = Depends(get_token)):
    try:
        content = await file.read()
        tariffs_data = json.loads(content)
        for tariff_data in tariffs_data:
            tariff_check = await Tariff.filter(
                date_tariff=tariff_data.get("date_tariff"),
                cargo_type=tariff_data.get("cargo_type")
            ).first()
            if tariff_check:
                logger.error("Try to add already exists tariff")
                raise HTTPException(status_code=409, detail="Tariff already exists")
            tariff = Tariff(**tariff_data)
            await tariff.save()
        logger.info("Add new tariffs from json file")
        return {"message": "Tariffs uploaded successfully"}
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in the uploaded file")
        raise HTTPException(status_code=400, detail="Invalid JSON format in the uploaded file")


@router.patch("/tariff/{tariff_id}", tags=["tariff"])
async def update_tariff(tariff_id: int, updated_tariff: TariffPatch = Depends(get_tariff_patch)):

    # Проверяем id тарифа
    tariff = await Tariff.get_or_none(id=tariff_id)
    if not tariff:
        logger.error(f"Tariff {tariff_id} not found")
        raise HTTPException(status_code=404, detail="Tariff not found")

    # Проверяем, какие поля надо обновить
    if updated_tariff.date_tariff is not None:
        tariff.date_tariff = updated_tariff.date_tariff
    if updated_tariff.cargo_type is not None:
        tariff.cargo_type = updated_tariff.cargo_type
    if updated_tariff.rate is not None:
        tariff.rate = updated_tariff.rate
    await tariff.save()

    logger.info(f"Patch tariff {tariff_id}")
    return await Tariff.get(id=tariff_id)


@router.delete("/tariff/{tariff_id}", tags=["tariff"])
async def delete_tariff(tariff_id: int, token: Token = Depends(get_token)):
    deleted_count = await Tariff.filter(id=tariff_id).delete()
    if deleted_count == 0:
        logger.error(f"Tariff {tariff_id} not found")
        raise HTTPException(status_code=404, detail="Tariff not found")
    logger.info(f"Tariff {tariff_id} deleted")
    return {"message": f"Deleted tariff with id={tariff_id}"}
