import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import json

def get_races_from_url(url):
    # Send a GET request to the website
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    race_table = soup.find('table', class_="5e")

    # Find all the links to the races within this section
    race_links = race_table.find_all('a', href=True)

    # Extract the URLs and the text (race names) from the links
    races = []

    link_filter = ["Charisma", "Constitution", "Strength", "Intelligence", "Wisdom", "Dexterity"]
    for link in race_links:
        race_url = "https://www.dandwiki.com" + link['href']
        race_name = link.get_text()
        
        if race_name not in link_filter:
            races.append((race_name, race_url))
    
    return races

def get_data_from_race(url):
    # Send a GET request to the website
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    traits = soup.findAll('span', class_="mw-headline")
    traits_text = None

    # Finds the actual traits not the jibberjabber
    for t in traits:
        if t.get_text().strip().endswith("Traits"):
            traits_text = t.find_next('p')
    
    if traits_text != None:
    
        # Extract text content from the <p> tag, stripping unnecessary tags
        text_content = []
        current_text = ""
        for element in traits_text.contents:
            if element.name == 'br':
                text_content.append(current_text)
                current_text = ""
            else:
                current_text = current_text + element.get_text()

        return text_content
    return None

# Adds value from dictionary keys to the total value
def update_stats(stats_count, updates):
    for key, value in updates.items():
        if key in stats_count:
            if value.isdigit():
                stats_count[key] += int(value)
        else:
            print(f"Stat '{key}' does not exist.")
    
    return stats_count

def clean_string_abilities(text, allowed_strings):
    # Escape and join allowed strings for the regex pattern
    allowed_pattern = '|'.join(re.escape(s) for s in allowed_strings)
    # Define a pattern to match either the allowed strings or numbers
    pattern = rf"({allowed_pattern}|\d+)"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Get rid of when people specify its a max of 20
    if "20" in matches:
        matches.remove("20")

    return matches

def clean_string_sizes(text, allowed_strings):
    # Escape and join allowed strings for the regex pattern
    allowed_pattern = '|'.join(re.escape(s) for s in allowed_strings)
    # Define a pattern to match either the allowed strings or numbers
    pattern = rf"({allowed_pattern})"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    return matches

def clean_string_speeds(text, allowed_strings):
    # Escape and join allowed strings for the regex pattern
    allowed_pattern = '|'.join(re.escape(s) for s in allowed_strings)
    # Define a pattern to match either the allowed strings or numbers
    pattern = rf"({allowed_pattern}|\d+)"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    return matches

def clean_string_attributes(text, allowed_strings):
    # Escape and join allowed strings for the regex pattern
    allowed_pattern = '|'.join(re.escape(s) for s in allowed_strings)
    # Define a pattern to match either the allowed strings or numbers
    pattern = rf"({allowed_pattern})"

    # Find all matches in the text
    matches = re.findall(pattern, text, re.IGNORECASE)

    return matches

def preprocess_traits_abilities(data_array, stats_count):
    if data_array == None:
        return None
    ability_scores = ["Charisma", "Constitution", "Strength", "Intelligence", "Wisdom", "Dexterity", "choice", "either", "each", "decreases"]

    cleaned = None

    for data in data_array:
        if data.startswith("Ability Score"):
            cleaned = clean_string_abilities(data, ability_scores)
    
    if cleaned == None:
        return None
    
    if "choice" in cleaned or "either" in cleaned or "each" in cleaned or "decreases" in cleaned:
        return None
    if len(cleaned) % 2 != 0:
        return None
    else:
        stats_dictionary = {}
        for i in range(0, len(cleaned), 2):
            stats_dictionary[cleaned[i]] = cleaned[i + 1]

        return update_stats(stats_count, stats_dictionary)

def preprocess_traits_sizes(data_array, sizes_count):
    if data_array == None:
        return None
    sizes_list = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]

    cleaned = None

    for data in data_array:
        if data.startswith("Size"):
            cleaned = clean_string_sizes(data, sizes_list)
    
    if cleaned == None:
        return None
    
    sizes_dictionary = {}
    for i in range(len(cleaned)):
        sizes_dictionary[cleaned[i]] = "1"

    return update_stats(sizes_count, sizes_dictionary)

