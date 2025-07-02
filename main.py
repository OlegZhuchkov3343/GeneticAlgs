from modules.interface import TkWindow
from modules.model import StripPackingGenAlg

global StripePacking
global paused


def get_analytical_info():
    if get_status() == "idle":
        info = None
    else:
        info = StripePacking.get_info()
    return info


def start_algorithm():
    global StripePacking
    StripePacking = StripPackingGenAlg(data, params)


def restart_algorithm():
    global StripePacking
    prev_data = StripePacking.get_data()
    StripePacking = StripPackingGenAlg(prev_data, params)


def next_step():
    status = get_status()
    if status == "idle":
        start_algorithm()
    StripePacking.next_step()


def get_status():
    if paused:
        return "pause"
    if StripePacking:
        return StripePacking.status()
    else:
        return "idle"


def reset():
    print("reset")
    global StripePacking
    StripePacking = None


def pause():
    global paused
    paused = True


def unpause():
    global paused
    paused = False


def step_back():
    if StripePacking:
        StripePacking.step_back()


if __name__ == "__main__":
    paused = False
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
        "reset": reset,
        "get_status": get_status,
        "restart": restart_algorithm,
        "pause": pause,
        "unpause": unpause,
        "step_back": step_back
    }
    StripePacking = None
    window = TkWindow(data, params, functions)
    window.mainloop()