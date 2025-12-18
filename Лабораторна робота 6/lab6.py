from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta
# Шаблон СТРАТЕГІЯ (Strategy)
# Дозволяє змінювати спосіб відправки повідомлень (Консоль, Email тощо)

class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class ConsoleNotification(NotificationStrategy):
    def send(self, message: str) -> None:
        print(f" >>> [SYSTEM MSG]: {message}")


class User:
    _id_counter = 1
    def __init__(self, name: str, email: str, password: str):
        self.id = str(User._id_counter)
        User._id_counter += 1
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = False

class Admin(User):
    def __init__(self, name: str, email: str, password: str):
        super().__init__(name, email, password)
        self.is_admin = True

class RaceSession:
    """Клас, що описує один заїзд"""
    _id_counter = 1
    def __init__(self, date_time: datetime, capacity: int = 4):
        self.id = str(RaceSession._id_counter)
        RaceSession._id_counter += 1
        self.date_time = date_time
        self.capacity = capacity
        self.booked_count = 0

    @property
    def free_slots(self) -> int:
        return self.capacity - self.booked_count

    def is_available(self) -> bool:
        return self.free_slots > 0

    def book_spot(self):
        if self.is_available():
            self.booked_count += 1
        else:
            raise ValueError("Немає вільних місць")

    def release_spot(self):
        if self.booked_count > 0:
            self.booked_count -= 1

class Booking:
    """Клас бронювання"""
    _id_counter = 1
    def __init__(self, user: User, session: RaceSession):
        self.id = str(Booking._id_counter)
        Booking._id_counter += 1
        self.user = user
        self.session = session
        self.created_at = datetime.now()

# Шаблон ФАСАД (Facade)
# Приховує всю логіку роботи зі списками users, sessions, bookings

class KartingSystemFacade:
    def __init__(self, notification: NotificationStrategy):
        self.notification = notification
        
        self.users: List[User] = []
        self.bookings: List[Booking] = []
        self.sessions: List[RaceSession] = []  
        
        self.current_user: Optional[User] = None

    def register(self, name: str, password: str) -> bool:
        if any(u.name == name for u in self.users):
            return False
        new_user = User(name, f"{name}@mail.com", password)
        self.users.append(new_user)
        self.notification.send(f"Реєстрація успішна! ID: {new_user.id}")
        return True

    def login(self, name: str, password: str) -> bool:
        user = next((u for u in self.users if u.name == name and u.password == password), None)
        if user:
            self.current_user = user
            role = "АДМІНІСТРАТОР" if user.is_admin else "Користувач"
            self.notification.send(f"Вхід виконано як {role}: {user.name}")
            return True
        return False

    def logout(self):
        self.current_user = None

    def get_future_sessions(self) -> List[RaceSession]:
        """Отримати список майбутніх заїздів"""
        now = datetime.now()
        return [s for s in self.sessions if s.date_time > now]

    def create_booking(self, session_index: int) -> bool:
        """Логіка запису на заїзд"""
        if not self.current_user:
            print("Спочатку увійдіть у систему!")
            return False
        
        available_sessions = self.get_future_sessions()
        
        if 0 <= session_index < len(available_sessions):
            session = available_sessions[session_index]
            if session.is_available():
                session.book_spot()
                new_booking = Booking(self.current_user, session)
                self.bookings.append(new_booking)
                self.notification.send(f"Успішно заброньовано на {session.date_time}")
                return True
            else:
                self.notification.send("Помилка: Немає вільних місць.")
        return False

    def get_my_bookings(self) -> List[Booking]:
        if not self.current_user:
            return []
        return [b for b in self.bookings if b.user.id == self.current_user.id]

    def cancel_booking(self, booking_index: int) -> bool:
        my_bookings = self.get_my_bookings()
        if 0 <= booking_index < len(my_bookings):
            booking = my_bookings[booking_index]
            booking.session.release_spot() 
            self.bookings.remove(booking) 
            self.notification.send("Бронювання скасовано.")
            return True
        return False

    def admin_add_session(self, date_time: datetime, capacity: int) -> None:
        """Метод для адміна: додає заїзд у загальний список"""
        if self.current_user and self.current_user.is_admin:
            new_session = RaceSession(date_time, capacity)
            self.sessions.append(new_session) 
            self.notification.send(f"Додано заїзд на {date_time}")
        else:
            print("У вас немає прав адміністратора!")

# КОНСОЛЬНЕ МЕНЮ 

