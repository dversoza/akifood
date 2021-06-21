from ui import AkiFoodUI
from akifood import Game, DatabaseRepository
from settings import *


class Controller:
    def __init__(self, db=None) -> None:
        self.database = DatabaseRepository(db)
        self.game = Game(self.database)
        self.ui = AkiFoodUI(self, self.game)
        self.ui.root.mainloop()
        pass

    def game_next_step(self):
        next_step, next_step_info = self.game.next_step()

        if next_step == 'attempt_dish':
            self.ui.attempt_dish_form(next_step_info)

        elif next_step == 'no_dishes':
            self.ui.new_dish_form()

        elif next_step == 'attempt_adjective':
            self.ui.attempt_adjective_form(next_step_info)

    def wrong_attemp_handler(self, wrong_dish: str) -> None:
        self.ui.new_dish_form(wrong_dish)
        return

    def ask_for_new_adjective(self, wrong_dish: str, right_dish_name: str) -> None:
        self.ui.new_adjective_form(wrong_dish, right_dish_name)
        return

    def create_new_dish_handler(self, new_dish: str):
        self.database.create_dish(new_dish)
        self.reload_game()

    def new_adjective_handler(self, wrong_dish: str, right_dish: str, new_adjective: str):
        if wrong_dish == right_dish:
            print('Está tentando me enganar né?')
            return

        # Create new dish dict, preserving current adjectives configuration
        right_dish: dict = {
            '_name': right_dish,
            new_adjective: True
        } | self.game.asked_adjectives

        # Update wrong tried dish dict, preserving current adjectives configuration
        wrong_dish: dict = {
            '_name': wrong_dish,
            new_adjective: False
        } | self.game.asked_adjectives

        self.database.create_dish(right_dish)
        self.database.create_dish(wrong_dish)
        self.reload_game()
        return

    def reload_game(self):
        self.ui.root.destroy()
        self.__init__(self.database.dishes)
