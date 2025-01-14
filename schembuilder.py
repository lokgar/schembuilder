import svgwrite


class Port:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape:
    def __init__(self, dwg, x, y):
        self.dwg = dwg
        self.x = x
        self.y = y
        self.ports = []

    def add_port(self, x, y):
        port = Port(self.x + x, self.y + y)
        self.ports.append(port)
        return port

    def draw(self):
        raise NotImplementedError("Draw method should be implemented by subclasses")


class Rectangle(Shape):
    def __init__(self, dwg, x, y, width, height):
        super().__init__(dwg, x, y)
        self.width = width
        self.height = height

    def draw(self):
        self.dwg.add(
            self.dwg.rect(
                insert=(self.x, self.y),
                size=(self.width, self.height),
                fill="none",
                stroke="black",
            )
        )


class Circle(Shape):
    def __init__(self, dwg, x, y, radius):
        super().__init__(dwg, x, y)
        self.radius = radius

    def draw(self):
        self.dwg.add(
            self.dwg.circle(
                center=(self.x, self.y), r=self.radius, fill="none", stroke="black"
            )
        )


class Laser(Rectangle):
    def __init__(self, dwg, x, y):
        super().__init__(dwg, x, y, 100, 50)
        self.add_ports()

    def add_ports(self):
        self.add_port(0, 25)  # Left middle port
        self.add_port(100, 25)  # Right middle port


class Modulator(Rectangle):
    def __init__(self, dwg, x, y):
        super().__init__(dwg, x, y, 120, 60)
        self.add_ports()

    def add_ports(self):
        self.add_port(0, 30)  # Left middle port
        self.add_port(120, 30)  # Right middle port


class Amplifier(Circle):
    def __init__(self, dwg, x, y):
        super().__init__(dwg, x, y, 30)
        self.add_ports()

    def add_ports(self):
        self.add_port(0, 0)  # Left port
        self.add_port(60, 0)  # Right port


class Schematic:
    def __init__(self, filename):
        self.filename = filename
        self.dwg = svgwrite.Drawing(filename, profile="tiny")
        self.shapes = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def add_shape(self, shape):
        self.shapes.append(shape)
        shape.draw()

    def connect_ports(self, port1, port2):
        self.dwg.add(
            self.dwg.line(
                start=(port1.x, port1.y), end=(port2.x, port2.y), stroke="black"
            )
        )

    def save(self):
        self.dwg.save()


# Example usage with context manager
with Schematic("schematic.svg") as schematic:
    laser = Laser(schematic.dwg, 10, 10)
    schematic.add_shape(laser)

    modulator = Modulator(schematic.dwg, 200, 10)
    schematic.add_shape(modulator)

    amplifier = Amplifier(schematic.dwg, 100, 100)
    schematic.add_shape(amplifier)

    schematic.connect_ports(laser.ports[1], modulator.ports[0])
    schematic.connect_ports(modulator.ports[1], amplifier.ports[0])
