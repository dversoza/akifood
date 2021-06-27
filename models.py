class Dish:
    def __init__(self, name, dish_adjectives_id):
        self.name: str = name
        self.dish_adjectives_id: list = dish_adjectives_id


class DishAdjective:
    def __init__(self, _id, name):
        self._id: int = _id
        self.name: str = name
