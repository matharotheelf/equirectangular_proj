import moderngl
import numpy as np
import math
from enum import Enum

class StripCell:
    WIDTH_PLOT = 1
    MIDDLE_PLOT = 0
    HORIZONTAL_COLOUR_MULTIPLIER = 100
    VERTICAL_COLOUR_MULTIPLIER = 100

    def __init__(self, coordinate, row, next_row, column_index, row_index, base_colour, alpha, shift_index=0):
        self.base_colour = base_colour
        self.alpha = alpha

        self.colour = self.coordinate_colour(column_index + shift_index, row_index)

        self.coordinate = coordinate
        self.primary_edge_coordinate = self.closest_edge_coordinate(coordinate)
        self.centre_line_coordinate = self.centre_line_coordinate()

        self.is_split_horizontal = self.is_split_horizontally(row, column_index)

        self.set_bottom_coordinate(next_row, column_index)

        if self.is_split_vertical or self.is_split_horizontal:
            self.set_edge_coordinates()

    def set_bottom_coordinate(self, next_row, column_index): 
        if self.is_bottom_coordinate(next_row, column_index):
            self.bottom_coordinate = next_row[column_index]
            self.is_split_vertical = self.is_split_vertically()
        else:
            self.bottom_coordinate = self.coordinate
            self.is_split_vertical = False

    def is_bottom_coordinate(self, next_row, column_index):
        return len(next_row) >= column_index + 1

    def cell_vertices(self, current_coord, next_coord):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        colour_r, colour_g, colour_b, colour_a = self.colour
        current_coord_x, current_coord_y = current_coord
        next_coord_x, next_coord_y = next_coord

        return np.asarray([
            current_coord_x, current_coord_y,
            colour_r, colour_g, colour_b, colour_a,
            next_coord_x, next_coord_y,
            colour_r, colour_g, colour_b, colour_a,
        ], dtype='f4').ravel()

    def set_edge_coordinates(self):
        self.closest_bottom_edge_coordinate = self.closest_edge_coordinate(self.bottom_coordinate)

        self.furthest_bottom_edge_coordinate = self.furthest_edge_coordinate(self.bottom_coordinate)
        self.furthest_edge_coordinate = self.furthest_edge_coordinate(self.coordinate)

    def is_split_horizontally(self, row, column_index):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """
        is_next_coordinate = len(row) > column_index + 1

        if is_next_coordinate is False:
            return False
        else:
            next_coordinate = row[column_index + 1]

            distance_coordinate_edge = np.linalg.norm(self.coordinate - self.primary_edge_coordinate)
            distance_centre_line = np.linalg.norm(self.coordinate - self.centre_line_coordinate)
            distance_between_coordinates = np.linalg.norm(self.coordinate - next_coordinate)

            return distance_between_coordinates >= distance_coordinate_edge and distance_between_coordinates >= distance_centre_line

    def is_split_vertically(self):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """
        distance_coordinate_edge = np.linalg.norm(self.coordinate - self.primary_edge_coordinate)
        distance_centre_line = np.linalg.norm(self.coordinate - self.centre_line_coordinate)
        distance_between_coordinates = np.linalg.norm(self.coordinate - self.bottom_coordinate)

        return distance_between_coordinates > distance_coordinate_edge and distance_between_coordinates > distance_centre_line


    def closest_edge_coordinate(self, single_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        if single_coordinate[0] > self.MIDDLE_PLOT:
            edge_coordinate = np.array([ self.WIDTH_PLOT, single_coordinate[1] ])
        else:
            edge_coordinate = np.array([ -self.WIDTH_PLOT, single_coordinate[1] ])

        return edge_coordinate

    def furthest_edge_coordinate(self, single_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        if single_coordinate[0] < self.MIDDLE_PLOT:
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

    def generate_vertices(self):
        if self.is_split_horizontal and self.is_split_vertical:
            print("Coordinate not rendered as split by both edges")
            return (None, False)
        elif self.is_split_horizontal:
            return self.horizontal_split_squares(), True
        elif self.is_split_vertical:
            return self.vertical_split_squares(), True
        else:
            return self.no_split_square(), False

    def horizontal_split_squares(self):
        return [
            [
                self.cell_vertices(self.coordinate, self.bottom_coordinate),
                self.cell_vertices(self.primary_edge_coordinate, self.closest_bottom_edge_coordinate)
            ],
            [ 
                self.cell_vertices(self.furthest_edge_coordinate, self.furthest_bottom_edge_coordinate),
            ]
        ]

    def vertical_split_squares(self):
        return [
            [
            self.cell_vertices(
                self.coordinate,
                self.furthest_bottom_edge_coordinate,
            )
            ],
            [
            self.cell_vertices(
                self.closest_bottom_edge_coordinate,
                self.bottom_coordinate
            )
            ]
        ]

    def no_split_square(self):
        return (
            [ self.cell_vertices(
                self.coordinate,
                self.bottom_coordinate
            )]
        )

    def coordinate_colour(self, horizontal_index, vertical_index):
        return np.array([
            (horizontal_index/self.HORIZONTAL_COLOUR_MULTIPLIER + vertical_index/self.VERTICAL_COLOUR_MULTIPLIER + self.base_colour[0])%1,
            (horizontal_index/self.HORIZONTAL_COLOUR_MULTIPLIER + vertical_index/self.VERTICAL_COLOUR_MULTIPLIER + self.base_colour[1])%1,
            (horizontal_index/self.HORIZONTAL_COLOUR_MULTIPLIER + vertical_index/self.VERTICAL_COLOUR_MULTIPLIER + self.base_colour[2])%1,
            self.alpha
        ])
