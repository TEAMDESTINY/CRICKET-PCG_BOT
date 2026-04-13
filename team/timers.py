import asyncio
from typing import Optional, Callable, Dict, Any
from datetime import datetime
from pyrogram.types import Message


class GameTimer:
    """Timer manager for bowler and batter responses"""
    
    def __init__(self, timeout_seconds: int = 60):
        self.timeout_seconds = timeout_seconds
        self.active_timers: Dict[str, asyncio.Task] = {}
        self.warning_30_sent: Dict[str, bool] = {}
        self.warning_10_sent: Dict[str, bool] = {}
    
    async def start_bowler_timer(
        self,
        bowler_id: int,
        bowler_name: str,
        on_timeout: Callable,
        on_warning_30: Optional[Callable] = None,
        on_warning_10: Optional[Callable] = None
    ):
        """Start timer for bowler response"""
        timer_key = f"bowler_{bowler_id}"
        
        # Cancel existing timer if any
        await self.cancel_timer(timer_key)
        
        self.warning_30_sent[timer_key] = False
        self.warning_10_sent[timer_key] = False
        
        async def timer_task():
            # 30 seconds warning
            await asyncio.sleep(30)
            if not self.warning_30_sent.get(timer_key, False):
                self.warning_30_sent[timer_key] = True
                if on_warning_30:
                    await on_warning_30(bowler_name)
            
            # 10 seconds warning
            await asyncio.sleep(20)
            if not self.warning_10_sent.get(timer_key, False):
                self.warning_10_sent[timer_key] = True
                if on_warning_10:
                    await on_warning_10(bowler_name)
            
            # Timeout
            await asyncio.sleep(10)
            await on_timeout(bowler_name)
            
            # Cleanup
            self.active_timers.pop(timer_key, None)
            self.warning_30_sent.pop(timer_key, None)
            self.warning_10_sent.pop(timer_key, None)
        
        task = asyncio.create_task(timer_task())
        self.active_timers[timer_key] = task
        return task
    
    async def start_batter_timer(
        self,
        batter_id: int,
        batter_name: str,
        on_timeout: Callable,
        on_warning_30: Optional[Callable] = None,
        on_warning_10: Optional[Callable] = None
    ):
        """Start timer for batter response"""
        timer_key = f"batter_{batter_id}"
        
        # Cancel existing timer if any
        await self.cancel_timer(timer_key)
        
        self.warning_30_sent[timer_key] = False
        self.warning_10_sent[timer_key] = False
        
        async def timer_task():
            # 30 seconds warning
            await asyncio.sleep(30)
            if not self.warning_30_sent.get(timer_key, False):
                self.warning_30_sent[timer_key] = True
                if on_warning_30:
                    await on_warning_30(batter_name)
            
            # 10 seconds warning
            await asyncio.sleep(20)
            if not self.warning_10_sent.get(timer_key, False):
                self.warning_10_sent[timer_key] = True
                if on_warning_10:
                    await on_warning_10(batter_name)
            
            # Timeout
            await asyncio.sleep(10)
            await on_timeout(batter_name)
            
            # Cleanup
            self.active_timers.pop(timer_key, None)
            self.warning_30_sent.pop(timer_key, None)
            self.warning_10_sent.pop(timer_key, None)
        
        task = asyncio.create_task(timer_task())
        self.active_timers[timer_key] = task
        return task
    
    async def cancel_timer(self, timer_key: str):
        """Cancel an active timer"""
        if timer_key in self.active_timers:
            self.active_timers[timer_key].cancel()
            self.active_timers.pop(timer_key, None)
            self.warning_30_sent.pop(timer_key, None)
            self.warning_10_sent.pop(timer_key, None)
    
    async def cancel_bowler_timer(self, bowler_id: int):
        """Cancel bowler timer"""
        await self.cancel_timer(f"bowler_{bowler_id}")
    
    async def cancel_batter_timer(self, batter_id: int):
        """Cancel batter timer"""
        await self.cancel_timer(f"batter_{batter_id}")
    
    def is_timer_active(self, timer_key: str) -> bool:
        """Check if timer is active"""
        return timer_key in self.active_timers


# Timer warning messages
async def send_bowler_warning_30(bowler_name: str, client, chat_id: int):
    """Send 30 seconds warning to bowler in DM"""
    from team.messages import get_timer_warning_30
    await client.send_message(
        chat_id=chat_id,
        text=get_timer_warning_30(bowler_name, "bowling")
    )


async def send_bowler_warning_10(bowler_name: str, client, chat_id: int):
    """Send 10 seconds warning to bowler in DM"""
    from team.messages import get_timer_warning_10
    await client.send_message(
        chat_id=chat_id,
        text=get_timer_warning_10(bowler_name, "bowling")
    )


async def send_bowler_timeout(bowler_name: str, client, chat_id: int, group_id: int):
    """Handle bowler timeout"""
    from team.messages import TIMEOUT_BOWLER
    
    await client.send_message(
        chat_id=chat_id,
        text=TIMEOUT_BOWLER.format(bowler_name=bowler_name)
    )
    
    # Also notify in group
    await client.send_message(
        chat_id=group_id,
        text=f"⏰ Bowler {bowler_name} didn't respond in time! Random number will be generated."
    )


async def send_batter_warning_30(batter_name: str, client, group_id: int):
    """Send 30 seconds warning to batter in group"""
    from team.messages import get_timer_warning_30
    await client.send_message(
        chat_id=group_id,
        text=get_timer_warning_30(batter_name, "batting")
    )


async def send_batter_warning_10(batter_name: str, client, group_id: int):
    """Send 10 seconds warning to batter in group"""
    from team.messages import get_timer_warning_10
    await client.send_message(
        chat_id=group_id,
        text=get_timer_warning_10(batter_name, "batting")
    )


async def send_batter_timeout(batter_name: str, client, group_id: int):
    """Handle batter timeout"""
    from team.messages import TIMEOUT_BATTER
    
    await client.send_message(
        chat_id=group_id,
        text=TIMEOUT_BATTER.format(batter_name=batter_name)
    )


# Global timer instance
game_timer = GameTimer(timeout_seconds=60)
