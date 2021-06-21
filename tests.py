import unittest
from akifood import DatabaseRepository, Game


class TestDatabaseRepository(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.database = DatabaseRepository()

    def test_database_has_default_data(self):
        self.assertIsNotNone(self.database.dishes,
                             'Database has no initial data !')

    def test_database_creates_dishes(self):
        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)
        self.assertIn(fake_dish, self.database.dishes,
                      'Database is not creating dishes!')

    def test_database_retrieves_dishes_names(self):
        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)
        dishes_names = self.database.get_dishes_names()
        self.assertIn(fake_dish['_name'], dishes_names,
                      'Database name retrieving not working!')

    def test_database_retrieves_all_adjectives(self):
        error_msg = 'Database adjectives retrieving not working!'

        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)
        adjectives = self.database.get_adjectives()
        self.assertIn('massa', adjectives, error_msg)
        self.assertIn('Italiano', adjectives, error_msg)
        self.assertGreaterEqual(len(adjectives), 2, error_msg)

    def test_database_retrieves_dish_adjectives(self):
        error_msg = 'Database not retrieving a specific dish adjective!'

        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)
        adjectives = self.database.get_dish_adjectives(fake_dish['_name'])
        self.assertIn('massa', adjectives, error_msg)
        self.assertIn('Italiano', adjectives, error_msg)
        self.assertGreaterEqual(len(adjectives), 2, error_msg)

    def test_database_updates_existing_dish_instead_of_duplicating_it(self):
        error_msg = 'Existing duplicates. Database not updating dishes, but duplicating it.'

        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)

        fake_dish_update = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True,
            'bom': True
        }

        self.database.create_dish(fake_dish_update)

        self.assertIn(fake_dish_update, self.database.dishes, error_msg)
        self.assertNotIn(fake_dish, self.database.dishes, error_msg)

        dish_entries = [
            x for x in self.database.dishes if x['_name'] == 'Macarrão']
        self.assertEqual(len(dish_entries), 1, error_msg)

    def test_database_remove_dish(self):
        error_msg = 'Database not removing dishes!'

        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)
        self.database.remove_dish(fake_dish)
        self.assertNotIn(fake_dish, self.database.dishes, error_msg)

    def test_database_completes_dish_adjectives(self):
        error_msg = 'Database not completing dish adjectives!'

        fake_dish = {
            '_name': 'Macarrão',
            'massa': True,
            'Italiano': True
        }

        self.database.create_dish(fake_dish)

        fake_dish_extra_adjectives = {
            '_name': 'Macarrão',
            'bom': True,
            'Japonês': False
        }

        result = self.database.complete_dish_adjectives(
            fake_dish_extra_adjectives)
        self.assertDictEqual(result, fake_dish | fake_dish_extra_adjectives,
                             error_msg)


class TestGame(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        database = DatabaseRepository()
        self.game = Game(database)

    def test_game_starts_with_default_values(self):
        error_msg = 'Game starting with no {} default values!'
        self.assertIsNotNone(self.game.possible_dishes,
                             error_msg.format('possible_dishes'))
        self.assertIsNotNone(self.game.adjectives_to_ask,
                             error_msg.format('adjectives_to_ask'))

    def test_game_filters_dishes_according_to_user_input(self):
        error_msg = 'Game not filtering dishes'
        dish_1 = {'_name': 'Sushi', 'Japonês': True, 'Italiano': False}
        dish_2 = {'_name': 'Macarrão', 'Japonês': False, 'Italiano': True}

        self.game.possible_dishes = [dish_1, dish_2]

        self.game.filter_possible_dishes_according_to_user_input(
            'Italiano', False)
        self.assertNotIn(dish_2, self.game.possible_dishes, error_msg)
        self.assertIn(dish_1, self.game.possible_dishes, error_msg)

    def test_game_appends_adjective_to_asked_adjectives(self):
        error_msg = "Game appending adjectives to it's state"
        adjective, situation = ('Italiano', False)
        self.game.append_adjective_to_asked_adjectives(adjective, situation)
        self.assertIn(adjective, self.game.asked_adjectives, error_msg)
        self.assertEqual(
            situation, self.game.asked_adjectives[adjective], error_msg)

    def test_game_removes_attempted_adjectives(self):
        error_msg = "Game is not removing a attempted adjective!"
        adjective, situation = ('Italiano', False)
        self.game.append_adjective_to_asked_adjectives(adjective, situation)
        self.assertNotIn(adjective, self.game.adjectives_to_ask, error_msg)

    def test_game_returns_tuple_as_next_step(self):
        response = self.game.next_step()
        self.assertIsInstance(
            response, tuple, 'Game not giving tuple as next step.')


if __name__ == '__main__':
    unittest.main()
