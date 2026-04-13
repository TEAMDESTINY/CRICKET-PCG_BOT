def calculate_csr(runs: int, balls: int) -> int:
    """Calculate Cricket Strike Rate"""
    if balls == 0:
        return 0
    return int((runs / balls) * 100)

def calculate_crr(score: int, overs: float) -> float:
    """Calculate Current Run Rate"""
    if overs == 0:
        return 0.00
    return round(score / overs, 2)

def get_mention(user_id: int, name: str) -> str:
    """Get clickable mention"""
    return f"[{name}](tg://user?id={user_id})"

def format_overs(balls: int) -> float:
    """Convert balls to overs format (e.g., 7 balls = 1.1 overs)"""
    overs = balls // 6
    remaining_balls = balls % 6
    return float(f"{overs}.{remaining_balls}")
