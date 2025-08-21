from src.panel import Panel

class Tessellation:
    def __init__(self, colours=None):
        self.panels = [self.createPanel(config, colour) for config, colour in zip(self.panel_configuration, colours or [])]

    def createPanel(self, config, colour):
       return Panel(colour, config['angle'], config['position'], config['width'], config['height'], self.face_geometry)
