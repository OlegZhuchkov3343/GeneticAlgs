import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import exit
from random import randint


class TkWindow(tk.Tk):
    def finish(self):
        self.destroy()
        exit()

    def __init__(self, data, params, functions):
        super().__init__()
        self.geometry("1000x650")
        self.resizable(False, False)
        self.response = None
        # Ссылки на единые поля данных для обеих структур
        self.data = data
        self.params = params
        # Функции для взаимодействия GUI с программой
        self.functions = functions
        frame = ttk.Frame(self)
        entry_frame = ttk.Frame(frame)
        ttk.Label(entry_frame, text="Размер популяции").grid(padx=5, pady=5, column=0, row=0, sticky=tk.W)
        param1 = ttk.Entry(entry_frame, width=15)
        param1.grid(padx=5, pady=5, column=1, row=0, sticky=tk.W)
        ttk.Label(entry_frame, text="Количество шагов (поколений)").grid(padx=5, pady=5, column=0, row=1, sticky=tk.W)
        param2 = ttk.Entry(entry_frame, width=15)
        param2.grid(padx=5, pady=5, column=1, row=1, sticky=tk.W)
        ttk.Label(entry_frame, text="Вероятность скрещивания").grid(padx=5, pady=5, column=0, row=2, sticky=tk.W)
        param3 = ttk.Entry(entry_frame, width=15)
        param3.grid(padx=5, pady=5, column=1, row=2, sticky=tk.W)
        ttk.Label(entry_frame, text="Вероятность мутации").grid(padx=5, pady=5, column=0, row=3, sticky=tk.W)
        param4 = ttk.Entry(entry_frame, width=15)
        param4.grid(padx=5, pady=5, column=1, row=3, sticky=tk.W)
        entry_frame.grid(column=0, row=0, sticky=tk.W)
        self.param_fields = {"population_size": param1,
                             "generations": param2,
                             "crossover_prob": param3,
                             "mutation_prob": param4}

        ttk.Button(frame, text="Случайный набор прямоугольников", command=self.random_input).grid(padx=5, pady=5, column=0, row=1, sticky=tk.W)
        ttk.Button(frame, text="Ручной ввод данных", command=self.manual_input).grid(padx=5, pady=5, column=0, row=2, sticky=tk.W)
        ttk.Button(frame, text="Ввод данных из файла", command=self.file_input).grid(padx=5, pady=5, column=0, row=3, sticky=tk.W)
        ttk.Button(frame, text="Сброс выполняемого алгоритма", command=self.reset).grid(padx=5, pady=30, column=0, row=4, sticky=tk.W)
        ttk.Button(frame, text="Следующий шаг", command=self.next_step).grid(padx=5, pady=5, column=0, row=5, sticky=tk.W)
        ttk.Button(frame, text="Выполнить до конца", command=self.execute).grid(padx=5, pady=5, column=0, row=6, sticky=tk.W)
        ttk.Button(frame, text="Сгенерировать случайное решение", command=self.random_solution).grid(padx=5, pady=5, column=0, row=7, sticky=tk.W)

        frame.grid(column=0, row=0)

        plot_frame = ttk.Frame(self)
        plot_frame.grid(padx=5, pady=5, column=1, row=0)

        figure1 = Figure(figsize=(5,3))
        plot1 = figure1.add_subplot(1, 1, 1)
        plot1.set_title("Лучшая и средняя приспособленность на шаге")
        ax1 = figure1.gca()
        ax1.xaxis.get_major_locator().set_params(integer=True)
        ax1.yaxis.get_major_locator().set_params(integer=True)
        figure1.supylabel("Приспособленность")
        figure1.supxlabel("№ шага")
        self.canvas_suitability = FigureCanvasTkAgg(figure1, master=plot_frame)
        self.canvas_suitability.get_tk_widget().grid(row=0,column=0)

        figure2 = Figure(figsize=(5,3))
        plot2 = figure2.add_subplot(1, 1, 1)
        plot2.set_title("Графическое представление решения")
        ax2 = figure2.gca()
        ax2.xaxis.get_major_locator().set_params(integer=True)
        ax2.yaxis.get_major_locator().set_params(integer=True)
        figure2.supylabel("Ширина")
        figure2.supxlabel("Длина")
        self.canvas_solution = FigureCanvasTkAgg(figure2, master=plot_frame)
        self.canvas_solution.get_tk_widget().grid(row=1,column=0)

        info_frame = ttk.Frame(self)
        info_frame.grid(row=0, column=2)
        self.info_text = ttk.Label(info_frame, wraplength=200,
                                   text="Здесь будет выводиться информация о выполнении алгоритма:\nВведенные параметры, сведения о популяции и текущем лучшем решении")
        self.info_text.grid(row=0, column=0)
        self.protocol("WM_DELETE_WINDOW", self.finish)

    def input_popup(self, prompt="", prefill=""):
        popup = tk.Toplevel(self)
        popup.geometry("400x400")
        popup.rowconfigure(1, weight=1)
        popup.columnconfigure(0, weight=1)
        label = tk.Label(popup, wraplength=400, justify='left', text=prompt)
        label.grid(row=0, column=0, sticky=tk.W)
        entry = tk.Text(popup)
        entry.grid(row=1, column=0, sticky=tk.NSEW)
        entry.insert("1.0", prefill)

        def ok():
            self.response = entry.get("1.0", tk.END).strip()
            popup.destroy()

        ok_button = tk.Button(popup, text="OK", command=ok)
        ok_button.grid(row=2, column=0)
        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)

    # Методы ввода данных
    def manual_input(self):
        self.input_popup(
            "Введите: ширину полосы N и количество прямоугольников M через пробел; на следующих N строках через пробел ширину и длину Wi и Li",
            (f"{self.data["n"]} {self.data["width"]}\n{'\n'.join([" ".join(map(str, line)) for line in self.data["rectangles"]])}" if
             self.data["n"] else ""))
        processed = [tuple(map(int, line.strip().split())) for line in self.response.split("\n")]
        self.data["n"] = processed[0][0]
        self.data["width"] = processed[0][1]
        self.data["rectangles"] = tuple(processed[1:])

    def random_input(self):
        #TODO: ввод параметров для случайной генерации входных данных
        min_side = 1
        max_side = 20
        self.data["n"] = 20
        self.data["width"] = 40
        self.data["rectangles"] = tuple([(randint(min_side, max_side), randint(min_side, max_side)) for i in range(self.data["n"])])

    def file_input(self):
        filepath = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filepath:
            with open(filepath, "r") as file:
                processed = [tuple(map(int, line.strip().split())) for line in file.read().strip().split('\n')]
                self.data["n"] = processed[0][0]
                self.data["width"] = processed[0][1]
                self.data["rectangles"] = tuple(processed[1:])

    def draw_solution(self):
        ax = self.canvas_solution.figure.gca()
        ax.cla()
        ax.set_title("Графическое представление решения")
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.yaxis.get_major_locator().set_params(integer=True)
        length, placed = self.functions["get_displayed_solution"]()
        ax.set_ylim(0, self.data["width"])
        ax.set_xlim(0, length)
        for rectangle in placed:
            rect = Rectangle((rectangle[1], rectangle[0]), rectangle[3], rectangle[2], linewidth=1, edgecolor='black',
                             facecolor='lightblue')
            ax.add_patch(rect)
        self.canvas_solution.draw()

    def reset(self):
        pass

    def execute(self):
        pass

    def next_step(self):
        pass

    def random_solution(self):
        self.functions["generate_random_solution"]()
        self.draw_solution()
