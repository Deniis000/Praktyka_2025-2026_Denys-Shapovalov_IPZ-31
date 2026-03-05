class Car:
    def __init__(self, brand, year, mileage=0):
        self.brand = brand
        self._year = year
        self._mileage = mileage

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        if value < 0:
            raise ValueError("Пробіг не може бути від'ємним")
        if value < self._mileage:
            raise ValueError("Пробіг не може зменшуватися")
        self._mileage = value
        print(f"Пробіг оновлено до {self._mileage} км")

    @property
    def year(self):
        return self._year

    def drive(self, km):
        if km > 0:
            self.mileage += km
        else:
            print("Не можна проїхати від'ємну відстань")

    def __str__(self):
        return f"{self.brand} ({self.year}) - пробіг {self.mileage} км"

print("--- Використання property для валідації ---")
my_car = Car("Tesla", 2022, 5000)
print(my_car)

my_car.mileage = 5500
print(my_car)

try:
    my_car.mileage = 500
except ValueError as e:
    print(f"Помилка: {e}")

my_car.drive(100)
print(my_car)
