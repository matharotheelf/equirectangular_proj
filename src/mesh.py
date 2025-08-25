import moderngl
import numpy as np
import math

class Mesh:
    WIDTH_PLOT = 1

    def __init__(self, program, panel):
        self.base_colour = panel.base_colour
        self.alpha = 1.0
        self.ctx = moderngl.get_context()
        self.triangles = self.generate_mesh(panel.equi_coordinates)
        self.program = program

    def render(self):
        for index, triangle in enumerate(self.triangles):
            vertices_buffer = triangle.tobytes()
            vbo = self.ctx.buffer(vertices_buffer)
            vao = self.ctx.vertex_array(self.program, [vbo.bind('in_vert', 'in_color', layout='2f 4f')])
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
                coordinate_colour = self.coordinate_colour(row_index, column_index)

                coordinate_triangles = self.generate_triangles_for_coordinate(coordinate, row, next_row, column_index, coordinate_colour)
                triangle_mesh.extend(coordinate_triangles)
        return triangle_mesh

    def triangle(self, coordinate, horizontal_coordinate, vertical_coordinate, colour):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """
        colour_r, colour_g, colour_b, colour_a = colour

        vertices = np.asarray([
            coordinate[0], coordinate[1], colour_r, colour_g, colour_b, colour_a,
            horizontal_coordinate[0], horizontal_coordinate[1], colour_r, colour_g, colour_b, colour_a,
            vertical_coordinate[0], vertical_coordinate[1], colour_r, colour_g, colour_b, colour_a
        ], dtype='f4').ravel()

        return vertices

    def is_split_by_edge(self, coordinate, next_coordinate, close_edge_coordinate, centre_line_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        distance_coordinate_edge = np.linalg.norm(coordinate - close_edge_coordinate)
        distance_centre_line = np.linalg.norm(coordinate - centre_line_coordinate)
        distance_between_coordinates = np.linalg.norm(coordinate - next_coordinate)

        return distance_between_coordinates > distance_coordinate_edge and distance_between_coordinates > distance_centre_line

    def closest_edge_coordinate(self, coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        if coordinate[0] > 0:
            close_edge_coordinate = np.array([ self.WIDTH_PLOT, coordinate[1] ])
        else:
            close_edge_coordinate = np.array([ -self.WIDTH_PLOT, coordinate[1] ])

        return close_edge_coordinate

    def centre_line_coordinate(self, coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        return np.array([ 0, coordinate[1] ])

    def generate_triangles_for_coordinate(self, coordinate, row, next_row, column_index, colour):
        right_coordinate = row[column_index + 1]
        bottom_right_coordinate = next_row[column_index + 1]
        bottom_coordinate = next_row[column_index]

        close_edge_coordinate = self.closest_edge_coordinate(coordinate)
        centre_line_coordinate = self.centre_line_coordinate(coordinate)

        is_split_horizontal = self.is_split_by_edge(coordinate, right_coordinate, close_edge_coordinate, centre_line_coordinate)
        is_split_bottom_split = self.is_split_by_edge(coordinate, bottom_coordinate, close_edge_coordinate, centre_line_coordinate)

        if is_split_horizontal and is_split_bottom_split:
            print("Coordinate not rendered as split by both edges")
        elif is_split_horizontal:
            return self.horizontal_split_squares(coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, close_edge_coordinate, colour)
        elif is_split_bottom_split:
            return self.vertical_split_squares(coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, close_edge_coordinate, colour)
        else:
            return self.no_split_square(coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, colour)

    def horizontal_split_squares(self, coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, close_edge_coordinate, colour):
        bottom_edge_coordinate = self.closest_edge_coordinate(bottom_coordinate)
        right_edge_coordinate = self.closest_edge_coordinate(right_coordinate)
        bottom_right_edge_coordinate = self.closest_edge_coordinate(bottom_right_coordinate)

        return [
            self.triangle(coordinate, bottom_coordinate, bottom_edge_coordinate, colour),
            self.triangle(coordinate, close_edge_coordinate, bottom_edge_coordinate, colour),
            self.triangle(right_coordinate, right_edge_coordinate, bottom_right_edge_coordinate, colour),
            self.triangle(right_coordinate, bottom_right_coordinate, bottom_right_edge_coordinate, colour)
        ]

    def vertical_split_squares(self, coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, close_edge_coordinate, colour):
        right_edge_coordinate = self.closest_edge_coordinate(right_coordinate)
        bottom_edge_coordinate = self.closest_edge_coordinate(bottom_coordinate)
        bottom_right_edge_coordinate = self.closest_edge_coordinate(bottom_right_coordinate)

        return [
            self.triangle(coordinate, close_edge_coordinate, right_edge_coordinate, colour),
            self.triangle(coordinate, right_coordinate, right_edge_coordinate, colour),
            self.triangle(bottom_edge_coordinate, right_edge_coordinate, bottom_right_edge_coordinate, colour),
            self.triangle(bottom_edge_coordinate, bottom_right_coordinate, bottom_right_edge_coordinate, colour)
        ]

    def no_split_square(self, coordinate, right_coordinate, bottom_coordinate, bottom_right_coordinate, colour):
        return [
            self.triangle(coordinate, right_coordinate, bottom_right_coordinate, colour),
            self.triangle(coordinate, bottom_coordinate, bottom_right_coordinate, colour)
        ]

    def coordinate_colour(self, row_index, column_index):
        return np.array([
            (row_index/100 + column_index/50 + self.base_colour[0])%1,
            (row_index/100  + column_index/50 + self.base_colour[1])%1,
            (row_index/100 + column_index/50 + self.base_colour[2])%1,
            self.alpha
        ])


