import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.path as mpath

class Panel:
    PANEL_RESOLUTION=200
    LATITUDE_RANGE=90
    LONGITUDE_RANGE=180

    def __init__(self, colour, angle, position, width, height, geometry):
        self.base_colour = colour
        self.angle = angle
        self.position = position
        self.width = width
        self.height = height
        self.geometry = geometry

        self.equi_coordinates = self.generate_equi_coordinates()

    # Function to convert Cartesian coordinates to equirectangular
    def cartesian_to_equirectangular(self, coordinate):
        """

        :param coordinate:
        :return: np.array([lon, lat])
        """
        lon = np.degrees(np.arctan2(coordinate[0], coordinate[2]))/self.LONGITUDE_RANGE
        lat = np.degrees(np.arcsin(
            np.clip(coordinate[1] / np.sqrt(coordinate[0] ** 2 + coordinate[1] ** 2 + coordinate[2] ** 2), -1, 1)))/self.LATITUDE_RANGE

        return np.array([lon, lat])

    # Function to return the rotated coordinates using euler
    def apply_rotational_transformation(self, coordinate, rotation_matrix):
        """

        :param coordinate:
        :param angle:
        :return: rotated_coordinate
        """

        return rotation_matrix.apply(coordinate).flatten()

    # Function to apply translation
    def apply_translation_transformation(self, coordinate, translation):
        """

        :param coordinate:
        :param translation:
        :return: coordinate + translation

        """
        return coordinate + translation

    # Function to generate coordinates using panel
    def generate_coordinates(self):
        """

        :param panel:
        :return: coordinates
        """

        # Create initial meshgrid in xz plane with panel width and height
        x_initial = np.linspace(-self.width / 2, self.width / 2,  self.PANEL_RESOLUTION)
        z_initial = np.linspace(-self.height / 2, self.height / 2, self.PANEL_RESOLUTION)

        # Convert meshgrid into coordinate array
        x_grid, z_grid = np.meshgrid(x_initial, z_initial)
        grid_array = np.column_stack((x_grid.ravel(), z_grid.ravel()))

        grid_rows = self.split_grid_array_to_rows(grid_array)

        processed_coordinates = self.process_coordinates(grid_rows)

        return processed_coordinates

    def split_grid_array_to_rows(self, grid_array):
        rows = []

        for i in range(self.PANEL_RESOLUTION):
            row = grid_array[i * self.PANEL_RESOLUTION:(i + 1) * self.PANEL_RESOLUTION]
            rows.append(row)

        return rows

    def process_coordinates(self, grid_rows):
       coordinate_rows = []

       for grid_row in grid_rows:
           shaped_grid_row = self.cut_meshgrid_to_triangle(grid_row) if self.geometry == "TRIANGLE" else grid_row

           if shaped_grid_row.size == 0:
               continue

           coordinate_row = np.insert(shaped_grid_row, 1, 0, axis=1)
           coordinate_rows.append(coordinate_row)

       return coordinate_rows

    # Function to cut a meshgrid to tessellation's face triangle geometry
    def cut_meshgrid_to_triangle(self, points):
       """

       :param points:
       :param panel:
       :return: points[points_mask]
       """
     
       # create path around triangle with width and height of panel
       polygon_path = self.triangle_vertex_path(self.width, self.height)

       # create mask to remove all coordinates outside triangle
       points_mask = polygon_path.contains_points(points)

       # filter points to those within triangle
       return points[points_mask]

    # Function to generate vertex path of an equilateral triangle
    def triangle_vertex_path(self, width, height):
        """

        :param width:
        :param height:
        :return: mpath.Path(polygon_vertices)
        """

        polygon_vertices = np.array([[-width/2, -height/4], [width/2, -height/4], [0, height/2.85]])

        return mpath.Path(polygon_vertices)

    # Function to apply transforms onto the coordinates
    def apply_transformations(self, coordinates):
        """

        :param coordinates:
        :param angle:
        :param translation:
        :return: equi_coordinates
        """

        # Apply Euler rotations to rotate coordinates to angle of the panel 
        rot_matrix = Rotation.from_euler('zxy', np.array([self.angle]), degrees=True)
        rotated_coordinates = np.apply_along_axis(self.apply_rotational_transformation, axis=1, arr=coordinates, rotation_matrix=rot_matrix)

        # Translate coordinates to position of the panel
        transformed_coordinates = np.apply_along_axis(self.apply_translation_transformation, axis=1, arr=rotated_coordinates,
                                                      translation=self.position)

        # Generate equirectangular coordinates from cartesian
        equi_coordinates = np.apply_along_axis(self.cartesian_to_equirectangular, axis=1, arr=transformed_coordinates)
        return equi_coordinates

    def generate_equi_coordinates(self):
        base_mesh_coordinate_rows = self.generate_coordinates()

        equi_coordinate_rows = []

        for coordinate_row in base_mesh_coordinate_rows:
            # Convert each row of coordinates to equirectangular coordinates
            equi_coordinates = self.apply_transformations(coordinate_row)

            equi_coordinate_rows.append(equi_coordinates)

        return equi_coordinate_rows
