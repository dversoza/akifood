from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

from models import DishAdjective, Dish


class Game:
    def __init__(self, root) -> None:
        self.game_name = 'Jogo Gourmet'
        self.root = root
        pass

    def filter_with_adjective(self, adjective_id, dishes) -> list:
        list_filter = filter(
            lambda x: True if adjective_id in x.dish_adjectives_id else False,
            dishes
        )
        filtered_dishes = list(list_filter)
        return filtered_dishes

    def filter_without_adjective(self, adjective_id, dishes) -> list:
        list_filter = filter(
            lambda x: True if adjective_id not in x.dish_adjectives_id else False,
            dishes
        )
        filtered_dishes = list(list_filter)
        return filtered_dishes

    def ask_user_right_dish(self, dish_name):
        resp = askyesno(self.game_name, f'Você pensou em {dish_name}?')
        return resp

    def get_dish_name(self):
        dish_name = askstring(title=self.game_name,
                              prompt='Qual prato você pensou?\n',
                              parent=self.root)

        return dish_name

    def get_new_adjective(self, new_dish, wrong_dish):
        new_adjective = askstring(title=self.game_name,
                                  prompt=f'O {new_dish} é ______ mas o {wrong_dish} não?\n',
                                  parent=self.root)
        return new_adjective

    def create_dish(self, name, adjectives):
        new_dish = Dish(
            name=name,
            dish_adjectives_id=adjectives
        )
        return new_dish

    def create_dish_adjective(self, _id, dish_adjective):
        new_dish_adjective = DishAdjective(
            _id=_id,
            name=dish_adjective
        )
        return new_dish_adjective

    def next_adjective_id(self, current_adjectives):
        return len(current_adjectives) + 1

    def get_user_answers(self, dishes, adjectives):

        user_answer_adjectives = []

        for adjective in adjectives:

            resp = askyesno('AkiFood', f'Seu prato é {adjective.name}?\n')

            if resp:
                user_answer_adjectives.append(adjective._id)
                dishes = self.filter_with_adjective(adjective._id, dishes)

            if not resp:
                dishes = self.filter_without_adjective(adjective._id, dishes)

            if len(dishes) == 1:
                dish_attempt = dishes[0].name
                success = self.ask_user_right_dish(dish_attempt)
                return (success, user_answer_adjectives, dish_attempt)
