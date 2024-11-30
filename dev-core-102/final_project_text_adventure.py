import random
import time


class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):
    def __init__(self, name, damage):
        super().__init__(name)
        self.damage = damage


class Armor(Item):
    def __init__(self, name, defense):
        super().__init__(name)
        self.defense = defense


class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.armor = None

    def take_damage(self, amount):
        self.health -= amount
        self.health = max(self.health, 0)  # Здоровье не может быть меньше 0
        print(f"{self.name} получает {amount} урона и теперь имеет {self.health} здоровья.")

    def attack(self, target):
        base_damage = random.randint(self.attack_power - 5, self.attack_power + 5)
        base_damage = max(base_damage, 0)  # Урон не может быть отрицательным

        if random.random() <= 0.05:  # 5% шанс критического удара
            base_damage *= 2
            print(f"Критический удар! {self.name} наносит удвоенный урон!")

        if target.armor:
            base_damage -= target.armor.defense
            base_damage = max(base_damage, 0)

        print(f"{self.name} атакует {target.name} и наносит {base_damage} урона.")
        target.take_damage(base_damage)


class Player(Character):
    def __init__(self, name, health, attack_power):
        super().__init__(name, health, attack_power)
        self.inventory = [Item("Зелье лечения")]
        self.weapon = None
        self.armor = None

    def equip_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            self.weapon = weapon
            self.attack_power += weapon.damage
            print(f"{self.name} экипировал {weapon.name} с уроном {weapon.damage}.")

    def equip_armor(self, armor):
        if isinstance(armor, Armor):
            self.armor = armor
            print(f"{self.name} экипировал {armor.name} с защитой {armor.defense}.")

    def use_health_potion(self):
        potion = next((item for item in self.inventory if item.name == "Зелье лечения"), None)
        if potion:
            self.health += 40
            self.inventory.remove(potion)
            print(f"{self.name} использовал зелье лечения и восстановил 30 здоровья. Теперь у него {self.health} здоровья.")
        else:
            print("У вас нет зелий лечения!")

    def interact_with_inventory(self):
        print("Ваш инвентарь:")
        for i, item in enumerate(self.inventory, start=1):
            print(f"{i}. {item.name}")
        print("\nВыберите предмет для взаимодействия (введите номер или 0 для выхода):")
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return
            if 1 <= choice <= len(self.inventory):
                selected_item = self.inventory[choice - 1]
                if isinstance(selected_item, Weapon):
                    self.equip_weapon(selected_item)
                    self.inventory.pop(choice - 1)
                elif isinstance(selected_item, Armor):
                    self.equip_armor(selected_item)
                    self.inventory.pop(choice - 1)
                elif selected_item.name == "Зелье лечения":
                    self.use_health_potion()
                else:
                    print(f"Невозможно использовать {selected_item.name}.")
            else:
                print("Неверный выбор.")
        else:
            print("Введите корректное число.")


def generate_enemy(wave):
    names = ["Гоблин", "Орк", "Тролль", "Разбойник", "Убийца"]
    name = random.choice(names)
    health = 50 + wave * 10 + random.randint(-5, 5)
    attack_power = 10 + wave * 2 + random.randint(-2, 2)
    return Character(name, health, attack_power)


def generate_loot():#Генерация лута
    if random.randint(1, 100) <= 51:  # 51% шанс на зелье лечения
        return Item("Зелье лечения")
    elif random.randint(1, 100) <= 30:  # 30% шанс на уникальное оружие
        return Weapon("Ржавый железный меч", 14)
    elif random.randint(1,100) <= 30:
        return Armor("Кожанная броня", 12)
    elif random.randint(1,100) <= 2:
        return Armor("Доспехи бога", 200)
    elif random.randint(1,100) <= 2:
        return Weapon("Экскалибур", 200)
    elif random.randint(1,100) <= 25:
        return Armor("Доспехи гладиатора", 15)
    elif random.randint(1,100) <= 25:
        return Weapon("Хороший железный меч", 17)
    elif random.randint(1,100) <= 10:
        return Armor("Доспехи паладина", 18)
    elif random.randint(1,100) <= 10:
        return Armor("Двуручный меч паладина", 30)            
    return None


