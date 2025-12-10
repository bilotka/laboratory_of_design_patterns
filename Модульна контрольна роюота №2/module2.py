#14.Реалізувати систему моделювання поведінки ворогів у комп’ютерній грі. Усі вони виконують однакову послідовність: пошук цілі, 
# наближення, удар та відступ. Загальна структура алгоритму повинна бути визначена в базовому класі, а конкретний спосіб визначатись в дочірніх (наприклад: деякі вороги
#повинні наблизиться до цілі щільно, і атакувати її кулаком, а інші – наблизитис на певну відстань і здійснити постріл).
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

class IEnemyActions(Protocol):
    def approach(self) -> None: ...
    def hit(self) -> None: ...
    def retreat(self) -> None: ...
class Enemy(ABC):

    def perform_combat_cycle(self, target_name: str):

        print("-" * 30)
        print(f"[{self.__class__.__name__}]: Початок бойового циклу.")
        
        self._search_target(target_name)
        
        self._approach()
        
        self._attack()
        
        self._retreat()
        
        print(f"[{self.__class__.__name__}]: Бойовий цикл завершено.")



    def _search_target(self, target: str):

        print(f"   [Пошук]: Виявлено ціль: {target}.")

    @abstractmethod
    def _approach(self) -> None: ...

    @abstractmethod
    def _attack(self) -> None: ...


    @abstractmethod
    def _retreat(self) -> None: ...


class Enemy1(Enemy):

    def _approach(self)-> None:
        print("   [Наближення]: Швидко наближається до цілі впритул.")

    def _attack(self)-> None:
        print("   [Удар]: Здійснює потужний удар кулаком.")

    def _retreat(self)-> None:
        print("   [Відступ]: Повільно відходить на один крок.")

class Enemy2(Enemy):

    def _approach(self)-> None:
        print("   [Наближення]: Наближається на безпечну відстань (10 метрів) і займає позицію.")

    def _attack(self)-> None:
        print("   [Удар]: Здійснює серію пострілів по цілі.")

    def _retreat(self)-> None:
        print("   [Відступ]: Стрімко відступає, шукаючи нове укриття.")


# Приклад використання
if __name__ == "__main__":
    player = "Головний Герой"

    enemy_1 = Enemy1()
    enemy_1.perform_combat_cycle(player)

    enemy_2 = Enemy2()
    enemy_2.perform_combat_cycle(player)
