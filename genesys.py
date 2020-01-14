import sys
import json
import data.skills
import data.weapons
import data.armor
import data.archetypes
import data.talents
import data.careers

yellowImage = "<img class=\"genesys-die-type-proficiency\" />"
greenImage = "<img class=\"genesys-die-type-ability\" />"
blueImage = "<img class=\"genesys-die-type-boost\" />"
blackImage = "<img class=\"genesys-die-type-setback\" />"
successImage = "<img class=\"genesys-die-result-success\" />"
failureImage = "<img class=\"genesys-die-result-failure\" />"
advantageImage = "<img class=\"genesys-die-result-advantage\" />"
difficultyImage = "<img class=\"genesys-die-type-difficulty\" />"

skills = data.skills.getFlattenedSkills()
weapons = data.weapons.weapons
armor = data.armor.armor
archetypes = data.archetypes.archetypes
talents = data.talents.talents
careers = data.careers.careers

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
	career = careers[character["career"]]
	keys = sorted(skills.keys())

	for key in keys :
		skill = skills[key]
		isCareer = ""
		if key in career["careerSkills"] :
			isCareer = "Yes"
		ranks, yellow, green = calculate_skill(character, characteristics, key)
		wiki = skill["wiki"]

		if(skill["category"] == category) :
			row = build_table_row(wiki, isCareer, ranks, build_dice_pool(yellow, green, 0, 0))
			file.write(row)

def write_vital_stats(file, description):
	d = description
	file.write("h3. Vital Statistics\n\n")
	file.write(build_table_row("_Age_", "_Gender_", "_Height_", "_Build_", "_Eyes_", "_Hair_"))
	file.write(build_table_row(
		d.get("age", "Unknown"),
		d.get("gender", "Unknown"),
		d.get("height", "Unknown"),
		d.get("build", "Unknown"),
		d.get("eyes", "Unknown"),
		d.get("hair", "Unknown")))

def write_notes_block(file, description) :
	if "notes" in description :
		file.write("h3. Notes\n\n")
		file.write(description["notes"] + "\n\n")

def apply_tags(text) :
	result = text.replace("[BOOST]", blueImage)
	result = result.replace("[SETBACK]", blackImage)
	result = result.replace("[SUCCESS]", successImage)
	result = result.replace("[FAILURE]", failureImage)
	result = result.replace("[ADVANTAGE]", advantageImage)
	result = result.replace("[DIFFICULTY]", difficultyImage)
	return result

def write_talent_block(file, talent) :

	if talent in talents :
		t = talents[talent]
	else :
		t = {
			"name" : talent,
			"activation" : "?",
			"ranked" : "?",
			"description" : "Talent not found see the [[Talent List | Talent List]]",
			"wiki" : talent
		}

	file.write("<td class=\"genesys-talent-block\">")
	file.write("<div>")

	# talent name
	file.write("<div class=\"genesys-talent-header\">")
	file.write("<p class=\"genesys-talent-header-link\"><b>" + t["wiki"] + "</b></p>")
	file.write("</div>")

	# talent details
	file.write("<div class=\"genesys-talent-detail\">")
	file.write("<p class=\"genesys-talent-detail-text\">")
	file.write("<b>Activation:</b> " + t["activation"] + "<br>")
	file.write("<b>Ranked:</b> " + t["ranked"] + "<br>")
	file.write(apply_tags(t["description"]))
	file.write("</p>")
	file.write("</div>")

	file.write("</div>")
	file.write("</td>\n")

def write_talent_row(file, character, row) :
	if "masterTalents" in character :
		if str(row) in character["masterTalents"] :
			file.write("<tr class=\"genesys-talent-row\">")
			section = character["masterTalents"][str(row)]
			for rank in range(1, 6) :
				if str(rank) in section :
					talent = section[str(rank)]
					if(len(talent) > 0) :
						write_talent_block(file, talent)

			file.write("</tr>\n")

def write_talent_table(file, character) :

	talentRows = 0
	if "masterTalents" in character :
		talentRows = len(character["masterTalents"].keys())

	file.write("<table>\n")
	file.write("<tr>\n")
	for rank in range(1, 6) :
		file.write("<td class=\"genesys-talent-column\"><em>Rank " + str(rank) + "</em></td>")
	file.write("</tr>")

	for row in range(1, talentRows) :
		write_talent_row(file, character, row)

	file.write("</table>\n\n")

def write_archetype_table(file, archetype) :
	a = archetypes[archetype]
	file.write("<table>")
	file.write("<tr class=\"genesys-talent-row\">")
	for talent in a["StartingTalents"] :
		write_talent_block(file, talent)
	file.write("</tr>")	
	file.write("</table>\n\n")

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

			row = build_table_row(a["name"], a["soak"], a["defense"], a["encum"])
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
				return armor[character["equipmentArmor"][a]["id"]]["defense"]

	return 0

