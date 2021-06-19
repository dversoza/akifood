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

        # If no dish remains in game remaining tries, exit run and create new dish
        elif len(self.current_game_dishes) == 0:
            print('Eita... Então eu não sei...')
            self.get_smarter()

    def attempt_adjective(self, adjective):
        # Prompt adjective to user say if it matches or not to his/her dish
        while True:
            response = input(f'O prato que você pensou é {adjective}?\n')

            # Updates current game adjectives according to user input
            # Also saves adjective to current game adjectives, to be later used
            # in new dish
            if response == 's':
                self.current_game_dishes = [
                    x for x in self.current_game_dishes
                    if adjective not in x
                    or x[adjective] == True
                ]
                self.current_game_adjectives[adjective] = True
                break

            elif response == 'n':
                self.current_game_dishes = [
                    x for x in self.current_game_dishes
                    if adjective not in x
                    or x[adjective] == False
                ]
                self.current_game_adjectives[adjective] = False
                break

            else:
                print(
                    "Resposta inválida. Responda com 's' para 'Sim' ou 'n' para 'Não'.")
        return

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

    def get_smarter(self, wrong_dish):
        # Prompts user to input right dish and assign one new adjective to it
        # Capitalizes string to save dishes names prettier
        new_dish_name = input(
            'Aproveitando que você ainda está ai, em que prato pensou?\n').capitalize()

        time.sleep(1)
        print(
            f'Nossa... Seu prato era {new_dish_name}, como não pensei nisso antes?')
        time.sleep(1)

        # Save adjectives as lower string to make it prettier
        new_dish_adjective = input(
            f"Se puder me ajudar a ficar mais inteligente, {new_dish_name} é ______, mas {wrong_dish['_name']} não.\n").lower()

        # Ignores '_name' adjective to avoid keyerror bug
        # TODO: fix using adjective and dishes Classes or ORM
        if new_dish_adjective == '_name':
            print('Está tentando me enganar né?')
            print(
                'https://images.freeimages.com/images/large-previews/637/sad-dog-1604766.jpg')

        # Create new dish dict, preserving current adjectives configuration
        new_dish = {
            '_name': new_dish_name,
            new_dish_adjective: True
        } | self.current_game_adjectives

        # Update wrong tried dish dict, preserving current adjectives configuration
        wrong_dish |= {
            new_dish_adjective: False
        } | self.current_game_adjectives

        # Save to DB
        self.save_game(new_dish, wrong_dish)
        print('Muito obrigado! 👊👊👊')
        return

    def save_game(self, new_dish, wrong_dish=None):
        # Saves inputs to DB
        # Calls global db variable (as it's still only saved in memory)
        global dishes_db

        # If user inputs existing dish, updates it
        existing_dishes = [x['_name'] for x in dishes_db]
        if new_dish in existing_dishes:
            new_dish_old_adjectives = [
                x for x in dishes_db if x.get('_name') == new_dish][0]
            new_dish |= new_dish_old_adjectives

        # If attempted a dish, creates it. If not, skip.
        if wrong_dish:
            dishes_db = [
                x for x in dishes_db
                if x['_name'] != wrong_dish['_name']
                and x['_name'] != new_dish['_name']
            ]
            # Appends new record to DB (currently, in memory list of dicts)
            dishes_db.append(wrong_dish)

        # Appends updated record to DB (currently, in memory list of dicts)
        dishes_db.append(new_dish)


while True:
    game = Game(db=dishes_db)
    game.run()
