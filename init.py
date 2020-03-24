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
    window = pygame.display.set_mode((x_screen_size, y_screen_size))#,
                                    # pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
    screen = pygame.Surface((x_screen_size, y_screen_size))
    default_field = gfld.GameField(13, 13, "hex")
    players = [
        gplr.Player("Red player", 0, 10, 1, 10, 10, 10),
        gplr.Player("Blue player", 1, 1, 1, 10, 10, 10)
    ]
    default_field.map[6][0].set_hero(players[0])  # see players_queue
    default_field.map[6][12].set_hero(players[1])
    default_field_x_size, default_field_y_size = default_field.get_field_size()
    selected_obj = None
    selected_obj_pos = None
    click_pos = None
    players_queue = (  # [bp, max_bp]
        [3, 3],
        [0, 3]
        )
    player_turn = 0
    # loading sprites
    tile = load_image('data/tile.gif')
    clicked = load_image('data/clicked.gif')
    bones = load_image('data/bones.gif')
    blue_player = load_image('data/blue_player.gif')
    red_player = load_image('data/red_player.gif')
    # height align
    tiles_pixel_size = int(round(y_screen_size / ((default_field_y_size - 1) * 0.75 + 1)))
    align = (tiles_pixel_size, tiles_pixel_size)
    tile = pygame.transform.scale(tile, align)
    clicked = pygame.transform.scale(clicked, align)
    bones = pygame.transform.scale(bones, align)
    blue_player = pygame.transform.scale(blue_player, align)
    red_player = pygame.transform.scale(red_player, align)
    # interface size
    interface_x_len = int((x_screen_size - (default_field.get_field_size()[0] + 0.5) * tiles_pixel_size) / 2)
    interface_y_len = y_screen_size
    interface_left = pygame.Surface((interface_x_len, interface_y_len))
    interface_left.set_alpha(30)
    player_turn_color = pygame.Surface((interface_x_len // 7, interface_x_len // 7))
    # TODO: add images
    hero_hp_block = pygame.Surface((interface_x_len // 8, interface_x_len // 8))
    hero_hp_block.fill((255, 0, 0))
    interface_right = pygame.Surface((interface_x_len, interface_y_len))
    run_game = True
    while run_game:
        # dt
        old_time = cur_time
        cur_time = time.time()
        dt = cur_time - old_time
        if dt < 0.1:  # max 10 fps
            time.sleep(0.1 - dt)
            cur_time = time.time()
            dt = cur_time - old_time
        # events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = event.pos

        # every tick action
        if players_queue[player_turn][0] == 0:
            click_pos = None
            if len(players_queue) - 1 == player_turn:  # switch to anover
                player_turn = 0
            else:
                player_turn += 1
            if players[player_turn].hp > 0:
                players_queue[player_turn][0] = players_queue[player_turn][1]
        # select game object
        clicked_tile = default_field.get_clicked_obj()
        clicked_tile_pos = default_field.get_clicked_pos()
        if clicked_tile_pos is not None and selected_obj_pos is not None and selected_obj.hero is not None:
            if selected_obj.hero.team == player_turn and default_field.near_tiles(selected_obj_pos, clicked_tile_pos) \
                    and default_field.move_person(selected_obj_pos, clicked_tile_pos):  # move hero
                players_queue[player_turn][0] -= 1
            elif clicked_tile.hero is not None and clicked_tile.hero.team != player_turn \
                    and default_field.near_tiles(selected_obj_pos, clicked_tile_pos):  # dmg clicked hero
                print(1)
                players_queue[player_turn][0] -= 1
                if clicked_tile.hero.get_dmg_is_dead(selected_obj.hero.dmg):
                    clicked_tile.hero = None
                    clicked_tile.placed_item = "Bones"
        selected_obj = clicked_tile
        selected_obj_pos = clicked_tile_pos

        # draw field
        screen.fill((0, 125, 0))
        # interface
        color = None
        if player_turn == 0:  # team colors set
            color = (255, 0, 0)
        if player_turn == 1:
            color = (0, 0, 255)
        player_turn_color.fill(color)
        text_color = (0, 0, 0)
        if selected_obj is not None and selected_obj.hero is not None:
            if selected_obj.hero.hp is not None:
                screen.blit(pygame.font.Font(None, int(interface_x_len / 6)).render('HP:', 0, (255, 255, 255)),
                                    (interface_x_len // 10, interface_x_len // 20 + interface_y_len // 20))
                i = 0
                while selected_obj.hero.hp > i:
                    screen.blit(hero_hp_block,
                                (int(interface_x_len // 20
                                     + (i % 4) * interface_x_len // 6
                                     + interface_x_len // 16 * 5),
                                 int(interface_y_len // 20 * (1.2 + 0.7 * (i // 4)))))
                    i += 1
        screen.blit(pygame.font.Font(None, int(interface_x_len / 6)).render('Player turn:', 1, color),
                            (interface_x_len // 10, interface_x_len // 20))
        screen.blit(player_turn_color, (int(interface_x_len * 0.8), interface_x_len // 20))
        screen.blit(interface_left, (0, 0))
        screen.blit(interface_right, (int(x_screen_size - interface_x_len), 0))

        clicked_on_map = False
        double_x_ident = x_screen_size - (default_field_x_size + 0.5) * tiles_pixel_size
        for x in range(default_field_x_size):
            for y in range(default_field_y_size):
                x_locate = int((x + (y % 2) / 2) * tiles_pixel_size + double_x_ident / 2)
                y_locate = int(tiles_pixel_size * y * 0.74)
                # field_type
                if default_field.map[x][y].field_type == "No tile":
                    continue
                if default_field.map[x][y].field_type == "Empty":
                    screen.blit(tile, (x_locate, y_locate))
                # click detecting of an inscribed circle
                if click_pos is not None and (x_locate + tiles_pixel_size / 2 - click_pos[0]) ** 2\
                        + (y_locate + tiles_pixel_size / 2 - click_pos[1]) ** 2 <= (tiles_pixel_size / 2 * 0.866) ** 2:
                    default_field.set_clicked_pos((x, y))
                    screen.blit(clicked, (x_locate, y_locate))
                    clicked_on_map = True
                # items
                if default_field.map[x][y].placed_item is not None:
                    if default_field.map[x][y].placed_item == "Bones":
                        screen.blit(bones, (x_locate, y_locate))
                # hero
                if default_field.map[x][y].hero is not None:
                    if default_field.map[x][y].hero.type == "Blue player":
                        screen.blit(blue_player, (x_locate, y_locate))
                    if default_field.map[x][y].hero.type == "Red player":
                        screen.blit(red_player, (x_locate, y_locate))
        if not clicked_on_map:
            default_field.set_clicked_pos(None)

        window.blit(screen, (0, 0))

        pygame.display.update()

    pygame.quit()


main(1280, 720)
