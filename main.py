import pygame
import random
import time
import math


class FallingItem:
    fallingSpeed = 3  # class variable

    # set coordinate for falling item and condition control when to drop next item
    def __init__(self, item_x_coordinate, item_y_coordinate):
        self.item_x_Coordinate = item_x_coordinate
        self.item_y_Coordinate = item_y_coordinate
        self.start_drop_item = True

    # function used to change the falling speed when player level up
    def set_speed(self, speed):
        self.fallingSpeed = speed
    # create a static list to store falling item

    @staticmethod
    def item_list():
        item = [  # meat
                {"itemName": "Chicken", "image": pygame.image.load('images/chicken.png'), "experience": 50,
                 "hungryDegree": 10, "type": "meat"},

                {"itemName": "hamburger", "image": pygame.image.load('images/hamburger.png'), "experience": 40,
                 "hungryDegree": 10, "type": "meat"},

                {"itemName": "beef", "image": pygame.image.load('images/beef.png'), "experience": 60,
                 "hungryDegree": 15, "type": "meat"},

                {"itemName": "sausage", "image": pygame.image.load('images/sausage.png'), "experience": 30,
                 "hungryDegree": 8, "type": "meat"},

                # fruit and veg
                {"itemName": "carrot", "image": pygame.image.load('images/carrot.png'), "experience": 20,
                 "hungryDegree": 10, "type": "veg"},

                {"itemName": "banana", "image": pygame.image.load('images/banana.png'), "experience": 20,
                 "hungryDegree": 8, "type": "veg"},

                {"itemName": "broccoli", "image": pygame.image.load('images/broccoli.png'), "experience": 20,
                 "hungryDegree": 12, "type": "veg"},

                # drinks
                {"itemName": "water", "image": pygame.image.load('images/water.png'), "experience": 15,
                 "hungryDegree": 7, "type": "drinks"},

                {"itemName": "soup", "image": pygame.image.load('images/soup.png'), "experience": 40,
                 "hungryDegree": 15, "type": "drinks"},

                # health supply
                {"itemName": "pill", "image": pygame.image.load('images/pill.png'), "experience": 10,
                 "hungryDegree": 5, "type": "health supply"},

                {"itemName": "supplement", "image": pygame.image.load('images/supplement.png'), "experience": 15,
                 "hungryDegree": 10, "type": "health supply"},

                {"itemName": "bandage", "image": pygame.image.load('images/bandage.png'), "experience": 10,
                 "hungryDegree": 3, "type": "health supply"},

                # harmful item
                {"itemName": "fish-bones", "image": pygame.image.load('images/fish-bones.png'), "experience": 10,
                 "hungryDegree": 5, "type": "harmful"},

                {"itemName": "screw", "image": pygame.image.load('images/screw.png'), "experience": 10,
                 "hungryDegree": 5, "type": "harmful"},

                {"itemName": "broken-bottle", "image": pygame.image.load('images/broken-bottle.png'), "experience": 10,
                 "hungryDegree": 5, "type": "harmful"},

                {"itemName": "apple_core", "image": pygame.image.load('images/apple_core.png'), "experience": 10,
                 "hungryDegree": 5, "type": "harmful"}]
        return item[random.randrange(16)]


class Player:
    # class variables
    player_full_health = 100
    player_current_health = 100

    # set initial value of different attributes for player
    def __init__(self, player_x, player_y, player_width, player_height):
        self.x = player_x
        self.y = player_y
        self.width = player_width
        self.height = player_height
        self.speed = 3
        self.player_level = 5
        self.player_current_health = 100
        self.player_full_health = 100
        self.experience_initial = 1
        self.experience_target = 100
        self.starve = 50
        self.starve_full = 50
        self.player_img = pygame.image.load("images/player_size3_32x32.png")

    def player_lvl_up(self):
        # check whether meet level up requirement and variables change when level up
        if self.experience_initial >= self.experience_target:
            self.player_level += 1
            # self.player_full_health = self.player_full_health * 1.2
            # self.player_current_health = self.player_current_health * 1.2
            Player.player_full_health = Player.player_full_health * 1.2
            Player.player_current_health = Player.player_full_health
            self.experience_target *= 1.5
            self.experience_initial = 0
            self.speed += 0.5

            # when level up, increase item falling speed to increase difficulty
            FallingItem.fallingSpeed += 0.5
            if self.player_level >= 3:  # if player reaches level 3 and up, player size become bigger
                self.player_img = pygame.image.load("images/player_size4_64x64.png")
                self.y = 390

            if self.player_level >= 6:  # if player reaches level 6 and up, player size become bigger
                self.player_img = pygame.image.load("images/player_size5_128x128.png")
                self.y = 320

    def background_display(self, game_window, food_img, item_x, item_y, deliver_machine_x, deliver_machine_y,
                           player_img):
        # blit all images and display them
        background_1 = pygame.image.load("images/space_background_1.png")
        deliver_machine = pygame.image.load("images/UFO.png")
        game_window.fill((0, 0, 0))
        game_window.blit(background_1, (0, 0))
        game_window.blit(player_img, (int(self.x), int(self.y)))
        game_window.blit(deliver_machine, (deliver_machine_x, deliver_machine_y))
        game_window.blit(food_img, (int(item_x), int(item_y)))
        pygame.draw.rect(game_window, (200, 200, 200), (800, 0, 200, 450))


