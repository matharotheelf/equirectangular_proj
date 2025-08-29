import moderngl
import numpy as np
import math
from enum import Enum

from src.strip_cell import StripCell

class Strip:
    def __init__(self, row, next_row, row_index, mesh):
        vertices = self.generate_vertices(row, next_row, row_index, mesh)

        self.triangles = self.generate_triangle_strip(vertices)

    def generate_vertices(self, row, next_row, row_index, mesh, start_index=0):
        strip_vertices = []

        for column_index, coordinate in enumerate(row[:-1]):
            coordinate_cell = StripCell(coordinate, row, next_row, column_index, row_index, mesh.base_colour, mesh.alpha, shift_index=start_index)
            coord_vertices, is_split = coordinate_cell.generate_vertices()

            if coord_vertices is not None:
                if is_split:
                    strip_vertices.extend(coord_vertices[0])

                    split_vertices = coord_vertices[1]

                    split_vertices.extend(self.generate_vertices(row[column_index + 1:], next_row[column_index + 1:], row_index, mesh, start_index = column_index + 1)[0])
                    return [strip_vertices, split_vertices]
                else:
                    strip_vertices.extend(coord_vertices)

        return [strip_vertices]

    def generate_triangle_strip(self, vertices):
        triangle_strips = []

        for index, vertex_set in enumerate(vertices):
            triangle_strip = np.array(vertex_set, dtype='f4').ravel()
            triangle_strips.append(triangle_strip)

        return triangle_strips
