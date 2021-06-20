import time


class Game:
    def run(self, db):
        # Assign db to local variable
        self.dishes_db = db

        # Copy global dishes_db to class variable, so partial results won't affect db
        self.current_game_dishes: list = db

        # Record game adjectives to update dishes atributes after run
        self.current_game_adjectives: dict = {}

        # Assign all adjectives to variable to iter them during execution
        self.adjectives: set = set().union(*(x.keys()
                                             for x in self.current_game_dishes))
        # Removes dishes names ('_name') from adjectives set
        self.adjectives.remove('_name')

    def update_adjective_status(self, adjective: str, status: bool):
        self.current_game_dishes = [
            x for x in self.current_game_dishes
            if adjective not in x
            or x[adjective] == status
        ]
        self.current_game_adjectives[adjective] = status

    def attempt_dish(self):
        # Prompt dish to user say if it's the right one
        # Should only be called if one dish remaining in current game options
        while True:
            # Retrieves remaining dish
            dish = self.current_game_dishes[0]
            response = input(f"Ahá! Então seu prato é {dish['_name']}?\n")

            # Exit run if right
            if response == 's':
                print('Acertei de novo!')
                break

            # Continues run to get smarter (save/update adjectives/dishes to db)
            elif response == 'n':
                print('Errei, que pena... Quem sabe na próxima...')
                time.sleep(1)
                self.get_smarter(dish)
                break

            else:
                print(
                    "Resposta inválida. Responda com 's' para 'Sim' ou 'n' para 'Não'.")
        return

    def get_smarter(self, wrong_dish: dict, new_dish: str, new_adjective: str):
        # Prompts user to input right dish and assign one new adjective to it

        # Quits game if user trying to cheat
        if wrong_dish['_name'] == new_dish:
            print('Está tentando me enganar né?')
            return

        # Create new dish dict, preserving current adjectives configuration
        new_dish: dict = {
            '_name': new_dish,
            new_adjective: True
        } | self.current_game_adjectives

        # Update wrong tried dish dict, preserving current adjectives configuration
        wrong_dish |= {
            new_adjective: False
        } | self.current_game_adjectives

        # Save to DB
        self.save_game(new_dish, wrong_dish)
        return

    def save_game(self, new_dish: dict, wrong_dish: dict = None):
        # Saves inputs to DB
        # If user inputs existing dish, updates it
        existing_dishes = [x['_name'] for x in self.dishes_db]
        if new_dish['_name'] in existing_dishes:
            new_dish_old_adjectives = [
                x for x in self.dishes_db if x.get('_name') == new_dish['_name']][0]
            new_dish |= new_dish_old_adjectives

        # If attempted a dish, creates it. If not, skip.
        if wrong_dish:
            self.dishes_db = [
                x for x in self.dishes_db
                if x['_name'] != wrong_dish['_name']
                and x['_name'] != new_dish['_name']
            ]
            # Appends new record to DB (currently, in-memory list of dicts)
            self.dishes_db.append(wrong_dish)

        # Appends updated record to DB (currently, in-memory list of dicts)
        self.dishes_db.append(new_dish)

    def create_new_dish(self, new_dish):
        # Creates new dish if inexistent and no matching attempts in game
        new_dish: dict = {'_name': new_dish} | self.current_game_adjectives
        self.save_game(new_dish=new_dish)
