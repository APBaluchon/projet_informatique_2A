from abc import ABC, abstractmethod


class Graph(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.indicators_dict = dict()
        self.calculate_indicators()
        self.display_graph()

    @abstractmethod
    def calculate_indicators(self):
        pass

    @abstractmethod
    def display_graph(self):
        pass