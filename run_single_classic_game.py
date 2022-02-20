from source import *


food_color=get_random_color()

def get_random_location(snake_body, foods):
    # 不能生成到蛇身上
    food_location = {'x': random.randint(0, map_width - 2), 'y': random.randint(0, map_height - 2)}
    for snake_rect in snake_body:
        if (snake_rect['x'] == food_location['x'] and snake_rect['y'] == food_location['y']) or \
                (snake_rect['x'] == food_location['x'] + 1 and snake_rect['y'] == food_location['y']) or \
                (snake_rect['x'] == food_location['x'] and snake_rect['y'] == food_location['y'] + 1) or \
                (snake_rect['x'] == food_location['x'] + 1 and snake_rect['y'] == food_location['y'] + 1):
            food_location = {'x': random.randint(0, map_width - 2), 'y': random.randint(0, map_height - 2)}
    for food in foods:
        if (food['x'] == food_location['x'] and food['y'] == food_location['y']) or \
                (food['x'] == food_location['x'] + 1 and food['y'] == food_location['y']) or \
                (food['x'] == food_location['x'] and food['y'] == food_location['y'] + 1) or \
                (food['x'] == food_location['x'] + 1 and food['y'] == food_location['y'] + 1) or \
                (food['x'] == food_location['x'] - 1 and food['y'] == food_location['y']) or \
                (food['x'] == food_location['x'] and food['y'] == food_location['y'] - 1) or \
                (food['x'] == food_location['x'] - 1 and food['y'] == food_location['y'] - 1):
            food_location = {'x': random.randint(0, map_width - 2), 'y': random.randint(0, map_height - 2)}
    return food_location


def is_alive(snake_body):
    if snake_body[head]['x'] <= -1 or snake_body[head]['y'] <= -1 or snake_body[head]['x'] == map_width or \
            snake_body[head]['y'] == map_height:
        return False
    for point in snake_body[1:]:  # 不判断头
        if snake_body[head]['x'] == point['x'] and snake_body[head]['y'] == point['y']:
            return False
    return True


def deal_is_eating_food(last, snake_body, foods):
    global food_color
    for food_location in foods:
        if (snake_body[head]['x'] == food_location['x'] and snake_body[head]['y'] == food_location['y']) or \
                (snake_body[head]['x'] == food_location['x'] + 1 and snake_body[head]['y'] == food_location['y'] + 1) or \
                (snake_body[head]['x'] == food_location['x'] + 1 and snake_body[head]['y'] == food_location['y']) or \
                (snake_body[head]['x'] == food_location['x'] and snake_body[head]['y'] == food_location['y'] + 1):
            snake_body.append(last)
            foods.remove(food_location)
            food_color=get_random_color()
            food_location = get_random_location(snake_body, foods)
            foods.append(food_location)
    return foods


def darw_snake(screen, snake_body):
    for point in snake_body:
        x = point['x'] * ceil
        y = point['y'] * ceil  # 左上角坐标
        arect = pygame.Rect(x, y, ceil, ceil)
        pygame.draw.rect(screen, black, arect)
        inner_rect = pygame.Rect(x + 4, y + 4, ceil - 8, ceil - 8)
        pygame.draw.rect(screen, gray, inner_rect)

def draw_food(screen, foods):
    for food_location in foods:
        x = food_location['x'] * ceil
        y = food_location['y'] * ceil
        arect = pygame.Rect(x, y, ceil * 2, ceil * 2)
        pygame.draw.rect(screen, food_color, arect)



def move_snake(direction, snake_body):
    if direction == up:
        new_head = {'x': snake_body[head]['x'], 'y': snake_body[head]['y'] - 1}
    elif direction == down:
        new_head = {'x': snake_body[head]['x'], 'y': snake_body[head]['y'] + 1}
    elif direction == left:
        new_head = {'x': snake_body[head]['x'] - 1, 'y': snake_body[head]['y']}
    elif direction == right:
        new_head = {'x': snake_body[head]['x'] + 1, 'y': snake_body[head]['y']}
    snake_body.insert(0, new_head)
    last = snake_body[-1]
    del snake_body[-1]
    return last



def run_single_classic_game(screen, speed_clock,player_name):
    # screen=pygame.display.set_mode(size=(500,500),flags=HWSURFACE)
    start_x = random.randint(5, map_width - 8)
    start_y = random.randint(3, map_height - 3)
    snake_body = [{'x': start_x, 'y': start_y}, {'x': start_x - 1, 'y': start_y}, {'x': start_x - 2, 'y': start_y}]
    direction = right
    foods = []
    last=snake_body[2]

    for i in range(3):
        food_location = get_random_location(snake_body, foods)
        foods.append(food_location)
    while True:
        pre_move = false
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != right:
                    direction = left
                    last = move_snake(direction, snake_body)
                    pre_move = true
                elif (event.key == K_RIGHT or event.key == K_d) and direction != left:
                    direction = right
                    last = move_snake(direction, snake_body)
                    pre_move=true
                elif (event.key == K_UP or event.key == K_w) and direction != down:
                    direction = up
                    last = move_snake(direction, snake_body)
                    pre_move=true
                elif (event.key == K_DOWN or event.key == K_s) and direction != up:
                    direction = down
                    last = move_snake(direction, snake_body)
                    pre_move=true
                elif event.key == K_ESCAPE:
                    return 'esc'
                elif event.key==K_SPACE:
                    if pause_game(screen)=='ecs':
                        return 'esc'
        foods = deal_is_eating_food(last, snake_body, foods)
        if pre_move==false:
            last = move_snake(direction, snake_body)
            foods = deal_is_eating_food(last, snake_body, foods)
        if not is_alive(snake_body):
            score=len(snake_body) - 3
            update_rank(player_name,score)
            return show_end_info(screen)
        screen.fill(white)
        darw_snake(screen, snake_body)
        draw_food(screen, foods)
        draw_score(screen, len(snake_body) - 3)
        pygame.display.update()
        speed_clock.tick(10 + len(snake_body) / 2)
       # speed_clock.tick(25)


