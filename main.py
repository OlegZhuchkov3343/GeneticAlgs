from modules import interface, model


def generate_random_solution():
    global random_solution
    random_solution = model.place_rectangles(model.random_permutations(len(data["rectangles"]), 1)[0], data["rectangles"], data["width"])


def get_displayed_solution():
    if StripePacking == None:
        return random_solution


if __name__ == "__main__":
    data = {
        "n": 0,
        "width": 0,
        "rectangles": tuple(),
    }
    params = {
        "population_size": 0,
        "generations": 0,
        "crossover_prob": 0,
        "mutation_prob": 0,
    }
    functions = {
        "generate_random_solution": generate_random_solution,
        "get_displayed_solution": get_displayed_solution
    }
    StripePacking = None
    random_solution = None
    window = interface.TkWindow(data, params, functions)
    window.mainloop()