def preprocess_traits_speeds(data_array, stats_count):
    if data_array == None:
        return None
    speed_types = ["walking", "swimming", "flying"]

    cleaned = None

    for data in data_array:
        if data.startswith("Speed"):
            cleaned = clean_string_speeds(data, speed_types)
    
    if cleaned == None:
        return None
    
    if len(cleaned) % 2 != 0:
        return None
    else:
        stats_dictionary = {}
        for i in range(0, len(cleaned), 2):
            stats_dictionary[cleaned[i]] = cleaned[i + 1]

        return update_stats(stats_count, stats_dictionary)

def preprocess_traits_attributes(data_array):
    if data_array == None:
        return None
    filter = ["proficient", "proficiency", "advantage", "disadvantage", "resistant", "resistance", "immune", "immunity", "weak", "weakness", "vulnerable", "vulnerability", "disadvantage", "acrobatics", "animal handling", "arcana", "athletics", "deception",
              "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "slight of hand", "stealth", "survival",
              "acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic", "piercing", "poison", "psychic", "radiant", "slashing", "thunder",
              "blinded", "charmed", "deafened", "exhaustion", "frightened", "grappled", "incapacitated", "invisible", "paralyzed", "petrified", "poisoned", "prone", "restrained", "sleep", "stunned", "unconscious",
              "spell", "cantrip", "armour class", "temporary hitpoints", "temporary hit points"]
    # The long vector thing - [Darkvision, skill checks, {0 - None, 1 - Resistant, 2 - Immune} Damage types, status effects, Cantrip/Spells, Bulkiness]
    # 18 In total
    skill_checks = ["acrobatics", "animal handling", "arcana", "athletics", "deception", "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "slight of hand", "stealth", "survival"]
    # 13 In total
    damage_types = ["acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic", "piercing", "poison", "psychic", "radiant", "slashing", "thunder"]
    # 16 In total
    status_effects = ["blinded", "charmed", "deafened", "exhaustion", "frightened", "grappled", "incapacitated", "invisible", "paralyzed", "petrified", "poisoned", "prone", "restrained", "sleep", "stunned", "unconscious"]

    # Should be 50
    attributes_vector = [0] * 50

    next_feature_words = ["proficient", "proficiency", "advantage", "disadvantage", "resistant", "resistance", "immune", "immunity", "disadvantage", "spell", "cantrip", "armour class", "temporary hitpoints", "temporary hit points"]

    # Gets the darkvision out the way, then cleans the data
    cleaned = []
    for data in data_array:
        data = data.strip()
        if data.startswith("Superior Darkvision"):
            attributes_vector[0] = 2
        elif data.startswith("Darkvision"):
            attributes_vector[0] = 1
        if not (data.startswith("Darkvision") or data.startswith("Ability Score") or data.startswith("Age") or data.startswith("Alignment") or data.startswith("Size") or data.startswith("Speed")):
            to_append = clean_string_attributes(data, filter)
            if to_append != []:
                cleaned.append(to_append)
    
    cleaned_split = []

    for cleaned_words in cleaned:
        for i in range(len(cleaned_words)): 
            if cleaned_words[i] in next_feature_words:
                count = 1
                while (i + count != len(cleaned_words) and cleaned_words[i + count] not in next_feature_words):
                    count += 1
                cleaned_split.append(cleaned_words[i:i + count])
    
    for i in cleaned_split:
        if i[0].lower() == "proficient" or i[0].lower() == "proficiency" or i[0].lower() == "advantage" or i[0].lower() == "disadvantage":
            for j in range(1,len(i)):
                try:
                    index = skill_checks.index(i[j].lower())
                    if i[0].lower() != "disadvantage":
                        attributes_vector[1 + index] = 1
                    else:
                        attributes_vector[1 + index] = -1
                except ValueError:
                    pass
        if i[0].lower() == "resistant" or i[0].lower() == "resistance" or i[0].lower() == "immune" or i[0].lower() == "immunity":
            for j in range(1,len(i)):
                try:
                    index = damage_types.index(i[j].lower())
                    if i[0].lower() == "resistant" or i[0].lower() == "resistance":
                        attributes_vector[19 + index] = 1
                    elif i[0].lower() == "immune" or i[0].lower() == "immunity":
                        attributes_vector[19 + index] = 2
                except ValueError:
                    pass
        if i[0].lower() == "weak" or i[0].lower() == "weakness" or i[0].lower() == "vulnerable" or i[0].lower() == "vulnerability":
            for j in range(1,len(i)):
                try:
                    index = damage_types.index(i[j].lower())
                    if i[0].lower() == "resistant" or i[0].lower() == "resistance":
                        attributes_vector[19 + index] = -1
                except ValueError:
                    pass
        if i[0].lower() == "immune" or i[0].lower() == "immunity" or i[0].lower() == "advantage" or i[0].lower() == "disadvantage":
            for j in range(1,len(i)):
                try:
                    index = status_effects.index(i[j].lower())
                    if i[0].lower() != "disadvantage":
                        attributes_vector[32 + index] = 1
                    else:
                        attributes_vector[32 + index] = -1
                except ValueError:
                    pass
        if i[0].lower() == "spell" or i[0].lower() == "cantrip":
            attributes_vector[48] = 1
        if i[0].lower() == "armour class" or i[0].lower() == "temporary hitpoints" or i[0].lower() == "temporary hit points":
            attributes_vector[49] = 1
        
    abilities_count = {
    "Constitution": 0,
    "Charisma": 0,
    "Dexterity": 0,
    "Intelligence": 0,
    "Strength": 0,
    "Wisdom": 0
    }

    sizes_count = {
    "Tiny": 0,
    "Small": 0,
    "Medium": 0,
    "Large": 0,
    "Huge": 0,
    "Gargantuan": 0
    }

    speeds_count = {
    "walking": 0,
    "swimming": 0,
    "flying": 0,
    }

    abilities_change = preprocess_traits_abilities(data_array, abilities_count)

    if abilities_change == None:
        abilities_vector = [0] * 6
    else:
        abilities_vector = list(abilities_change.values())

    sizes_change = preprocess_traits_sizes(data_array, sizes_count)

    if sizes_change == None:
        sizes_vector = [0] * 6
    else:
        sizes_vector = list(sizes_change.values())

    speeds_change = preprocess_traits_speeds(data_array, speeds_count)

    if speeds_change == None:
        speeds_vector = [0] * 3
    else:
        speeds_vector = list(speeds_change.values())
    
    for i in abilities_vector:
        attributes_vector.append(i)
    for i in sizes_vector:
        attributes_vector.append(i)
    for i in speeds_vector:
        attributes_vector.append(i)
    
    return attributes_vector

def remove_incomplete_data(data_array):
    # Checks for no or empty data
    if data_array == None or data_array == [0] * 65:
        return None
    
    # Check for missing movement (giveaway something didnt work)
    if data_array[-3:] == [0] * 3:
        return None
    
    # Check for missing ability score improvements
    if data_array[50:56] == [0] * 6:
        return None

    # Check for missing size
    if data_array[56:62] == [0] * 6:
        return None
    
    return data_array

# URL of the D&D homebrew races page
# Sorted by type for classification
url = "https://www.dandwiki.com/wiki/5e_Races_by_Type"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.content
else:
    print("Failed to retrieve the webpage")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all h2 tags, these seperate the race groups
h2_tags = soup.find_all('h2')

# Create empty array to store races groups in
h2_race_groups = []

for tag in h2_tags:
    # Extract the URLs and the text (race names) from the h2 tags
    races = []
    # Find all the links to the races within this section
    race_links = tag.find_all('a', href=True)
    for link in race_links:
        race_url = "https://www.dandwiki.com/" + link['href']
        race_name = link.get_text()
        races.append((race_name, race_url))

    # Adds the race groups to an array
    h2_race_groups.append(races)

races_by_group = []

for race_group in h2_race_groups:
    for race in race_group:
        races_by_group.append(get_races_from_url(race[1]))

def create_json_with_index(index):
    dataframe_array = []
    for race in races_by_group[index]:
        attributes_vector = preprocess_traits_attributes(get_data_from_race(race[1]))
        # Needs more processing
        attributes_vector = remove_incomplete_data(attributes_vector)
        if attributes_vector != None:
            dataframe_array.append(attributes_vector)
    
    return dataframe_array

race_types = ["aberrations", "beasts", "celestials", "constructs", "dragons", "elementals", "fey", "fiends", "giants", "humanoids", "monstrosoties", "oozes", "plants", "undead"]

temp = create_json_with_index(3)
# Save to a file using json
file_name = "constructs" + "_array.json"
with open(file_name, 'w') as f:
    json.dump(temp, f)