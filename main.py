import tkinter as tk
from tkinter.messagebox import showinfo

from akifood import Game
from models import DishAdjective, Dish

DISHES = [
    Dish(name='Lasanha', dish_adjectives_id=[1]),
    Dish(name='Bolo de chocolate', dish_adjectives_id=[])
]

ADJECTIVES = [
    DishAdjective(_id=1, name='massa')
]


def start(root):
    game = Game(root)
    success, game_adjectives, dish_attempt = game.get_user_answers(DISHES,
                                                                   ADJECTIVES)

    if success:
        showinfo('Ganhei!', 'Acertei de novo!')

    if not success:
        dish_name = game.get_dish_name()

        new_dish_adjective_name = game.get_new_adjective(
            dish_name, dish_attempt)
        new_dish_adjective = game.create_dish_adjective(
            game.next_adjective_id(ADJECTIVES), new_dish_adjective_name)
        game_adjectives.append(new_dish_adjective._id)
        ADJECTIVES.append(new_dish_adjective)

        new_dish = game.create_dish(dish_name, game_adjectives)
        DISHES.append(new_dish)


if __name__ == '__main__':
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    root.geometry('300x100')
    root.title('Jogo Gourmet')
    label = tk.Label(root, text='Pense em um prato que gosta.', pady=20)
    button = tk.Button(root, text='Ok', command=lambda: start(root), padx=25)
    label.pack()
    button.pack()
    root.mainloop()
