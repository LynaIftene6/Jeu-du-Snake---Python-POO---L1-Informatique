import tkinter as tk
import random
from Grid import Grid
from Element import Element, Ground, Animal
from PlanetAlpha import PlanetAlpha
from PlanetTk import PlanetTk

class SnakeHead(Animal):
    def __init__(self):
        super().__init__("🐍", life_max=100)

class SnakeBody(Animal):
    def __init__(self):
        super().__init__("◉", life_max=100)

class Food(Element):
    def __init__(self):
        super().__init__("🍎")

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.grid_width = self.width // self.cell_size
        self.grid_height = self.height // self.cell_size
        
        #creer les cadres du jeu
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.game_frame = tk.Frame(self.main_frame)
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        #creer la planet du jeu du snake avec ground comme base
        self.planet = PlanetAlpha("Snake Planet", self.grid_height, self.grid_width, Ground())
        
        #creer le convas
        self.canvas = tk.Canvas(self.game_frame, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        
        #afficher le score en bas du canvas
        self.score_label = tk.Label(self.game_frame, text="Score: 0")
        self.score_label.pack()
     
     #creer le cadre des bouttons en bas du score
        self.button_frame = tk.Frame(self.game_frame)
        self.button_frame.pack()
        
    #Création de trois bouttons demarrer, pause et reinitialiser
        
        self.start_btn = tk.Button(self.button_frame, text="Démarrer", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(self.button_frame, text="Pause", command=self.pause_game)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(self.button_frame, text="Réinitialiser", command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.snake_cells = []
        self.food_cell = None
        self.direction = "Right"
        self.running = False
        self.score = 0
        self.game_speed = 150

        self.bind("<space>", self.start_game)
        self.canvas.bind("<Button-1>", self.turn_left)
        self.canvas.bind("<Button-3>", self.turn_right)
        
        self.reset_game()
        
    #Dessin de la grille 
    
    def draw_grid(self):
        for i in range(0, self.width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.height, fill="lightgray")
        for i in range(0, self.height, self.cell_size):
            self.canvas.create_line(0, i, self.width, i, fill="lightgray")
    
    #Fonction pour commencer le jeu 
    
    def start_game(self, event=None):
        if not self.running:
            self.running = True
            self.update()
      
    #Fonction pour mettre en pause le jeu 
          
    def pause_game(self):
        self.running = False
        
    #Fonction pour reinitialisation le jeu 
      
    def reset_game(self):
        self.canvas.delete("all")
        self.draw_grid()
        
        for cell in range(self.grid_width * self.grid_height):
            self.planet.die(cell)
        
        start_x, start_y = 5, 5
        head_cell = self.planet.get_cell_number_from_coordinates(start_y, start_x)
        body1_cell = self.planet.get_cell_number_from_coordinates(start_y, start_x-1)
        body2_cell = self.planet.get_cell_number_from_coordinates(start_y, start_x-2)
        
        self.planet.born(head_cell, SnakeHead())
        self.planet.born(body1_cell, SnakeBody())
        self.planet.born(body2_cell, SnakeBody())
        
        self.snake_cells = [head_cell, body1_cell, body2_cell]
        self.direction = "Right"
        self.running = False
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        
        self.draw_snake()
        self.create_food()
       
    #Dessiner le snake   
        
    def draw_snake(self):
        self.canvas.delete("snake")
        
        for cell in self.snake_cells:
            i, j = self.planet.get_coordinates_from_cell_number(cell)
            x, y = j * self.cell_size, i * self.cell_size
            
            fill_color = "darkgreen" if cell == self.snake_cells[0] else "green"
            
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill=fill_color, tags="snake"
            )
       
     #Generation de food
        
    def create_food(self):
        self.canvas.delete("food")
        
        free_cells = []
        for cell in range(self.grid_width * self.grid_height):
            if cell not in self.snake_cells:
                free_cells.append(cell)
                
        if free_cells:
            self.food_cell = random.choice(free_cells)
            i, j = self.planet.get_coordinates_from_cell_number(self.food_cell)
            x, y = j * self.cell_size, i * self.cell_size
            
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill="red", tags="food"
            )
            
            self.planet.born(self.food_cell, Food())
            
    #definition des directions
        
    def move(self):
        if not self.running:
            return
            
        head_cell = self.snake_cells[0]
        i, j = self.planet.get_coordinates_from_cell_number(head_cell)
        
        if self.direction == "Right":
            j += 1
        elif self.direction == "Left":
            j -= 1
        elif self.direction == "Up":
            i -= 1
        elif self.direction == "Down":
            i += 1
            
        # Vérifier les limites avant de déplacer
        if i < 0 or i >= self.grid_height or j < 0 or j >= self.grid_width:
            self.game_over()
            return
            
        new_head_cell = self.planet.get_cell_number_from_coordinates(i, j)
        
        if new_head_cell in self.snake_cells:
            self.game_over()
            return
            
        if new_head_cell == self.food_cell:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            
            self.planet.born(new_head_cell, SnakeHead())
            old_head_cell = self.snake_cells[0]
            self.planet.die(old_head_cell)
            self.planet.born(old_head_cell, SnakeBody())
            
            self.snake_cells.insert(0, new_head_cell)
            self.create_food()
        else:
            tail_cell = self.snake_cells.pop()
            self.planet.die(tail_cell)
            
            old_head_cell = self.snake_cells[0]
            self.planet.die(old_head_cell)
            self.planet.born(old_head_cell, SnakeBody())
            
            self.planet.born(new_head_cell, SnakeHead())
            self.snake_cells.insert(0, new_head_cell)
            
            
    #Partie ou on verifie les collisions
        
    def check_collision(self):
        head_cell = self.snake_cells[0]
        i, j = self.planet.get_coordinates_from_cell_number(head_cell)
        
        if head_cell in self.snake_cells[1:]:
            return True
        
        if i < 0 or i >= self.grid_height or j < 0 or j >= self.grid_width:
            return True
            
        return False
    
    #fonction de ce qu'on affiche quand on perds
    
    def game_over(self):
        self.running = False
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Game Over! Score: {self.score}",
            fill="black",
            font=("Arial", 14, "bold")
        )
    
    #fonction pour tourner à gauche
    
    def turn_left(self, event=None):
        directions = ["Right", "Down", "Left", "Up"]
        current_index = directions.index(self.direction)
        new_direction = directions[(current_index + 1) % 4]
        self.direction = new_direction
        
        if not self.running:
            self.start_game()
        
    #fonction pour tourner à Droite
    
    def turn_right(self, event=None):
        directions = ["Right", "Up", "Left", "Down"]
        current_index = directions.index(self.direction)
        new_direction = directions[(current_index + 1) % 4]
        self.direction = new_direction
        
        if not self.running:
            self.start_game()
        
   #mise à jour
        
    def update(self):
        if not self.running:
            return
            
        self.move()
        self.draw_snake()
        self.after(self.game_speed, self.update)
        
if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