def start_menu():

    # set display size and title
    menu_window = pygame.display.set_mode((1000, 450))
    pygame.display.set_caption("Eat or Die")

    # create text rectangle for game name and display it
    font = pygame.font.SysFont("Arial", 50)
    text = font.render("EAT OR DIE", True, (255, 50, 50))
    text_rect = text.get_rect()
    text_rect.center = (500, 150)

    # create text rectangle for game option "play" and "Quit"
    small_font = pygame.font.SysFont("comicsansms", 20)
    play = small_font.render("Play", True, (0, 255, 0))
    quit_game = small_font.render("Quit", True, (0, 255, 0))

    # only blit one time enough, so outside while loop
    menu_window.fill((255, 255, 255))
    menu_window.blit(text, text_rect)
    pygame.draw.rect(menu_window, (0, 0, 0), (300, 190, 50, 30), 1)
    pygame.draw.rect(menu_window, (0, 0, 0), (650, 190, 50, 30), 1)
    menu_window.blit(play, (308, 190))
    menu_window.blit(quit_game, (653, 190))
    pygame.display.update()
    start = True
    while start:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # what to do when mouse click

                # this area belong to "Play" text option, will call main function when mouse move here and click
                if 350 > mouse[0] > 300 and 220 > mouse[1] > 190:
                    main()

                # this area belong to "Quit" text option, will quit when mouse move here and click
                elif 700 > mouse[0] > 650 and 220 > mouse[1] > 190:
                    start = False
            else:
                break


def item_player_collision(item_x, item_y, player_x, player_y, player_lvl):
    # use math formula to calculate distance between player and falling item to determine whether they collide or not
    distance = int(math.sqrt(math.pow(item_x - player_x, 2) + (math.pow(item_y - player_y, 2))))
    if player_lvl < 3:
        if distance < 50:
            return True
        else:
            return False

    elif 6 > player_lvl >= 3:
        if distance < 55:
            return True
        else:
            return False

    else:
        if distance < 65:
            return True
        else:
            return False


def item_effect(food):
    # increase or reduce health if eat certain type food, to increase difficulty
    if food["type"] == "health supply":

        if food["itemName"] == "pill":
            Player.player_current_health += 0.1*Player.player_full_health

        elif food["itemName"] == "bandage":
            Player.player_current_health += 0.2*Player.player_full_health

        elif food["itemName"] == "supplement":
            Player.player_current_health += 0.3*Player.player_full_health

    elif food["type"] == "harmful":
        if food["itemName"] == "fish-bones":
            Player.player_current_health -= 0.1 * Player.player_full_health

        elif food["itemName"] == "apple_core":
            Player.player_current_health -= 0.05 * Player.player_full_health

        elif food["itemName"] == "screw":
            Player.player_current_health -= 0.15 * Player.player_full_health

        elif food["itemName"] == "broken-bottle":
            Player.player_current_health -= 0.2 * Player.player_full_health
    else:
        pass


