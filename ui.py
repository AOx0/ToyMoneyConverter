import sys
import tkinter as tk
from typing import Callable, NewType, Tuple


class UIElement:
    def __init__(self, name: str, element) -> None:
        self.name = name
        self.element = element


constructor = Callable[..., UIElement]
objet_id = NewType('objet_id', str)
row = NewType('row', int)
column = NewType('column', int)


class Ref:
    def __init__(self, obj): self.obj = obj

    def get(self): return self.obj

    def set(self, obj): self.obj = obj


class UICreationMethods:
    def __init__(self):
        self.window: tk.Tk | None = None
        self.object_frame: tk.Frame | None = None

    def entry(self, target: None, **kwargs) -> tk.Entry:
        entry = tk.Entry(master=self.object_frame, **kwargs)
        if target:
            entry.bind("<Return>", target)
        return entry

    def label(self, **kwargs) -> tk.Label:
        return tk.Label(master=self.object_frame, **kwargs)

    def frame(self, **kwargs) -> tk.Frame:
        return tk.Frame(master=self.window, **kwargs)

    def button(self, **kwargs) -> tk.Button:
        return tk.Button(master=self.object_frame, **kwargs)

    def dd_menu(self, store_in: list, options: tuple, **kwargs) -> tk.OptionMenu:
        command = kwargs['command'] if 'command' in kwargs else None
        if command:
            del kwargs['command']

        store_in.append(tk.StringVar(master=self.object_frame, **kwargs))
        store_in[0].set(options[0])
        if command:
            store_in[0].trace("w", command)
        menu = tk.OptionMenu(self.object_frame, store_in[0], *options)
        return menu


class UIGrid(UICreationMethods):
    def __init__(self, parent, *body: Tuple[int, int, str, str, dict]) -> None:
        super().__init__()
        self.object_frame = tk.Frame(parent)
        self.members = []

        for (ROW, COLUMN, NAME, CONSTRUCTOR, ARGS) in body:
            element = UIElement(NAME, self.__getattribute__(CONSTRUCTOR)(**ARGS))

            self.__setattr__(element.name, element.element)
            self.__getattribute__(element.name).grid(row=ROW, column=COLUMN)
            self.members.append(element)


class Window(UICreationMethods):
    def __init__(self):
        super().__init__()

        # Window config
        self.window = tk.Tk()
        self.window.title("Money Converter")

        self.window.geometry("420x300")
        self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(False, False)

        self.window.anchor = "center"
        self.main_frame = self.frame(width=420, height=300)
        self.main_frame.place(anchor=tk.CENTER, relx=.5, rely=.5)

        # All ui elements go in this one, which is later palced in the center of the main frame
        self.object_frame = tk.Frame()

        # Currency pickers options
        self.OPTIONS = ("USD", "MXN", "COL")

        # Used to store the value of currency pickers
        self.has = []
        self.wants = []

        def update_ui(*_, **__):
            print("Lmao")
            self.in_label.configure(
                text="Convert from " + str(self.has[0].get()) + " to " + str(self.wants[0].get()) + ":")

        def get_conversion(*_, **__):
            print(self.has_q.get(), self.wants_q.get(), self.has[0].get(), self.wants[0].get())

        def invert(*_, **__):
            temp = self.has[0].get()
            self.has[0].set(self.wants[0].get())
            self.wants[0].set(temp)

            temp = self.has_q.get()
            self.has_q.delete(0, 'end')
            self.has_q.insert(0, str(self.wants_q.get()))
            self.wants_q.delete(0, 'end')
            self.wants_q.insert(0, str(temp))

        # The body of the program
        self.body(
            UIElement('in_label', self.label(text="Convert from USD to USD:")),
            UIGrid(
                self.object_frame,
                (1, 0, 'has_q', 'entry', {'target': None}),
                (1, 1, 'has_picker', 'dd_menu', {'store_in': self.has, 'options': self.OPTIONS, 'command': update_ui}),
                (2, 0, 'wants_q', 'entry', {'target': None}),
                (
                    2, 1, 'wants_picker', 'dd_menu',
                    {'store_in': self.wants, 'options': self.OPTIONS, 'command': update_ui}
                ),
            ),
            UIGrid(
                self.object_frame,
                (0, 1, 'convert_button', 'button', {'text': "Convert", 'command': get_conversion}),
                (0, 0, 'invert_button', 'button', {'text': 'Invert', 'command': invert})
            )
        )

        # Last tweaks
        self.wants_q.bind("<Key>", lambda a: "break")
        self.wants[0].set('MXN')
        update_ui()

        self.object_frame.place(in_=self.main_frame, anchor=tk.CENTER, relx=.5, rely=.5)
        self.window.mainloop()

    def body(self, *args: UIElement or UIGrid):
        for element in args:
            if type(element) is UIElement:
                if hasattr(self, element.name):
                    print(
                        f"Error: `element.name` '{element.name}' (`element.element`: {element.element})\
 has the same id as `self.{element.name}` \
(value: {self.__getattribute__(element.name)})")
                    sys.exit(9)
                self.__setattr__(element.name, element.element)
                self.__getattribute__(element.name).pack()
            elif type(element) is UIGrid:
                for grid_element in element.members:
                    if hasattr(self, grid_element.name):
                        print(
                            f"Error: element.name ('{grid_element.name}' has the same id as `self.{grid_element.name}` \
(value: {self.__getattribute__(grid_element.name)})")
                        sys.exit(9)
                    self.__setattr__(grid_element.name, grid_element.element)

                element.object_frame.pack()


Window()
