from settings import DISHES


class Game:
    def __init__(self, database) -> None:
        self.possible_dishes: list = database.dishes
        self.adjectives_to_ask: list = database.get_adjectives()
        self.asked_adjectives: dict = {}
        pass

    def filter_possible_dishes_according_to_user_input(self, adjective: str, situation: bool):
        self.possible_dishes = [
            x for x in self.possible_dishes
            if adjective not in x
            or x[adjective] == situation
        ]

    def append_adjective_to_asked_adjectives(self, adjective: str, situation: bool):
        self.asked_adjectives[adjective] = situation

    def update_adjective_status(self, adjective: str, situation: bool):
        self.filter_possible_dishes_according_to_user_input(
            adjective, situation)
        self.append_adjective_to_asked_adjectives(adjective, situation)
        self.adjectives_to_ask.remove(adjective)

    def next_step(self):
        if len(self.possible_dishes) == 1:
            dish = self.possible_dishes[0]
            return ('attempt_dish', dish['_name'])

        elif len(self.possible_dishes) == 0 or len(self.adjectives_to_ask) == 0:
            return ('no_dishes',)

        else:
            return ('attempt_adjective', self.adjectives_to_ask[0])


class DatabaseRepository:
    def __init__(self, database=None) -> None:
        initial_db = DISHES
        self.dishes = database if database is not None else initial_db
        pass

    def get_adjectives(self) -> list:
        def remove_name_adjective(adjectives: list):
            adjectives.remove('_name')

        adjectives: set = set().union(*(x.keys() for x in self.dishes))
        remove_name_adjective(adjectives)
        return list(adjectives)

    def get_dishes_names(self) -> list:
        existing_dishes = [x['_name'] for x in self.dishes]
        return existing_dishes

    def get_dish_adjectives(self, dish_name: str) -> dict:
        dish = [x for x in self.dishes if x['_name'] == dish_name]
        adjectives = dish[0]
        return adjectives

    def create_dish(self, dish: dict) -> None:
        if self.dish_already_exists(dish):
            new_dish: dict = self.complete_dish_adjectives(dish)
            self.remove_dish(dish)

        else:
            new_dish = dish

        self.dishes.append(new_dish)

    def complete_dish_adjectives(self, dish: dict) -> dict:
        existing_adjectives = self.get_dish_adjectives(dish['_name'])
        dish |= existing_adjectives
        return dish

    def remove_dish(self, dish: dict):
        self.dishes = [x for x in self.dishes if x['_name'] != dish['_name']]

    def dish_already_exists(self, dish: dict) -> bool:
        existing_dishes = self.get_dishes_names()
        if dish['_name'] in existing_dishes:
            return True
        else:
            return False
