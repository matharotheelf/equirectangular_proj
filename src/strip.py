import moderngl
import numpy as np
import math
from enum import Enum

from src.strip_cell import StripCell

class Strip:
    def __init__(self, row, next_row, row_index, mesh):
        vertices = self.generate_vertices(row, next_row, row_index, mesh)

        self.triangles = self.generate_triangle_strip(vertices)

    def generate_vertices(self, row, next_row, row_index, mesh):
        strip_vertices = []

        for column_index, coordinate in enumerate(row[:-1]):
            coordinate_cell = StripCell(coordinate, row, next_row, column_index, row_index, mesh.base_colour, mesh.alpha)
            coord_vertices, is_split = coordinate_cell.generate_vertices()

            if coord_vertices is not None:
                if is_split:
                    strip_vertices.extend(coord_vertices[0])

                    split_strip_vertices = [coord_vertices[1]]

                    split_strip_vertices.extend(self.generated_vertices(row[column_index:], next_row[column_index:], row_index, mesh))

                    return [strip_vertices, split_strip_vertices]
                else:
                    strip_vertices.extend(coord_vertices)

        return [strip_vertices]

    def generate_triangle_strip(self, vertices):
        triangle_strips = []

        for vertex_set in vertices:
            triangle_strip = np.array(vertex_set, dtype='f4').ravel()
            triangle_strips.append(triangle_strip)

        return triangle_strips
