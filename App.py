import tkinter as tk
from tkinter import ttk
from math import ceil, floor
from PIL import ImageTk, Image
import re


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')

        self.title('Չիկի-Պուկի')
        icon = tk.PhotoImage(file='info.png')
        self.iconphoto(False, icon)

        self.length = tk.StringVar()
        self.unit_count = tk.StringVar()
        self.unit_width = tk.StringVar()
        self.spacing = tk.StringVar()

        self.uc_length = tk.StringVar()
        self.uc_unit_width = tk.StringVar()
        self.uc_spacing = tk.StringVar()
        self.uc_unit_count = tk.StringVar()

        self.vcmd = (self.register(self.validate), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        self.create_image_widget()
        self.create_spacing_widget()
        self.create_unit_counting_widgets()

    def create_image_widget(self):
        image_frame = tk.Frame(self, bg='black', width=640, height=452, borderwidth=2)
        image_frame.grid(row=0, column=0, padx=10, pady=20)
        photo = ImageTk.PhotoImage(Image.open("img.jpg").resize((640, 452), Image.ANTIALIAS))

        label = ttk.Label(image_frame, image=photo, background='green')
        label.image = photo
        label.pack()

    def create_spacing_widget(self):
        l = ttk.Label(text="Հաշվել արանքի չափը (սմ)", foreground="yellow", font='Helvetica 12 bold')
        spacing_frame = ttk.LabelFrame(self, labelwidget=l)
        spacing_frame.grid(row=0, column=1, padx=10, pady=11, sticky="nw")

        ttk.Label(spacing_frame, text="Երկարություն").grid(column=0, row=0)
        length_entry = ttk.Entry(spacing_frame, width=7, textvariable=self.length)
        length_entry.grid(column=1, row=0)

        ttk.Label(spacing_frame, text="Քանակ").grid(column=0, row=1, sticky="w")
        unit_count_entry = ttk.Entry(spacing_frame, width=7, textvariable=self.unit_count)
        unit_count_entry.grid(column=1, row=1)

        ttk.Label(spacing_frame, text="Միավորի լայնություն").grid(column=0, row=2)
        unit_width_entry = ttk.Entry(spacing_frame, width=7, textvariable=self.unit_width)
        unit_width_entry.grid(column=1, row=2)


        spacing_answer = ttk.Label(spacing_frame, textvariable=self.spacing,
                                     font = ('courier', 13, 'bold'), foreground="green")
        spacing_answer.grid(column=1, row=3)

        self.button1 = ttk.Button(spacing_frame, text="Հաշվել", command=self.spacing_calc)
        self.button1.grid(column=0, row=4, sticky="w", columnspan=2)

        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)

        for widget in spacing_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5, sticky="nws")
            if widget.winfo_class() == 'TEntry':
                widget.configure(validate="focusout", validatecommand=self.vcmd, invalidcommand=self.ivcmd)

    def create_unit_counting_widgets(self):
        l = ttk.Label(text="Հաշվել միավորի քանակը (սմ)", foreground="yellow", font='Helvetica 12 bold')
        self.uc_frame = ttk.LabelFrame(self, labelwidget=l)
        self.uc_frame.grid(row=0, column=1, padx=10, pady=20, sticky="ws")

        ttk.Label(self.uc_frame, text="Երկարություն").grid(column=0, row=0)
        length2_entry = ttk.Entry(self.uc_frame, width=7, textvariable=self.uc_length)
        length2_entry.grid(column=1, row=0, padx=10, pady=5, sticky="news")

        ttk.Label(self.uc_frame, text="Արանքի չափ").grid(column=0, row=1)
        unit_count_entry2 = ttk.Entry(self.uc_frame, width=7, textvariable=self.uc_spacing)
        unit_count_entry2.grid(column=1, row=1)

        ttk.Label(self.uc_frame, text="Միավորի լայնություն").grid(column=0, row=2)
        unit_width_entry2 = ttk.Entry(self.uc_frame, width=7, textvariable=self.uc_unit_width)
        unit_width_entry2.grid(column=1, row=2)

        uc_answer = tk.Label(self.uc_frame, textvariable=self.uc_unit_count, font=('courier', 13, 'bold'), foreground="green")
        uc_answer.grid(column=1, row=3)
        button2 = ttk.Button(self.uc_frame, text="Հաշվել", command=self.unit_counting)
        button2.grid(column=0, row=4)

        for widget in self.uc_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5, sticky="nws")
            if widget.winfo_class() == 'TEntry':
                widget.configure(validate="focusout", validatecommand=self.vcmd, invalidcommand=self.ivcmd)

    def spacing_calc(self):
        try:
            len1 = float(self.length.get())
            u_count = float(self.unit_count.get())
            u_width = float(self.unit_width.get())
            space = (len1 - u_count * u_width) / (u_count + 1)
            self.spacing.set(round(space, 2))
        except (ValueError, ZeroDivisionError):
            pass

    def unit_counting(self):
        try:
            length = float(self.uc_length.get())
            u_width = float(self.uc_unit_width.get())
            space = float(self.uc_spacing.get())
            unit_cnt = (length + u_width) / (space + u_width) - 1
            if (unit_cnt % 1) % 10 != 0:
                up_cnt = ceil(unit_cnt)
                down_cnt = floor(unit_cnt)
                spacing_up = self.spacing_calc2(length, up_cnt, u_width)
                spacing_down = self.spacing_calc2(length, down_cnt, u_width)
                answer = ttk.Label(self.uc_frame, text="Կլոր թիվ չի ստացվում.\n արանքի չափը կլինի՝", font="Helvetica 10 italic").grid(column=0, row=3)
                self.uc_unit_count.set(
                    f"{up_cnt} հատի դեպքում։ {round(spacing_up, 2)}\n{down_cnt} հատի դեպքում։ {round(spacing_down, 2)}")
            else:
                self.uc_unit_count.set(int(unit_cnt))
        except (ValueError, ZeroDivisionError):
            pass

    @staticmethod
    def spacing_calc2(length, count, unit_width):
        spacing = (length - count * unit_width) / (count + 1)
        return spacing

    def show_empty_entry_error(self, error=''):
        self.label_error['text'] = error

    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        # self.email_entry['foreground'] = color

    def validate(self, value):
        """
        Validate the email entry
        :param value:
        :return:
        """
        pattern = r'\b([0-9]*[.])?[0-9]+\b'
        if re.fullmatch(pattern, value) is None:
            self.show_message()
            return False

        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.show_message('Թույլատրվում են միայն դրական իրական թվեր', 'red')

if __name__ == '__main__':
    app = App()
    app.mainloop()