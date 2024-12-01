from sqlalchemy.orm import Session
from pereval.models import PerevalAdded, User, Coords, Level, Image
from pereval.schemas import PerevalCreate


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

        # Добавляем изображения
        for image_data in pereval_data.images:
            image = Image(
                url=image_data.url,
                title=image_data.title
            )
            self.db.add(image)
            new_pereval.images.append(image)

        self.db.commit()
        return new_pereval

    def get_pereval_by_id(self, pereval_id: int):
        return self.db.query(PerevalAdded).filter(PerevalAdded.id == pereval_id).first()

    def update_pereval(self, pereval_id: int, updated_pereval: PerevalCreate):
        pereval = self.db.query(PerevalAdded).filter(PerevalAdded.id == pereval_id).first()

        if not pereval or pereval.status != "new":
            return None  # Запись не найдена или не в статусе 'new', не обновляем

        # Обновляем разрешенные поля
        if updated_pereval.title:
            pereval.title = updated_pereval.title
        if updated_pereval.other_titles:
            pereval.other_titles = updated_pereval.other_titles
        if updated_pereval.connect:
            pereval.connect = updated_pereval.connect
        if updated_pereval.add_time:
            pereval.add_time = updated_pereval.add_time
        if updated_pereval.coords:
            coords = self.db.query(Coords).filter(Coords.id == pereval.coord_id).first()
            coords.latitude = updated_pereval.coords.latitude
            coords.longitude = updated_pereval.coords.longitude
            coords.height = updated_pereval.coords.height
        if updated_pereval.level:
            level = self.db.query(Level).filter(Level.id == pereval.level_id).first()
            level.winter = updated_pereval.level.winter
            level.summer = updated_pereval.level.summer
            level.autumn = updated_pereval.level.autumn
            level.spring = updated_pereval.level.spring

        self.db.commit()
        self.db.refresh(pereval)
        return pereval

    def get_perevals_by_user_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None  # Пользователь с таким email не найден
        return self.db.query(PerevalAdded).filter(PerevalAdded.user_id == user.id).all()
