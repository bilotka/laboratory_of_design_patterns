#Пояснити код #Варіант 6. Розробити інтегратор для замовлення транспорту. Користувач передає адресу свого перебування та адресу призначення. # Передбачити що кожна служба
#таксі має власну систему замовлення: Uklon приймає запит (адреса кінця, адреса початку), Bolt # приймає запит тип пункту (початок поїздки чи кінець) та адресу тому потребує 
# 2 послідовних запитів для замовлення, а Uber приймає # запит із 3 параметрами (адреса початку, адреса кінця та час замовлення).Наприклад, для поїздки із вул. Університетська 
# 14 на пл. # Народна 3 Uklon прийме запит ("пл. Народна 3", "вул. Університетська 14") Bolt приймає 2 запити ("begin", "вул. Університетська 14") # та ("end", "пл. Народна 3 "),
#  а Uber приймає запит ("вул. Університетська 14", "пл. Народна 3", 9:30 21.09.2022)
from datetime import datetime

class Uklon:
    def make_order(self, end, start):
        print(f"[Uklon] Замовлення створено: з {start} до {end}")

class Bolt:
    def request(self, point_type, address):
        print(f"[Bolt] Запит: {point_type} -> {address}")

class Uber:
    def order(self, start, end, time):
        print(f"[Uber] Замовлення: {start} -> {end} о {time}")


class UklonAdapter:
    def __init__(self, service):
        self.service = service

    def order_trip(self, start, end):
        self.service.make_order(end, start)


class BoltAdapter:
    def __init__(self, service):
        self.service = service

    def order_trip(self, start, end):
        self.service.request("begin", start)
        self.service.request("end", end)


class UberAdapter:
    def __init__(self, service):
        self.service = service

    def order_trip(self, start, end):
        now = datetime.now().strftime("%H:%M %d.%m.%Y")
        self.service.order(start, end, now)


class TaxiIntegrator:
    def __init__(self):
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    def order_taxi(self, start, end):
        print(f"\n Замовлення таксі з {start} до {end}")
        for service in self.services:
            service.order_trip(start, end)


# Приклад виконання
def test_adapter() -> None: 
    uklon = UklonAdapter(Uklon()) 
    bolt = BoltAdapter(Bolt()) 
    uber = UberAdapter(Uber()) 
    integrator = TaxiIntegrator() 
    integrator.add_service(uklon) 
    integrator.add_service(bolt) 
    integrator.add_service(uber) 
    integrator.order_taxi("вул. Університетська 14", "пл. Народна 3") 
    
if __name__ == "__main__": 
    test_adapter()
