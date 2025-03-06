import uuid

from sqlalchemy import Boolean, Integer, DateTime, Float, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Assortment(Base):
    __tablename__ = 'assortment'
    
    position_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, nullable=False, unique=True) #connect with Sales
    updated = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    code = Column(String, nullable=False)
    archived = Column(Boolean, nullable=False)
    pathname = Column(String, nullable=False)
    paymentitemtype = Column(String, nullable=False)
    volume = Column(Float, nullable=False)
    variantscount = Column(Float, nullable=False)
    stock = Column(Float, nullable=False)
    reserve = Column(Float, nullable=False)
    intransit = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    price_usd = Column(Float, nullable=False)
    price_distr = Column(Float, nullable=False)
    price_opt = Column(Float, nullable=False)
    price_proiz = Column(Float, nullable=False)
    price_rrz = Column(Float, nullable=False)
    price_site = Column(Float, nullable=False)
    price_tech = Column(Float, nullable=False)

    sales = relationship("Sales", back_populates="assortment")
    # assortment_stock = relationship("Stock", back_populates="assortment_stock")

class Sales(Base):
    __tablename__ = "sales"

    id_sale = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(String, nullable=False)
    agent_id = Column(String, ForeignKey('agents.agent_id'), nullable=False)
    name = Column(String, nullable=False)
    updated = Column(DateTime, nullable=False)
    moment = Column(DateTime, nullable=False) 
    created = Column(DateTime, nullable=False) 
    state = Column(String, nullable=False)
    sum = Column(Float, nullable=False)
    vatSum = Column(Float, nullable=False)
    payedSum = Column(Float, nullable=False)
    shippedSum = Column(Float, nullable=False)
    invoicedSum = Column(Float, nullable=False)
    reservedSum = Column(Float, nullable=False)
    assortment_id = Column(String, ForeignKey('assortment.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipmentAddress = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    assortment = relationship("Assortment", back_populates="sales")
    agent = relationship("Agents", back_populates="agent")


class Agents(Base):
    __tablename__ = 'agents'

    id_agent_base = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String, nullable=False, unique=True)
    updated = Column(DateTime)
    name = Column(String)
    created = Column(DateTime)
    companyType = Column(String)
    actualAddress = Column(String)
    phone = Column(String)
    tags = Column(String)
    legalTitle = Column(String)
    legalLastName = Column(String)
    legalFirstName = Column(String)
    email = Column(String)
    legalAddress = Column(String)

    # Странный контрагент, которого возможно надо добавлять руками "https://online.moysklad.ru/app/#Company/edit?id=6159d9b1-8503-11ed-0a80-01400053123a"

    agent = relationship("Sales", back_populates="agent")


class Stock(Base):
    __tablename__ = 'stock'

    id_stock_base = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock = Column(Float)
    inTransit = Column(Float)
    reserve = Column(Float)
    quantity = Column(Float)
    name = Column(String)
    # code = Column(String, ForeignKey('assortment.code'), unique=True)
    code = Column(String)
    article = Column(String)
    stockDays = Column(Float)

    # assortment_stock = relationship("Assortment", back_populates="")