def attack_action(player, enemy):
    player.attack(enemy)
    if enemy.health > 0:
        enemy.attack(player)


def defend_action(player, enemy):#Функция "Ухода в защиту" с 40% вероятностью на контратаку
    print(f"{player.name} переходит в защиту, снижая урон от следующей атаки врага.")
    original_attack_power = enemy.attack_power  # Сохранить исходное значение атаки врага
    reduced_damage = max(0, enemy.attack_power - 5)
    enemy.attack_power = reduced_damage

    # Контратака
    if random.random() <= 0.4:  # 40% шанс на контратаку
        counter_damage = random.randint(player.attack_power - 5, player.attack_power + 5)
        counter_damage = max(counter_damage, 0)
        print(f"*** {player.name} контратакует! ***")
        print(f"{player.name} наносит {counter_damage} урона {enemy.name}.")
        enemy.take_damage(counter_damage)

    # Атака врага после уменьшения урона
    enemy.attack(player)
    enemy.attack_power = original_attack_power  # Восстановить исходное значение атаки врага

def type_writer(text, delay=0.05):# Функция для вывода сообщения побуквенно

    for char in text:
        print(char, end='', flush=True)  # Выводим символ без переноса строки
        time.sleep(delay)  # Пауза между символами
    print()  # Переход на новую строку после окончания текста



def final_battle(player, enemy):
    type_writer(f"\nОкровавленный и обессиленный {enemy.name} падает на колени.")
    time.sleep(1)
    type_writer("Диктатор поднимается со своего места, удивленный тем, что его лучший гладиатор приближается к смерти.")
    time.sleep(2)
    type_writer("1) Бросить оружие и отказаться драться на арене снова\n"
          "2) Убить гладиатора и стать чемпионом арены\n"
          "3) Убить гладиатора и бросить оружие в диктатора.")
    choice = input("Ваш выбор: ")
    if choice == "1":
        type_writer("Вы бросили оружие. Толпа возмущенно кричит. Диктатор смотрит на начальника своей охраны \n \
        и проводит пальцем у горла. Охрана окружает вас и казнит. Конец игры.")
    elif choice == "2":
        type_writer("Вы убиваете гладиатора самым жестоким образом, даже зрители которые отдали золото\n \
             за это зрелище затихли. Вы - чемпион арены. Вы продолжаете сражаться, пока однажды не погибаете.")
    elif choice == "3":
        time.sleep(1)
        type_writer("Вы убиваете гладиатора, совершаете прыжок отталкиваясь от его тела, бросаете оружие в диктатора и пронзаете его сердце. Конец игры.")
    else:
        print("Некорректный ввод!Введите 1,2 или 3")
        final_battle(player,enemy)

def start_game():
    player = Player("Герой", 100, 15)
    type_writer("Вы пробуждаетесь из-за громких криков кровожадной толпы\n \
        оглядевшись вы понимаете что находитесь на гладиаторской арене.\n \
        Вам предстоит выживать в схватках.Удачи!")
    for wave in range(1, 11):
        type_writer(f"\nВолна {wave}: Появляется новый враг!")
        enemy = generate_enemy(wave)
        type_writer(f"Противник: {enemy.name} с {enemy.health} здоровья и атакой {enemy.attack_power}.")
        
        while player.health > 0 and enemy.health > 0:
            print("\n1) Атаковать\n2) Уйти в защиту\n3) Использовать зелье лечения\n4) Проверить инвентарь")
            action = input("Выберите действие: ")
            if action == "1":
                attack_action(player, enemy)
            elif action == "2":
                defend_action(player, enemy)
            elif action == "3":
                player.use_health_potion()
            elif action == "4":
                player.interact_with_inventory()
            else:
                print("Неверный выбор.")
            
            if enemy.health <= 0:
                print(f"Вы победили {enemy.name}!")
                loot = generate_loot()
                if loot:
                    player.inventory.append(loot)
                    print(f"{loot.name} добавлено в ваш инвентарь.")
                break

            if player.health <= 0:
                type_writer("Вы погибли. Игра окончена.")
                return

        if wave == 10 and player.health > 0:
            final_battle(player, enemy)
            return


# Запуск игры
start_game()
