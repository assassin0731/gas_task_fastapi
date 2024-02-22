

from datetime import date
from statistics import median

from fastapi import FastAPI, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from funcs import get_async_session
from models.model import stat

app = FastAPI()


device_stat = dict()

@app.get("/")
async def get_stats(id: int, session: AsyncSession = Depends(get_async_session)):
    """Статистика по идентификатору"""
    query = select(stat).where(stat.c.id == id)
    result = await session.execute(query)
    device_stat[id] = result.mappings().all()
    return {"stat": id}


@app.post('/')
async def load_stats(id: int, x: float, y: float, z: float, session: AsyncSession = Depends(get_async_session)):
    """Добавление устройства со статистикой"""
    stmt = insert(stat).values(id=id, x=x, y=y, z=z)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@app.get('/analyse_all')
def analyse_stats(id: int):
    """Просмотр статистики по устройству за все время"""
    if id in device_stat:
        x_all = [dev['x'] for dev in device_stat[id]]
        y_all = [dev['y'] for dev in device_stat[id]]
        z_all = [dev['z'] for dev in device_stat[id]]
        return [
                {'x_min': min(x_all), 'y_min': min(y_all), 'z_min': min(z_all)},
                {'x_max': max(x_all), 'y_max': max(y_all), 'z_max': max(z_all)},
                {'count': len(device_stat[id])},
                {'x_sum': sum(x_all), 'y_sum': sum(y_all), 'z_sum': sum(z_all)},
                {'x_med': median(x_all), 'y_med': median(y_all), 'z_med': median(z_all)}
                ]
    else:
        return {"error": "Статистики по устройству с таким id нет"}


@app.get('/analyse_date')
def analyse_stats(id: int, begin: date, end: date):
    """Просмотр статистики по устройству за период"""
    if id in device_stat:
        x_all = [dev['x'] for dev in device_stat[id] if begin <= dev['registered_at'].date() <= end]
        y_all = [dev['y'] for dev in device_stat[id] if begin <= dev['registered_at'].date() <= end]
        z_all = [dev['z'] for dev in device_stat[id] if begin <= dev['registered_at'].date() <= end]
        if x_all:
            return [
                {'x_min': min(x_all), 'y_min': min(y_all), 'z_min': min(z_all)},
                {'x_max': max(x_all), 'y_max': max(y_all), 'z_max': max(z_all)},
                {'count': len(device_stat[id])},
                {'x_sum': sum(x_all), 'y_sum': sum(y_all), 'z_sum': sum(z_all)},
                {'x_med': median(x_all), 'y_med': median(y_all), 'z_med': median(z_all)}
            ]
        else:
            return {"status": "Статистики за этот период нет"}
    else:
        return {"error": "Статистики по устройству с таким id нет"}
