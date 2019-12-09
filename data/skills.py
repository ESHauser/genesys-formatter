
# [characteristis][category] = <list of skills>

abbr = {
    "Intellect" : "INT",
    "Brawn" : "BR",
    "Presence" : "PR",
    "Agility" : "AG",
    "Willpower" : "WILL",
    "Cunning" : "CUN"
}

compressedSkills = {
    "Intellect": {
        "General": ['Alchemy', 'Computers', 'Medicine', 'Mechanics', 'Operating', 'Knowledge'],   
        "Magic": ['Arcana']
    },
    "Brawn": {
        "General": ['Athletics', 'Resilience'],
        "Combat": ['Brawl', 'Melee']
    },
    "Presence": {
        "General": ['Cool'],
        "Social": ['Charm', 'Leadership', 'Negotiation']
    },
    "Agility": {
        "General": ['Coordination', 'Driving', 'Piloting', 'Stealth'],
        "Combat": ['Gunnery', 'Ranged (Heavy)', 'Ranged (Light)']
    },
    "Willpower": {
        "General": ['Discipline', 'Vigilance'],
        "Magic": ['Divine'],
        "Social": ['Coercion']
    },
    "Cunning": {
        "General": ['Perception', 'Skulduggery', 'Streetwise', 'Survival'],
        "Magic": ['Primal'],
        "Social": ['Deception']
    },
}

def getFlattenedSkills():
    skills = {}
    for x in compressedSkills:
        for y in compressedSkills[x]:
            for z in compressedSkills[x][y]:
                skills[z] = {}
                skills[z]["category"] = y
                skills[z]["characteristic"] = x
                skills[z]["wiki"] = "[[" + z + " (" + abbr[x] + ")]]"
    return skills
