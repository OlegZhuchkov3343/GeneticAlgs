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
        self.geometry("1100x850")
        self.resizable(False, False)
        self.response = None
        self.data = data
        self.params = params
        # Функции для взаимодействия GUI с программой
        self.functions = functions
        self.finished = False
        frame = ttk.Frame(self)
        entry_frame = ttk.Frame(frame)
        ttk.Label(entry_frame, text="Размер популяции\n(нат. число)").grid(padx=5, pady=5, column=0, row=0, sticky=tk.W)
        param1 = ttk.Entry(entry_frame, width=15)
        param1.grid(padx=5, pady=5, column=1, row=0, sticky=tk.W)
        param1.insert("0", "100")
        ttk.Label(entry_frame, text="Количество поколений\n(нат. число)").grid(padx=5, pady=5, column=0, row=1, sticky=tk.W)
        param2 = ttk.Entry(entry_frame, width=15)
        param2.grid(padx=5, pady=5, column=1, row=1, sticky=tk.W)
        param2.insert("0", "100")
        ttk.Label(entry_frame, text="Нижний порог разницы\nсреднего и минимума\n(float > 0)").grid(padx=5, pady=5, column=0, row=2, sticky=tk.W)
        param6 = ttk.Entry(entry_frame, width=15)
        param6.grid(padx=5, pady=5, column=1, row=2, sticky=tk.W)
        param6.insert("0", "1.0")
        ttk.Label(entry_frame, text="Вероятность скрещивания\n(0.0 <= float <= 1.0)").grid(padx=5, pady=5, column=0, row=4, sticky=tk.W)
        param3 = ttk.Entry(entry_frame, width=15)
        param3.insert("0", "0.9")
        param3.grid(padx=5, pady=5, column=1, row=4, sticky=tk.W)
        ttk.Label(entry_frame, text="Вероятность мутации\n(0.0 <= float <= 1.0)").grid(padx=5, pady=5, column=0, row=5, sticky=tk.W)
        param4 = ttk.Entry(entry_frame, width=15)
        param4.insert("0", "0.1")
        param4.grid(padx=5, pady=5, column=1, row=5, sticky=tk.W)
        ttk.Label(entry_frame, text="Количество отбираемых родителей\n(2 <= int <= pop_size)").grid(padx=5, pady=5, column=0, row=3, sticky=tk.W)
        param5 = ttk.Entry(entry_frame, width=15)
        param5.insert("0", "20")
        param5.grid(padx=5, pady=5, column=1, row=3, sticky=tk.W)
        entry_frame.grid(column=0, row=0, sticky=tk.W)
        self.param_fields = {"population_size": param1,
                             "generations": param2,
                             "crossover_prob": param3,
                             "mutation_prob": param4,
                             "sample_size": param5,
                             "diff": param6
                             }

        ttk.Button(frame, text="Случайный набор прямоугольников", command=self.random_input).grid(padx=5, pady=5, column=0, row=1, sticky=tk.W)
        ttk.Button(frame, text="Ручной ввод данных", command=self.manual_input).grid(padx=5, pady=5, column=0, row=2, sticky=tk.W)
        ttk.Button(frame, text="Ввод данных из файла", command=self.file_input).grid(padx=5, pady=5, column=0, row=3, sticky=tk.W)
        ttk.Button(frame, text="Сброс", command=self.reset_button).grid(padx=5, pady=30, column=0, row=4, sticky=tk.W)
        ttk.Button(frame, text="Следующий шаг", command=self.next_step_button).grid(padx=5, pady=5, column=0, row=5, sticky=tk.W)
        ttk.Button(frame, text="Шаг назад", command=self.step_back_button).grid(padx=5, pady=5, column=0, row=6, sticky=tk.W)
        ttk.Button(frame, text="Выполнить до\nмакс. количества поколений", command=self.execute_button).grid(padx=5, pady=5, column=0, row=7, sticky=tk.W)
        ttk.Button(frame, text="Выполнить до условия остановки\n(разница ниже порога)", command=self.executediff_button).grid(padx=5, pady=5, column=0, row=8, sticky=tk.W)
        ttk.Button(frame, text="Приостановить работу", command=self.pause_button).grid(padx=5, pady=5, column=0,
                                                                                             row=9, sticky=tk.W)
        ttk.Button(frame, text="Перезапуск с параметрами", command=self.restart_button).grid(padx=5, pady=30, column=0, row=10, sticky=tk.W)

        frame.grid(column=0, row=0)

        plot_frame = ttk.Frame(self)
        plot_frame.grid(padx=5, pady=5, column=1, row=0)

        figure1 = Figure(figsize=(5,4))
        plot1 = figure1.add_subplot(1, 1, 1)
        plot1.set_title("Лучшая и средняя приспособленность на шаге")
        ax1 = figure1.gca()
        ax1.xaxis.get_major_locator().set_params(integer=True)
        ax1.yaxis.get_major_locator().set_params(integer=True)
        figure1.supylabel("Приспособленность")
        figure1.supxlabel("№ поколения")
        self.canvas_suitability = FigureCanvasTkAgg(figure1, master=plot_frame)
        self.canvas_suitability.get_tk_widget().grid(row=0,column=0)

        figure2 = Figure(figsize=(5,4))
        plot2 = figure2.add_subplot(1, 1, 1)
        plot2.set_title("Графическое представление решения")
        ax2 = figure2.gca()
        ax2.xaxis.get_major_locator().set_params(integer=True)
        ax2.yaxis.get_major_locator().set_params(integer=True)
        figure2.supylabel("Ширина")
        figure2.supxlabel("Длина")
        self.canvas_solution = FigureCanvasTkAgg(figure2, master=plot_frame)
        self.canvas_solution.get_tk_widget().grid(row=1,column=0)

        self.info_text = ttk.Label(self, wraplength=250,
                                   text="Здесь будет выводиться информация о выполнении алгоритма:\nВведенные параметры, сведения о популяции и текущем лучшем решении")
        self.info_text.grid(row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

        self.status_label = ttk.Label(self, wraplength=700)
        self.status_label.grid(row=1, column=0, columnspan=3)
        self.update_status()

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
        self.input_popup("Введите через пробел: ширину полосы N, количество прямоугольников M, минимальную и максимальную длины стороны прямоугольника",
                         "40 20 1 20")
        processed = [int(i) for i in self.response.split()]
        min_side = processed[2]
        max_side = processed[3]
        self.data["n"] = processed[1]
        self.data["width"] = processed[0]
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

    def update_params(self):
        for param in self.param_fields:
            self.params[param] = float(self.param_fields[param].get())

    def draw_solution(self, solution, length, width):
        ax = self.canvas_solution.figure.gca()
        ax.cla()
        ax.set_title("Графическое представление решения")
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.set_ylim(0, width)
        ax.set_xlim(0, length)
        for rectangle in solution:
            rect = Rectangle((rectangle[1], rectangle[0]), rectangle[3], rectangle[2], linewidth=1, edgecolor='black',
                             facecolor='lightblue')
            ax.add_patch(rect)
        self.canvas_solution.draw()

    def update_pop_graph(self, avg, minimum):
        n = len(avg)
        canvas = self.canvas_suitability
        ax = canvas.figure.gca()
        ax.cla()
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.plot(range(1, n+1), avg, label="Средняя", color="black", linestyle="--")
        ax.plot(range(1, n+1), minimum, label="Минимальная", color="black", linestyle="-")
        ax.legend()
        ax.set_title("Лучшая и средняя приспособленность на шаге")
        canvas.draw()

    def reset_button(self):
        self.functions["unpause"]()
        self.functions["reset"]()
        self.update_window()

    def execute_button(self):
        self.finished = False
        self.functions["unpause"]()
        self.update_params()
        while self.functions["get_status"]() not in ["pause", "generation limit", "generation+diff limit"]:
            self.functions["next_step"]()
            self.update_window()
        self.finished = True
        self.update_window()

    def executediff_button(self):
        self.finished = False
        self.functions["unpause"]()
        self.update_params()
        while self.functions["get_status"]() not in ["diff limit", "pause", "generation+diff limit"]:
            self.functions["next_step"]()
            self.update_window()
        self.finished = True
        self.update_window()

    def next_step_button(self):
        self.functions["unpause"]()
        self.update_params()
        self.functions["next_step"]()
        self.update_window()

    def restart_button(self):
        self.functions["unpause"]()
        self.update_params()
        self.functions["restart"]()
        self.functions["next_step"]()
        self.update_window()

    def pause_button(self):
        self.functions["pause"]()

    def step_back_button(self):
        if self.functions["get_status"]() not in ["idle", "init"]:
            self.functions["step_back"]()
        self.update_window()

    def update_status(self):
        status = self.functions["get_status"]()
        if status == "idle":
            self.status_label.config(text="Алгоритм не запущен, введите данные и параметры и нажмите \'Следующий шаг\' или \'Выполнить до конца\'")
        elif status == "pause":
            self.status_label.config(text="Алгоритм приостановлен")
        elif not self.finished:
            self.status_label.config(text="Алгоритм запущен")
        else:
            self.status_label.config(text="Алгоритм завершил работу, нажмите \'Перезапуск с параметрами\', чтобы запустить алгоритм с новыми параметрами и старыми данными, или \'Сброс\', чтобы удалить старые данные")
        return

    def update_window(self):
        self.update_status()
        info = self.functions["get_analytical_info"]()
        if info:
            solution = info["best_solution"][1]
            solution_len = info["best_solution"][0]
            text = (f"Ширина полосы: {info["width"]}\nКоличество прямоугольников: {info["rect_count"]}\n"
                    f"Текущее поколение: {info["cur_generation"]}\nВсего поколений: {info["generations"]}\n"
                    f"Размер популяции: {info["pop_size"]}\nКоличество отбираемых родителей: {info["sample_size"]}\n"
                    f"Вероятность скрещивания: {info["cross_prob"]}\nВероятность мутации: {info["mut_prob"]}\n"
                    f"Средняя приспособленность: {round(info["avg_suitability"][-1], 3)}\nМинимальная приспособленность: {info["min_suitability"][-1]}\n"
                    f"Отображено лучшее решение в поколении, длина: {solution_len}\n"
                    f"Минимум за всю работу алгоритма: {min(info["min_suitability"])}")
            self.draw_solution(solution, solution_len, info["width"])
            self.update_pop_graph(info["avg_suitability"], info["min_suitability"])
        else:
            text = "Здесь будет выводиться информация о выполнении алгоритма:\nВведенные параметры, сведения о популяции и текущем лучшем решении"
            self.canvas_solution.figure.gca().cla()
            self.canvas_suitability.figure.gca().cla()
        self.info_text.config(text=text)
        self.update()

