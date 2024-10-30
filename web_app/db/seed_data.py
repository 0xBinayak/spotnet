"""
Seed data for initializing the database with predefined values.
"""
from faker import Faker
from sqlalchemy.orm import Session
from .models import User, Position, AirDrop, TelegramUser
from .database import Base, engine, SessionLocal

# Initialize Faker
fake = Faker()

def create_users(session: Session):
    """
    Create and save a list of fake users to the database.
    Args:
        session (Session): SQLAlchemy session object.
    Returns:
        list: A list of User objects added to the database.
    """
    users = []
    for _ in range(10):
        user = User(
            wallet_id=fake.unique.uuid4(),
            contract_address=fake.address(),
            is_contract_deployed=fake.boolean()
        )
        users.append(user)
    session.bulk_save_objects(users)
    session.commit()
    return users

def create_positions(session: Session, users):
    """
    Create and save fake position records associated with given users.
    Args:
        session (Session): SQLAlchemy session object.
        users (list): List of User objects to associate with positions.
    """
    positions = []
    for user in users:
        for _ in range(10):
            position = Position(
                user_id=user.id,
                token_symbol=fake.word(),
                amount=fake.random_number(digits=5),
                multiplier=fake.random_int(min=1, max=10),
                start_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                status=fake.random_element(elements=[status.value for status in Status]),
            )
            positions.append(position)
    session.bulk_save_objects(positions)
    session.commit()

def create_airdrops(session: Session, users):
    """
    Create and save fake airdrop records for each user.
    Args:
        session (Session): SQLAlchemy session object.
        users (list): List of User objects to associate with airdrops.
    """
    airdrops = []
    for user in users:
        for _ in range(10):
            airdrop = AirDrop(
                user_id=user.id,
                amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                is_claimed=fake.boolean(),
                claimed_at=fake.date_time_this_decade() if fake.boolean() else None,
            )
            airdrops.append(airdrop)
    session.bulk_save_objects(airdrops)
    session.commit()

def create_telegram_users(session: Session):
    """
    Create and save fake Telegram user records to the database.
    Args:
        session (Session): SQLAlchemy session object.
    """
    telegram_users = []
    for _ in range(10):
        telegram_user = TelegramUser(
            telegram_id=fake.unique.uuid4(),
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            wallet_id=fake.unique.uuid4(),
            photo_url=fake.image_url(),
        )
        telegram_users.append(telegram_user)
    session.bulk_save_objects(telegram_users)
    session.commit()

if __name__ == '__main__':
    # Create tables
    Base.metadata.create_all(engine)

    # Start a new session for seeding data
    with SessionLocal() as session:
        # Populate the database
        users = create_users(session)
        create_positions(session, users)
        create_airdrops(session, users)
        create_telegram_users(session)

    print("Database populated with fake data.")
