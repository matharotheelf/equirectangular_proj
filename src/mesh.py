import moderngl
import numpy as np
import math

from src.cell import Cell

class Mesh:
    WIDTH_PLOT = 1
    MIDDLE_PLOT = 0

    def __init__(self, program, panel):
        self.base_colour = panel.base_colour
        self.alpha = 1.0
        self.ctx = moderngl.get_context()
        self.triangles = self.generate_mesh(panel.equi_coordinates)
        self.program = program

    def render(self, currentTime):
        for index, triangle in enumerate(self.triangles):
            vertices_buffer = triangle.tobytes()
            vbo = self.ctx.buffer(vertices_buffer)
            vao = self.ctx.vertex_array(self.program, [vbo.bind('in_vert', 'in_color', layout='2f 4f')])

            vao.program['time'] = currentTime / 10.0
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
                coordinate_cell = Cell(coordinate, row, next_row, column_index, row_index, self)
                coordinate_triangles = coordinate_cell.generate_triangles()

                if coordinate_triangles is not None:
                    triangle_mesh.extend(coordinate_triangles)
        return triangle_mesh
