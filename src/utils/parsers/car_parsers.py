from src.models.pydantic_models.car.car_db import CarDB


class CarParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_car(car_data: CarDB):
        return {
            'id': str(car_data.id),
            'brand': car_data.brand,
            'make': car_data.make,
            'year': car_data.year,
            'price': float(car_data.price),
            'km': car_data.km,
            'cm3': car_data.cm3,
        }
