from abc import ABC, abstractmethod

class BaseChar(ABC):
    def __init__(self,health_poin,defend,demage):
        self.__name = ""
        self.health_poin=health_poin
        self.defend=defend
        self.demage=demage
        self._level=1

    def get_name(self):
        return self.__name ,self.health_poin, self.deffend,self.demage
       
    def set_name(self,name) :
        self.__name = name
        

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def guard(self) :
        pass

    @abstractmethod
    def skill(self) :
        pass
    

