
# Dataset Interface
from abc import ABC, abstractmethod
import pandas as pd

class LegalDataset(ABC):
    
    def __init__(self) -> None:
        self._df = pd.DataFrame()
    
    def get_df(self):
        return self._df



# Dataset Concrete 
    
class CaseDataset(LegalDataset):
    pass
    
class NewsDataset():
    pass
    
class LawDataset():
    pass
    
class BlogDataset():
    pass