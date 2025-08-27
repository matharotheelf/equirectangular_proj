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
        self.primary_colour = self.coordinate_colour(row_index, column_index)
        self.primary_coord_and_colour = (self.coordinate, self.primary_colour)
        
        self.right_coordinate = row[column_index + 1]
        self.right_colour = self.coordinate_colour(row_index, column_index + 1)
        self.right_coord_and_colour = (self.right_coordinate, self.right_colour)

        self.bottom_right_coordinate = next_row[column_index + 1]
        self.bottom_right_colour = self.coordinate_colour(row_index + 1, column_index + 1)
        self.bottom_right_coord_and_colour = (self.bottom_right_coordinate, self.bottom_right_colour)

        self.bottom_coordinate = next_row[column_index]
        self.bottom_colour = self.coordinate_colour(row_index + 1, column_index)
        self.bottom_coord_and_colour = (self.bottom_coordinate, self.bottom_colour)

        self.close_edge_coordinate = self.closest_edge_coordinate(coordinate)
        self.centre_line_coordinate = self.centre_line_coordinate()

        self.is_split_horizontal = self.is_split_by_edge(self.right_coordinate)
        self.is_split_bottom = self.is_split_by_edge(self.bottom_coordinate)

        if self.is_split_bottom or self.is_split_horizontal:
            self.bottom_edge_coordinate = self.closest_edge_coordinate(self.bottom_coordinate)
            self.right_edge_coordinate = self.closest_edge_coordinate(self.right_coordinate)
            self.bottom_right_edge_coordinate = self.closest_edge_coordinate(self.bottom_right_coordinate)

            self.bottom_edge_colour = (self.primary_colour + self.bottom_colour) / 2
            self.close_edge_colour = (self.primary_colour + self.right_colour) / 2
            self.bottom_right_edge_colour = (self.right_colour + self.bottom_right_colour) / 2
            self.right_edge_colour = (self.primary_colour + self.right_colour) / 2

            self.bottom_edge_coord_and_colour = (self.bottom_edge_coordinate, self.bottom_edge_colour)
            self.close_edge_coord_and_colour = (self.close_edge_coordinate, self.close_edge_colour)
            self.bottom_right_edge_coord_and_colour = (self.bottom_right_edge_coordinate, self.bottom_right_edge_colour)
            self.right_edge_coord_and_colour = (self.right_edge_coordinate, self.right_edge_colour)

        self.colour = self.coordinate_colour(row_index, column_index)

    def triangle(self, current_coord_and_colour, next_coord_and_colour, vert_coord_and_colour):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """
        current_colour_r, current_colour_g, current_colour_b, current_colour_a = current_coord_and_colour[1]
        next_colour_r, next_colour_g, next_colour_b, next_colour_a = next_coord_and_colour[1]
        vert_colour_r, vert_colour_g, vert_colour_b, vert_colour_a = vert_coord_and_colour[1]

        current_coord_x, current_coord_y = current_coord_and_colour[0]
        next_coord_x, next_coord_y = next_coord_and_colour[0]
        vert_coord_x, vert_coord_y = vert_coord_and_colour[0]

        vertices = np.asarray([
            current_coord_x, current_coord_y,
            current_colour_r, current_colour_g, current_colour_b, current_colour_a,
            next_coord_x, next_coord_y,
            next_colour_r, next_colour_g, next_colour_b, next_colour_a,
            vert_coord_x, vert_coord_y,
            vert_colour_r, vert_colour_g, vert_colour_b, vert_colour_a
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
            self.triangle(
                self.primary_coord_and_colour, 
                self.bottom_coord_and_colour,
                self.bottom_edge_coord_and_colour
            ),
            self.triangle(
                self.primary_coord_and_colour, 
                self.close_edge_coord_and_colour, 
                self.bottom_edge_coord_and_colour,
            ),
            self.triangle(
               self.right_coord_and_colour,
               self.right_edge_coord_and_colour,
               self.bottom_right_edge_coord_and_colour
            ),
            self.triangle(
                self.right_coord_and_colour,
                self.bottom_right_coord_and_colour,
                self.bottom_right_edge_coord_and_colour
            )
        ]

    def vertical_split_squares(self):
        return [
            self.triangle(
                self.primary_coord_and_colour,
                self.close_edge_coord_and_colour,
                self.right_edge_coord_and_colour
            ),
            self.triangle(
                self.primary_coord_and_colour,
                self.right_coord_and_colour,
                self.right_edge_coord_and_colour
            ),
            self.triangle(
                self.bottom_coord_and_colour,
                self.bottom_edge_coord_and_colour,
                self.bottom_right_edge_coord_and_colour
            ),
            self.triangle(
                self.bottom_coord_and_colour,
                self.bottom_right_coord_and_colour,
                self.bottom_right_edge_coord_and_colour
            )
        ]

    def no_split_square(self):
        return [
            self.triangle(
                self.primary_coord_and_colour,
                self.right_coord_and_colour,
                self.bottom_right_coord_and_colour
            ),
            self.triangle(
                self.primary_coord_and_colour,
                self.bottom_coord_and_colour, 
                self.bottom_right_coord_and_colour
            )
        ]

    def coordinate_colour(self, horizontal_index, vertical_index):
        return np.array([
            (horizontal_index/40 + vertical_index/20 + self.base_colour[0])%1,
            (horizontal_index/40  + vertical_index/20 + self.base_colour[1])%1,
            (horizontal_index/40 + vertical_index/20 + self.base_colour[2])%1,
            self.alpha
        ])


