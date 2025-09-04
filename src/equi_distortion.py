from scipy.spatial.transform import Rotation
import numpy as np

class EquiDistortion:
    LATITUDE_RANGE=90
    LONGITUDE_RANGE=180

    def __init__(self, angle, position):
        self.angle = angle
        self.position = position

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

    def generate_equi_coordinates(self, undistorted_coordinates):
        equi_coordinate_rows = []

        for coordinate_row in undistorted_coordinates:
            # Convert each row of coordinates to equirectangular coordinates
            equi_coordinates = self.apply_transformations(coordinate_row)

            equi_coordinate_rows.append(equi_coordinates)

        return equi_coordinate_rows

