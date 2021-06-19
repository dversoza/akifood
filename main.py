import time
from akifood import Game

# Base dishes to start application
dishes_db = [
    {'_name': 'Bolo de chocolate', 'massa': False},
    {'_name': 'Lasanha', 'massa': True}
]

if __name__ == '__main__':
    """Program entry point"""
    while True:
        game = Game(db=dishes_db)
        game.run()

        # Updates DB after each run
        dishes_db = game.dishes_db

        # Automatically restarts game
        time.sleep(1)
        print('Vamos jogar novamente?')
        time.sleep(1)
