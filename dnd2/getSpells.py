import pandas as pd
import json
import datetime
import requests 

# ----------------- PHASE ONE: GET CLAN MEMBERS -----------------
# Replace this later with an api call to get the data
with open('spells.json') as f:
    data = json.load(f)

# ----------------- Build dataframe ---------------

df = pd.json_normalize(data['results'])
# Ue this if you want to filter a df
# df = df.filter([], axis=1)

# add a readable timestamp for each log entry
# df['lastRun'] = pd.Timestamp.now()

# ----------------- PHASE TWO: GET ALL CHARACTERS -----------------
spell_json = []

for index, row in df.iterrows():
    response=requests.get('https://www.dnd5eapi.co{}'.format(row['url']),headers={'Content-Type': 'application/json'}).json()
    spell_json.append(response)
    with open('spellDesc.json', 'w') as outfile:
        json.dump(spell_json, outfile)


with open('spellDesc.json') as f:
    data = json.load(f)

df2 = pd.json_normalize(data)

dfComplete = pd.merge(df, df2, on=['index','name','url'])

#dfComplete['AtSlot1'] = dfComplete['heal_at_slot_level.1'] + dfComplete['damage.damage_at_slot_level.1']

dfComplete = dfComplete.fillna('')
dfComplete['AtSlot1'] = dfComplete[['heal_at_slot_level.1', 'damage.damage_at_slot_level.1']].agg(''.join, axis=1)
dfComplete['AtSlot2'] = dfComplete[['heal_at_slot_level.2', 'damage.damage_at_slot_level.2']].agg(''.join, axis=1)
dfComplete['AtSlot3'] = dfComplete[['heal_at_slot_level.3', 'damage.damage_at_slot_level.3']].agg(''.join, axis=1)
dfComplete['AtSlot4'] = dfComplete[['heal_at_slot_level.4', 'damage.damage_at_slot_level.4']].agg(''.join, axis=1)
dfComplete['AtSlot5'] = dfComplete[['heal_at_slot_level.5', 'damage.damage_at_slot_level.5']].agg(''.join, axis=1)
dfComplete['AtSlot6'] = dfComplete[['heal_at_slot_level.6', 'damage.damage_at_slot_level.6']].agg(''.join, axis=1)
dfComplete['AtSlot7'] = dfComplete[['heal_at_slot_level.7', 'damage.damage_at_slot_level.7']].agg(''.join, axis=1)
dfComplete['AtSlot8'] = dfComplete[['heal_at_slot_level.8', 'damage.damage_at_slot_level.8']].agg(''.join, axis=1)
dfComplete['AtSlot9'] = dfComplete[['heal_at_slot_level.9', 'damage.damage_at_slot_level.9']].agg(''.join, axis=1)

dfComplete.to_csv('classSpellsAndDesc.csv', header=True,index=False) 