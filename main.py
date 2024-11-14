from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db, Base, engine
from schemas import PerevalCreate, PerevalResponse
from crud import PerevalDB

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
