from db.models import async_session
from db.models import User
from db.models import Progr
from sqlalchemy import select

async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name=name))
            session.add(Progr(id=tg_id, et1=0, et2=0, et3=0))
            await session.commit()
        else:
            progr = await session.scalar(select(Progr).where(Progr.id == tg_id))  # Получаем объект из базы по ID
            if progr:  # Проверяем, существует ли объект
                # Обновляем атрибуты на 0
                progr.et1 = 0
                progr.et2 = 0
                progr.et3 = 0
                await session.commit()

async def set_ball(tg_id, c1, c2, c3):
    async with async_session() as session:
        progr = await session.scalar(select(Progr).where(Progr.id == tg_id))  # Получаем объект программы
        if progr:
            # Обновляем атрибуты
            progr.et1 += c1
            progr.et2 += c2
            progr.et3 += c3
            await session.commit()


async def give_res(tg_id):
    async with async_session() as session:
        res = 0
        try:
            progr = await session.scalar(select(Progr).where(Progr.id == tg_id))  # Получаем объект программы
            if progr:
                # Обновляем атрибуты
                res = progr.et1 + progr.et2 + progr.et3
            else:
                print(f"Запись для tg_id {tg_id} не найдена.")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
    return res
