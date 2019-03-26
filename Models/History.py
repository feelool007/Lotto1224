from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    n01 = Column(String)
    n02 = Column(String)
    n03 = Column(String)
    n04 = Column(String)
    n05 = Column(String)
    n06 = Column(String)
    n07 = Column(String)
    n08 = Column(String)
    n09 = Column(String)
    n10 = Column(String)
    n11 = Column(String)
    n12 = Column(String)
    radno = Column(Integer)
    date = Column(String)
    firstPrize = Column(Integer)
    secondPrize = Column(Integer)
    thirdPrize = Column(Integer)
    forthPrize = Column(Integer)
    totalAmount = Column(Integer)
    oddEven = Column(String)
    smallLarge = Column(String)

    def __repr__(self):
        return "<History(radNo=%s, date=%s, result=%s)>" %(
            self.radno, self.date,
            [self.n01, self.n02, self.n03, self.n04, self.n05, self.n06,
             self.n07, self.n08, self.n09, self.n10, self.n11, self.n12]
        )

    def __call__(self, *args, **kwargs):
        return [
            self.n01, self.n02, self.n03, self.n04, self.n05, self.n06,
            self.n07, self.n08, self.n09, self.n10, self.n11, self.n12
        ]
