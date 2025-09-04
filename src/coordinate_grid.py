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

        # Create initial meshgrid in xz plane with panel width and height
        x_initial = np.linspace(-self.width / 2, self.width / 2,  self.RESOLUTION)
        z_initial = np.linspace(-self.height / 2, self.height / 2, self.RESOLUTION)

        # Convert meshgrid into coordinate array
        x_grid, z_grid = np.meshgrid(x_initial, z_initial)
        grid_array = np.column_stack((x_grid.ravel(), z_grid.ravel()))

        grid_rows = self.split_grid_array_to_rows(grid_array)

        shaped_grid_rows = self.triangle_coordinate_rows(grid_rows)

        return shaped_grid_rows

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
