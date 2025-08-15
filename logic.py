from random import randint
import time
import requests

class Pokemon:
    pokemons = {}

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = randint(50, 100)
        self.power = randint(20, 40)
        self.coins = 0
        self.cooldowntime = 0
        self.cdtime = 0
        self.iscooldown = False
        self.iscd = False

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.pokemon_number}.png"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            with open(f"pokemon_{self.pokemon_number}.png", "wb") as file:
                file.write(data)
                return f"pokemon_{self.pokemon_number}.png"



    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
    
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            self.coins -= 10
            enemy.coins += 10
            return f"Сражение @{self.pokemon_trainer} ({self.hp} hp) с @{enemy.pokemon_trainer} ({enemy.hp} hp)"
        else:
            enemy.hp = 0
            self.coins += 10
            enemy.coins -= 10
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "
        

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name}, у него {self.hp} здоровья, его сила {self.power}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    def heal(self):
        if self.iscooldown == False:
            self.hp += 20
            self.iscooldown = True
            self.cooldowntime = 30
            for i in range(30):
                time.sleep(1)
                self.cooldowntime -= 1
            self.iscooldown = False
        else:
            return f"Осталось {self.cooldowntime}s"
    

            
    
class Wizard(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = randint(80, 110)
        
        
    def info(self):
        return f"Имя твоего покемона: {self.name}, у него {self.hp} здоровья, его сила {self.power}, он волшебник"
    
    def heal(self):
        if self.iscooldown == False:
            self.hp += 40
            self.iscooldown = True
            self.cooldowntime = 30
            for i in range(30):
                time.sleep(1)
                self.cooldowntime -= 1
            self.iscooldown = False
        else:
            return f"Осталось {self.cooldowntime}s"


class Fighter(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power = randint(30, 50)

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой:{super_power} "
    
    def info(self):
        return f"Имя твоего покемона: {self.name}, у него {self.hp} здоровья, его сила {self.power}, он боец"
        
