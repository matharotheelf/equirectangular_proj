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
                triangle_mesh.append(self.upper_triangle(coordinate, column_index, row, next_row))
                triangle_mesh.append(self.lower_triangle(coordinate, column_index, row, next_row))

        return triangle_mesh

    def upper_triangle(self, coordinate, column_index, row, next_row):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        right_coordinate = row[column_index + 1]
        bottom_right_coordinate = next_row[column_index + 1]

        vertices = np.asarray([
            coordinate,
            right_coordinate,
            bottom_right_coordinate

        ], dtype='f4').ravel()

        return vertices

    def lower_triangle(self, coordinate, column_index, row, next_row):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        bottom_coordinate = next_row[column_index]
        bottom_right_coordinate = next_row[column_index + 1]

        vertices = np.asarray([
            coordinate,
            bottom_coordinate,
            bottom_right_coordinate

        ], dtype='f4').ravel()

        return vertices
