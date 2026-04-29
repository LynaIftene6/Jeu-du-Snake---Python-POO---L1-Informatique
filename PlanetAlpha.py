import random
from Grid import Grid

class PlanetAlpha(Grid):
    NORTH, EAST,SOUTH,WEST= (-1,0), (0,1), (1,0), (0,-1)
    NORTH_EAST, SOUTH_EAST, NORTH_WEST, SOUTH_WEST= (-1,1), (1,1), (1,-1), (-1,-1)
    CARDINAL_POINT=(NORTH, EAST,SOUTH,WEST)
    WIND_ROSE=(NORTH, EAST,SOUTH,WEST,NORTH_EAST, SOUTH_EAST, NORTH_WEST, SOUTH_WEST)

    def __init__(self, name, latitude_cells_count, longitude_cells_count, ground=' '):
    # Utiliser une liste de listes pour représenter la grille
        self.__grid = [[ground for _ in range(longitude_cells_count)] for _ in range(latitude_cells_count)]
        # Appel au constructeur de la classe parente (Grid)
        super().__init__(self.__grid)  # Appelle le constructeur de Grid pour initialiser la grille
        self.__name = name
        self.__ground = ground
    
    def _init_(self,name, latitude_cells_count, longitude_cells_count, ground=' '):
        Grid._init_(self, [ground for i in range (longitude_cells_count) for j in range (latitude_cells_count)])
        self.__name = name
        self.__ground = ground
    
    def get_name(self):
        return self.__name
    
    def get_ground(self):
        return self.__ground
    
    def get_random_free_place(self):
        vals= self.get_same_value_cell_numbers(self.__ground)
        return random.choice(vals) if vals else -1
    
    def born(self, cell_number, element):
        if self.get_cell(cell_number) == self.__ground:
            self.set_cell(cell_number, element)
            return 1
        return 0
    
    def die(self, cell_number):
        if self.get_cell(cell_number) != self.__ground:
            self.set_cell(cell_number, self.__ground)
            return 1
        return 0
    
    def __repr__(self):
        population= len(self.get_same_value_cell_numbers(self.__ground))
        return f"{self.__name} ({population} habitants)\n" + self.get_grid_str(' ')

    
if __name__ == '__main__':
    random.seed (10)
    PLANET_TEST= PlanetAlpha("Terre", 5, 10, '.')
    INHABITANT_TEST={'D':7, 'C':3}
    RESOURCES_TEST= {'E':10, 'H':20}
    print(PLANET_TEST)

    for letter, letter_count in INHABITANT_TEST.items():
        for _ in range(letter_count):
            PLANET_TEST.born(PLANET_TEST.get_random_free_place(),letter)
    print(PLANET_TEST)
    print("All test ok")
