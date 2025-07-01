from modules.interface import TkWindow
from modules.model import StripPackingGenAlg

global StripePacking


def get_analytical_info():
    info = {
        "best_solution": StripePacking.get_best_solution(),
        #остальная информация для вывода на экран
    }
    return info


def start_algorithm():
    global StripePacking
    StripePacking = StripPackingGenAlg(data, params)


def restart_algorithm():
    global StripePacking
    prev_data = StripePacking.get_data()
    StripePacking = StripPackingGenAlg(data, params)


def next_step():
    StripePacking.next_step()


def execute():
    StripePacking.execute()


def get_status():
    if StripePacking:
        return StripePacking.status()
    else:
        return "idle"


def reset():
    global StripePacking
    StripePacking = None


if __name__ == "__main__":
    data = {
        "n": 0,
        "width": 0,
        "rectangles": tuple(),
    }
    params = {
        "population_size": 0,
        "generations": 0,
        "crossover_prob": 0.0,
        "mutation_prob": 0.0,
        "sample_size": 0
    }
    functions = {
        "get_analytical_info": get_analytical_info,
        "next_step": next_step,
        "execute": execute,
        "reset": reset,
        "get_status": get_status
    }
    StripePacking = None
    window = TkWindow(data, params, functions)
    window.mainloop()