from sqlalchemy import VARCHAR, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from base import BaseModel


class Order(BaseModel):
    """
    Represents an order placed by a user.

    Attributes:
    - user_id (UUID): The unique identifier of the user who placed the order.
                      Acts as both a primary key and a foreign key referencing the "user" table.
    - price (float): The price of the order, stored with a precision of up to 10 digits and 2 decimal places.
    - token (str): The token associated with the order.
    - position (UUID): The identifier of the position related to the order.

    Table:
    - Name: "order"
    """
    __tablename__ = "order"
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    token: Mapped[str] = mapped_column(VARCHAR)
    position: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
