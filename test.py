import sqlalchemy as SA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pdb


def main():
    Base = declarative_base()

    class Sensor(Base):
        __tablename__ = 'sensors'
        id = SA.Column(SA.Integer, primary_key=True)
        name = SA.Column(SA.String)
        value = SA.Column(SA.Integer)

        def __repr__(self):
            return('{}:{}'.format(self.name, self.value))

    class Limit(Base):
        __tablename__ = 'limits'
        id = SA.Column(SA.Integer, primary_key=True)
        value = SA.Column(SA.Integer)
        name = SA.Column(SA.String)
        sensor_id = SA.Column(None, SA.ForeignKey('sensors.id'))
        sensor = relationship('Sensor', back_populates='limits')

        def __repr__(self):
            return(':{}'.format(self.name, self.value))

    class History(Base):
        __tablename__ = 'histories'
        id = SA.Column(SA.Integer, primary_key=True)
        value = SA.Column(SA.Integer)
        timestamp = SA.Column(SA.DateTime, server_default=SA.utcnow())
        sensor_id = SA.Column(None, SA.ForeignKey('sensors.id'))
        sensor = relationship('Sensor', back_populates='histories')

        def __repr__(self):
            return(':{}'.format(self.timestamp, self.value))

    Sensor.limits = relationship('Limit', order_by=Limit.id, back_populates='sensor')
    Sensor.histories = relationship('History', order_by=History.id, back_populates='sensor')
    Base.metadata.create_all(engine)

    sensor_1 = Sensor(value=42, name='GT1')
    sensor_2 = Sensor(value=43, name='GT2')
    sensor_1.limits = [
            Limit(value=23),
            Limit(value=23),
            Limit(value=23),
            Limit(value=23),
            Limit(value=84)
            ]
    sensor_2.limits = [
            Limit(value=45),
            Limit(value=46),
            Limit(value=47),
            Limit(value=48),
            Limit(value=49)
            ]
    sensor_1.histories = [History(value=42)]

    conn = engine.connect()

    Session = SA.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add_all([sensor_1, sensor_2])
    session.commit()

    print(session.query(Sensor).join(Limit).\
            filter(Limit.value==23).\
            all()
    )

    pdb.set_trace()

if __name__ == '__main__':
    engine = SA.create_engine('sqlite:///data.sqlite', echo=True)
    main()
