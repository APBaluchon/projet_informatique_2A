from business_layer.service.graphs.graph import Graph


class SupportGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "UTILITY")

