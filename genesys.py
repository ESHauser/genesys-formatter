import sys
import json
import data.skills
import data.weapons
import data.armor
import data.archetypes

yellowImage = "<img class=\"genesys-die-type-proficiency\" />"
greenImage = "<img class=\"genesys-die-type-ability\" />"
blueImage = "<img class=\"genesys-die-type-boost\" />"
blackImage = "<img class=\"genesys-die-type-setback\" />"

skills = data.skills.getFlattenedSkills()
weapons = data.weapons.weapons
armor = data.armor.armor
archetypes = data.archetypes.archetypes

def build_table_row(*args, **kwargs):
	str_args = [""] + [str(x) for x in args] + [""]
	return "|".join(str_args) + "\n" + kwargs.get("postfix", "")

def calculate_skill(character, characteristics, skill) :
	archetype = archetypes[character["archetype"]]

	starting = 0
	career = 0
	special = 0
	training = 0

	stat = characteristics[skills[skill]["characteristic"]]

	if "StartingSkills" in archetype :
		if(skill in archetype["StartingSkills"]) :
			starting = archetype["StartingSkills"][skill]

	if(skill in character["careerSkillsRank"]):
		career = 1

	if(skill in character["archetypeSpecialSkills"]):
		special = character["archetypeSpecialSkills"][skill]["rank"]

	if("masterSkills" in character) :
		if(skill in character["masterSkills"]):
			training += character["masterSkills"][skill].get("rank", 0)
			training += character["masterSkills"][skill].get("careerRank", 0)

	ranks = starting + career + special + training

	if ranks > stat :
		return ranks, stat, ranks - stat
	else :
		return ranks, ranks, stat - ranks

def calculate_weapon_quality(weapon) :
	blue = 0
	black = 0
	qualities = weapon["qualities"].split(",")
	for q in qualities :
		tokens = q.split(" ")
		if q.startswith("Accurate") :
			blue = int(tokens[len(tokens)-1])
		if q.startswith("Inaccurate") :
			black = int(tokens[len(tokens)-1])

	return blue, black

def build_dice_pool(yellow, green, blue, black) :
	result = ""
	for y in range(yellow) :
		result = result + yellowImage
	for g in range(green) :
		result = result + greenImage
	for u in range(blue) :
		result = result + blueImage
	for b in range(black) :
		result = result + blackImage		
	return result

def write_skill_block(file, character, characteristics, category) :
	keys = sorted(skills.keys())

	for key in keys :
		skill = skills[key]
		career = ""
		if key in character["careerSkillsRank"] :
			career = "Yes"
		ranks, yellow, green = calculate_skill(character, characteristics, key)

		if(skill["category"] == category) :
			row = build_table_row(key, career, ranks, build_dice_pool(yellow, green, 0, 0))
			file.write(row)

def build_talent_block(talent, rank) :
	return "|" + talent

def write_talent_row(file, character, row) :
	if "masterTalents" in character :
		if str(row) in character["masterTalents"] :
			section = character["masterTalents"][str(row)]
			for rank in range(1, 6) :
				if str(rank) in section :
					talent = section[str(rank)]
					if(len(talent) > 0) :
						file.write(build_talent_block(talent, rank))
					else :
						file.write("|")
				else :
					file.write("|")
		file.write("|\n")


def write_weapon_block(file, character, characteristics) :
	if "equipmentWeapons" in character :
		for ew in character["equipmentWeapons"] :
			w = weapons[character["equipmentWeapons"][ew]["id"]]

			ranks, yellow, green = calculate_skill(character, characteristics, w["skill"])
			blue, black = calculate_weapon_quality(w)

			row = build_table_row(w["name"], w["damage"], w["crit"], w["skill"], w["range"],
				w["encum"], w["qualities"], build_dice_pool(yellow, green, blue, black))
			file.write(row)

def write_armor_block(file, character) :
	if "equipmentArmor" in character :
		for ea in character["equipmentArmor"] :
			a = armor[character["equipmentArmor"][ea]["id"]]

			row = build_table_row(a["name"], a["soak"], a["meleeDefense"], a["rangedDefense"], a["encum"])
			file.write(row)

