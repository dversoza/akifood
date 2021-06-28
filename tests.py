import unittest
from src.models import Dish, DishAdjective
from src.akifood import Game


class TestGame(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)

    def setUp(self) -> None:
        self.TEST_DISHES = [
            Dish(name='Sushi', dish_adjectives_id=[2]),
            Dish(name='Brigadeiro', dish_adjectives_id=[]),
            Dish(name='Pizza de calabresa', dish_adjectives_id=[1])
        ]

        self.TEST_ADJECTIVES = [
            DishAdjective(_id=1, name='massa'),
            DishAdjective(_id=2, name='salgado')
        ]

        self.game = Game()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_filter_with_adjective(self) -> None:
        filtered_dishes = self.game.filter_with_adjective(1, self.TEST_DISHES)
        self.assertEqual(len(filtered_dishes), 1)

    def test_filter_without_adjective(self) -> None:
        filtered_dishes = self.game.filter_without_adjective(
            1, self.TEST_DISHES)
        self.assertEqual(len(filtered_dishes), 2)

    def test_create_dish_adjective(self) -> None:
        new_dish_adjective = self.game.create_dish_adjective(5, 'doce')
        self.assertIsInstance(new_dish_adjective, DishAdjective)
        self.assertEqual(new_dish_adjective.name, 'doce')

    def test_create_dish(self) -> None:
        new_dish = self.game.create_dish(name='Salada', adjectives=[2])
        self.assertIsInstance(new_dish, Dish)
        self.assertEqual(new_dish.name, 'Salada')
        self.assertEqual(new_dish.dish_adjectives_id, [2])
        self.assertIsInstance(new_dish.dish_adjectives_id, list)


if __name__ == '__main__':
    unittest.main()
