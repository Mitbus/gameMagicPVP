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


def button_click_action(click_active, click_pos, x_pos, y_pos, block_size, mp, inc_mp, screen, button, button_pressed):
    ret_mp = mp
    if click_active and 0 < click_pos[0] - x_pos < block_size and 0 < click_pos[1] - y_pos < block_size:
        if inc_mp < 0:
            if mp > 0:
                ret_mp += inc_mp
        else:
             ret_mp += inc_mp
        screen.blit(button_pressed, (x_pos, y_pos))
    else:
        screen.blit(button, (x_pos, y_pos))
    return ret_mp


def chose_color(player_turn):
    color = None
    if player_turn == 0:  # team colors set
        color = (255, 0, 0)
    if player_turn == 1:
        color = (0, 0, 255)
    return color


def main(x_screen_size, y_screen_size):
    pygame.init()
    # init code here
    cur_time = time.time()
    window = pygame.display.set_mode((x_screen_size, y_screen_size),
                                    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
    screen = pygame.Surface((x_screen_size, y_screen_size))
    default_field = gfld.GameField(7, 17, "hex1")
    players = [  # hero_type, team, hp, dmg, mp_d, mp_i, mp_c, mp_h
        gplr.Player("Red player", 0, 10, 5, 10, 10, 10, 10),
        gplr.Player("Blue player", 1, 1, 1, 0, 5, 10, 7)
    ]
    default_field.map[6][0].set_hero(players[0])  # see players_queue
    default_field.map[6][4].set_hero(players[1])
    default_field_x_size, default_field_y_size = default_field.get_field_size()
    selected_obj = None
    selected_obj_pos = None
    click_pos = None
    click_active = False
    mp_d, mp_i, mp_c, mp_h = 0, 0, 0, 0  # for interface menu
    is_light = None
    l_color, d_color = (255, 255, 255), (255, 255, 255)
    ench_or_invoke_param = 0 # -3 ench, 3 invoke
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
    button_plus = load_image('data/button_+.gif')
    button_plus_pressed = load_image('data/button_+_pressed.gif')
    button_minus = load_image('data/button_-.gif')
    button_minus_pressed = load_image('data/button_-_pressed.gif')
    button_line = load_image('data/button_line.gif')
    button_line_cursore = load_image('data/button_line_cursore.gif')


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
    block_size = min(interface_x_len // 8, interface_y_len // 30)
    block_sizes = (block_size, block_size)
    button_plus = pygame.transform.scale(button_plus, block_sizes)
    button_plus_pressed = pygame.transform.scale(button_plus_pressed, block_sizes)
    button_minus = pygame.transform.scale(button_minus, block_sizes)
    button_minus_pressed = pygame.transform.scale(button_minus_pressed, block_sizes)
    button_line = pygame.transform.scale(button_line, (interface_x_len // 3 * 2, block_size))
    button_line_cursore = pygame.transform.scale(button_line_cursore, block_sizes)
    interface_left = pygame.Surface((interface_x_len, interface_y_len))
    interface_left.set_alpha(30)
    interface_right = pygame.Surface((interface_x_len, interface_y_len))
    interface_right.set_alpha(30)
    player_turn_color = pygame.Surface(block_sizes)
    # TODO: add images
    test_block = pygame.Surface(block_sizes)
    test_block.fill((0, 0, 0))
    test_block.set_alpha(70)
    hero_hp_block = pygame.Surface(block_sizes)
    hero_hp_block.fill((255, 0, 0))
    hero_mp_block = pygame.Surface(block_sizes)
    hero_mp_block.fill((0, 0, 255))
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
                click_active = True
            else:
                click_active = False

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
        # right
        print(click_pos, click_active)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('Magic craft:', 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('__________', 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + interface_y_len // 25))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('Destroy: ' + str(mp_d), 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + 2 * interface_y_len // 25))
        mp_d = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9,
                                   interface_x_len // 20 + 3 * interface_y_len // 25, block_size, mp_d, -1,
                                   screen, button_minus, button_minus_pressed)
        mp_d = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9 + interface_x_len // 6,
                                   interface_x_len // 20 + 3 * interface_y_len // 25, block_size, mp_d, 1,
                                   screen, button_plus, button_plus_pressed)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('Illusion: ' + str(mp_i), 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + 4 * interface_y_len // 25))
        mp_i = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9,
                                   interface_x_len // 20 + 5 * interface_y_len // 25, block_size, mp_i, -1,
                                   screen, button_minus, button_minus_pressed)
        mp_i = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9 + interface_x_len // 6,
                                   interface_x_len // 20 + 5 * interface_y_len // 25, block_size, mp_i, 1,
                                   screen, button_plus, button_plus_pressed)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('Call: ' + str(mp_c), 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + 6 * interface_y_len // 25))
        mp_c = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9,
                                   interface_x_len // 20 + 7 * interface_y_len // 25, block_size, mp_c, -1,
                                   screen, button_minus, button_minus_pressed)
        mp_c = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9 + interface_x_len // 6,
                                   interface_x_len // 20 + 7 * interface_y_len // 25, block_size, mp_c, 1,
                                   screen, button_plus, button_plus_pressed)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('Heal: ' + str(mp_h), 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + 8 * interface_y_len // 25))
        mp_h = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9,
                                   interface_x_len // 20 + 9 * interface_y_len // 25, block_size, mp_h, -1,
                                   screen, button_minus, button_minus_pressed)
        mp_h = button_click_action(click_active, click_pos,
                                   int(x_screen_size - interface_x_len) + interface_x_len // 9 + interface_x_len // 6,
                                   interface_x_len // 20 + 9 * interface_y_len // 25, block_size, mp_h, 1,
                                   screen, button_plus, button_plus_pressed)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('__________', 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 10,
                     interface_x_len // 20 + 10 * interface_y_len // 25))
        if click_active \
                and 0 < click_pos[0] - (int(x_screen_size - interface_x_len) + interface_x_len // 9) < 2 * block_size \
                and 0 < click_pos[1] - (interface_x_len // 20 + 11 * interface_y_len // 25) < block_size:
            is_light = True
            l_color = (255, 255, 255)
            d_color = (127, 127, 127)
        if click_active \
                and 0 < click_pos[0] - (int(x_screen_size - interface_x_len)
                                        + interface_x_len // 9 + interface_x_len // 2) < 2 * block_size \
                and 0 < click_pos[1] - (interface_x_len // 20 + 11 * interface_y_len // 25) < block_size:
            is_light = False
            l_color = (127, 127, 127)
            d_color = (255, 255, 255)
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('light', 1, l_color),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 9,
                     interface_x_len // 20 + 11 * interface_y_len // 25))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('dark', 1, d_color),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 9 + interface_x_len // 2,
                     interface_x_len // 20 + 11 * interface_y_len // 25))
        screen.blit(button_line, (int(x_screen_size - interface_x_len) + interface_x_len // 6,
                                  interface_x_len // 20 + 12 * interface_y_len // 25))
        i_param = -3
        while i_param < 4:
            if click_active and 0 < click_pos[0] - (int(x_screen_size - interface_x_len) + interface_x_len // 2
                                                    + (interface_x_len * i_param) // 9 - block_size // 2) < block_size \
                    and 0 < click_pos[1] - (interface_x_len // 20 + 12 * interface_y_len // 25) < block_size:
                ench_or_invoke_param = i_param
            i_param += 1
        screen.blit(button_line_cursore, (int(x_screen_size - interface_x_len) + interface_x_len // 2
                                          + (interface_x_len * ench_or_invoke_param) // 9 - block_size // 2,
                                          interface_x_len // 20 + 12 * interface_y_len // 25))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                    .render('CREATE', 1, (255, 255, 255)),
                    (int(x_screen_size - interface_x_len) + interface_x_len // 4,
                     interface_x_len // 20 + 13 * interface_y_len // 25))


        screen.blit(interface_right, (int(x_screen_size - interface_x_len), 0))
        # left
        player_turn_color.fill(chose_color(player_turn))
        screen.blit(player_turn_color, (int(interface_x_len * 0.8), interface_x_len // 20))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('Player turn:', 1, (255, 255, 255)),
                    (interface_x_len // 10, interface_x_len // 20))
        screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('__________', 1, (255, 255, 255)),
                    (interface_x_len // 10, interface_x_len // 20 + interface_y_len // 25))
        if selected_obj is not None and selected_obj.hero is not None:
            step_blocks_down = 2  # for blocks step, 1 for players turn + empty line
            if selected_obj.hero.team is not None:
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                            .render('TEAM:', 0, (255, 255, 255)),
                            (interface_x_len // 10, interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                player_turn_color.fill(chose_color(selected_obj.hero.team))
                screen.blit(player_turn_color, (int(interface_x_len * 0.5),
                                                interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                step_blocks_down += 1
            if selected_obj.hero.dmg is not None:
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                            .render('DMG: ' + str(selected_obj.hero.dmg), 0, (255, 255, 255)),
                            (interface_x_len // 10, interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                step_blocks_down += 1
            if selected_obj.hero.hp is not None:
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30))
                            .render('HP:', 0, (255, 255, 255)),
                            (interface_x_len // 10, interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                i = 0
                while selected_obj.hero.hp > i:
                    screen.blit(hero_hp_block, (int(interface_x_len // 9 + (i % 5) * interface_x_len // 6),
                                                int(interface_x_len // 20
                                                    + interface_y_len // 25 * (step_blocks_down + 1 + (i // 5)))))
                    i += 1
                step_blocks_down += ((i + 4) // 5) + 2
            if selected_obj.hero.mp_destroy is not None:
                hero_mp_block.fill((127, 0, 255))
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('DESTROY:', 0, (255, 255, 255)),
                            (interface_x_len // 10,
                             interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                i = 0
                while selected_obj.hero.mp_destroy > i:
                    screen.blit(hero_mp_block, (int(interface_x_len // 9 + (i % 5) * interface_x_len // 6),
                                                int(interface_x_len // 20
                                                    + interface_y_len // 25 * (step_blocks_down + 1 + (i // 5)))))
                    i += 1
                step_blocks_down += ((i + 4) // 5) + 2
            if selected_obj.hero.mp_illusion is not None:
                hero_mp_block.fill((255, 255, 0))
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('ILLUSION:', 0, (255, 255, 255)),
                            (interface_x_len // 10,
                             interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                i = 0
                while selected_obj.hero.mp_illusion > i:
                    screen.blit(hero_mp_block, (int(interface_x_len // 9 + (i % 5) * interface_x_len // 6),
                                                int(interface_x_len // 20
                                                    + interface_y_len // 25 * (step_blocks_down + 1 + (i // 5)))))
                    i += 1
                step_blocks_down += ((i + 4) // 5) + 2
            if selected_obj.hero.mp_call is not None:
                hero_mp_block.fill((0, 255, 255))
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('CALL:', 0, (255, 255, 255)),
                            (interface_x_len // 10,
                             interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                i = 0
                while selected_obj.hero.mp_call > i:
                    screen.blit(hero_mp_block, (int(interface_x_len // 9 + (i % 5) * interface_x_len // 6),
                                                int(interface_x_len // 20
                                                    + interface_y_len // 25 * (step_blocks_down + 1 + (i // 5)))))
                    i += 1
                step_blocks_down += ((i + 4) // 5) + 2
            if selected_obj.hero.mp_heal is not None:
                hero_mp_block.fill((255, 127, 127))
                screen.blit(pygame.font.Font(None, int(interface_y_len / 30)).render('HEAL:', 0, (255, 255, 255)),
                            (interface_x_len // 10,
                             interface_x_len // 20 + interface_y_len // 25 * step_blocks_down))
                i = 0
                while selected_obj.hero.mp_heal > i:
                    screen.blit(hero_mp_block, (int(interface_x_len // 9 + (i % 5) * interface_x_len // 6),
                                                int(interface_x_len // 20
                                                    + interface_y_len // 25 * (step_blocks_down + 1 + (i // 5)))))
                    i += 1
                step_blocks_down += ((i + 4) // 5) + 2

        screen.blit(interface_left, (0, 0))

        # draw map
        clicked_on_map = False
        double_x_ident = x_screen_size - (default_field_x_size + 0.5) * tiles_pixel_size
        correction_on_center = 0
        if default_field.field_type == "hex":
            correction_on_center = tiles_pixel_size // 4
            correction_on_center *= -1 if default_field.get_field_size()[0] % 4 == 3 else 1
        for x in range(default_field_x_size):
            for y in range(default_field_y_size):
                x_locate = int((x + (y % 2) / 2) * tiles_pixel_size + double_x_ident / 2 + correction_on_center)
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
