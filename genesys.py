import sys
import json

yellowImage = "<img class=\"genesys-die-type-proficiency\" />"
greenImage = "<img class=\"genesys-die-type-ability\" />"

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

def build_dice_pool(yellow, green) :
	result = ""
	for y in range(yellow) :
		result = result + yellowImage
	for g in range(green) :
		result = result + greenImage
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
			file.write("|" + build_dice_pool(yellow, green) + "|\n")

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
	soak = characteristics["Brawn"]
	rangedDefense = 0
	meleeDefense = 0

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