class AutoScaler:
    def __init__(self):
        self._max_threshold = 0.8
        self._min_threshold = 0.5
        self._growing_ratio = 1.5
        self._shrinking_ratio = 0.5

    def set_max_threshold(self, threshold):
        self._max_threshold = threshold
    
    def set_min_threshold(self, threshold):
        self._min_threshold = threshold

    def set_growing_ratio(self, ratio):
        self._growing_ratio = ratio
    
    def set_shrinking_ratio(self, ratio):
        self._shrinking_ratio = ratio

    def get_max_threshold(self):
        return self._max_threshold 
    
    def get_min_threshold(self):
        return self._min_threshold 

    def get_growing_ratio(self):
        return self._growing_ratio 
    
    def get_shrinking_ratio(self):
        return self._shrinking_ratio 
    
auto_scaler = AutoScaler()
def get_auto_scaler():
    return auto_scaler