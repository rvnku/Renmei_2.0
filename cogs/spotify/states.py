from dataclasses import dataclass
from subprocess import Popen
from typing import Optional
import os


@dataclass
class PlayerInfo:
    guild_id: int
    user_id: int
    process: Popen
    path: str
    active: bool = True


def get_player(players, guild_id: int) -> Optional[PlayerInfo]:
    return next((player for player in players if player.guild_id == guild_id), None)

def remove_player(players, guild_id: int):
    if (idx := next((idx for idx, player in enumerate(players) if player.guild_id == guild_id), None)) is not None:
        players.pop(idx)

def cleanup_player(players, guild_id: int):
    if not (player := get_player(players, guild_id)):
        return
    if player.process and player.process.poll() is None:
        player.process.terminate()
        try:
            player.process.wait(timeout=5)
        except: pass
    if player.path and os.path.exists(player.path):
        os.unlink(player.path)
    remove_player(players, guild_id)
