from models.character.templated import Character

abilities = ['firearms', 'driving']
profession = 'soldier'

for i in range(10):
    try:
        character = Character(profession=profession, templated_abilities=abilities)
        character.age_modifier(30)
        character.generate_abilities()
    except:
        print(f"error on {i}")
