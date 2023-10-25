from business_layer.service.graphs.graph import Graph


class TopGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "TOP")