def display_info(initial_experience, target_experience, player_lvl,game_win, current_hungry, full_lvl):
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)

    font = pygame.font.SysFont("Arial", 15, bold=True)

    # level up experience needed and current level text
    show_experience = font.render(str(int(initial_experience)) + "/" + str(int(target_experience)), True, black)
    show_lvl = font.render("Lvl " + str(player_lvl), True, black)

    # display current hungry level and hungry text
    show_current_hungry = font.render(str(int(current_hungry)) + "/" + str(int(full_lvl)), True, black)
    show_hungry_text = font.render("Hungry Degree ", True, black)

    # experience bar rectangle
    exp_base_rect = (810, 20, 100, 15)
    pygame.draw.rect(game_win, white, exp_base_rect)
    exp_rect = (810, 20, int(initial_experience / target_experience * exp_base_rect[2]), 15)
    pygame.draw.rect(game_win, green, exp_rect)

    # display health bar
    health_base_rect = (810, 70, 100, 15)
    pygame.draw.rect(game_win, white, health_base_rect)
    health_current_rect = (810, 70, int(Player.player_current_health / Player.player_full_health * health_base_rect[2]), 15)
    pygame.draw.rect(game_win, green, health_current_rect)

    # display health value
    cur_health = font.render(str(int(Player.player_current_health)) + "/" + str(int(Player.player_full_health)), True, black)
    health_text = font.render("Health ", True, black)

    # hungry degree bar rec
    pygame.draw.rect(game_win, white, (810, 120, full_lvl, 15))
    pygame.draw.rect(game_win, yellow, (810, 120, round(current_hungry), 15))
    if current_hungry <= 25:
        pygame.draw.rect(game_win, red, (810, 120, round(current_hungry), 15))

    # display the above attribute bar and text
    game_win.blit(show_experience, (920, 18))
    game_win.blit(show_lvl, (810, 2))
    game_win.blit(show_current_hungry, (870, 120))
    game_win.blit(show_hungry_text, (810, 100))
    game_win.blit(cur_health, (920, 70))
    game_win.blit(health_text, (810, 50))


def game_over_text(game_win):
    # display game over text
    font = pygame.font.SysFont("Arial", 50)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (800 // 2, 450 // 2)
    game_win.blit(text, text_rect)
    pygame.display.update()


def player_move(player):
    # player move right and left
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.speed
        if player.x <= 0:
            player.x = 0

    elif keys[pygame.K_RIGHT]:
        player.x += player.speed
        if player.x >= 736:
            player.x = 736


def main():
    clock = pygame.time.Clock()

    # set the initial position and speed for deliver machine
    deliver_machine_x = 368
    deliver_machine_y = -20
    deliver_machine_speed = 3

    # create object player and item will be delivered
    player = Player(400, 410, 64, 64)
    game_window = pygame.display.set_mode((1000, 450))

    run = True
    item = FallingItem(368, 10)
    while run:
        # end the game if player health or hungry level reaches 0
        if player.starve <= 0 or Player.player_current_health <= 0:
            player.starve = 0
            Player.player_current_health = 0
            game_over_text(game_window)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        # check whether player catch the item delivered by deliver machine
        is_collision = item_player_collision(player.x, player.y, item.item_x_Coordinate, item.item_y_Coordinate,
                                             player.player_level)
        player_move(player)

        # deliver machine will keep moving left and right
        deliver_machine_x = deliver_machine_x + deliver_machine_speed

        # set boundaries for deliver machine
        if deliver_machine_x < 0:
            deliver_machine_x = 0
            deliver_machine_speed = 3
        elif deliver_machine_x > 680:
            deliver_machine_x = 680
            deliver_machine_speed = -3

        item.item_y_Coordinate += FallingItem.fallingSpeed  # item will keep falling down once been dropped

        # to make sure one time only one item will be delivered, and set the initial x-coordinates of falling item
        # equals to deliver machine x
        if item.start_drop_item:
            item.item_x_Coordinate = deliver_machine_x
            food = FallingItem.item_list()
            # print("dropping item: " + food["itemName"])  ## debug log
            item.item_y_Coordinate = 60
            item.start_drop_item = False

        # if player catch the current falling item what will happen
        if is_collision and food:
            player.experience_initial += food["experience"]
            player.starve += food["hungryDegree"]
            # print("collide: " + food["itemName"])
            player.player_lvl_up()
            item_effect(food)
            item.item_x_Coordinate = deliver_machine_x
            item.item_y_Coordinate = 60
            item.start_drop_item = True
            food = None                   # reset food to NONE, will start to deliver next item

        # if item fall on ground reset food to none and start to deliver next item
        if item.item_y_Coordinate > 536:
            item.item_y_Coordinate = -20
            item.start_drop_item = True
            food = None

        # hungry level will increase when player level up to increase difficulty
        player.starve -= (0.02 + round(player.player_level / 100, 2))

        # health will keep reducing if hungry level lower than half, to increase difficulty
        if player.starve < 25:
            Player.player_current_health -= 0.05

        # make sure hungry level won't exceed max value 50
        elif player.starve >= 50:
            player.starve = 50

        # make sure current health points won't exceed full health condition
        if Player.player_current_health >= Player.player_full_health:
            Player.player_current_health = Player.player_full_health

        # if food equals to NONE, won't blit any image, to save resource
        if food:
            player.background_display(game_window, food["image"], item.item_x_Coordinate, item.item_y_Coordinate,
                                      deliver_machine_x, deliver_machine_y, player.player_img)

        # display player information on the right side
        display_info(player.experience_initial, player.experience_target, player.player_level,
                     game_window, player.starve, player.starve_full)

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    start_menu()
