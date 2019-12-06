import sys
import json

yellowImage = "<img class=\"genesys-die-type-proficiency\" />"
greenImage = "<img class=\"genesys-die-type-ability\" />"
blueImage = "<img class=\"genesys-die-type-boost\" />"
blackImage = "<img class=\"genesys-die-type-setback\" />"

skills = {
	"Alchemy" : {
		"category" : "General",
		"characteristic" : "Intellect"
	},
	"Athletics" : {
		"category" : "General",
		"characteristic" : "Brawn"
	}
	,
	"Computers" : {
		"category" : "General",
		"characteristic" : "Intellect"
	},
	"Cool" : {
		"category" : "General",
		"characteristic" : "Presence"
	},
	"Coordination" : {
		"category" : "General",
		"characteristic" : "Agility"
	},
	"Discipline" : {
		"category" : "General",
		"characteristic" : "Willpower"
	},
	"Driving" : {
		"category" : "General",
		"characteristic" : "Agility"
	},
	"Medicine" : {
		"category" : "General",
		"characteristic" : "Intellect"
	},
	"Mechanics" : {
		"category" : "General",
		"characteristic" : "Intellect"
	},
	"Operating" : {
		"category" : "General",
		"characteristic" : "Intellect"
	},
	"Perception" : {
		"category" : "General",
		"characteristic" : "Cunning"
	},
	"Piloting" : {
		"category" : "General",
		"characteristic" : "Agility"
	},
	"Resilience" : {
		"category" : "General",
		"characteristic" : "Brawn"
	},
	"Skulduggery" : {
		"category" : "General",
		"characteristic" : "Cunning"
	},
	"Stealth" : {
		"category" : "General",
		"characteristic" : "Agility"
	},
	"Streetwise" : {
		"category" : "General",
		"characteristic" : "Cunning"
	},
	"Survival" : {
		"category" : "General",
		"characteristic" : "Cunning"
	},
	"Vigilance" : {
		"category" : "General",
		"characteristic" : "Willpower"
	},
	"Arcana" : {
		"category" : "Magic",
		"characteristic" : "Intellect"
	},
	"Divine" : {
		"category" : "Magic",
		"characteristic" : "Willpower"
	},
	"Primal" : {
		"category" : "Magic",
		"characteristic" : "Cunning"
	},
	"Brawl" : {
		"category" : "Combat",
		"characteristic" : "Brawn"
	},
	"Gunnery" : {
		"category" : "Combat",
		"characteristic" : "Agility"
	},
	"Melee" : {
		"category" : "Combat",
		"characteristic" : "Brawn"
	},
	"Ranged (Heavy)" : {
		"category" : "Combat",
		"characteristic" : "Agility"
	},
	"Ranged (Light)" : {
		"category" : "Combat",
		"characteristic" : "Agility"
	},
	"Charm" : {
		"category" : "Social",
		"characteristic" : "Presence"
	},
	"Coercion" : {
		"category" : "Social",
		"characteristic" : "Willpower"
	},
	"Deception" : {
		"category" : "Social",
		"characteristic" : "Cunning"
	},
	"Leadership" : {
		"category" : "Social",
		"characteristic" : "Presence"
	},
	"Negotiation" : {
		"category" : "Social",
		"characteristic" : "Presence"
	},
	"Knowledge" : {
		"category" : "General",
		"characteristic" : "Intellect"
	}
}

