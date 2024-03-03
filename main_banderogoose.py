import os, pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT


def main():
    pygame.init()

    FPS = pygame.time.Clock()

    HEIGHT = 700
    WIDTH = 1050
    PLAYER_HEIGHT = 76
    PLAYER_WIDTH = 182
    ENEMY_HEIGHT = 0.7*72
    ENEMY_WIDTH = 0.7*205
    BONUS_HEIGHT = 0.5*298
    BONUS_WIDTH = 0.5*180

    FONT = pygame.font.SysFont("Lusida Console", 30)

    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)

    main_display = pygame.display.set_mode((WIDTH,HEIGHT))

    bg = pygame.transform.scale(pygame.image.load('./Img/background.png'), (WIDTH, HEIGHT))
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3

    boom = pygame.transform.scale(pygame.image.load('./Img/boom2.png').convert_alpha(), (100, 100))

    IMAGE_PATH = "Goose"
    PLAYER_IMAGES = os.listdir(IMAGE_PATH)

    player = pygame.transform.scale(pygame.image.load('./Img/player.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
    player_rect = pygame.Rect(0, HEIGHT/2, *player.get_size())
    player_move_down = [0, 4]
    player_move_right = [4, 0]
    player_move_up = [0, -4]
    player_move_left = [-4, 0]

    def create_enemy():
        enemy = pygame.transform.scale(pygame.image.load('./Img/enemy.png').convert_alpha(), (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height(), HEIGHT - enemy.get_height()), *enemy.get_size())
        enemy_move = [random.randint(-16, -8), 0]
        return [enemy, enemy_rect, enemy_move]

    def create_bonus():
        bonus = pygame.transform.scale(pygame.image.load('./Img/bonus.png').convert_alpha(), (BONUS_WIDTH, BONUS_HEIGHT))
        bonus_rect = pygame.Rect(random.randint(bonus.get_width(), WIDTH - bonus.get_width()), -bonus.get_height(), *bonus.get_size())
        bonus_move = [0, random.randint(4, 8)]
        return [bonus, bonus_rect, bonus_move]

    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 4000)
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 6000)
    CHANGE_IMAGE = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMAGE, 500)

    enemies = []

    bonuses = []

    score = 0

    image_index = 0

    playing = True

    while playing:
        FPS.tick(120)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0          

        bg_X1 -= bg_move
        bg_X2 -= bg_move

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()

        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1,0))
        main_display.blit(bg, (bg_X2,0))

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                playing = False
        
        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.pop(bonuses.index(bonus))
            
            if bonus[1].colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                bonuses.pop(bonuses.index(bonus))
                # boom_rect = pygame.Rect((bonus[0].get_width() + enemy[0].get_width())/2, (bonus[0].get_height() + enemy[0].get_height())/2, *boom.get_size())
                main_display.blit(boom, bonus[1])

        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-35, 10))
        main_display.blit(player, player_rect)
        
        pygame.display.flip()

        for enemy in enemies:
            if enemy[1].right < 0:
                enemies.pop(enemies.index(enemy))

        for bonus in bonuses:
            if bonus[1].top > HEIGHT:
                bonuses.pop(bonuses.index(bonus))

        # print(len(bonuses))


if __name__ == "__main__":
    main()