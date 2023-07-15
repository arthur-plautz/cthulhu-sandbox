from models.character.base import Base

character = Base('character')
character.age_modifier(30)
character.save()