archetypes = {
	"AverageHuman" : {
		"StartingStats" : {
			"Brawn" : 2,
			"Agility" : 2,
			"Intellect" : 2,
			"Cunning" : 2,
			"Willpower" : 2,
			"Presence" : 2
		},
		"StartingTalents" : {
			"Ready for Anything"
		},
		"WoundThreshold" : 10,
		"StrainThreshold" : 10
	},
	"Laborer" : {
		"StartingStats" : {
			"Brawn" : 3,
			"Agility" : 2,
			"Intellect" : 2,
			"Cunning" : 2,
			"Willpower" : 1,
			"Presence" : 2	
		},
		"StartingSkills" : {
			"Athletics" : 1
		},
		"StartingTalents" : {
			"Tough as Nails"
		}
		,
		"WoundThreshold" : 12,
		"StrainThreshold" : 8
	},
	"Intellectual" : {
		"StartingStats" : {
			"Brawn" : 2,
			"Agility" : 1,
			"Intellect" : 3,
			"Cunning" : 2,
			"Willpower" : 2,
			"Presence" : 2	
		},
		"StartingSkills" : {
			"Knowledge" : 1
		},
		"StartingTalents" : {
			"Brilliant!"
		},
		"WoundThreshold" : 8,
		"StrainThreshold" : 12
	},
	"Aristocrat" : {
		"StartingStats" : {
			"Brawn" : 1,
			"Agility" : 2,
			"Intellect" : 2,
			"Cunning" : 2,
			"Willpower" : 2,
			"Presence" : 3
		},
		"StartingSkills" : {
			"Cool" : 1
		},
		"StartingTalents" : {
			"Forceful Personality"
		},
		"WoundThreshold" : 10,
		"StrainThreshold" : 10
	}
}

armor = {
	"riotArmor" : {
		"name" : "Riot Armor",
		"soak" : 2,
		"meleeDefense" : 0,
		"rangedDefense" : 0,
		"encum" : 3
	}, 
	"heavyJacket" : {
		"name" : "Heavy Jacket",
		"soak" : 1,
		"meleeDefense" : 0,
		"rangedDefense" : 0,
		"encum" : 1
	}, 
	"lightBodyArmor" : {
		"name" : "Light Body Armor",
		"soak" : 2,
		"meleeDefense" : 0,
		"rangedDefense" : 0,
		"encum" : 2
	}, 
	"durableClothing" : {
		"name" : "Durable Clothing",
		"soak" : 1,
		"meleeDefense" : 0,
		"rangedDefense" : 0,
		"encum" : 1
	}
}

