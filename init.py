import pygame

def main():
    pygame.init()
    # init code here
    window = pygame.display.set_mode((400, 400))
    screen = pygame.Surface((400, 400))
    #
    done = False
    while not done:
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                done = True
        screen.fill((0, 125, 0))
        window.blit(screen, (0, 0))
        pygame.display.update()

    pygame.quit()

main()