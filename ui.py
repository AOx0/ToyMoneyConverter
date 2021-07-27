import sys
import tkinter as tk
from typing import Tuple


class UIElement:
    """
    This class wraps any element in the UI with its name. There can not be repeated names or 'ids'
    """
    def __init__(self, name: str, element) -> None:
        self.name = name
        self.element = element


class UICreationMethods:
    """
    A bunch of methods some classes may inherit for creating tkinter Widgets
    """
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
    """
    Class in charge of creating grids. All elements of the grid go into a custom frame that then is packed into
    its parent frame.

    Example:
        UIGrid(
                self.object_frame,
                (0, 0, 'has_q', 'entry', {'target': None}),
                (0, 1, 'has_pick', 'dd_menu', {'store_in': self.has, 'options': self.OPTIONS, 'command': update_ui}),
            ),

        Notice it receives the name of its parent frame and all elements as a tuples of:
            row: int, column: int, name: str, constructor: UICreationMethod, constructor_args: Dictionary

        Some of the methods defined within UICreationMethods may have some obligatory args for `constructor_args`
    """
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
    """
    The main program. Everything merges to conform the application's UI

    self.body is where all UI elements are declared. It expects types UIElement and UIGrid.
    """
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

        # All ui elements go in this one, which is later placed in the center of the main frame
        self.object_frame = tk.Frame()

        # Currency pickers options
        self.OPTIONS = ("USD", "MXN", "COL")

        # Used to store the value of currency pickers
        self.has = []
        self.wants = []

        def update_ui(*_, **__):
            self.in_label.configure(
                text="Convert from " + str(self.has[0].get()) + " to " + str(self.wants[0].get()) + ":")

        def get_conversion(*_, **__):
            pass

        def invert(*_, **__):
            temp = self.has[0].get()
            self.has[0].set(self.wants[0].get())
            self.wants[0].set(temp)

            temp = self.has_q.get()
            self.has_q.delete(0, 'end')
            self.has_q.insert(0, str(self.wants_q.get()))
            self.wants_q.delete(0, 'end')
            self.wants_q.insert(0, str(temp))

            get_conversion()

        # The body of the program
        self.body(
            UIElement('in_label', self.label(text="Convert from USD to USD:")),
            UIGrid(
                self.object_frame,
                (0, 0, 'has_q', 'entry', {'target': None}),
                (0, 1, 'has_pick', 'dd_menu', {'store_in': self.has, 'options': self.OPTIONS, 'command': update_ui})
            ),
            UIGrid(
                self.object_frame,
                (0, 0, 'wants_q', 'entry', {'target': None}),
                (0, 1, 'wants_pick', 'dd_menu', {'store_in': self.wants, 'options': self.OPTIONS, 'command': update_ui})
            ),
            UIGrid(
                self.object_frame,
                (0, 1, 'convert_button', 'button', {'text': "Convert", 'command': get_conversion}),
                (0, 0, 'invert_button', 'button', {'text': 'Invert', 'command': invert})
            )
        )

        # Last tweaks to UI
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
