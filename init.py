import pygame
import time
import game.gameObject as gobj
import game.gameField as gfld


def load_image(name):
    try:
        image = pygame.image.load(name).convert()
    except:
        print("can't load image ", name)
        raise SystemExit()

    return image


def main(x_screen_size, y_screen_size):
    pygame.init()
    # init code here
    cur_time = time.time()
    window = pygame.display.set_mode((x_screen_size, y_screen_size))
    screen = pygame.Surface((x_screen_size, y_screen_size))
    player = pygame.Surface((50, 50))
    tile = load_image('data/tile.gif')
    default_field = gfld.GameField(10, 10)
    _, default_field_y_size = default_field.get_field_size()
    height_tiles_count = int(round(y_screen_size / default_field_y_size))
    tile = pygame.transform.scale(tile, (height_tiles_count, height_tiles_count))  # height align
    done = False
    while not done:
        old_time = cur_time
        cur_time = time.time()
        dt = cur_time - old_time
        if dt < 0.01:  # max 100 fps
            time.sleep(0.01 - dt)
            cur_time = time.time()
            dt = cur_time - old_time
        # every tick action
        screen.fill((0, 125, 0))
        screen.blit(player, (50, 50))
        screen.blit(tile, (150, 150))
        window.blit(screen, (0, 0))
        # events
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                done = True
        pygame.display.update()


    pygame.quit()

main(800, 600)
