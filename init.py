import pygame
import time
import game.gameObject as gobj
import game.gameField as gfld

def main(x_size, y_size):
    pygame.init()
    # init code here
    cur_time = time.time()
    window = pygame.display.set_mode((x_size, y_size))
    screen = pygame.Surface((x_size, y_size))
    player = pygame.Surface((50, 50))
    default_field = gfld.GameField(10, 10)
    done = False
    while not done:
        old_time = cur_time
        cur_time = time.time()
        dt = cur_time - old_time
        if dt < 0.01:  # max 100 fps
            time.sleep(0.01 - dt)
            cur_time = time.time()
            dt = cur_time - old_time

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                done = True
        screen.fill((0, 125, 0))
        screen.blit(player, (50, 50))
        window.blit(screen, (0, 0))
        pygame.display.update()
        print(dt)


    pygame.quit()

main(800, 600)