def calculate_soak(character) :
	if "equipmentArmor" in character :
		for a in character["equipmentArmor"] :
			if character["equipmentArmor"][a]["equipped"] :
				return armor[character["equipmentArmor"][a]["id"]]["soak"]

	return 0

def calculate_defense(character) :
	if "equipmentArmor" in character :
		for a in character["equipmentArmor"] :
			if character["equipmentArmor"][a]["equipped"] :
				return armor[character["equipmentArmor"][a]["id"]]["meleeDefense"], armor[character["equipmentArmor"][a]["id"]]["rangedDefense"]

	return 0, 0

def write_character(character) :
	print(character["name"])
	creationCharacteristics = character["creationCharacteristics"]
	archetype = archetypes[character["archetype"]]

	characteristics = {
		"Brawn" : archetype["StartingStats"]["Brawn"] + creationCharacteristics["Brawn"],
		"Agility" : archetype["StartingStats"]["Agility"] + creationCharacteristics["Agility"],
		"Intellect" : archetype["StartingStats"]["Intellect"] + creationCharacteristics["Intellect"],
		"Cunning" : archetype["StartingStats"]["Cunning"] + creationCharacteristics["Cunning"],
		"Willpower" : archetype["StartingStats"]["Willpower"] + creationCharacteristics["Willpower"],
		"Presence" : archetype["StartingStats"]["Presence"] + creationCharacteristics["Presence"]
	}

	talentRows = 0
	if "masterTalents" in character :
		talentRows = len(character["masterTalents"].keys()) - 1

	wounds = archetype["WoundThreshold"] + characteristics["Brawn"]
	strain = archetype["StrainThreshold"] + characteristics["Willpower"]
	soak = characteristics["Brawn"] + calculate_soak(character)
	meleeDefense, rangedDefense = calculate_defense(character)

	f = open(character["name"] + ".txt", "w")

	f.write("h3. Archetype\n\n")
	f.write(character["archetype"] + " " + character["career"] + "\n\n")

	f.write("h3. Attributes\n\n")
	f.write(build_table_row("_Wounds_","_Strain_", "_Soak Value_","_Melee Defense_","_Ranged Defense_"))
	f.write(build_table_row(wounds, strain, soak, meleeDefense, rangedDefense, postfix="\n"))

	f.write("h3. Characteristics\n\n")
	f.write(build_table_row("_Brawn_", "_Agility_", "_Intellect_", "_Cunning_", "_Willpower_", "_Presence_"))
	f.write(build_table_row(characteristics["Brawn"], characteristics["Agility"], characteristics["Intellect"], 
				characteristics["Cunning"], characteristics["Willpower"], characteristics["Presence"], postfix="\n"))

	f.write("h3. Skills\n\n")
	f.write(build_table_row("_Skill_", "_Career_", "_Rank_", "_Dice Pool_"))
	f.write(build_table_row("\\4=.*General*"))
	write_skill_block(f, character, characteristics, "General")
	f.write(build_table_row("\\4=.*Combat*"))
	write_skill_block(f, character, characteristics, "Combat")
	f.write(build_table_row("\\4=.*Social*"))
	write_skill_block(f, character, characteristics, "Social")
	f.write(build_table_row("\\4=.*Magic*"))
	write_skill_block(f, character, characteristics, "Magic")
	f.write("\n")

	f.write("h3. Talents\n\n")
	f.write(build_table_row("_Rank 1_", "_Rank 2_", "_Rank 3_", "_Rank 4_", "_Rank 5_") )
	for row in range(1, talentRows + 1) :
		write_talent_row(f, character, row)

	f.write("h3. Weapons\n\n")
	f.write(build_table_row("_Weapon_", "_Dam_", "_Crit_", "_Range_", "_Skill_", "_Encum_", "_Qualities_", "_Dice Pool_"))
	write_weapon_block(f, character, characteristics)
	f.write("\n\n")

	f.write("h3. Armor\n\n")
	f.write(build_table_row("_Armor_", "_Soak_", "_Melee Def_", "_Ranged Def_", "_Encum_"))
	write_armor_block(f, character)

	f.close()

if len(sys.argv) != 2: 
	print("usage: genesys.py [filename]")
	exit()

file = sys.argv[1]
print("Designated filename = %s" % (file))

with open(file) as json_file:
	data = json.load(json_file)
	characters = data["characters"]
	for character in characters:
		write_character(character)