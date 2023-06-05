from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from .database import *
from sqlalchemy.orm import relationship

# Create an engine to connect to the database
engine = create_engine('sqlite:///inventory.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'Purchase'

    id = Column(Integer, primary_key=True, autoincrement="ignore_fk")
    AuctionDate = Column(Date,default=func.current_date())
    FirmName = Column(Integer,ForeignKey('PartyName.id'))
    MarkingID = Column(String)
    Box = Column(Integer)
    AuctionRate = Column(Float)
    Rate = Column(Float)
    weight = Column(Float,default=0)
    sells = relationship('Sell', backref="Purchase")
    coldfacility_id = Column(Integer, ForeignKey('ColdFacility.id'))

    def __repr__(self):
        return f"ID:{self.id} | Auction Date:{self.AuctionDate} | Firm Name:{self.FirmName} | MarkingID:{self.MarkingID} | Box:{self.Box} | Auction Rate:{self.AuctionRate} | Net Rate:{self.Rate} | Net Weight:{self.weight} | Cold Facility:{self.coldfacility_id}"

class Sell(Base):
    __tablename__ = 'Sell'
    id = Column(Integer, primary_key=True, autoincrement="ignore_fk")
    MarkingID = Column(String)    
    SellTo = Column(Integer,ForeignKey('PartyName.id'))
    Box = Column(Integer)
    Dispatched = Column(Boolean,default=False)
    DispatchDate = Column(Date)     
    purchase_id = Column(Integer, ForeignKey('Purchase.id'))

    def __repr__(self):
        return f"ID: {self.id} | Marking ID: {self.MarkingID} | Sold To: {self.SellTo} | Box: {self.Box} | Dispatched: {self.Dispatched}"

class ColdFacility(Base):
    __tablename__ = 'ColdFacility'
    id = Column(Integer, primary_key=True, autoincrement="ignore_fk")
    Name = Column(String)
    lots = relationship("Purchase", backref="coldfacility")

    def __repr__(self):
        return f"{self.id} | {self.Name}"

class PartyName(Base):
    __tablename__ = 'PartyName'
    id = Column(Integer, primary_key=True, autoincrement="ignore_fk")
    Name = Column(String)
    business = relationship("Purchase", backref="PartyName")

    def __repr__(self):
        return f"{self.id} | {self.Name}"


# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


# Example usage: adding purchase to the database
# p1 = Purchase(AuctionDate='31/05/2023', FirmName="Ganesh Traders", MarkingID="BCD",Box=18,AuctionRate=88)
# p2 = Purchase(AuctionDate='31/05/2023', FirmName="KC Traders", MarkingID="ABC",Box=25,AuctionRate=60)

# session.add(p1)
# session.add(p2)
# session.commit()

# Example usage: querying items from the database
# items = session.query(Purchase).all()
# for item in items:
#     print(item)






# Insert data into the table
# person = Purchase(name='John', age=30)
# session.add(person)
# session.commit()
