from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..models import UserModel, CarModel, OrderModel
from .db_conf import ENGINE, ORM_BASE
from .hash import hash_password


async def seed_database():
    async with ENGINE.begin() as conn:
        await conn.run_sync(ORM_BASE.metadata.create_all)

    async_session = async_sessionmaker(ENGINE, expire_on_commit=False)
    async with async_session() as session:
        users_result = await session.execute(select(UserModel))
        if users_result.scalars().all():
            print("Database already seeded. Skipping.")
            return

        user1 = UserModel(
            username="user1",
            email="user1@example.com",
            hashed_password=hash_password("password123"),
            is_active=True,
            created_at=datetime.utcnow(),
        )
        user2 = UserModel(
            username="user2",
            email="user2@example.com",
            hashed_password=hash_password("password123"),
            is_active=True,
            created_at=datetime.utcnow(),
        )
        session.add_all([user1, user2])
        await session.commit()
        await session.refresh(user1)
        await session.refresh(user2)

        # Seed Cars
        car1 = CarModel(
            brand="Toyota",
            model="Camry",
            year=2022,
            body_type="Sedan",
            engine_type="Inline-4",
            engine_size_liters=2.5,
            horsepower=203,
            transmission="Automatic",
            fuel_type="Gasoline",
            mileage_km=50000,
            top_speed_kmh=210,
            color="Silver",
            features="Bluetooth, Cruise Control, Backup Camera",
            price_usd=25000.0,
            discount_percent=5.0,
            num_in_stock=10,
            description="Reliable mid-size sedan with great fuel efficiency.",
        )
        car2 = CarModel(
            brand="Honda",
            model="Civic",
            year=2021,
            body_type="Hatchback",
            engine_type="Inline-4",
            engine_size_liters=1.5,
            horsepower=174,
            transmission="CVT",
            fuel_type="Gasoline",
            mileage_km=30000,
            top_speed_kmh=200,
            color="Red",
            features="Apple CarPlay, Android Auto, Lane Assist",
            price_usd=22000.0,
            discount_percent=0.0,
            num_in_stock=15,
            description="Sporty compact car with modern tech features.",
        )
        car3 = CarModel(
            brand="Ford",
            model="Mustang",
            year=2023,
            body_type="Coupe",
            engine_type="V8",
            engine_size_liters=5.0,
            horsepower=450,
            transmission="Manual",
            fuel_type="Gasoline",
            mileage_km=10000,
            top_speed_kmh=250,
            color="Black",
            features="Performance Package, Leather Seats, Premium Audio",
            price_usd=45000.0,
            discount_percent=10.0,
            num_in_stock=5,
            description="Iconic muscle car with powerful performance.",
        )
        session.add_all([car1, car2, car3])
        await session.commit()
        await session.refresh(car1)
        await session.refresh(car2)
        await session.refresh(car3)

        order1 = OrderModel(
            user_id=user1.id, created_at=datetime.utcnow(), cars=[car1, car2]
        )
        order2 = OrderModel(user_id=user2.id, created_at=datetime.utcnow(), cars=[car3])
        session.add_all([order1, order2])
        await session.commit()

        print("Database seeded with dummy data.")
