import numpy as np
from random import random
import tkinter as tk
import tkinter.ttk as ttk
from tksheet import Sheet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DataTable(Sheet):
    def __init__(self, master):
        self.__data = []
        super().__init__(master, data=self.__data, headers=["x", "y", "p"])
        self.sheet_display_dimensions(total_columns=3)
        self.enable_bindings()
        self.extra_bindings([("end_edit_cell", self.__end_edit_cell)])
        self.__callbacks = []

    def add_point(self, x, y, p=1):
        self.__data.append([x, y, p])

    def add_callback(self, callback):
        self.__callbacks.append(callback)

    def __end_edit_cell(self, event):
        for c in self.__callbacks:
            c()

    def randomize_data(self, xmin, ymin, xmax, ymax, n=10):
        self.__data.clear()
        for i in range(n):
            x = round(xmin + random() * (xmax - xmin), 2)
            y = round(ymin + random() * (ymax - ymin), 2)
            self.__data.append([x, y, 1])
        self.__data.sort(key=lambda d: d[0])
        self.set_sheet_data(self.__data)

    def get_data(self) -> list:
        return self.__data


class Plotter(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.__figure = Figure()
        self.__plot = self.__figure.add_subplot()
        self.__canvas = FigureCanvasTkAgg(self.__figure, master=self)
        self.__canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.plot_data()

    def plot_data(self, data=None, approx=None):
        self.__plot.clear()
        self.__plot.set_title("Наилучшее ср.кв. приближение")
        self.__plot.set_xlabel("x")
        self.__plot.set_ylabel("y")
        if data is not None:
            X = [row[0] for row in data]
            Y = [row[1] for row in data]
            self.__plot.plot(X, Y, "ro", label="данные")
            self.__plot.legend()
        if approx is not None:
            colors = (None, "r", "g", "b", "y")
            styles = (None, "-", "-", "-", "-")
            for n, X, Y in approx:
                self.__plot.plot(X, Y, colors[n] + styles[n], label=f"n = {n}")
            self.__plot.legend()
        self.__canvas.draw()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа №4")
        self.__configure_grid()

        self.plotter = Plotter(self)
        self.plotter.grid(row=0, column=0, sticky=tk.NSEW)

        self.data_table = DataTable(self)
        self.data_table.add_callback(self.__display_data)
        self.data_table.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        self.randomize_button = ttk.Button(self, text="случайные точки")
        self.randomize_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.SE)
        self.randomize_button.configure(command=self.randomize_action)

    def __configure_grid(self):
        rows = [14, 1]
        cols = [1, 1]

        for row, weight in enumerate(rows):
            self.rowconfigure(row, weight=weight)

        for col, weight in enumerate(cols):
            self.columnconfigure(col, weight=weight)

    def feed_approximator(self, approx_factory):
        self.approx_factory = approx_factory
        return self
    
    def __display_data(self):
        data = self.data_table.get_data()
        approx = []

        if self.approx_factory is not None:
            X = [float(row[0]) for row in data]
            Y = [float(row[1]) for row in data]
            W = [float(row[2]) for row in data]
            for n in 1, 2, 4:
                func = self.approx_factory(X, Y, W, n)
                X_ext = np.linspace(min(X), max(X), 200)
                Y_ext = [func(x) for x in X_ext]
                approx.append([n, X_ext, Y_ext])

        self.plotter.plot_data(data, approx)

    def randomize_action(self):
        self.data_table.randomize_data(0, 0, 100, 100, n=6)
        self.__display_data()
