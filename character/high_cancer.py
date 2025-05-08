from base import BaseChar

class Wolf(BaseChar) :
    def __init__(self,health_poin,deffend,demage) :
        super().__init__(health_poin,deffend,demage)
        self.set_name("nigger")
    
    def attack(self):
        pass
    def guard(self):
        pass
    def skill(self):
        pass


Wolf = Wolf(400, 0, 21)
print(Wolf.get_name())
