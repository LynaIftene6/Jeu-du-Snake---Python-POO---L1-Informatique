import tkinter as tk
from PlanetAlpha import PlanetAlpha


class PlanetTk(tk.Canvas, PlanetAlpha):
    def __init__(self, root, name, latitude_cells_count, longitude_cells_count, authorized_classes, background_color='white', foreground_color='dark blue',
                 gridlines_color='maroon', cell_size=40, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw):
        PlanetAlpha.__init__(self, name, latitude_cells_count, longitude_cells_count, Ground())
        kw['width'] = cell_size * longitude_cells_count + 2 * margin_size + (longitude_cells_count - 1) * gutter_size
        kw['height'] = cell_size * latitude_cells_count + 2 * margin_size + (latitude_cells_count - 1) * gutter_size
        kw['bg'] = background_color
        tk.Canvas.__init__(self,root, **kw)
        for cell_number in range(self.get_columns_count() * self.get_lines_count()):
            i, j = self.get_coordinates_from_cell_number(cell_number)
            x = j * (cell_size + gutter_size) + margin_size
            y = i * (cell_size + gutter_size) + margin_size
            self.create_rectangle(x, y, x + cell_size, y + cell_size, tags=(f'c_{i}_{j}', f'c_{cell_number}'))
            self.create_text(x + cell_size // 2, y + cell_size // 2, text=str(Ground()), fill=foreground_color, font=('Arial', cell_size // 5, 'bold'), tags=(f't_{i}_{j}', f't_{cell_number}'))
        self._authorized_class = authorized_classes
        root.title(name)
        self.__cell_size=cell_size
        self.__gutter_size=gutter_size
        self.__margin_size=margin_size
        self.__root=root
        self.__show_content=show_content
        self.__show_grid_lines=show_grid_lines
        self.__background_color=background_color
        self.__foreground_color=foreground_color
        self.__gridlines_color=gridlines_color


    def get_root(self):
        return self.__root

    def get_background_color(self):
        return self.__background_color
    
    def get_foreground_color(self):
        return self.__foreground_color
    
    def born(self, cell_number, element):
        if element.__class__ in self._authorized_class:
            success = PlanetAlpha.born(self,cell_number, element)
            if success:
                self.itemconfigure(f't_{cell_number}', text=str(element), fill=self.__foreground_color)
    

    def die(self, cell_number):
        success = PlanetAlpha.die(self,cell_number)
        if success:
            self.itemconfigure(f't_{cell_number}', text=str(Ground()), fill= self.__background_color)


    def born_randomly(self, element):
        rand = random.randint(0, self.get_lines_count() * self.get_columns_count())
        if self.get_cell(rand):
            self.born(rand, element)

    def populate(self, class_names_count):
        for element_name in class_names_count:
            if element_name in self._authorized_class:
                for _ in range(class_names_count[element_name]):
                    self.born_randomly(element_name())

    def move_element(self,cell_number,new_cell_number):
        if self.is_free_place(cell_number) and not  self.is_free_place(cell_number):
            type_name = self.get_cell(cell_number).__class__
            self.born(new_cell_number,type_name)
            self.die(cell_number)
    
    def get_classes_cell(self):
        res = dict()
        for cell_number in range(self.get_columns_count()* self.get_lines_count()):
            class_type = self.get_cell(cell_number).__class__
            res[class_type]=res.get(class_type,0)+1
        return res

    def __str__(self):
        return planetAlpha.__repr__(self)

    __repr__ = __str__




if __name__ == "__main__":
    random.seed(1000)
    root = tk.Tk()
    dic = {Water: 40, Mouse: 40, Cow: 40}
    can = PlanetTk(root, 'MyPlanet', 15, 30, [Water, Mouse,Cow])
    can.pack()
    can.born(2, Water())
    can.born(20, Mouse())
    can.die(2)
    can.born_randomly(Water())
    can.born_randomly(Cow())
    can.populate(dic)
    root.mainloop()

