from typing import Dict, List, Optional
from utils.helpers import calculate_csr, calculate_crr
from team.buttons import get_live_score_button


class ScorecardGenerator:
    """Generate scorecard displays for matches"""
    
    @staticmethod
    def generate_full_scorecard(match_data: Dict) -> str:
        """Generate complete scorecard for the match"""
        
        team_a = match_data.get("team_a", {})
        team_b = match_data.get("team_b", {})
        host = match_data.get("host", {}).get("username", "Unknown")
        total_overs = match_data.get("total_overs", 10)
        batting_team = match_data.get("batting_team", "A")
        bowling_team = match_data.get("bowling_team", "B")
        current_innings = match_data.get("current_innings", 1)
        
        # Team A batting display
        team_a_batsmen = ScorecardGenerator._get_batsmen_display(team_a)
        team_a_bowlers = ScorecardGenerator._get_bowlers_display(team_a)
        
        # Team B batting display
        team_b_batsmen = ScorecardGenerator._get_batsmen_display(team_b)
        team_b_bowlers = ScorecardGenerator._get_bowlers_display(team_b)
        
        # Calculate CRR
        team_a_crr = calculate_crr(team_a.get("score", 0), team_a.get("overs", 0))
        team_b_crr = calculate_crr(team_b.get("score", 0), team_b.get("overs", 0))
        
        scorecard = f"""
╭━─━─━─━─≪✠≫─━─━─━─━╮

───────⊱ Tᴇᴀᴍ - A ⊰──────
{team_a_batsmen}
╭──────── • ◆ • ─────────
ᴛᴇᴀᴍ A sᴄᴏʀᴇ = {team_a.get('score', 0)}/{team_a.get('wickets', 0)} ʀᴜɴs | ᴏᴠᴇʀs: {team_a.get('overs', 0)}
╰──────── • ◆ • ─────────

× •-•-•-•-•-••-•-•⟮ 🏏 ⟯•-•-•-•-•-•-•-•-• ×

───────⊱ Tᴇᴀᴍ - B ⊰──────
{team_b_batsmen}
╭──────── • ◆ • ─────────
ᴛᴇᴀᴍ B sᴄᴏʀᴇ = {team_b.get('score', 0)}/{team_b.get('wickets', 0)} ʀᴜɴs | ᴏᴠᴇʀs: {team_b.get('overs', 0)}
╰──────── • ◆ • ─────────

༺═────────────────═༻

👑Host: {host}
"""
        return scorecard
    
    @staticmethod
    def generate_live_scorecard(match_data: Dict) -> str:
        """Generate live scorecard (simpler version for during match)"""
        
        team_a = match_data.get("team_a", {})
        team_b = match_data.get("team_b", {})
        host = match_data.get("host", {}).get("username", "Unknown")
        total_overs = match_data.get("total_overs", 10)
        batting_team = match_data.get("batting_team", "A")
        bowling_team = match_data.get("bowling_team", "B")
        
        # Get current batsmen
        current_batsmen = match_data.get("current_batsmen", [])
        current_bowler = match_data.get("current_bowler", {})
        
        # Batting team display
        batting_team_data = team_a if batting_team == "A" else team_b
        bowling_team_data = team_b if batting_team == "A" else team_a
        
        batsmen_display = ""
        for batsman in current_batsmen:
            csr = calculate_csr(batsman.get("runs", 0), batsman.get("balls", 0))
            batsmen_display += f"\n🏏 {batsman.get('username')} = {batsman.get('runs', 0)}({batsman.get('balls', 0)})\n╰⊚(𝗖𝗦𝗥: {csr})"
        
        # Bowler display
        bowler = current_bowler
        balls_bowled = bowler.get("balls_bowled", [])
        bowler_display = f"\n⚾ {bowler.get('username')}\n╰⊚ ({', '.join(balls_bowled)})"
        
        # Calculate CRR
        batting_crr = calculate_crr(batting_team_data.get("score", 0), batting_team_data.get("overs", 0))
        bowling_crr = calculate_crr(bowling_team_data.get("score", 0), bowling_team_data.get("overs", 0))
        
        live_scorecard = f"""
╾ ⏳ 𝗧𝗼𝘁𝗮𝗹 𝗢𝘃𝗲𝗿𝘀: {total_overs}
╾ 📯 𝗛𝗼𝘀𝘁: {host}
────┈┄┄╌╌╌╌┄┄┈────
𝗕𝗮𝘁𝘁𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {batting_team}
{batsmen_display}
────┈┄┄╌╌╌╌┄┄┈────
𝗕𝗼𝘄𝗹𝗶𝗻𝗴 𝗧𝗲𝗮𝗺 - {bowling_team}
{bowler_display}
────┈┄┄╌╌╌╌┄┄┈────
👥 𝗧𝗲𝗮𝗺 - A: {team_a.get('score', 0)}/{team_a.get('wickets', 0)} | {team_a.get('overs', 0)} ov
╰⊚ 𝗖𝗥𝗥: {team_a_crr}
⊱⋅ ──────────── ⋅⊰
👥 𝗧𝗲𝗮𝗺 - B: {team_b.get('score', 0)}/{team_b.get('wickets', 0)} | {team_b.get('overs', 0)} ov
╰⊚ 𝗖𝗥𝗥: {team_b_crr}
────┈┄┄╌╌╌╌┄┄┈────
"""
        return live_scorecard
    
    @staticmethod
    def _get_batsmen_display(team: Dict) -> str:
        """Get batsmen display for team"""
        players = team.get("players", [])
        if not players:
            return "No batsmen yet.\n"
        
        display = ""
        for player in players:
            if player.get("is_out", False):
                display += f"\n✴️ {player.get('username')} = {player.get('runs', 0)}({player.get('balls', 0)}) 🏏 OUT"
            else:
                display += f"\n✴️ {player.get('username')} = {player.get('runs', 0)}({player.get('balls', 0)})"
            display += f"\n  ╰⊚ ID : {player.get('user_id')}"
            
            ball_by_ball = player.get("ball_by_ball", [])
            if ball_by_ball:
                display += f"\n    ╰⊚ ({', '.join(ball_by_ball)})"
        
        return display
    
    @staticmethod
    def _get_bowlers_display(team: Dict) -> str:
        """Get bowlers display for team"""
        players = team.get("players", [])
        display = ""
        for player in players:
            balls_bowled = player.get("balls_bowled", [])
            if balls_bowled:
                wickets = player.get("wickets", 0)
                runs = player.get("runs_conceded", 0)
                display += f"\n⚾ {player.get('username')} - {runs}/{wickets}\n╰⊚ ({', '.join(balls_bowled)})"
        return display if display else "No bowling figures yet.\n"
    
    @staticmethod
    async def send_scorecard(client, chat_id: int, match_data: Dict, is_live: bool = True):
        """Send scorecard to chat"""
        if is_live:
            scorecard = ScorecardGenerator.generate_live_scorecard(match_data)
        else:
            scorecard = ScorecardGenerator.generate_full_scorecard(match_data)
        
        await client.send_message(
            chat_id=chat_id,
            text=scorecard,
            reply_markup=get_live_score_button()
        )
    
    @staticmethod
    def generate_over_summary(match_data: Dict, over_number: int, over_balls: List[Dict]) -> str:
        """Generate summary of a completed over"""
        batting_team = match_data.get("batting_team", "A")
        team_data = match_data.get(f"team_{batting_team.lower()}", {})
        
        runs_in_over = sum([ball.get("runs", 0) for ball in over_balls if isinstance(ball.get("runs"), int)])
        wickets_in_over = len([ball for ball in over_balls if ball.get("result") == "wicket"])
        
        ball_results = []
        for ball in over_balls:
            if ball.get("result") == "wicket":
                ball_results.append("W")
            else:
                ball_results.append(str(ball.get("runs", 0)))
        
        summary = f"""
📊 **Over {over_number} Summary**

Team {batting_team}: {runs_in_over}/{wickets_in_over} runs in this over
Ball by ball: {', '.join(ball_results)}

Current Score: {team_data.get('score', 0)}/{team_data.get('wickets', 0)}
"""
        return summary


# ========== SINGLETON INSTANCE ==========
scorecard_gen = ScorecardGenerator()
