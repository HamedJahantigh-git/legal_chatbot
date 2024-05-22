import numpy as np
class CaseIrText():
    
    def __init__(self,
                 reference_matrix: np.array, 
                 candidate_matrix: np.array) -> None:
        self._ref = reference_matrix
        self._can = candidate_matrix
        
    def number_score(self, margin: int) -> int:
        ref_sorted_indices = np.argsort(-self._ref)[:,1:margin]
        can_sorted_indices = np.argsort(-self._can)[:,1:margin]
        accept_item = []
        for i in range(len(self._can)):
            if any(item in can_sorted_indices[i] for item in ref_sorted_indices[i]):
                accept_item.append(i)
        accept_percent = 100*len(accept_item)/len(self._can)
        return f"{accept_percent:.2f}"
    
            