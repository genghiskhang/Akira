from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc
import psycopg2

class SerializableAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        if not 'isolation_level' in options:
            options['isolation_level'] = 'SERIALIZABLE'
        return super(SerializableAlchemy, self).apply_driver_hacks(app, info, options)
    
db = SerializableAlchemy()

def retries(transaction_function):
    while True:
        try:
            transaction_function()
        except sqlalchemy.exc.OperationalError as e:
            if not isinstance(e.orig, psycopg2.errors.SerializationFailure):
                raise
            db.session.rollback()
        else:
            break