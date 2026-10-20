import asyncio

from poke_env.data import GenData
from poke_env.player import SimpleHeuristicsPlayer
from poke_env.player import MaxBasePowerPlayer
from battle_agent import BattleAgent


async def main():
    player_1 = SimpleHeuristicsPlayer(max_concurrent_battles=4)
    player_2 = BattleAgent(max_concurrent_battles=4)

    await player_1.battle_against(player_2, n_battles=40)

    print(f"Finished battles: {player_1.n_finished_battles}")
    print(f"Player 1 wins: {player_1.n_won_battles}")


if __name__ == "__main__":
    asyncio.run(main())