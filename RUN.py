from demineur_matrix import *
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel
import sys
import time
import os
import json

class App:

    def __init__(self):

        #grid values
        self.x = 0
        self.y = 0
        self.n = 0
        self.dx = 0
        self.dy = 0
        self.flag = False
        self.visited = set()

        self.won = False

        #data players
        self.best_player = None
        self.best_time = None

        script_dir = os.path.dirname(os.path.abspath(__file__)) #donne la direction de ce fichier, c'est à dire qu'il indique par où on est arrivé jusqu'ici -1
        self.image_path = os.path.join(script_dir, "image.png")
        self.json_path = os.path.join(script_dir, "scores.json")

        pygame.init()
        

        self.state_game = False
        self.level = "easy"
        self.username = ""

        self.draw_screen_size()
        self.calculate_best_time()
        self.draw_main_page()
        self.display_best_time()

        self.score = 0
    
    def draw_screen_size(self):
        if not self.state_game :
            
            self.l = 800
            self.h = 600
            self.size = (self.l, self.h)
            self.screen = pygame.display.set_mode(self.size)
            self.manager = pygame_gui.UIManager(self.size)

        if self.state_game :

            self.l = ( 2 + self.x ) * self.dx 
            self.h = ( 4 + self.y ) * self.dy

            self.size = (self.l, self.h)
            self.screen = pygame.display.set_mode(self.size)
            self.manager = pygame_gui.UIManager(self.size)
    
    def calculate_best_time(self):
        try:
            with open(self.json_path, "r") as file:
                data = json.load(file)

            self.best_time = None
            self.best_player = None

            for elem in data["scores"]:
                if self.best_time is None or elem["time"] < self.best_time:
                    self.best_player = elem["name"]
                    self.best_time = elem["time"]

        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON : {e}")
        except FileNotFoundError as e:
            print(f"Erreur : fichier introuvable - {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

    def display_best_time(self):
        try:
            if (self.best_time) > 60:
                return f"{int(self.best_time/60)} min et {int((self.best_time%60))} sec"
            else :
                return f"{int(self.best_time)} secondes"
        except:
            pass
            
    def draw_main_page(self) :
        self.screen.fill((236,186,79))
        self.logo = pygame.image.load(self.image_path)
        self.logo = pygame.transform.scale(self.logo, (304, 220))  # Redimensionner à la taille de l'écran
        self.screen.blit(self.logo, (248, 20))
        self.best_player_label_position = (200, 265, 400, 50)
        pygame.draw.rect(self.screen, (80,84,84), pygame.Rect(self.best_player_label_position))
        self.best_player_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(self.best_player_label_position), text= f"Meilleur joueur: {self.best_player} / Temps: {self.display_best_time()}", manager=self.manager)
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(200, 335, 400, 50), manager=self.manager)
        self.name_input.set_text("Nom du joueur")
        
        
        self.easy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(110, 410, 180, 50), manager=self.manager, text = 'Débutant')
        self.medium_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(310, 410, 180, 50), manager=self.manager, text = 'Amateur')
        self.pro_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(510, 410, 180, 50), manager=self.manager, text = 'Pro')
        self.start_button = UIButton(relative_rect=pygame.Rect(300, 500, 200, 50),text='Lancer le jeu',manager=self.manager)

    def handle_main_page_events(self, event):
            if not self.manager.process_events(event):
                if event.type == pygame.USEREVENT and event.ui_element == self.name_input:
                    if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        entered_text = self.name_input.get_text().strip()
                        if entered_text:  # Vérifie que le texte n'est pas vide
                            self.username = entered_text
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        self.start_time = pygame.time.get_ticks()
                        self.state_game = True
                        self.create_grid()
                        self.draw_screen_size()
                        self.draw_game_page()
                    elif event.ui_element == self.easy_button:
                        self.level = "easy"
                    elif event.ui_element == self.medium_button:
                        self.level = "medium"
                    elif event.ui_element == self.pro_button:
                        self.level = "pro"

    def create_grid(self):
        try:
            if self.level == "easy":
                self.x = 9
                self.y = 9
                self.n = 10
                self.dx = 60
                self.dy = 60
            elif self.level == "medium":
                self.x = 16
                self.y = 16
                self.n = 40
                self.dx = 40
                self.dy = 40
            elif self.level == "pro":
                self.x = 30
                self.y = 30
                self.n = 90
                self.dx = 30
                self.dy = 30
        except :
            App().run()
        
    def draw_game_page(self) :

        self.butt'ons = [[None for _ in range(self.y)] for _ in range(self.x)]'

        for i in range(self.x):
            for j in range(self.y):
                self.buttons[i][j] = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(self.dx * ( 1 + i ), self.dy * ( 3 + j ), self.dx, self.dy ),
                    text="",
                    manager=self.manager,
                    object_id = f"#button_{i}_{j}")

        self.username_label_position = (self.l/2 - self.dx*5, self.dy/2, self.dx*4,self.dy)
        self.username_label = UILabel(relative_rect=pygame.Rect(self.username_label_position),text='',manager=self.manager)
        self.username_label.set_text(f"Joueur : {self.username if self.username else 'Inconnu'}")

        self.score_label_position = (self.l/2 + self.dx, self.dy/2, self.dx*4, self.dy)
        self.score_label = UILabel(relative_rect=pygame.Rect(self.score_label_position),text='Box déminées : 0',manager=self.manager)
        
        self.time_label_position = (self.l/2 + self.dx, self.dy*3/2 + 2, self.dx*4, self.dy)
        self.time_label = UILabel(relative_rect=pygame.Rect(self.time_label_position),text='',manager=self.manager)
        
        self.flag_label_position = (self.l/2 - self.dx*2/3, self.dy*2/3, self.dx*3/2, self.dy*3/2)
        self.flag_label = UIButton(relative_rect=pygame.Rect(self.flag_label_position),manager=self.manager,text="OFF")
        
        self.game_over_label_position = (self.l/2 - self.dx*5, self.dy*3/2 + 2, self.dx*4,self.dy)
        self.game_over_label = UILabel(relative_rect=pygame.Rect(self.game_over_label_position),text='',manager=self.manager)
                
    def draw_rectangles(self):
        self.rect = pygame.draw.rect(self.screen, (10,0,0), pygame.Rect(self.username_label_position))
        self.rect = pygame.draw.rect(self.screen, (10,0,0), pygame.Rect(self.score_label_position))
        self.rect = pygame.draw.rect(self.screen, (10,0,0), pygame.Rect(self.time_label_position))
        self.rect = pygame.draw.rect(self.screen, (10,0,0), pygame.Rect(self.game_over_label_position))

    def handle_game_events(self, event):
        if not self.manager.process_events(event):
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.flag_label:
                    self.flag = not self.flag
                    self.flag_label.set_text("ON" if self.flag else "OFF")
                else:
                    self.handle_game_buttons(event)

    def handle_game_buttons(self, event):
        for i in range(self.x):
            for j in range(self.y):
                if event.ui_element == self.buttons[i][j]:
                    # Initialiser les bombes au premier clic
                    if self.score <= 1:
                        self.mat = callout(bombmap(self.x, self.y, self.n, i, j))  # Passe i, j à bombmap
                        print(self.mat)
                        print(int(self.x) * int(self.y) - int(self.n))
                        self.matdim = self.mat.shape[::-1]
                        self.n_x = self.matdim[0]
                        self.n_y = self.matdim[1]
                        
                        
                    if self.flag:
                        self.toggle_flag(i, j)
                    else:
                        self.reveal_cell(i, j)

    def add_score(self, i, j):
        
        if (i, j) not in self.visited:
            self.score += 1
            self.score_label.set_text(str(f"Box déminées : {self.score}"))
            self.visited.add((i, j))

        pass

    def toggle_flag(self, i, j):
        if self.mat[j][i] <= 9:
            self.mat[j][i] += 10
            self.buttons[i][j].set_text('F')
        else:
            self.mat[j][i] -= 10
            self.buttons[i][j].set_text("")

    def reveal_cell(self, i, j):
            value = self.mat[j][i]
            if int(value) == 9:
                self.game_over()
            elif int(value) < 9:
                self.add_score(i, j)
                self.buttons[i][j].set_text(f"{int(value)}")
                #print(self.score == int(self.x) * int(self.y) - int(self.n))
                
                if int(value) == 0:
                    self.reveal_empty_area(i, j)

    def reveal_empty_area(self, i, j):
        zeros = [(i, j)]
        visited = []
        while zeros:
            x, y = zeros.pop(0)
            if (x, y) not in visited:
                visited.append((x, y))
                value = self.mat[y][x]
                self.add_score(x, y)
                self.buttons[x][y].set_text(f"{int(value)}")
                if value == 0:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if 0 <= x + k < self.n_x and 0 <= y + l < self.n_y:
                                if (x + k, y + l) not in visited:
                                    zeros.append((x + k, y + l))

    def win(self):

        #if not hasattr(self, 'game_over_label'):
                #return

        nbr_empty = int(self.x) * int(self.y) - int(self.n)

        if self.score == int(self.x) * int(self.y) - int(self.n):
            self.won = True
            self.upload_data_json()
            self.game_over_label.set_text(f"Terrain déminé !")
            self.screen.fill((76, 243, 43))
            self.draw_rectangles()
            self.manager.update(0)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
            time.sleep(5)
            App().run()
        return self.won

    def game_over(self):

        #if not hasattr(self, 'game_over_label'):
            #return
    
        self.game_over_label.set_text(f"BOUM")
        self.screen.fill((255, 0, 0))
        self.draw_rectangles()
        self.manager.update(0)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        time.sleep(5)
        App().run()

    def upload_data_json(self):

        try:
            self.game_time = (pygame.time.get_ticks() - self.start_time)
            with open(self.json_path, "r") as file:
                data = json.load(file)
                
            user_exist = False
            for elem in data["scores"]:
                if self.username in elem["name"]:
                    elem["time"] = self.score
                    user_exist = True
                    break
            if not user_exist :
                new_entry = {
                    "name": self.username,
                    "time": self.game_time
                }

                data["scores"].append(new_entry)

            with open(self.json_path, "w") as file:
                json.dump(data, file, indent=4)  # Utilisez json.dump pour écrire les données sérialisées

            self.calculate_best_time()

        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON : {e}")
        except FileNotFoundError as e:
            print(f"Erreur : fichier introuvable - {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
          
    def run(self):
        clock = pygame.time.Clock()
        while True:
            #print(self.win())
            time_delta = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif not self.state_game:
                    self.handle_main_page_events(event)
                else:
                    self.handle_game_events(event)

            if self.state_game:
                self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                self.time_label.set_text(str(round(self.elapsed_time, 2)))
                self.screen.fill((236, 186, 79))
                self.draw_rectangles()
                self.win()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

App().run()