weapons = {
	"knife" : {
		"name" : "Knife",
		"damage" : "+1",
		"crit" : "3",
		"range" : "Engaged",
		"skill" : "Melee",
		"encum" : "1",
		"qualities" : ""
	},
	"sniperRifle" : {
		"name" : "Sniper Rifle",
		"damage" : "9",
		"crit" : "2",
		"range" : "Extreme",
		"skill" : "Ranged (Heavy)",
		"encum" : "4",
		"qualities" : "Accurate 2, Limited Ammo 4, Pierce 2"
	},
	"rifle" : {
		"name" : "Rifle",
		"damage" : "8",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Ranged (Heavy)",
		"encum" : "4",
		"qualities" : "Accurate 1"
	},
	"huntingRifle" : {
		"name" : "Hunting Rifle",
		"damage" : "8",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Ranged (Heavy)",
		"encum" : "4",
		"qualities" : "Accurate 1, Limited Ammo 2"
	},
	"dagger" : {
		"name" : "Dagger",
		"damage" : "+2",
		"crit" : "3",
		"range" : "Engaged",
		"skill" : "Melee",
		"encum" : "1",
		"qualities" : "Accurate 1"
	},
	"collapsibleBaton" : {
		"name" : "Collapsible Baton",
		"damage" : "+2",
		"crit" : "3",
		"range" : "Engaged",
		"skill" : "Melee",
		"encum" : "1",
		"qualities" : ""
	},
	"bullpupCarbine" : {
		"name" : "Bullpup Carbine",
		"damage" : "7",
		"crit" : "3",
		"range" : "Medium",
		"skill" : "Ranged (Heavy)",
		"encum" : "3",
		"qualities" : "Accurate 1, Auto-Fire"
	},
	"fletcherPistol" : {
		"name" : "Fletchet Pistol",
		"damage" : "4",
		"crit" : "2",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "1",
		"qualities" : "Pierce 2, Vicious 2"
	},
	"heavyPistol" : {
		"name" : "Heavy Pistol",
		"damage" : "6",
		"crit" : "3",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "1",
		"qualities" : ""
	},
	"pistol" : {
		"name" : "Pistol",
		"damage" : "6",
		"crit" : "3",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "1",
		"qualities" : ""
	},
	"assaultCannon" : {
		"name" : "Assault Cannon",
		"damage" : "15",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Gunnery",
		"encum" : "6",
		"qualities" : "Auto-Fire , Cumbersome 4, Inaccurate 1, Pierce 3, Vicious 3"
	},
	"autoFletcher" : {
		"name" : "Auto-Fletcher",
		"damage" : "3",
		"crit" : "2",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "2",
		"qualities" : "Auto-Fire , Pierce 2, Vicious 2"
	},
	"lightPistol" : {
		"name" : "Light Pistol",
		"damage" : "5",
		"crit" : "4",
		"range" : "Short",
		"skill" : "Ranged (Light)",
		"encum" : "1",
		"qualities" : ""
	},
	"AssaultRifle" : {
		"name" : "Assault Rifle",
		"damage" : "8",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Ranged (Heavy)",
		"encum" : "4",
		"qualities" : "Auto-Fire"
	},
	"combatShotgun" : {
		"name" : "Combat Shotgun",
		"damage" : "8",
		"crit" : "3",
		"range" : "Short",
		"skill" : "Ranged (Heavy)",
		"encum" : "4",
		"qualities" : "Auto-Fire , Blast 5, Inaccurate 1, Vicious 2"
	},
	"revolver" : {
		"name" : "Revolver",
		"damage" : "6",
		"crit" : "4",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "2",
		"qualities" : "Accurate 1"
	},
	"shotgun" : {
		"name" : "Shotgun",
		"damage" : "8",
		"crit" : "3",
		"range" : "Short",
		"skill" : "Ranged (Heavy)",
		"encum" : "3",
		"qualities" : "Blast 5, Knockdown , Vicious 2"
	},
	"autoRotaryGun" : {
		"name" : "Auto-Rotary Gun",
		"damage" : "11",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Ranged (Heavy)",
		"encum" : "7",
		"qualities" : "Auto-Fire , Cumbersome 4, Prepare 1"
	},
	"handCannon" : {
		"name" : "Hand Cannon",
		"damage" : "7",
		"crit" : "3",
		"range" : "Medium",
		"skill" : "Ranged (Light)",
		"encum" : "1",
		"qualities" : "Inaccurate 1, Knockdown , Limited Ammo 2, Prepare 1"
	},
	"flechetteLauncher" : {
		"name" : "Flechette Launcher",
		"damage" : "4",
		"crit" : "2",
		"range" : "Medium",
		"skill" : "Ranged (Heavy)",
		"encum" : "3",
		"qualities" : "Blast 4, Pierce 2, Vicious 3"
	},
	"lightMachineGun" : {
		"name" : "Light Machine Gun",
		"damage" : "10",
		"crit" : "3",
		"range" : "Long",
		"skill" : "Gunnery",
		"encum" : "6",
		"qualities" : "Auto-Fire , Cumbersome 3, Pierce 2, Vicious 2"
	},
	"brassKnuckles" : {
		"name" : "Brass Knuckles",
		"damage" : "+1",
		"crit" : "4",
		"range" : "Engaged",
		"skill" : "Brawl",
		"encum" : "1",
		"qualities" : "Disorient 3"
	}
}

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
			training = character["masterSkills"][skill]["rank"]

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
			file.write("|" + key)
			file.write("|" + career)
			file.write("|" + str(ranks))
			file.write("|" + build_dice_pool(yellow, green, 0, 0) + "|\n")

def build_talent_block(character, rank) :
	talents = []
	result = ", "

	if "masterTalents" in character :
		for row in character["masterTalents"] :
			if str(rank) in character["masterTalents"][row] :
				talent = character["masterTalents"][row][str(rank)]
				if len(talent) > 0 :
					talents.append(talent)

	return result.join(talents)

