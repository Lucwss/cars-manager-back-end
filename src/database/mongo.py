from dotenv import find_dotenv, load_dotenv
import motor.motor_asyncio
import os

# DB_URL = "mongodb+srv://<dbName>:<dbPassword>@cluster0.fkm24.mongodb.net/?retryWrites=true&w=majority"
# DB_NAME = "carsApp"
# COLLECTION_NAME = "cars1"

load_dotenv(find_dotenv('../../.env.dev'))


class Mongo:
    def __init__(self):
        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')
        self.connection = self._connection()

    def _connection(self):
        return motor.motor_asyncio.AsyncIOMotorClient(
            f'mongodb://{self.host}:{self.port}/'
        )

    def database(self):
        return self.connection.carsApp
