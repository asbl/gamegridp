class Position:
    def __init(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid

    def is_in_grid(self):
        if self.grid.is_in_grid((self.x,self.y)):
            return True
        else:
            return False

