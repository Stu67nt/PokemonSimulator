from poke_env.data import GenData
from poke_env.player import Player
from poke_env.calc import damage_calc_gen9 as calc_gen9
from poke_env.stats import compute_raw_stats
from poke_env.battle import pokemon_type
import random
import json


"""
This bot is a very limited and rudementry bot which odes not try predict any switches
It is optimised for gen 9 randoms.
"""
class BattleAgent(Player):

	def __init__(self):
		super().__init__(max_concurrent_battles=2)
		self.opponent_team = {}

	def choose_move(self, battle):
		if battle.battle_tag not in self.opponent_team:
			self.opponent_team[battle.battle_tag] = {}

		# Getting ids
		user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
		opponent_pokemon_id = battle.opponent_active_pokemon.identifier(battle.opponent_role)

		self.add_opponent_pokemon(battle)
		# Not currently in use
		# opponent_pokemon_out = self.calc_opponent_stats(battle)


		if battle.available_moves:
			selected_attack = self.best_attack(battle)
		elif battle.available_switches:
			selected_switch = self.best_switch(battle)
		return self.choose_random_move(battle)

	def best_attack(self, battle):
		# Initalising vars
		max_dmg = 0
		selected_move = None
		user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
		opponent_pokemon_id = battle.opponent_active_pokemon.identifier(battle.opponent_role)

		# Checking if we have any avaliable moves
		if battle.available_moves:
			# Only 1 avaliable option lmao
			if len(battle.available_moves) == 1:
				return battle.available_moves[0]

			# Calcing dmg for each avaliable move
			for battle_move in battle.available_moves:
				# Assuming low roll
				tested_dmg = calc_gen9.calculate_damage(user_pokemon_id, opponent_pokemon_id, battle_move, battle)[0]
				if tested_dmg > max_dmg:
					max_dmg = tested_dmg
					selected_move = battle_move

			if selected_move == None:
				# No valid move found
				# Should not trigger unless I am a dofus
				return random.choice(battle.available_moves)
			else:
				return selected_move

	def best_switch(self, battle):
		opponent_name = battle.opponent_active_pokemon.base_species

		# Defaults to a random choice
		return random.choice(battle.available_switches)

	def calc_opponent_stats(self, battle):
		gen = GenData.from_gen(9)

		opponent_pokemon_out = battle.opponent_active_pokemon
		opponent_stats = compute_raw_stats(opponent_pokemon_out.species,
										   [85, 85, 85, 85, 85, 85],
										   [31, 31, 31, 31, 31, 31],
										   level=opponent_pokemon_out.level,
										   nature="quirky",
										   data=gen)
		opponent_pokemon_out.stats = {
			'atk': opponent_stats[1],
			'def': opponent_stats[2],
			'hp': opponent_stats[0],
			'spa': opponent_stats[3],
			'spd': opponent_stats[4],
			'spe': opponent_stats[5]
		}
		return opponent_pokemon_out

	def add_opponent_pokemon(self, battle):
		battle_tag = battle.battle_tag
		opposing_pokemon_out = battle.opponent_active_pokemon
		opponent_name = opposing_pokemon_out.base_species
		with open("data/sets.json", "r") as f:
			all_sets = json.load(f)
			if opponent_name not in self.opponent_team:
				self.opponent_team[battle_tag][opponent_name] = all_sets[opponent_name]