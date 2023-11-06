from enum import Enum

class GameState(Enum):
    
    INITIATING = 0
    WAITING_FOR_START = 1
    START = 2
    PLAYING = 3
    SCREAMER = 4
    END = 5