def purify_name(unclean_name):
	keepcharacters = (' ','.','_')
	purified_name = "".join(c for c in unclean_name if c.isalnum() or c in keepcharacters).rstrip()
	return purified_name

def get_adjustment(character, target) :
	adjustment = 0

	if "masterTalents" in character :
		for row in character["masterTalents"] :
			section = character["masterTalents"][str(row)]
			for rank in range(1, 6) :
				if str(rank) in section :
					talent = section[str(rank)]
					if(len(talent) > 0) :
						if talent in talents :
							details = talents[talent]
							if "special" in details :
								special = details["special"]
								if "target" in special :
									if special["target"] == target :
										adjustment += special["value"]

	return adjustment

def write_characteristic(file, characteristics, key, svg_name) :
	file.write("<div class=\"genesys-characteristics-block\">")
	file.write("   <img src=\"" + svg_name + "\" class=\"genesys-characteristic-svg\" />")
	file.write("   <div class=\"genesys-characteristic-value\">")
	file.write(str(characteristics[key]))
	file.write("   </div>")
	file.write("</div>")

def write_characteristic_block(file, characteristics) :
	file.write("<div class=\"genesys-characteristic-row\">")
	write_characteristic(file, characteristics, "Brawn", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030928/Brawn.svg?1577417616")
	write_characteristic(file, characteristics, "Agility", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030929/Agility.svg?1577417616")
	write_characteristic(file, characteristics, "Intellect", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030931/Intellect.svg?1577417619")
	write_characteristic(file, characteristics, "Cunning", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030930/Cunning.svg?1577417618")
	write_characteristic(file, characteristics, "Willpower", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030933/Willpower.svg?1577417620")	
	write_characteristic(file, characteristics, "Presence", "https://db4sgowjqfwig.cloudfront.net/campaigns/233492/assets/1030932/Presence.svg?1577417620")
	file.write("</div>\n\n")

def write_motivations(file, motivations) :
	strength = motivations["Strength"]
	flaw = motivations["Flaw"]
	desire = motivations["Desire"]
	fear = motivations["Fear"]

	file.write("h3. Motivations\n\n")
	file.write("|Strength: " + strength["key"] + "|" + strength["description"] + "|\n")
	file.write("|Flaw: " + flaw["key"] + "|" + flaw["description"] + "|\n")
	file.write("|Desire: " + desire["key"] + "|" + desire["description"] + "|\n")
	file.write("|Fear: " + fear["key"] + "|" + fear["description"] + "|\n")

def apply_talent_rules(character) :
	if "masterTalents" in character :
		for row in character["masterTalents"] :
			section = character["masterTalents"][str(row)]
			for rank in range(1, 6) :
				if str(rank) in section :
					talent = section[str(rank)]
					if(len(talent) > 0) :
						if talent in talents :
							details = talents[talent]
							if "special" in details :
								special = details["special"]
								if "target" in special :
									for subtarget in special["target"].split(',') :
										if subtarget in skills :
											skills[subtarget]["characteristic"] = special["characteristic"]

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

	wounds = archetype["WoundThreshold"] + characteristics["Brawn"] + get_adjustment(character, "wounds")
	strain = archetype["StrainThreshold"] + characteristics["Willpower"] + get_adjustment(character, "strain")
	soak = characteristics["Brawn"] + calculate_soak(character)
	defense = calculate_defense(character)

	apply_talent_rules(character)

	f = open(purify_name(character["name"]) + ".txt", "w")

	if "description" in character :
		write_vital_stats(f, character["description"])
		f.write("\n\n")

	f.write("h3. Archetype\n\n")
	f.write(character["archetype"] + " " + careers[character["career"]]["name"] + "\n")
	write_archetype_table(f, character["archetype"])

	f.write("h3. Attributes\n\n")
	f.write(build_table_row("_Wounds_","_Strain_", "_Soak Value_","_Defense_"))
	f.write(build_table_row(wounds, strain, soak, defense, postfix="\n"))

	f.write("h3. Characteristics\n\n")
	write_characteristic_block(f, characteristics)

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
	write_talent_table(f, character)

	f.write("h3. Weapons\n\n")
	f.write(build_table_row("_Weapon_", "_Dam_", "_Crit_", "_Skill_", "_Range_", "_Encum_", "_Qualities_", "_Dice Pool_"))
	write_weapon_block(f, character, characteristics)
	f.write("\n\n")

	f.write("h3. Armor\n\n")
	f.write(build_table_row("_Armor_", "_Soak_", "_Defense_", "_Encum_"))
	write_armor_block(f, character)
	f.write("\n\n")

	if "masterMotivations" in character :
		write_motivations(f, character["masterMotivations"])
		f.write("\n\n")

	write_notes_block(f, character["description"])

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
