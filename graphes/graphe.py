from abc import ABC, abstractmethod


class Graphe(ABC):

    def __init__(self, pseudo):
        self.calculate_indicators()
        self.display_graph()

    @abstractmethod
    def calculate_indicators(self):
        pass

    @abstractmethod
    def display_graph(self):
        pass