import pygame
import time
import game.gameObject as gobj
import game.gameField as gfld
import game.player as gplr


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
    interface = pygame.Surface((150, 550))
    default_field = gfld.GameField(10, 10)
    default_field_x_size, default_field_y_size = default_field.get_field_size()
    # loading sprites
    tile = load_image('data/tile.gif')
    player = load_image('data/blue_player.gif')
    # height align
    tiles_pixel_size = int(y_screen_size / (default_field_y_size * 0.75) - 0.25 * default_field_y_size)
    align = (tiles_pixel_size, tiles_pixel_size)
    tile = pygame.transform.scale(tile, align)
    player = pygame.transform.scale(player, align)
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
        screen.blit(interface, (25, 25))
        screen.blit(interface, (x_screen_size - 25 - 150, 25))
        # draw field
        double_x_ident = x_screen_size - (default_field_x_size + 0.5) * tiles_pixel_size
        for x in range(default_field_x_size):
            for y in range(default_field_y_size):
                x_locate = (x + (y % 2) / 2) * tiles_pixel_size + double_x_ident / 2
                y_locate = tiles_pixel_size * y * 0.75
                screen.blit(tile, (x_locate, y_locate))
                if default_field.map[x][y].type == "Player":
                    screen.blit(player, (x_locate, y_locate))
        window.blit(screen, (0, 0))

        # events
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                done = True
        pygame.display.update()


    pygame.quit()

main(1200, 600)
