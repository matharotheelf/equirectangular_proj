from src.tessellation import Tessellation
import numpy as np

class Octohedron(Tessellation):
  face_geometry = "TRIANGLE" 

  # 8 sides of octohedran width and height of equilateral triangle
  panel_configuration = [
          {
              'position': [1, 1, 1],
              'angle': [0, 45, 45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, 1, 1],
              'angle': [0, 45, -45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, -1, 1],
              'angle': [0, -45, 45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, 1, -1],
              'angle': [0, 45, 135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [1, -1, -1],
              'angle': [0, -45, 135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, 1, -1],
              'angle': [0, 45, -135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, -1, 1],
              'angle': [0, -45, -45],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          },
          {
              'position': [-1, -1, -1],
              'angle': [0, -45, -135],
              'width': 5,
              'height': 5*np.sqrt(4/3)
          }
  ]
