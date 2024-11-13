from sqlalchemy.orm import Session
from models import Pass, PerevalAdded
from schemas import RawData, PerevalCreate

def create_pass(db: Session, pass_data: RawData):
    db_pass = Pass(
        beauty_title=pass_data.beauty_title,
        title=pass_data.title,
        other_titles=pass_data.other_titles,
        connect=pass_data.connect,
        add_time=pass_data.add_time,
        latitude=pass_data.coords.latitude,
        longitude=pass_data.coords.longitude,
        height=pass_data.coords.height,
        winter=pass_data.level.winter,
        summer=pass_data.level.summer,
        autumn=pass_data.level.autumn,
        spring=pass_data.level.spring,
        user_fam=pass_data.user.fam,
        user_name=pass_data.user.name,
        user_otc=pass_data.user.otc,
        user_email=pass_data.user.email,
        user_phone=pass_data.user.phone
    )
    db.add(db_pass)
    db.commit()
    db.refresh(db_pass)
    return db_pass

class PerevalDB:
    def __init__(self):
        self.db = db

    def add_pereval(self, pereval_data: PerevalCreate):
        new_pereval = PerevalAdded(
            date_added=pereval_data.date_added,
            raw_data=pereval_data.raw_data,
            images=pereval_data.images,
            status="new"  # Устанавливаем статус new
        )
        self.db.add(new_pereval)
        self.db.commit()
        self.db.refresh(new_pereval)
        return new_pereval
