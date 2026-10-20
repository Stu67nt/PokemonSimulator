from poke_env.data import GenData
from poke_env.player import Player
from poke_env.calc import damage_calc_gen9 as calc_gen9
from poke_env.stats import compute_raw_stats
import random

class BattleAgent(Player):
	def choose_move(self, battle):

		user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
		opponent_pokemon_id = battle.opponent_active_pokemon.identifier(battle.opponent_role)
		gen = GenData.from_gen(9)

		opponent_pokemon_out = battle.opponent_active_pokemon
		opponent_stats = compute_raw_stats(opponent_pokemon_out.species,
										   [85, 85, 85, 85, 85, 85],
										   [31, 31, 31, 31, 31, 31],
										   level = opponent_pokemon_out.level,
										   nature="quirky",
										   data = gen)
		opponent_pokemon_out.stats = {
			'atk': opponent_stats[1],
			'def': opponent_stats[2],
			'hp': opponent_stats[0],
			'spa': opponent_stats[3],
			'spd': opponent_stats[4],
			'spe': opponent_stats[5]
		}
		max_dmg = 0
		selected_move = None
		if battle.available_moves:
			for battle_move in battle.available_moves:
				tested_dmg = calc_gen9.calculate_damage(user_pokemon_id, opponent_pokemon_id, battle_move, battle)[0]
				if tested_dmg > max_dmg:
					max_dmg = tested_dmg
					selected_move = battle_move
			return self.create_order(selected_move)
		elif battle.available_switches:
			return self.create_order(random.choice(battle.available_switches))
		else:
			return self.choose_random_move(battle)
