from sqlalchemy.orm import Session
from models import PerevalAdded, User, Coords, Level, Image
from schemas import PerevalCreate


class PerevalDB:
    def __init__(self, db: Session):
        self.db = db

    def add_pereval(self, pereval_data: PerevalCreate):
        user = self.db.query(User).filter(User.email == pereval_data.user.email).first()
        if not user:
            user = User(
                fam=pereval_data.user.fam,
                name=pereval_data.user.name,
                otc=pereval_data.user.otc,
                email=pereval_data.user.email,
                phone=pereval_data.user.phone
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        # Создаем координаты
        coords = Coords(
            latitude=pereval_data.coords.latitude,
            longitude=pereval_data.coords.longitude,
            height=pereval_data.coords.height
        )
        self.db.add(coords)
        self.db.commit()
        self.db.refresh(coords)

        # Создаем уровень сложности
        level = Level(
            winter=pereval_data.level.winter,
            summer=pereval_data.level.summer,
            autumn=pereval_data.level.autumn,
            spring=pereval_data.level.spring
        )
        self.db.add(level)
        self.db.commit()
        self.db.refresh(level)

        # Создаем запись о перевале
        new_pereval = PerevalAdded(
            user_id=user.id,
            beauty_title=pereval_data.beauty_title,
            title=pereval_data.title,
            other_titles=pereval_data.other_titles,
            connect=pereval_data.connect,
            add_time=pereval_data.add_time,
            coord_id=coords.id,
            level_id=level.id,
            status="new"
        )
        self.db.add(new_pereval)
        self.db.commit()
        self.db.refresh(new_pereval)


        for image_data in pereval_data.images:
            image = Image(
                url=image_data.url,
                title=image_data.title
            )
            self.db.add(image)
            new_pereval.images.append(image)

        self.db.commit()
        return new_pereval
