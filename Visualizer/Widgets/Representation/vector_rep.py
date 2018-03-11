from Visualizer.Widgets.Representation.matrix_rep import MatrixRep


class VectorRep(MatrixRep):
    def __init__(self):
        super(VectorRep, self).__init__()
        self.set_image_name("vector")
