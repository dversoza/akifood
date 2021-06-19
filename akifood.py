import time

# Base dishes to start application
dishes_db = [
    {'_name': 'Bolo de cholocate', 'massa': False},
    {'_name': 'Lasanha', 'massa': True}
]


class Game:
    def __init__(self, db: list) -> None:
        # Copy global dishes_db to class variable, so partial results won't affect db
        self.current_game_dishes: list = db

        # Record game adjectives to update dishes atributes after run
        self.current_game_adjectives: dict = {}
        pass

    def run(self):
        print('Seja bem-vindo ao AkiFood! 🍕🍟🍗🌮🥨🍤🍖🍳🥞')
        time.sleep(1)
        print('Pense em um prato que gosta ...')
        time.sleep(1)

        # Assign all adjectives to variable to iter them during execution
        adjectives: set = set().union(*(x.keys() for x in self.current_game_dishes))
        # Removes dishes names ('_name') from adjectives set
        adjectives.remove('_name')

        # Tries each adjective until correct dish remains in current_game_dishes
        for adjective in adjectives:
            if len(self.current_game_dishes) > 1:
                print(self.current_game_adjectives, self.current_game_dishes)
                self.attempt_adjective(adjective)

        # If only one dish maching choices, tries it
        if len(self.current_game_dishes) == 1:
            self.attempt_dish()

    def attempt_adjective(self):
        # Prompt adjective to user say if it matches or not to his/her dish
        return

    def attempt_dish(self):
        # Prompt dish to user say if it's the right one
        return

    def get_smarter(self):
        # Saves new dish to and updates wrong dish adjectives to db
        return


while True:
    game = Game(db=dishes_db)
    game.run()
