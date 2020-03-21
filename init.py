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
    interface_left = pygame.Surface((150, 550))
    player_turn_color = pygame.Surface((50, 50))
    interface_right = pygame.Surface((150, 550))
    default_field = gfld.GameField(12, 20)
    default_field.map[0][0] = gobj.GameObject("Blue player", 1)  # see players_queue
    default_field.map[1][2] = gobj.GameObject("Red player", 0)
    default_field_x_size, default_field_y_size = default_field.get_field_size()
    selected_obj = None
    selected_obj_pos = None
    click_pos = None
    players_queue = (
        gplr.Player("red", 10, 5, 5, 10, 10, 10),
        gplr.Player("blue", 10, 5, 5, 10, 10, 10)
                     )
    player_turn = 0
    # loading sprites
    tile = load_image('data/tile.gif')
    blue_player = load_image('data/blue_player.gif')
    red_player = load_image('data/red_player.gif')
    clicked = load_image('data/clicked.gif')
    # height align
    tiles_pixel_size = int(round(y_screen_size / ((default_field_y_size - 1) * 0.75 + 1)))
    print(tiles_pixel_size)
    align = (tiles_pixel_size, tiles_pixel_size)
    tile = pygame.transform.scale(tile, align)
    blue_player = pygame.transform.scale(blue_player, align)
    red_player = pygame.transform.scale(red_player, align)
    clicked = pygame.transform.scale(clicked, align)
    run_game = True
    while run_game:
        # dt
        old_time = cur_time
        cur_time = time.time()
        dt = cur_time - old_time
        if dt < 0.01:  # max 100 fps
            time.sleep(0.01 - dt)
            cur_time = time.time()
            dt = cur_time - old_time

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = event.pos

        # every tick action
        if players_queue[player_turn].bp == 0:
            players_queue[player_turn].bp = players_queue[player_turn].max_bp
            if len(players_queue) - 1 == player_turn:
                player_turn = 0
            else:
                player_turn += 1
        # select game object
        clicked_tile = default_field.get_clicked_obj()
        clicked_tile_pos = default_field.get_clicked_pos()
        if selected_obj_pos is not None and selected_obj.team == player_turn:  # select correct hero
            if selected_obj_pos != clicked_tile_pos:  # test
                r = default_field.tiles_route(selected_obj_pos, clicked_tile_pos)
                for i in r:
                    print(i)
                    default_field.map[i[0]][i[1]].type = "Red player"
            if default_field.near_tiles(selected_obj_pos, clicked_tile_pos) \
                    and default_field.move_person(selected_obj_pos, clicked_tile_pos):
                players_queue[player_turn].bp -= 1
        selected_obj = clicked_tile
        selected_obj_pos = clicked_tile_pos

        # draw field
        screen.fill((0, 125, 0))
        if players_queue[player_turn].team == "red":  # team colors set
            player_turn_color.fill((255, 0, 0))
        if players_queue[player_turn].team == "blue":
            player_turn_color.fill((0, 0, 255))
        interface_left.blit(player_turn_color, (10, 10))
        screen.blit(interface_left, (25, 25))
        screen.blit(interface_right, (x_screen_size - 25 - 150, 25))
        double_x_ident = x_screen_size - (default_field_x_size + 0.5) * tiles_pixel_size
        for x in range(default_field_x_size):
            for y in range(default_field_y_size):
                x_locate = int((x + (y % 2) / 2) * tiles_pixel_size + double_x_ident / 2)
                y_locate = int(tiles_pixel_size * y * 0.74)
                screen.blit(tile, (x_locate, y_locate))
                # click detecting of an inscribed circle
                if click_pos is not None and (x_locate + tiles_pixel_size / 2 - click_pos[0]) ** 2\
                        + (y_locate + tiles_pixel_size / 2 - click_pos[1]) ** 2 <= (tiles_pixel_size / 2 * 0.866) ** 2:
                    default_field.set_clicked_pos((x, y))
                    screen.blit(clicked, (x_locate, y_locate))
                if default_field.map[x][y].type == "Blue player":
                    screen.blit(blue_player, (x_locate, y_locate))
                if default_field.map[x][y].type == "Red player":
                    screen.blit(red_player, (x_locate, y_locate))
        window.blit(screen, (0, 0))

        pygame.display.update()

    pygame.quit()


main(1200, 600)
