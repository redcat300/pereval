from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from schemas import RawData
from crud import create_pass

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/submitData")
async def submit_data(pass_data: RawData, db: Session = Depends(get_db)):
    try:
        new_pass = create_pass(db=db, pass_data=pass_data)
        return {"status": 200, "message": "null", "id": new_pass.id}

    except ValidationError as e:
        return {"status": 400, "message": "Ошибка валидации данных: недостаточно полей или неверные типы данных", "id": None}

    except SQLAlchemyError as e:
        return {"status": 500, "message": "Ошибка при выполнении операции: ошибка базы данных", "id": None}

    except Exception as e:
        return {"status": 500, "message": f"Ошибка при выполнении операции: {str(e)}", "id": None}