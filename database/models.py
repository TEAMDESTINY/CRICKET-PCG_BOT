from datetime import datetime
from typing import List, Optional, Dict

class Player:
    def __init__(self, number: int, username: str, user_id: int, is_captain: bool = False):
        self.number = number
        self.username = username
        self.user_id = user_id
        self.mention = f"[{username}](tg://user?id={user_id})"
        self.is_captain = is_captain
        self.runs = 0
        self.balls = 0
        self.fours = 0
        self.sixes = 0
        self.is_out = False
        self.ball_by_ball = []  # List of runs or 'W'
    
    def to_dict(self):
        return {
            "number": self.number,
            "username": self.username,
            "user_id": self.user_id,
            "mention": self.mention,
            "is_captain": self.is_captain,
            "runs": self.runs,
            "balls": self.balls,
            "fours": self.fours,
            "sixes": self.sixes,
            "is_out": self.is_out,
            "ball_by_ball": self.ball_by_ball
        }

class Team:
    def __init__(self, name: str):
        self.name = name
        self.players: List[Player] = []
        self.score = 0
        self.wickets = 0
        self.overs = 0.0
        self.current_batsman: Optional[Player] = None
        self.current_bowler: Optional[Player] = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "players": [p.to_dict() for p in self.players],
            "score": self.score,
            "wickets": self.wickets,
            "overs": self.overs
        }

class Match:
    def __init__(self, group_id: int, host_id: int, host_name: str, total_overs: int = 10):
        self.group_id = group_id
        self.host = {"user_id": host_id, "username": host_name}
        self.total_overs = total_overs
        self.status = "waiting"  # waiting, toss, inning1, inning2, completed
        self.current_innings = 1
        self.target = None
        self.team_a = Team("Team A")
        self.team_b = Team("Team B")
        self.batting_team = None
        self.bowling_team = None
        self.ball_count = 0
        self.over_count = 0
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "group_id": self.group_id,
            "host": self.host,
            "total_overs": self.total_overs,
            "status": self.status,
            "current_innings": self.current_innings,
            "target": self.target,
            "team_a": self.team_a.to_dict(),
            "team_b": self.team_b.to_dict(),
            "batting_team": self.batting_team,
            "bowling_team": self.bowling_team,
            "ball_count": self.ball_count,
            "over_count": self.over_count,
            "created_at": self.created_at
        }
