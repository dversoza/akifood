from tkinter import *
from tkinter import messagebox as mb

from settings import *
from akifood import Game


class BaseUI:
    # Base user interface
    def __init__(self, root, width=None, height=None, title=None, *args, **kwargs) -> None:
        """Pass options to base UI using kwargs"""
        self.app_width = width if width else APP_DEFAULT_WIDTH
        self.app_height = height if height else APP_DEFAULT_HEIGHT
        self.title = title if title else APP_TITLE

        # Sets config through Tkinter
        root.title(self.title)

        # Centers UI window to user screen
        self.center_window(root)

        self.root = root

    def center_window(self, win):
        # Centers window to user screen
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        x = (screen_width/2) - (self.app_width/2)
        y = (screen_height/2) - (self.app_height/2)

        win.geometry(f'{self.app_width}x{self.app_height}+{int(x)}+{int(y)}')

    def mainframe(self, root):
        _frame = Frame(root)
        _frame.grid(column=0, row=0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        return _frame

    def popup(self, root):
        _window = Toplevel(root)
        _window.focus()
        self.center_window(_window)
        _frame = self.mainframe(_window)
        return (_window, _frame)


class AkiFoodUI(BaseUI):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.game = Game()
        self.main_interface()

    def main_interface(self):
        _frame = self.mainframe(self.root)

        Label(_frame, text='Seja bem-vindo ao AkiFood!').grid()
        Label(_frame, text='Pense em um prato que gosta ...').grid()
        Button(_frame, text="OK", padx=25, pady=5,
               command=self.start_game).grid()

    def start_game(self):
        # Calls Game class and manage runtime
        self.game.run(db=DISHES)

        for adjective in self.game.adjectives:
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
            _window.destroy()

        def false_btn():
            self.game.update_adjective_status(adjective, False)
            _window.destroy()

        _window, _frame = self.popup(self.root)

        question = Label(
            _frame, text=f'O prato que você pensou é {adjective}?')
        question.grid(column=0, row=0, columnspan=2)
        yes_btn = Button(_frame, padx=25, pady=5, text="Sim", command=true_btn)
        yes_btn.grid(column=0, row=1)
        no_btn = Button(_frame, padx=25, pady=5, text="Não", command=false_btn)
        no_btn.grid(column=1, row=1)

        self.root.wait_window(_window)

    def attempt_dish_form(self, dish: dict):
        def true_btn():
            mb.showinfo('Uhul!', 'Acertei de novo!')
            self.reload_game()
            _window.destroy()

        def false_btn():
            self.new_dish_form(wrong_dish=dish)
            _window.destroy()

        _window, _frame = self.popup(self.root)

        Label(_frame, text=f"Ahá! Então seu prato é {dish['_name']}?").grid(
            columnspan=2)
        yes_btn = Button(_frame, text="Sim", padx=25, pady=5, command=true_btn)
        yes_btn.grid(column=0, row=1)
        yes_btn.focus()
        no_btn = Button(_frame, text="Não", padx=25, pady=5, command=false_btn)
        no_btn.grid(column=1, row=1)

        self.root.wait_window(_window)

    def new_dish_form(self, wrong_dish: dict = None):
        def button_handler():
            if wrong_dish:
                self.new_adjective_form(new_dish_name.get(), wrong_dish)
                _window.destroy()

            else:
                self.game.create_new_dish(new_dish_name.get())
                _window.destroy()
                self.reload_game()

        _window, _frame = self.popup(self.root)

        self.center_window(_window)
        Label(_frame, text='Aproveitando que você ainda está ai...').grid()
        Label(_frame, text='Em que prato pensou?').grid()

        new_dish_name = StringVar()
        new_dish_name_entry = Entry(_frame, textvariable=new_dish_name)
        new_dish_name_entry.grid()

        new_dish_name_entry.focus()

        Button(_window, text="OK", padx=25, pady=5,
               command=button_handler).grid()
        self.root.bind("<Return>", button_handler)

    def new_adjective_form(self, new_dish_name, wrong_dish):
        def ok_btn():
            self.game.get_smarter(wrong_dish=wrong_dish,
                                  new_dish=new_dish_name,
                                  new_adjective=new_adjective.get())
            _window.destroy()
            self.reload_game()

        _window, _frame = self.popup(self.root)

        Label(_frame, text="Se puder me ajudar a ficar mais inteligente ...").grid()
        Label(
            _frame, text=f"{new_dish_name} é ______, mas {wrong_dish['_name']} não.").grid()

        new_adjective = StringVar()
        _entry = Entry(_frame, textvariable=new_adjective)
        _entry.grid()
        _entry.focus()
        ok_btn = Button(_frame, text="OK", padx=25, pady=5, command=ok_btn)
        ok_btn.grid()

    def reload_game(self):
        # Updates db from last game run, preserving entries to next run
        global DISHES
        DISHES = self.game.dishes_db
        self.main_interface()
