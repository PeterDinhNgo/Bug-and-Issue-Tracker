from tkinter import *
from math import sqrt
from random import shuffle
from time import sleep, time
from random import randint
from tkinter import ttk, messagebox

class WaitingGame(Tk):
    """Main Single Class for the waiting game."""
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.HEIGHT = 768
        self.WIDTH = 1366
        self.colors = ["#746658","#928975"]
        self.MID_X = self.WIDTH / 2
        self.MID_Y = self.HEIGHT / 2
        self.title("Killing Time")
        self.protocol('WM_DELETE_WINDOW', self.close_game)

    def game_init(self):
        """Game initialises with the game variables."""
        self.spaceship_radius = 15
        self.spaceship_speed = 10
        self.score = 0
        self.lives = 3
        self.high = 0

        self.asteroid_type = list()
        self.asteroid_r = list()
        self.asteroid_speed = list()
        self.asteroid_id_e = list()
        self.asteroid_r_e = list()
        self.asteroid_speed_e = list()
        self.min_asteroid_r = 10
        self.max_asteroid_r = 30
        self.max_asteroid_spd = 10
        self.gap = 100
        self.asteroid_chance = 30
        self.evil_asteroid = 50
        self.running = False

        self.running = True
        '''Game GUI Layout and Style
        '''
        self.game = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.game.pack()
        self.ship_id = self.game.create_polygon(5, 5, 5, 25, 30, 15, fill="#DC2EF7")
        self.Main_Ship = self.game.create_polygon(5, 5, 5, 25, 50, 15, fill="#226FF1")
        self.game.create_text(50, 30, text="PTS", fill="white")
        self.st = self.game.create_text(50, 50, fill="#00FF31")
        self.game.create_text(100, 30, text="HI-PTS", fill="white")
        self.ht = self.game.create_text(100, 50, fill="#00FF31")
        self.game.create_text(150, 30, text="LIVES", fill="white")
        self.lt = self.game.create_text(150, 50, fill="#FF1300")
        self.game.bind_all('<Key>', self.move_ship)

        self.game.move(self.ship_id, self.MID_X, self.MID_Y)
        self.game.move(self.Main_Ship, self.MID_X, self.MID_Y)
        
    
    def start_game(self):
        """Game starting function"""
        self.lives = 3
        self.score = 0
        while self.running:
            if randint(1, self.asteroid_chance) == 1:
                self.create_asteroid()
            if randint(1, self.evil_asteroid) == 1:
                self.create_asteroid_e()
            if randint(1, 100) == 1:
                self.create_asteroid_r()

            self.move_asteroids()
            self.intercept_e()
            self.score += self.intercept()
            if self.score > self.high:
                self.high = self.score
            if self.score >= 400:
                self.evil_asteroid = 40
                self.asteroid_chance = 25
                if self.score >= 1000:
                    self.evil_asteroid = 30
                    self.asteroid_chance = 20
            self.show(number=self.score, type='score')
            self.show(number=self.high, type='high')
            self.show(number=self.lives, type='lives')
            if self.lives <= 0:
                result = messagebox.askokcancel("Warning", "Do you want to play again?")
                if result:
                    self.cleanAll()
                    self.start_game()
                else:
                    self.close_game()
                    break
            self.update()
            shuffle(self.colors)
            sleep(0.01)

    def close_game(self):
        """Game closing function"""
        self.running = False
        sleep(0.5)
        self.destroy()

    def move_ship(self, event):
        """Handles when the player moves the ship."""
        directions = dict(Up=(0, -1), Down=(0, +1), Left=(-1, 0), Right=(1, 0))
        direction = event.keysym  
        if direction in directions:
            x_fact, y_fact = directions[direction] 
            cx = x_fact * self.spaceship_speed
            cy = y_fact * self.spaceship_speed
            self.game.move(self.ship_id, cx, cy)
            self.game.move(self.Main_Ship, cx, cy)

    def create_asteroid_common(self, rand_speed_min, outline, fill, enemy):
        """Creates asteroids for the game.
        
        Parameters:
           rand_speed_min (int): randomly selected minimum speed for asteroids.
           outline (str): outline of the asteroid
           fill (str): fill of the asteroid
        """
        x_pos = self.WIDTH + self.gap
        r = randint(self.min_asteroid_r, self.max_asteroid_r)
        y_pos = randint(0, self.HEIGHT)
        id1 = self.game.create_oval(x_pos - r, y_pos - r, x_pos + r, y_pos + r, outline=outline, fill=fill)
        if not enemy:
            self.asteroid_type.append(id1)
            self.asteroid_r.append(r)
            self.asteroid_speed.append(randint(rand_speed_min, self.max_asteroid_spd))
        else:
            self.asteroid_id_e.append(id1)
            self.asteroid_r_e.append(r)
            self.asteroid_speed_e.append(randint(rand_speed_min, self.max_asteroid_spd))

    def create_asteroid(self):
        """Creates the good asteroid."""
        self.create_asteroid_common(5, '#FFFFFF', '#63F621', enemy=False)

    def create_asteroid_e(self):
        """Creates the bad asteroid."""
        self.create_asteroid_common(6, self.colors[1], self.colors[1], enemy=True)

    def create_asteroid_r(self):
        """Creates the second type of bad asteroid."""
        self.create_asteroid_common(8, self.colors[0], self.colors[0], enemy=True)

    def move_asteroids(self):
        """Game movement of the asteroid"""
        for i in range(len(self.asteroid_type)):
            self.game.move(self.asteroid_type[i], -self.asteroid_speed[i], 0)
        for i in range(len(self.asteroid_id_e)):
            self.game.move(self.asteroid_id_e[i], -self.asteroid_speed_e[i], 0)

    def get_coords(self, id_num):
        """Gets the coordinates."""
        pos = self.game.coords(id_num)
        x = (pos[0] + pos[2]) / 2
        y = (pos[1] + pos[3]) / 2
        return x, y

    def del_asteroid(self, i):
        """Asteroid is deleted"""
        del self.asteroid_r[i]
        del self.asteroid_speed[i]
        self.game.delete(self.asteroid_type[i])
        del self.asteroid_type[i]

    def del_asteroid_e(self, i):
        del self.asteroid_r_e[i]
        del self.asteroid_speed_e[i]
        self.game.delete(self.asteroid_id_e[i])
        del self.asteroid_id_e[i]

    def clean(self):
        """Asteroid deletion given condition."""
        for i in range(len(self.asteroid_type) - 1, -1, -1):
            x, y = self.get_coords(self.asteroid_type[i])
            if x < -self.gap:
                self.del_asteroid(i)

    def distance(self, id1, id2):
        x1, y1 = self.get_coords(id1)
        x2, y2 = self.get_coords(id2)
        return sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) *(y2 - y1)))

    def intercept(self):
        """Asteroid collision point scoring asteroids."""
        points = 0
        for asteroid in range(len(self.asteroid_type) - 1, -1, -1):
            if self.distance(self.Main_Ship, self.asteroid_type[asteroid]) < (self.spaceship_radius + self.asteroid_r[asteroid]):
                points += (self.asteroid_r[asteroid] + self.asteroid_speed[asteroid])
                self.del_asteroid(asteroid)
        return points

    def cleanAll(self):
        """After game restarts all asteroids are deleted."""
        for i in range(len(self.asteroid_type) - 1, -1, -1):
            x, y = self.get_coords(self.asteroid_type[i])
            self.del_asteroid(i)

        for i in range(len(self.asteroid_id_e) - 1, -1, -1):
            x, y = self.get_coords(self.asteroid_id_e[i])
            self.del_asteroid_e(i)

    def intercept_e(self):
        """Asteroid collision for bad asteroids."""
        for asteroid in range(len(self.asteroid_id_e) - 1, -1, -1):
            if self.distance(self.Main_Ship, self.asteroid_id_e[asteroid]) < (self.spaceship_radius + self.asteroid_r_e[asteroid]):
                self.del_asteroid_e(asteroid)
                self.lives -= 1


    def show(self, number, type):
        if type == "score":
            self.game.itemconfig(self.st, text=str(number))

        if type == "lives":
            self.game.itemconfig(self.lt, text=str(number))

        if type == "high":
            self.game.itemconfig(self.ht, text=str(number))
