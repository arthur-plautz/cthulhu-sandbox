import pandas as pd
from random import randint

class Base:
    def __init__(self, name) -> None:
        self.name = name
        self._initial()

    def _roll(self, dice=6, times=1):
        roll_sum = 0
        for _ in range(times):
            roll_sum += randint(1, dice)
        return roll_sum

    def _pure_rolls(self):
        rolls = self._roll(times=3)
        return rolls * 5

    def _based_rolls(self):
        rolls = self._roll(times=2)
        return (rolls + 6) * 5

    def _initial(self):
        self.force = self._pure_rolls()
        self.constitution = self._pure_rolls()
        self.size = self._based_rolls()
        self.dexterity = self._pure_rolls()
        self.intelligence = self._based_rolls()
        self.power = self._pure_rolls()
        self.appearance = self._pure_rolls()
        self.luck = self._pure_rolls()
        self.knowledge = self._pure_rolls()
        self.education = self._pure_rolls()
        self.hp = (self.force + self.constitution) // 10

    @property
    def force(self):
        return self._force
    
    @force.setter
    def force(self, force):
        self._force = force

    @property
    def intelligence(self):
        return self._intelligence
    
    @intelligence.setter
    def intelligence(self, intelligence):
        self._intelligence = intelligence

    @property
    def constitution(self):
        return self._constitution
    
    @constitution.setter
    def constitution(self, constitution):
        self._constitution = constitution

    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, power):
        self._power = power

    @property
    def luck(self):
        return self._luck
    
    @luck.setter
    def luck(self, luck):
        self._luck = luck

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size

    @property
    def dexterity(self):
        return self._dexterity
    
    @dexterity.setter
    def dexterity(self, dexterity):
        self._dexterity = dexterity

    @property
    def knowledge(self):
        return self._knowledge
    
    @knowledge.setter
    def knowledge(self, knowledge):
        self._knowledge = knowledge

    @property
    def education(self):
        return self._education
    
    @education.setter
    def education(self, education):
        self._education = education

    @property
    def appearance(self):
        return self._appearance
    
    @appearance.setter
    def appearance(self, appearance):
        self._appearance = appearance

    @property
    def age(self):
        return self._age

    @property
    def moving_rate(self):
        if self.dexterity < self.size and self.force < self.size:
            moving_rate = 7
        elif self.dexterity >= self.size or self.force >= self.size:
            moving_rate = 8
        elif self.dexterity > self.size and self.force > self.size:
            moving_rate = 9
        
        if self.age > 80:
            return moving_rate - 5
        elif self.age > 70:
            return moving_rate - 4
        elif self.age > 60:
            return moving_rate - 3
        elif self.age > 50:
            return moving_rate - 2
        elif self.age > 40:
            return moving_rate - 1
        else:
            return moving_rate

    def attribute_test(self, attribute):
        roll = self._roll(100)
        value = getattr(self, attribute)
        return roll < value, abs(roll-value)

    def education_modifier(self, times=1):
        for _ in range(times):
            passed, _ = self.attribute_test('education')
            print(passed)
            if passed:
                bonus = self._roll(10)
                self.education += bonus
                if self.education >= 100:
                    self.education = 99

    def age_modifier(self, age, force=1, size=1, dexterity=1):
        dist = lambda points, attr: points*attr % points
        if age > 15 and age <= 19:
            self.force -= dist(5, force) // 2
            self.size -= dist(5, size) // 2
            self.education -= 5
            luck = self._pure_rolls()
            self.luck = luck if luck >= self.luck else self.luck
        if age > 20 and age <= 39:
            self.education_modifier()
        if age > 40 and age <= 49:
            self.appearance -= 5
            if force > size and force > dexterity:
                self.force -= 5
            if size > force and size > dexterity:
                self.size -= 5
            if dexterity > force and dexterity > size:
                self.dexterity -= 5
            self.education_modifier(2)
        if age > 50 and age <= 59:
            self.force -= dist(10, force) // 3
            self.size -= dist(10, size) // 3
            self.dexterity -= dist(10, dexterity) // 3
            self.appearance -= 10
            self.education_modifier(3)
        if age > 60 and age <= 69:
            self.force -= dist(20, force) // 3
            self.size -= dist(20, size) // 3
            self.dexterity -= dist(20, dexterity) // 3
            self.appearance -= 15
            self.education_modifier(4)
        if age > 70 and age <= 79:
            self.force -= dist(40, force) // 3
            self.size -= dist(40, size) // 3
            self.dexterity -= dist(40, dexterity) // 3
            self.appearance -= 20
            self.education_modifier(4)
        if age > 80 and age <= 89:
            self.force -= dist(80, force) // 3
            self.size -= dist(80, size) // 3
            self.dexterity -= dist(80, dexterity) // 3
            self.appearance -= 25
            self.education_modifier(4)
        self._age = age

    def save(self):
        serialized = dict(
            name=self.name,
            force=self.force,
            intelligence=self.intelligence,
            constitution=self.constitution,
            power=self.power,
            luck=self.luck,
            size=self.size,
            dexterity=self.dexterity,
            knowledge=self.knowledge,
            education=self.education,
            appearance=self.appearance,
            age=self.age,
            moving_rate=self.moving_rate,
            hp=self.hp
        )
        df = pd.DataFrame([serialized])
        df.to_json(f"data/{self.name}.json", orient="index")
