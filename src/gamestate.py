from enum import Enum

class GameState(Enum):
    
    INITIATING = 0
    WAITING_FOR_HISTORY = 1
    HISTORY = 2
    WAITING_FOR_CHARACTER = 3
    CHARACTER = 4
    WAITING_FOR_START = 5
    START = 6
    PLAYING = 7
    SCREAMER = 8
    END = 9
    CREDITS = 10