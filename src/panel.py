from src.equi_distortion import EquiDistortion
from src.coordinate_grid import CoordinateGrid

class Panel:
    def __init__(self, colour, angle, position, width, height, geometry):
        self.base_colour = colour
        self.angle = angle
        self.position = position
        self.width = width
        self.height = height
        self.geometry = geometry

        undistorted_coordinate_grid = CoordinateGrid(width, height, geometry).generate_grid()

        self.equi_coordinates = EquiDistortion(angle, position).generate_equi_coordinates(undistorted_coordinate_grid)
