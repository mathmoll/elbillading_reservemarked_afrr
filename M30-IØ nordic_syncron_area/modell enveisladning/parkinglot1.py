
class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.parked_cars = {}  # A dictionary to hold Car objects

    def add_car(self, car, timestamp):
        # Check if the parking lot has reached its capacity
        if len(self.parked_cars) < self.capacity:
            # Add the car to the parked cars dictionary
            self.parked_cars[car.name] = car
            #add arrival and departure time
            car.departure_time = timestamp
            return True
        else:
            # Parking lot is at capacity; cannot add more cars
            return False

    def remove_car(self, car_name):
        # Remove a car from the parked cars dictionary by its name
        if car_name in self.parked_cars:
            del self.parked_cars[car_name]

