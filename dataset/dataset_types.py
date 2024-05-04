
# Dataset Interface
from abc import ABC, abstractmethod

class LegalDataset(ABC):
    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass



# Dataset Concrete 
    
class CaseDataset():
    pass
    
class NewsDataset():
    pass
    
class LawDataset():
    pass
    
class BlogDataset():
    pass