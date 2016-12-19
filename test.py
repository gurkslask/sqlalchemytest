import sqlalchemy as SA


def main():
    metadata = SA.MetaData()

    sensors = SA.Table('sensors',
            metadata,
            SA.Column('id', SA.Integer, primary_key=True),
            SA.Column('value', SA.Integer)
            )
    limits = SA.Table('limits',
            metadata,
            SA.Column('id', SA.Integer, primary_key=True),
            SA.Column('value', SA.Integer),
            SA.Column('sensor_id', None, SA.ForeignKey('sensors.id'))
            )
    metadata.create_all(engine)
    ins = sensors.insert().values(value=42)
    ins2 = limits.insert().values(value=24, sensor_id=2)
    conn = engine.connect()
    result = conn.execute(ins)
    result = conn.execute(ins2)

if __name__ == '__main__':
    engine = SA.create_engine('sqlite:///:memory:', echo=True)
    main()
