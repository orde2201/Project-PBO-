from base import BaseChar

class Slime(BaseChar) :
    def __init__(self,health_poin,deffend,demage) :
        super().__init__(health_poin,deffend,demage)
        self.set_name("nigger")
    
    def attack(self):
        pass
    def guard(self):
        pass
    def skill(self):
        pass


player = Slime(100, 0, 1)
print(player.get_name())
