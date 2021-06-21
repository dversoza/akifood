from tkinter import *
from tkinter import messagebox as mb

from settings import *


class BaseUI:
    # Base user interface
    def __init__(self, width=None, height=None, *args, **kwargs) -> None:
        """Pass options to base UI using kwargs"""
        self.app_width = width if width else APP_DEFAULT_WIDTH
        self.app_height = height if height else APP_DEFAULT_HEIGHT

        # Centers UI window to user screen
        self.root = Tk()
        self.center_window(self.root)

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


class AkiFoodUI(BaseUI):
    def __init__(self, controller, game) -> None:
        super().__init__()
        self.controller = controller
        self.game = game
        self.main_interface()

    def main_interface(self):
        def btn_handler(event=None):
            self.controller.game_next_step()
            _frame.destroy()

        _frame = self.mainframe(self.root)
        self.root.title(APP_TITLE)

        Label(_frame, text='Seja bem-vindo ao AkiFood!').grid()
        Label(_frame, text='Pense em um prato que gosta ...').grid()
        Button(_frame, text="Iniciar", padx=25,
               pady=5, command=btn_handler).grid()

        _frame.focus()
        self.root.bind('<Return>', btn_handler)

    def attempt_adjective_form(self, adjective: str):
        def true_btn():
            self.game.update_adjective_status(adjective, True)
            self.controller.game_next_step()
            _frame.destroy()

        def false_btn():
            self.game.update_adjective_status(adjective, False)
            self.controller.game_next_step()
            _frame.destroy()

        _frame = self.mainframe(self.root)

        question = Label(
            _frame, text=f'O prato que você pensou é {adjective}?')
        question.grid(column=0, row=0, columnspan=2)
        yes_btn = Button(_frame, padx=25, pady=5, text="Sim", command=true_btn)
        yes_btn.grid(column=0, row=1)
        no_btn = Button(_frame, padx=25, pady=5, text="Não", command=false_btn)
        no_btn.grid(column=1, row=1)

    def attempt_dish_form(self, dish: str):
        def true_btn():
            mb.showinfo('Uhul!', 'Acertei de novo!')
            _frame.destroy()
            self.controller.reload_game()

        def false_btn():
            self.root.title('Errei... Desisto')
            _frame.destroy()
            self.controller.wrong_attemp_handler(wrong_dish=dish)

        _frame = self.mainframe(self.root)

        Label(_frame, text=f"Ahá! Então seu prato é {dish}?").grid(
            columnspan=2)
        yes_btn = Button(_frame, text="Sim", padx=25, pady=5, command=true_btn)
        yes_btn.grid(column=0, row=1)
        yes_btn.focus()
        no_btn = Button(_frame, text="Não", padx=25, pady=5, command=false_btn)
        no_btn.grid(column=1, row=1)

    def new_dish_form(self, attempted_wrong_dish: str = None):
        def btn_handler(event=None):
            if new_dish_name.get() is None:
                Label(_frame, text='Preencha o nome do prato para continuar!').grid()
                return

            elif attempted_wrong_dish:
                _frame.destroy()
                self.controller.ask_for_new_adjective(
                    attempted_wrong_dish, new_dish_name.get())

            # If no dish attempted (no options availabe), only creates a new one
            else:
                _frame.destroy()
                self.controller.create_new_dish_handler(new_dish_name.get())

        _frame = self.mainframe(self.root)

        Label(_frame, text='Aproveitando que você ainda está ai...').grid()
        Label(_frame, text='Em que prato pensou?').grid()

        new_dish_name = StringVar()
        _entry = Entry(_frame, textvariable=new_dish_name)
        _entry.grid()
        _entry.focus()

        Button(_frame, text="OK", padx=25, pady=5, command=btn_handler).grid()

        self.root.bind('<Return>', btn_handler)

    def new_adjective_form(self, wrong_dish, right_dish):
        def btn_handler(event=None):
            _frame.destroy()
            self.controller.new_adjective_handler(
                wrong_dish, right_dish, new_adjective.get())

        _frame = self.mainframe(self.root)

        Label(_frame, text="Se puder me ajudar a ficar mais inteligente ...").grid()
        Label(_frame,
              text=f"{right_dish} é ______, mas {wrong_dish} não."
              ).grid()

        new_adjective = StringVar()
        _entry = Entry(_frame, textvariable=new_adjective)
        _entry.grid()
        _entry.focus()

        Button(_frame, text="OK", padx=25, pady=5, command=btn_handler).grid()

        self.root.bind('<Return>', btn_handler)
