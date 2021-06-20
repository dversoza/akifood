from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk

from settings import *
from akifood import Game


class BaseUI:
    # Base user interface
    def __init__(self, window, width=None, height=None, **options) -> None:
        """Pass options to base UI using kwargs"""
        self.app_width = width if width else APP_DEFAULT_WIDTH
        self.app_height = height if height else APP_DEFAULT_HEIGHT
        if 'not_centered' in options:
            self.center_window(window) if options['not_centered'] else None
        pass

    def center_window(self, win):
        # Centers window to user screen
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        x = (screen_width/2) - (self.app_width/2)
        y = (screen_height/2) - (self.app_height/2)

        win.geometry(f'{self.app_width}x{self.app_height}+{int(x)}+{int(y)}')


class AkiFoodUI(BaseUI):
    def __init__(self, root, db) -> None:
        super().__init__(root)
        self.game = Game()
        self.root = root
        self.db = db
        self.main_interface()

    def main_interface(self):
        self.center_window(win=self.root)
        self.root.title("AkiFood")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text='Seja bem-vindo ao AkiFood!').grid()
        ttk.Label(mainframe, text='Pense em um prato que gosta ...').grid()
        ttk.Button(mainframe, text="OK", command=self.start_game).grid()

        self.root.bind("<Return>", self.start_game)

    def start_game(self):
        self.game.run(db=self.db)

        for adjective in self.game.adjectives:
            print(self.game.current_game_adjectives,
                  self.game.current_game_dishes)
            if len(self.game.current_game_dishes) > 1:
                self.attempt_adjective_form(adjective)

        if len(self.game.current_game_dishes) == 1:
            attempt_dish = self.game.current_game_dishes[0]
            self.attempt_dish_form(attempt_dish)

        elif len(self.game.current_game_dishes) == 0:
            print('Eita... Então eu não sei...')
            self.new_dish_form()

    def attempt_adjective_form(self, adjective: str):
        def true_btn():
            self.game.update_adjective_status(adjective, True)
            attempt_adjective_window.destroy()

        def false_btn():
            self.game.update_adjective_status(adjective, False)
            attempt_adjective_window.destroy()

        attempt_adjective_window = Toplevel(self.root)
        self.center_window(attempt_adjective_window)
        ttk.Label(attempt_adjective_window,
                  text=f'O prato que você pensou é {adjective}?').pack()
        yes_btn = ttk.Button(attempt_adjective_window,
                             text="Sim", command=true_btn)
        yes_btn.pack()
        no_btn = ttk.Button(attempt_adjective_window,
                            text="Não", command=false_btn)
        no_btn.pack()
        self.root.wait_window(attempt_adjective_window)

    def attempt_dish_form(self, dish: dict):
        def true_btn():
            mb.showinfo('Uhul!', 'Acertei de novo!')
            self.reload_game()
            attempt_dish_window.destroy()

        def false_btn():
            self.new_dish_form(wrong_dish=dish)
            attempt_dish_window.destroy()

        attempt_dish_window = Toplevel(self.root)
        self.center_window(attempt_dish_window)
        ttk.Label(attempt_dish_window,
                  text=f"Ahá! Então seu prato é {dish['_name']}?").pack()
        yes_btn = ttk.Button(attempt_dish_window, text="Sim", command=true_btn)
        yes_btn.pack()
        no_btn = ttk.Button(attempt_dish_window, text="Não", command=false_btn)
        no_btn.pack()
        self.root.wait_window(attempt_dish_window)

    def new_dish_form(self, wrong_dish: dict = None):
        def button_handler():
            if wrong_dish:
                self.new_adjective_form(new_dish_name.get(), wrong_dish)
                new_dish_window.destroy()

            else:
                self.game.create_new_dish(new_dish_name.get())
                new_dish_window.destroy()
                self.reload_game()

        new_dish_window = Toplevel(self.root)
        self.center_window(new_dish_window)
        ttk.Label(new_dish_window,
                  text='Aproveitando que você ainda está ai...').pack()
        ttk.Label(new_dish_window, text='Em que prato pensou?').pack()

        new_dish_name = StringVar()
        new_dish_name_entry = ttk.Entry(
            new_dish_window, textvariable=new_dish_name)
        new_dish_name_entry.pack()

        new_dish_name_entry.focus()

        ttk.Button(new_dish_window, text="OK",
                   command=button_handler).pack()
        self.root.bind("<Return>", button_handler)

    def new_adjective_form(self, new_dish_name, wrong_dish):
        def button_handler():
            self.get_smarter_caller(
                wrong_dish, new_dish_name, new_adjective.get())
            new_dish_attr_window.destroy()

        new_dish_attr_window = Toplevel(self.root)
        self.center_window(new_dish_attr_window)
        ttk.Label(new_dish_attr_window,
                  text="Se puder me ajudar a ficar mais inteligente ...").pack()
        ttk.Label(new_dish_attr_window,
                  text=f"{new_dish_name} é ______, mas {wrong_dish['_name']} não.").pack()

        new_adjective = StringVar()
        new_adjective_entry = ttk.Entry(
            new_dish_attr_window, textvariable=new_adjective)
        new_adjective_entry.pack()

        new_adjective_entry.focus()

        ttk.Button(new_dish_attr_window, text="OK",
                   command=button_handler).pack()

        self.root.bind("<Return>", button_handler)

    def get_smarter_caller(self, wrong_dish, new_dish, new_adjective):
        self.game.get_smarter(wrong_dish, new_dish, new_adjective)
        self.reload_game()

    def reload_game(self):
        # Updates db from last run
        self.db = self.game.dishes_db
        self.main_interface()
