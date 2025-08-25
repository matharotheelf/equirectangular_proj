import moderngl
import numpy as np

class Mesh:
    WIDTH_PLOT = 1

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
                bottom_right_coordinate = next_row[column_index + 1]
                bottom_coordinate = next_row[column_index]

                close_edge_coordinate = self.closest_edge_coordinate(coordinate)
                centre_line_coordinate = self.centre_line_coordinate(coordinate)

                is_split_horizontal = self.is_split_by_edge(coordinate, right_coordinate, close_edge_coordinate, centre_line_coordinate)
                is_split_bottom_split = self.is_split_by_edge(coordinate, bottom_coordinate, close_edge_coordinate, centre_line_coordinate)

                if is_split_horizontal and is_split_bottom_split:
                    print("Coordinate not rendered as split by both edges")
                elif is_split_horizontal:
                    # render two squares across right side
                    print("Split by right edge")

                    bottom_edge_coordinate = self.closest_edge_coordinate(bottom_coordinate)

                    triangle_mesh.append(self.triangle(coordinate, close_edge_coordinate, bottom_edge_coordinate))
                    triangle_mesh.append(self.triangle(coordinate, bottom_coordinate, bottom_edge_coordinate))

                    right_edge_coordinate = self.closest_edge_coordinate(right_coordinate)
                    bottom_right_edge_coordinate = self.closest_edge_coordinate(bottom_right_coordinate)

                    triangle_mesh.append(self.triangle(right_coordinate, right_edge_coordinate, bottom_right_edge_coordinate))
                    triangle_mesh.append(self.triangle(right_coordinate, bottom_right_coordinate, bottom_right_edge_coordinate))
                elif is_split_bottom_split:
                    print("Split by bottom edge")

                    # render two trianles across bottom
                else:
                    triangle_mesh.append(self.triangle(coordinate, right_coordinate, bottom_right_coordinate))
                    triangle_mesh.append(self.triangle(coordinate, bottom_coordinate, bottom_right_coordinate))

        return triangle_mesh

    def triangle(self, coordinate, horizontal_coordinate, vertical_coordinate):
        """
        Generate mesh for upper triangle from coordinate rows.

        :param coordinate_rows: List of coordinate rows.
        :return: None
        """

        vertices = np.asarray([
            coordinate,
            horizontal_coordinate,
            vertical_coordinate

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
