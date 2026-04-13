from typing import Tuple, Optional, Dict, Any
from datetime import datetime
from utils.helpers import calculate_csr, calculate_crr, format_overs


class GameEngine:
    """Core game engine for cricket match simulation"""
    
    @staticmethod
    def compare_ball(batter_number, bowler_number) -> Tuple[str, any]:
        """
        Compare batter and bowler numbers
        Returns: (result_type, value)
        result_type: "runs", "wicket"
        """
        # Same number = OUT
        if batter_number == bowler_number:
            return "wicket", None
        
        # Different number = runs to batter
        if isinstance(batter_number, int):
            return "runs", batter_number
        
        # If batter selected OUT button
        if batter_number == "OUT":
            return "wicket", None
        
        return "runs", 0
    
    @staticmethod
    def update_score_on_run(current_score: int, runs: int) -> int:
        """Update score after runs"""
        return current_score + runs
    
    @staticmethod
    def update_score_on_wicket(current_wickets: int) -> int:
        """Update wickets after wicket"""
        return current_wickets + 1
    
    @staticmethod
    def update_batsman_stats(batsman: Dict, runs: int, ball_number: int = 1):
        """Update batsman's personal stats"""
        if runs == "OUT" or runs == "wicket":
            # Batsman is out - don't add runs
            batsman["balls"] += ball_number
            batsman["ball_by_ball"].append("W")
            batsman["is_out"] = True
        else:
            # Add runs
            batsman["runs"] += runs
            batsman["balls"] += ball_number
            batsman["ball_by_ball"].append(str(runs))
            
            # Count fours and sixes
            if runs == 4:
                batsman["fours"] = batsman.get("fours", 0) + 1
            elif runs == 6:
                batsman["sixes"] = batsman.get("sixes", 0) + 1
        
        return batsman
    
    @staticmethod
    def update_bowler_stats(bowler: Dict, runs: int, wicket: bool = False):
        """Update bowler's personal stats"""
        if wicket:
            bowler["wickets"] = bowler.get("wickets", 0) + 1
            bowler["balls_bowled"].append("W")
        else:
            bowler["runs_conceded"] = bowler.get("runs_conceded", 0) + runs
            bowler["balls_bowled"].append(str(runs))
        
        return bowler
    
    @staticmethod
    def update_team_score(team: Dict, runs: int = 0, wicket: bool = False) -> Dict:
        """Update team's total score and wickets"""
        if wicket:
            team["wickets"] += 1
        else:
            team["score"] += runs
        
        return team
    
    @staticmethod
    def update_overs(ball_count: int, over_count: int) -> Tuple[int, int, float]:
        """Update overs after each ball"""
        ball_count += 1
        
        if ball_count >= 6:
            # Over complete
            over_count += 1
            ball_count = 0
        
        overs_display = format_overs((over_count * 6) + ball_count)
        
        return ball_count, over_count, overs_display
    
    @staticmethod
    def is_over_complete(ball_count: int) -> bool:
        """Check if over is complete"""
        return ball_count >= 6
    
    @staticmethod
    def is_innings_complete(team: Dict, total_overs: int, over_count: int, ball_count: int) -> bool:
        """Check if innings is complete"""
        # All out
        if team["wickets"] >= len(team.get("players", [])):
            return True
        
        # Overs completed
        if over_count >= total_overs and ball_count == 0:
            return True
        
        # Last over completed
        if over_count == total_overs - 1 and ball_count >= 6:
            return True
        
        return False
    
    @staticmethod
    def is_match_complete(innings: int, team_a: Dict, team_b: Dict, total_overs: int, 
                          over_count: int, ball_count: int, target: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """Check if match is complete and who won"""
        
        if innings == 1:
            return False, None
        
        # Second innings - check if target reached
        batting_team = team_b if innings == 2 else team_a
        bowling_team = team_a if innings == 2 else team_b
        
        if target is not None and batting_team["score"] >= target:
            return True, "batting_team_won"
        
        # Check if batting team all out
        if batting_team["wickets"] >= len(batting_team.get("players", [])):
            return True, "bowling_team_won"
        
        # Check if overs completed
        if over_count >= total_overs and ball_count == 0:
            if batting_team["score"] > bowling_team["score"]:
                return True, "batting_team_won"
            elif batting_team["score"] < bowling_team["score"]:
                return True, "bowling_team_won"
            else:
                return True, "tie"
        
        return False, None
    
    @staticmethod
    def calculate_target(team_score: int) -> int:
        """Calculate target for second innings"""
        return team_score + 1
    
    @staticmethod
    def get_required_runs(target: int, current_score: int) -> int:
        """Get runs needed to win"""
        return target - current_score
    
    @staticmethod
    def get_balls_remaining(over_count: int, ball_count: int, total_overs: int) -> int:
        """Get remaining balls in innings"""
        total_balls = total_overs * 6
        current_balls = (over_count * 6) + ball_count
        return total_balls - current_balls
    
    @staticmethod
    def get_current_run_rate(team_score: int, over_count: int, ball_count: int) -> float:
        """Get current run rate"""
        total_overs_played = over_count + (ball_count / 6)
        return calculate_crr(team_score, total_overs_played)
    
    @staticmethod
    def get_required_run_rate(target: int, current_score: int, over_count: int, ball_count: int, total_overs: int) -> float:
        """Get required run rate for second innings"""
        runs_needed = target - current_score
        balls_remaining = GameEngine.get_balls_remaining(over_count, ball_count, total_overs)
        overs_remaining = balls_remaining / 6
        
        if overs_remaining <= 0:
            return 0
        
        return round(runs_needed / overs_remaining, 2)
    
    @staticmethod
    def get_batting_order(team_players: list, current_batsman_index: int = 0) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Get striker and non-striker batsmen"""
        if not team_players:
            return None, None
        
        # Filter out out players
        active_players = [p for p in team_players if not p.get("is_out", False)]
        
        if len(active_players) == 0:
            return None, None
        
        if len(active_players) == 1:
            return active_players[0], None
        
        # Striker at current index, non-striker at next index
        striker = active_players[current_batsman_index % len(active_players)]
        non_striker = active_players[(current_batsman_index + 1) % len(active_players)]
        
        return striker, non_striker
    
    @staticmethod
    def swap_batsmen(striker: Dict, non_striker: Dict) -> Tuple[Dict, Dict]:
        """Swap striker and non-striker after odd runs"""
        return non_striker, striker
    
    @staticmethod
    def get_next_batsman(team_players: list, current_index: int) -> Optional[Dict]:
        """Get next batsman after wicket"""
        active_players = [p for p in team_players if not p.get("is_out", False)]
        
        if len(active_players) <= current_index + 1:
            return None
        
        return active_players[current_index + 1]
    
    @staticmethod
    def calculate_csr_from_dict(batsman: Dict) -> int:
        """Calculate CSR from batsman dict"""
        return calculate_csr(batsman.get("runs", 0), batsman.get("balls", 0))
    
    @staticmethod
    def create_ball_result(batter_num: any, bowler_num: int, runs: any, 
                           score: int, wickets: int, over_count: int, ball_count: int,
                           batsman_name: str, response_time: int = 0) -> Dict:
        """Create ball result dictionary"""
        overs_display = format_overs((over_count * 6) + ball_count)
        
        if runs == "OUT" or runs == "wicket":
            return {
                "type": "wicket",
                "message": f"🎯 **WICKET!** 🎯\n\n🏏 {batsman_name}\n📊 Score: {score}/{wickets} ({overs_display} ov)\n⏱️ {response_time}ms",
                "score": score,
                "wickets": wickets,
                "runs": 0
            }
        elif runs == 6:
            return {
                "type": "six",
                "message": f"🎯 **SIX!** 🚀\n\n🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}\n📊 Score: {score}/{wickets} ({overs_display} ov)\n⏱️ {response_time}ms",
                "score": score,
                "wickets": wickets,
                "runs": runs
            }
        elif runs == 4:
            return {
                "type": "four",
                "message": f"🎯 **FOUR!** 💥\n\n🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}\n📊 Score: {score}/{wickets} ({overs_display} ov)\n⏱️ {response_time}ms",
                "score": score,
                "wickets": wickets,
                "runs": runs
            }
        else:
            return {
                "type": "run",
                "message": f"🏏 **{runs} RUN{'S' if runs > 1 else ''}!**\n\n🏏 Batter: {batter_num} | 🎯 Bowler: {bowler_num}\n📊 Score: {score}/{wickets} ({overs_display} ov)\n⏱️ {response_time}ms",
                "score": score,
                "wickets": wickets,
                "runs": runs
            }


# ========== SINGLETON INSTANCE ==========
game_engine = GameEngine()
