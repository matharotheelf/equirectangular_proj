import numpy as np
import matplotlib.path as mpath

class CoordinateGrid:
    RESOLUTION = 200

    def __init__(self, width, height, geometry):
        self.width = width
        self.height = height
        self.geometry = geometry

    def generate_grid(self):
        if self.geometry == "SQUARE":
            return self.generate_square_grid()
        elif self.geometry == "TRIANGLE":
            return self.generate_triangle_grid()
        else:
            raise ValueError("Invalid geometry type. Supported types are 'SQUARE' and 'TRIANGLE'.")

    # Function to generate coordinates using panel
    def generate_square_grid(self):
        """

        :param panel:
        :return: coordinates
        """

        # Create initial meshgrid in xz plane with panel width and height
        x_initial = np.linspace(-self.width / 2, self.width / 2,  self.RESOLUTION)
        z_initial = np.linspace(-self.height / 2, self.height / 2, self.RESOLUTION)

        # Convert meshgrid into coordinate array
        x_grid, z_grid = np.meshgrid(x_initial, z_initial)
        grid_array = np.column_stack((x_grid.ravel(), z_grid.ravel()))

        grid_rows = self.split_grid_array_to_rows(grid_array)

        cartesian_coordinates = self.append_zero_to_coordinates(grid_rows)

        return cartesian_coordinates

    # Function to generate coordinates using panel
    def generate_triangle_grid(self):
        """

        :param panel:
        :return: coordinates
        """

        x_initial = np.linspace(- self.width / 2, self.width / 2,  self.RESOLUTION)
        z_initial = np.linspace(- self.height / 2, self.height / 2, self.RESOLUTION)

        coords = []

        for z_value in z_initial:
            # For each row, x runs from 0 to width - y (to stay inside the triangle)
            max_x = (z_value + self.height/2) * self.width/(2 * self.height)
            min_x = (- self.height/2 - z_value) * self.width/(2 * self.height)
            shaped_x_row = x_initial[self.triangle_mask(x_initial, min_x, max_x)]

            if len(shaped_x_row) == 0:
                continue

            shaped_z_row = np.full(len(shaped_x_row), z_value)
            shaped_2d_coordinates = np.column_stack((shaped_x_row, shaped_z_row))
            shaped_coordinates = np.insert(shaped_2d_coordinates, 1, 0, axis = 1)

            coords.append(shaped_coordinates)

        return coords

    def triangle_mask(self, x_value, min_x, max_x):
        return (x_value >= min_x) & (x_value <= max_x)


    def split_grid_array_to_rows(self, grid_array):
        rows = []

        for i in range(self.RESOLUTION):
            row = grid_array[i * self.RESOLUTION:(i + 1) * self.RESOLUTION]
            rows.append(row)

        return rows

    def append_zero_to_coordinates(self, grid_rows):
       coordinate_rows = []

       for grid_row in grid_rows:
           coordinate_row = np.insert(grid_row, 1, 0, axis=1)
           coordinate_rows.append(coordinate_row)

       return coordinate_rows

    def triangle_coordinate_rows(self, grid_rows):
       coordinate_rows = []

       for grid_row in grid_rows:
           shaped_grid_row = self.cut_meshgrid_to_triangle(grid_row)

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
