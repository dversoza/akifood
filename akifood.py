import time

dishes_db = [
    {'_name': 'Bolo de cholocate', 'massa': False},
    {'_name': 'Lasanha', 'massa': True}
]

class Game:
    def __init__(self) -> None:
        pass

    def run(self):
        print('Seja bem-vindo ao AkiFood! 🍕🍟🍗🌮🥨🍤🍖🍳🥞')
        time.sleep(1)
        print('Pense em um prato que gosta ...')
        time.sleep(1)

while True:
    game = Game()
    game.run()