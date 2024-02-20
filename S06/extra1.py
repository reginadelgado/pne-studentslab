class Car:
    def __init__(self, brand, speed=0):
        self.car_brand = brand
        self.speed = speed
    def set_speed(self, speed):
        self.speed = speed
    def get_bran_nationality(self):
        if self.car_brand == "Renault":
            return "France"
        elif self.car_brand == "Ferrari":
            return "Italy"

mycar = Car("Renault", 30)
mycar.set_speed(80)
print(mycar.speed)

print(mycar.get_bran_nationality())

yourcar = Car("Ferrari", 250)
print(yourcar.speed)