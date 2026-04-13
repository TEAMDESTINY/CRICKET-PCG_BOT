from typing import Tuple

def validate_batting_number(num: str) -> Tuple[bool, any]:
    """Validate batting number (0,1,2,3,4,6,OUT)"""
    valid = ["0", "1", "2", "3", "4", "6", "OUT", "out", "wicket", "W"]
    if num.upper() == "OUT" or num.upper() == "W":
        return True, "OUT"
    if num in valid:
        return True, int(num)
    return False, None

def validate_bowling_number(num: str) -> Tuple[bool, int]:
    """Validate bowling number (1-6)"""
    try:
        num_int = int(num)
        if 1 <= num_int <= 6:
            return True, num_int
    except:
        pass
    return False, None

def is_valid_player_number(num: str, max_players: int = 11) -> Tuple[bool, int]:
    """Validate player number (1-11)"""
    try:
        num_int = int(num)
        if 1 <= num_int <= max_players:
            return True, num_int
    except:
        pass
    return False, None
