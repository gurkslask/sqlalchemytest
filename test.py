import sqlalchemy as SA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pdb


def main():
    Base = declarative_base()
    class Sensor(Base):
        __tablename__ = 'sensors'
        id = SA.Column(SA.Integer, primary_key=True)
        value = SA.Column(SA.Integer)

        def __repr__(self):
            return(':{}'.format(self.value))

    class Limit(Base):
        __tablename__ = 'limits'
        id = SA.Column(SA.Integer, primary_key=True)
        value = SA.Column(SA.Integer)
        sensor_id = SA.Column(None, SA.ForeignKey('sensors.id'))
        sensor = relationship('Sensor', back_populates='limits')

        def __repr__(self):
            return(':{}'.format(self.value))

    Sensor.limits = relationship('Limit', order_by=Limit.id, back_populates='sensor')
    """sensors = SA.Table('sensors',
            metadata,
            SA.Column('id', SA.Integer, primary_key=True),
            SA.Column('value', SA.Integer)
            )
    limits = SA.Table('limits',
            metadata,
            SA.Column('id', SA.Integer, primary_key=True),
            SA.Column('value', SA.Integer),
            SA.Column('sensor_id', None, SA.ForeignKey('sensors.id'))
            )"""
    Base.metadata.create_all(engine)

    sensor_1 = Sensor(value=42)
    sensor_2 = Sensor(value=43)
    sensor_1.limits = [
            Limit(value=23),
            Limit(value=84)
            ]


    conn = engine.connect()

    Session = SA.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add_all([sensor_1, sensor_2])

    pdb.set_trace()

if __name__ == '__main__':
    engine = SA.create_engine('sqlite:///:memory:', echo=True)
    main()
