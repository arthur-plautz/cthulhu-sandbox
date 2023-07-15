import pandas as pd
from models.character.base import Base
from models.api import API

class Character(Base):
    def __init__(self, profession, templated_abilities) -> None:
        super().__init__()
        self._abilities = templated_abilities
        self._profession = profession

    def _build_expected(self):
        expected = {
            'background': None
        }
        for ability in self._abilities:
            expected[ability] = None
        return expected

    def _build_data(self):
        config = self.get_serialized()
        expected = self._build_expected()
        return dict(
            config=config,
            profession=self._profession,
            abilities=self._abilities,
            expected=expected
        )

    def generate_abilities(self):
        api = API()
        data = self._build_data()
        info = api.get_info(data)
        self.save(info)

    def save(self, serialized):
        base = self.get_serialized()
        data = {**base, **serialized}
        df = pd.DataFrame([data])
        df.to_json(f"data/{self.name}.json", orient="index")
