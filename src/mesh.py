import moderngl
import numpy as np

class Mesh:
    def __init__(self, program, panel):
        self.colour = panel.colour
        self.ctx = moderngl.get_context()
        self.triangles = self.generate_mesh(panel.equi_coordinates)
        self.program = program
        #
        # self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        # self.vao = self.ctx.vertex_array(program, [(self.vbo, '3f 12x 8x', 'in_vertex')])

    def render(self):
        for triangle in self.triangles:
            vertices_buffer = triangle.tobytes()
            vbo = self.ctx.buffer(vertices_buffer)
            vao = self.ctx.vertex_array(self.program, [(vbo, '2f', 'in_vertex')])

            vao.program['color'] = self.colour
            vao.render()

    def generate_mesh(self, coordinate_rows):
        """
        Generate mesh from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        triangle_mesh = []

        for row_index, row in enumerate(coordinate_rows[:-1]):
            next_row = coordinate_rows[row_index + 1]

            for column_index, coordinate in enumerate(row[:-1]):
                right_coordinate = row[column_index + 1]
                bottom_coordinate = next_row[column_index]

                vertices = np.asarray([
                    coordinate,
                    right_coordinate,
                    bottom_coordinate

                ], dtype='f4').ravel()

                triangle_mesh.append(vertices)

        return triangle_mesh