def write_weapon_block(file, character, characteristics) :
	if "equipmentWeapons" in character :
		for ew in character["equipmentWeapons"] :
			w = weapons[character["equipmentWeapons"][ew]["id"]]

			ranks, yellow, green = calculate_skill(character, characteristics, w["skill"])
			blue, black = calculate_weapon_quality(w)

			file.write("|" + w["name"])
			file.write("|" + w["damage"])
			file.write("|" + w["crit"])
			file.write("|" + w["skill"])
			file.write("|" + w["encum"])
			file.write("|" + w["qualities"])
			file.write("|" + build_dice_pool(yellow, green, blue, black) + "|\n")

def write_armor_block(file, character) :
	if "equipmentArmor" in character :
		for ea in character["equipmentArmor"] :
			a = armor[character["equipmentArmor"][ea]["id"]]

			file.write("|" + a["name"])
			file.write("|" + str(a["soak"]))
			file.write("|" + str(a["meleeDefense"]))
			file.write("|" + str(a["rangedDefense"]))
			file.write("|" + str(a["encum"]) + "|\n")

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

	wounds = archetype["WoundThreshold"] + characteristics["Brawn"]
	strain = archetype["StrainThreshold"] + characteristics["Willpower"]
	soak = characteristics["Brawn"] + calculate_soak(character)
	meleeDefense, rangedDefense = calculate_defense(character)

	f = open(character["name"] + ".txt", "w")

	f.write("h2. Archetype\n\n")
	f.write(character["archetype"] + " " + character["career"] + "\n\n")

	f.write("h2. Attributes\n\n")
	f.write("|_Wounds_|_Strain_|_Soak Value_|_Melee Defense_|_Ranged Defense_|\n")
	f.write("|" + str(wounds) + "|" + str(strain) + "|" + str(soak) + "|" + str(meleeDefense) + "|" + str(rangedDefense) + "|\n\n")

	f.write("h2. Characteristics\n\n")
	f.write("|_Brawn_|_Agility_|_Intellect_|_Cunning_|_Willpower_|_Presence_|\n")
	f.write("|" + str(characteristics["Brawn"]))
	f.write("|" + str(characteristics["Agility"]))
	f.write("|" + str(characteristics["Intellect"]))
	f.write("|" + str(characteristics["Cunning"]))
	f.write("|" + str(characteristics["Willpower"]))
	f.write("|" + str(characteristics["Presence"]) + "|")
	f.write("\n\n")

	f.write("h3. Skills\n\n")
	f.write("|_Skill_|_Career_|_Rank_|_Dice Pool_|\n")
	f.write("|\\4=.*General*|\n")
	write_skill_block(f, character, characteristics, "General")
	f.write("|\\4=.*Combat*|\n")
	write_skill_block(f, character, characteristics, "Combat")
	f.write("|\\4=.*Social*|\n")
	write_skill_block(f, character, characteristics, "Social")
	f.write("|\\4=.*Magic*|\n")
	write_skill_block(f, character, characteristics, "Magic")
	f.write("\n")

	f.write("h3. Talents\n\n")
	f.write("|_Rank 1_|_Rank 2_|_Rank 3_|_Rank 4_|_Rank 5_|\n")
	f.write("|" + build_talent_block(character, 1))
	f.write("|" + build_talent_block(character, 2))
	f.write("|" + build_talent_block(character, 3))
	f.write("|" + build_talent_block(character, 4))
	f.write("|" + build_talent_block(character, 5) + "|")
	f.write("\n\n")

	f.write("h3. Weapons\n\n")
	f.write("|_Weapon_|_Dam_|_Crit_|_Range_|_Skill_|_Encum_|_Qualities_|_Dice Pool_|\n")
	write_weapon_block(f, character, characteristics)
	f.write("\n\n")

	f.write("h3. Armor\n\n")
	f.write("|_Armor_|_Soak_|_Melee Def_|_Ranged Def_|_Encum_|\n")
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