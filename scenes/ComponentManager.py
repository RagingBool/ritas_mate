class ComponentManager(object):
    def __init__(self):
        self._components = []

    def add(self, component):
        self._components.append(component)

    def poke(self):
        for c in self._components:
            c.poke()

    def update(self, dt):
        for c in self._components:
            c.update(dt)
