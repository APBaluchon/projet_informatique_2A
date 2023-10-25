from business_layer.service.graphs.graph import Graph

class MidGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "MIDDLE")