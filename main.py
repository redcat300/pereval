from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pereval.database import get_db, Base, engine
from pereval.schemas import PerevalCreate, PerevalResponse
from pereval.crud import PerevalDB



Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/submitData", response_model=PerevalResponse)
async def submit_data(pass_data: PerevalCreate, db: Session = Depends(get_db)):
    try:
        pereval_db = PerevalDB(db)
        new_pass = pereval_db.add_pereval(pereval_data=pass_data)
        return new_pass

    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Ошибка валидации данных")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при выполнении операции: ошибка базы данных")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении операции: {str(e)}")

@app.get("/submitData/{pereval_id}", response_model=PerevalResponse)
async def get_pereval(pereval_id: int, db: Session = Depends(get_db)):
    try:
        pereval_db = PerevalDB(db)
        pereval = pereval_db.get_pereval_by_id(pereval_id)
        if not pereval:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        return pereval

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при выполнении операции: ошибка базы данных")


@app.patch("/submitData/{pereval_id}", response_model=dict)
async def update_pereval(pereval_id: int, pass_data: PerevalCreate, db: Session = Depends(get_db)):
    try:
        pereval_db = PerevalDB(db)

        # Получаем существующую запись по ID
        existing_pereval = pereval_db.get_pereval_by_id(pereval_id)

        # Проверяем, существует ли запись и её статус
        if not existing_pereval:
            return {"state": 0, "message": "Запись не найдена"}

        if existing_pereval.status != "new":
            return {"state": 0, "message": "Запись не в статусе 'new', редактирование невозможно"}

        # Проверяем, что поля пользователя не были изменены
        if (pass_data.user.fam != existing_pereval.user.fam or
                pass_data.user.name != existing_pereval.user.name or
                pass_data.user.otc != existing_pereval.user.otc or
                pass_data.user.email != existing_pereval.user.email or
                pass_data.user.phone != existing_pereval.user.phone):
            return {"state": 0, "message": "Нельзя изменять данные пользователя (ФИО, почта, телефон)"}

        # Обновляем поля записи, которые можно редактировать
        updated_pereval = pereval_db.update_pereval(pereval_id, updated_pereval=pass_data)

        # Проверка на успешность обновления
        if not updated_pereval:
            return {"state": 0, "message": "Не удалось обновить запись"}

        return {"state": 1, "message": "Запись успешно обновлена"}

    except SQLAlchemyError as e:
        db.rollback()
        return {"state": 0, "message": f"Ошибка базы данных: {str(e)}"}

    except Exception as e:
        return {"state": 0, "message": f"Ошибка: {str(e)}"}


@app.get("/submitData", response_model=list[PerevalResponse])
async def get_perevals_by_email(user_email: str, db: Session = Depends(get_db)):
    try:
        pereval_db = PerevalDB(db)
        perevals = pereval_db.get_perevals_by_user_email(user_email)
        if not perevals:
            raise HTTPException(status_code=404, detail="Записи не найдены")
        return perevals

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при выполнении операции: ошибка базы данных")