from abc import ABC, abstractmethod


class Graph(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.indicators = dict()
        self.calculate_indicators()
        self.display_graph()

    @abstractmethod
    def calculate_indicators(self):
        pass

    @abstractmethod
    def display_graph(self):
        pass


    def interpolate(self, val, before_min, before_max):
        if before_min == before_max:
            return None
        
        if val <= before_min:
            return 0
        if val >= before_max:
            return 1

        proportion = (val - before_min) / (before_max - before_min)
        return proportion

