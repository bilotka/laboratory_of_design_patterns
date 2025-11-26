#Варіант 6. Розробити інтегратор для замовлення транспорту. Користувач передає адресу свого перебування та адресу призначення. # Передбачити що кожна служба
# таксі має власну систему замовлення: Uklon приймає запит (адреса кінця, адреса початку), Bolt # приймає запит тип пункту (початок поїздки чи кінець) та адресу тому потребує 
# 2 послідовних запитів для замовлення, а Uber приймає # запит із 3 параметрами (адреса початку, адреса кінця та час замовлення).Наприклад, для поїздки із вул. Університетська 
# 14 на пл. # Народна 3 Uklon прийме запит ("пл. Народна 3", "вул. Університетська 14") Bolt приймає 2 запити ("begin", "вул. Університетська 14") # та ("end", "пл. Народна 3 "),
#  а Uber приймає запит ("вул. Університетська 14", "пл. Народна 3", 9:30 21.09.2022)
from typing import Protocol
from datetime import datetime

class ITaxi(Protocol):
    def order_trip(self, start: str, end: str) -> None:
        ...

class Uklon:
    def make_order(self, end: str, start: str):
        print(f"[Uklon] Замовлення створено: з {start} до {end}")


class Bolt:
    def request(self, point_type: str, address: str):
        print(f"[Bolt] Запит: {point_type} → {address}")


class Uber:
    def order(self, start: str, end: str, time: str):
        print(f"[Uber] Замовлення: {start} → {end} о {time}")

class UklonAdapter:
    def __init__(self, service: Uklon):
        self.service = service

    def order_trip(self, start: str, end: str):
        self.service.make_order(end, start)


class BoltAdapter:
    def __init__(self, service: Bolt):
        self.service = service

    def order_trip(self, start: str, end: str):
        self.service.request("begin", start)
        self.service.request("end", end)


class UberAdapter:
    def __init__(self, service: Uber):
        self.service = service

    def order_trip(self, start: str, end: str):
        now = datetime.now().strftime("%H:%M %d.%m.%Y")
        self.service.order(start, end, now)


class TaxiIntegrator:
    def __init__(self):
        self.services: list[ITaxi] = []

    def add_service(self, service):

        if isinstance(service, Uklon):
            self.services.append(UklonAdapter(service))

        elif isinstance(service, Bolt):
            self.services.append(BoltAdapter(service))

        elif isinstance(service, Uber):
            self.services.append(UberAdapter(service))

    def order_taxi(self, start: str, end: str):
        print(f"\nЗамовлення таксі з {start} до {end}")
        for service in self.services:
            service.order_trip(start, end)


# Приклад виконання
def test_adapter() -> None: 
    integrator.add_service(Uklon())
    integrator.add_service(Bolt())
    integrator.add_service(Uber())

    integrator.order_taxi("вул. Університетська 14", "пл. Народна 3")
    
if __name__ == "__main__": 
    test_adapter()
