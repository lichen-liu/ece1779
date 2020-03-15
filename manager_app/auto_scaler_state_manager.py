from enum import Enum
from datetime import datetime, timedelta
class ScalerState(Enum):
    READYTORESIZE = 0
    RESIZING = 1
    RESIZINGCOOLDOWN = 2

class ScalerStateManager:
    def __init__(self, auto_scaler, monitor_helper):
        # Time stamps
        self._resizing_start_timestamp = datetime(1970, 1, 1, 0, 0)
        self._resizing_timeout = timedelta(seconds = 120) 
        self._resizing_complete_timestamp = datetime(1970, 1, 1, 0, 0)
        self._cooldown_interval = timedelta(seconds = 100) 
        self._latest_cpu_utilization_timestamp = datetime(1970, 1, 1, 0, 0)
        # State
        self._state = ScalerState.READYTORESIZE
        # Helper objects
        self._scaler = auto_scaler
        self._monitor_helper = monitor_helper
    
    def try_scale_pool_and_update_state(self):
        if self._state == ScalerState.READYTORESIZE :
            resized = self._scaler.resize_pool()
            if resized :
                self.update_resizing_start_timestamp()
                self._state = ScalerState.RESIZING

        elif self._state == ScalerState.RESIZING :
            if self.is_resizing_finished() :
                self.update_resizing_complete_timestamp()
                self._latest_cpu_utilization_timestamp = self._monitor_helper.get_current_cpu_utilization_timestamp()
                self._state = ScalerState.RESIZINGCOOLDOWN

        else:
            if self.is_cooldown_complete() :
                self._state = ScalerState.READYTORESIZE

    def is_resizing_finished(self):

        # If resizing has timeout
        if(self._resizing_start_timestamp + self._resizing_timeout < datetime.now()):
            return True
        # If desired pool size has been reached
        if(self._scaler.desired_worker_num_reached()):
            return True
        return False

    def is_cooldown_complete(self):

        # If minimum cooldown has passed
        if(self._resizing_complete_timestamp + self._cooldown_interval < datetime.now()):
            return True
        # If latest Cpu info is updated, we can do another resizing
        if(self._monitor_helper.get_current_cpu_utilization_timestamp() > self._latest_cpu_utilization_timestamp):
            return True
        return False  

    def update_resizing_start_timestamp(self):
        self._resizing_start_timestamp = datetime.now()

    def update_resizing_complete_timestamp(self):
        self._resizing_complete_timestamp = datetime.now()
        
           

        