class ConsoleMenu:
    def __init__(self, system: KartingSystemFacade) -> None:
        self.system = system
        self.running = True

    def run(self) -> None:
        while self.running:
            if self.system.current_user is None:
                self.guest_menu()
            elif self.system.current_user.is_admin:
                self.admin_menu()
            else:
                self.user_menu()

    #  МЕНЮ ГОСТЯ 
    def guest_menu(self):
        print("\n=== KARTING SYSTEM (Гість) ===")
        print("1. Вхід")
        print("2. Реєстрація")
        print("0. Вихід")
        choice = input("Вибір: ")
        if choice == "1": self.login()
        elif choice == "2": self.register()
        elif choice == "0": self.running = False
        else: print("Невірний вибір")

    # МЕНЮ КОРИСТУВАЧА
    def user_menu(self):
        print(f"\n=== Кабінет: {self.system.current_user.name} ===")
        print("1. Розклад і вільні місця")
        print("2. Записатися")
        print("3. Мої бронювання (скасувати)")
        print("0. Вийти з акаунту")
        choice = input("Вибір: ")
        if choice == "1": self.show_schedule()
        elif choice == "2": self.make_booking()
        elif choice == "3": self.manage_bookings()
        elif choice == "0": self.system.logout()
        else: print("Невірний вибір")

    # МЕНЮ АДМІНА
    def admin_menu(self):
        print(f"\n=== АДМІН-ПАНЕЛЬ: {self.system.current_user.name} ===")
        print("1. Переглянути всі заїзди")
        print("2. Додати новий заїзд")
        print("0. Вийти з акаунту")
        choice = input("Вибір: ")
        if choice == "1": self.show_schedule()
        elif choice == "2": self.add_session_admin()
        elif choice == "0": self.system.logout()
        else: print("Невірний вибір")

    # МЕТОДИ 
    def register(self):
        name = input("Логін: ")
        pw = input("Пароль: ")
        if not self.system.register(name, pw):
            print("Логін зайнятий!")

    def login(self):
        name = input("Логін: ")
        pw = input("Пароль: ")
        if not self.system.login(name, pw):
            print("Помилка входу.")

    def show_schedule(self):
        sessions = self.system.get_future_sessions()
        print("\n--- РОЗКЛАД ЗАЇЗДІВ ---")
        if not sessions:
            print("Немає запланованих заїздів.")
        else:
            print(f"{'№':<3} | {'Час':<16} | {'Вільні місця'}")
            print("-" * 35)
            for i, s in enumerate(sessions, 1):
                time_str = s.date_time.strftime("%d.%m %H:%M")
                print(f"{i:<3} | {time_str:<16} | {s.free_slots}/{s.capacity}")

    def make_booking(self):
        self.show_schedule()
        try:
            val = input("Оберіть номер заїзду (Enter - назад): ")
            if val:
                self.system.create_booking(int(val) - 1)
        except ValueError:
            print("Введіть число!")

    def manage_bookings(self):
        bookings = self.system.get_my_bookings()
        print("\n--- ВАШІ БРОНЮВАННЯ ---")
        if not bookings:
            print("Список порожній.")
            return
        
        for i, b in enumerate(bookings, 1):
            print(f"{i}. {b.session.date_time.strftime('%Y-%m-%d %H:%M')}")
        
        try:
            val = input("Номер для скасування (Enter - назад): ")
            if val:
                self.system.cancel_booking(int(val) - 1)
        except ValueError:
            print("Введіть число!")

    def add_session_admin(self):
        try:
            h = int(input("Година заїзду (0-23): "))
            cap = int(input("Кількість місць: "))
            
            now = datetime.now()
            new_date = now.replace(hour=h, minute=0, second=0, microsecond=0)
            if new_date < now:
                new_date += timedelta(days=1)
                
            self.system.admin_add_session(new_date, cap)
        except ValueError:
            print("Помилка даних!")

# ЗАПУСК ПРОГРАМИ
if __name__ == "__main__":
    notification = ConsoleNotification()
    facade = KartingSystemFacade(notification)
    facade.users.append(Admin("admin", "admin@kart.com", "1111"))
    facade.users.append(User("user", "user@kart.com", "1234"))
    base_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    facade.sessions.append(RaceSession(base_time + timedelta(hours=1), 4))
    
    s2 = RaceSession(base_time + timedelta(hours=2), 2)
    s2.booked_count = 1
    facade.sessions.append(s2)
    facade.sessions.append(RaceSession(base_time + timedelta(hours=3), 6))
    menu = ConsoleMenu(facade)
    menu.run()