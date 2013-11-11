class ConnectedNodes:
    def __init__(self):
        self.connections_set = set(tuple())

    def not_connected(self, a_key, other_key):
        return self.connections_set.isdisjoint({(a_key, other_key)})

    def add(self, connection):
        self.connections_set.add(connection)