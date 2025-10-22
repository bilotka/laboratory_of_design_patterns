#Клас Messenger містить метод Надіслати повідомлення (отримувач,текст). Реалізувати непомітно 
# для користувача підрахунок надісланих повідомлень. Також повідомляти поліцію, якщо повідомлення містить слово «війна»
# Я думаю, що тут підходить шаблон Декоратор
class Messenger:
    def send_message(self, receiver, text):
        print(f"Повідомлення для {receiver}: {text}")

class MessengerDecorator:
    def __init__(self, messenger):
        self._messenger = messenger
        self._count = 0

    def send_message(self, receiver, text):
        self._count += 1
        if "війна" in text.lower():
            print("Повідомлення поліції: знайдено слово 'війна'!")
        self._messenger.send_message(receiver, text)

    def get_count(self):
        return self._count

# Приклад використання
def test_decorator() -> None:
    base = Messenger()
    secure_messenger = MessengerDecorator(base)

    secure_messenger.send_message("Настя", "Привіт, як справи?")
    secure_messenger.send_message("Олександр", "Почалась війна на сході!")
    secure_messenger.send_message("Олексій", "Добрий день!")

    print(f"Кількість повідомлень: {secure_messenger.get_count()}")

if __name__ == "__main__":
     test_decorator()


