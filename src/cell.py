import moderngl
import numpy as np
import math

class Cell:
    WIDTH_PLOT = 1
    MIDDLE_PLOT = 0

    def __init__(self, coordinate, row, next_row, column_index, row_index, mesh):
        self.base_colour = mesh.base_colour
        self.alpha = mesh.alpha

        self.coordinate = coordinate
        
        self.right_coordinate = row[column_index + 1]
        self.bottom_right_coordinate = next_row[column_index + 1]
        self.bottom_coordinate = next_row[column_index]

        self.close_edge_coordinate = self.closest_edge_coordinate(coordinate)
        self.centre_line_coordinate = self.centre_line_coordinate()

        self.is_split_horizontal = self.is_split_by_edge(self.right_coordinate)
        self.is_split_bottom = self.is_split_by_edge(self.bottom_coordinate)

        if self.is_split_bottom or self.is_split_horizontal:
            self.bottom_edge_coordinate = self.closest_edge_coordinate(self.bottom_coordinate)
            self.right_edge_coordinate = self.closest_edge_coordinate(self.right_coordinate)
            self.bottom_right_edge_coordinate = self.closest_edge_coordinate(self.bottom_right_coordinate)

        self.colour = self.coordinate_colour(row_index, column_index)

    def triangle(self, current_coordinate, horizontal_coordinate, vertical_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """
        colour_r, colour_g, colour_b, colour_a = self.colour

        vertices = np.asarray([
            current_coordinate[0], current_coordinate[1], colour_r, colour_g, colour_b, colour_a,
            horizontal_coordinate[0], horizontal_coordinate[1], colour_r, colour_g, colour_b, colour_a,
            vertical_coordinate[0], vertical_coordinate[1], colour_r, colour_g, colour_b, colour_a
        ], dtype='f4').ravel()

        return vertices

    def is_split_by_edge(self, next_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        distance_coordinate_edge = np.linalg.norm(self.coordinate - self.close_edge_coordinate)
        distance_centre_line = np.linalg.norm(self.coordinate - self.centre_line_coordinate)
        distance_between_coordinates = np.linalg.norm(self.coordinate - next_coordinate)

        return distance_between_coordinates > distance_coordinate_edge and distance_between_coordinates > distance_centre_line

    def closest_edge_coordinate(self, single_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        if single_coordinate[0] > 0:
            edge_coordinate = np.array([ self.WIDTH_PLOT, single_coordinate[1] ])
        else:
            edge_coordinate = np.array([ -self.WIDTH_PLOT, single_coordinate[1] ])

        return edge_coordinate

    def centre_line_coordinate(self):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        return np.array([ self.MIDDLE_PLOT, self.coordinate[1] ])

    def generate_triangles(self):
        if self.is_split_horizontal and self.is_split_bottom:
            print("Coordinate not rendered as split by both edges")
        elif self.is_split_horizontal:
            return self.horizontal_split_squares()
        elif self.is_split_bottom:
            return self.vertical_split_squares()
        else:
            return self.no_split_square()

    def horizontal_split_squares(self):
        return [
            self.triangle(self.coordinate, self.bottom_coordinate, self.bottom_edge_coordinate),
            self.triangle(self.coordinate, self.close_edge_coordinate, self.bottom_edge_coordinate),
            self.triangle(self.right_coordinate, self.right_edge_coordinate, self.bottom_right_edge_coordinate),
            self.triangle(self.right_coordinate, self.bottom_right_coordinate, self.bottom_right_edge_coordinate)
        ]

    def vertical_split_squares(self):
        return [
            self.triangle(self.coordinate, self.close_edge_coordinate, self.right_edge_coordinate),
            self.triangle(self.coordinate, self.right_coordinate, self.right_edge_coordinate),
            self.triangle(self.bottom_edge_coordinate, self.right_edge_coordinate, self.bottom_right_edge_coordinate),
            self.triangle(self.bottom_edge_coordinate, self.bottom_right_coordinate, self.bottom_right_edge_coordinate)
        ]

    def no_split_square(self):
        return [
            self.triangle(self.coordinate, self.right_coordinate, self.bottom_right_coordinate),
            self.triangle(self.coordinate, self.bottom_coordinate, self.bottom_right_coordinate)
        ]

    def coordinate_colour(self, horizontal_index, vertical_index):
        return np.array([
            (horizontal_index/100 + vertical_index/50 + self.base_colour[0])%1,
            (horizontal_index/100  + vertical_index/50 + self.base_colour[1])%1,
            (horizontal_index/100 + vertical_index/50 + self.base_colour[2])%1,
            self.alpha
        ])


