from source import *

def get_random_food():
    size = random.randint(1, 3)
    x = random.randint(0, 60 - size)
    y = random.randint(0, 40 - size)
    color = get_random_color()
    food = food_block(x, y, size, color)
    return food


def draw_food(screen, foods):
    for food in foods:
        food.show(screen)


def is_eating_food(mysnake, foods):
    for food in foods:
        if mysnake.is_eating_food(food):
            mysnake.deal_eating_food(food)
            foods.remove(food)


def generate_food(foods, food_number):
    while len(foods) > food_number:
        foods.remove(foods[0])
    while len(foods) < food_number:
        foods.append(get_random_food())


def move_foods(foods, food_move_time):
    if food_move_time == 20:
        for food in foods:
            food.move()
        food_move_time = 0
    food_move_time += 1
    return food_move_time


def run_single_new_game(screen, speed_clock, player_name):
    mysnake = snake()
    foods = []
    for i in range(3):
        foods.append(get_random_food())
    direction = right
    food_number = 3
    food_move_time = 0
    star=star_block(20,15,1)
    while true:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    direction = left
                elif event.key == K_RIGHT or event.key == K_d:
                    direction = right
                elif event.key == K_UP or event.key == K_w:
                    direction = up
                elif event.key == K_DOWN or event.key == K_s:
                    direction = down
                elif event.key == K_ESCAPE:
                    return 'esc'
                elif event.key == K_SPACE:
                    if pause_game(screen) == 'ecs':
                        return 'esc'
        screen.fill(white)
        star.show(screen)
        mysnake.move(direction)
        is_eating_food(mysnake, foods)
        generate_food(foods, food_number)
        food_move_time = move_foods(foods, food_move_time)
        direction = stay
        mysnake.show(screen)
        draw_food(screen, foods)
        draw_score(screen, mysnake.score)
        if not mysnake.is_alive():
            return show_end_info(screen)
        pygame.display.update()
        if(len(mysnake.body)/3)<=100:
            speed_clock.tick(10 + len(mysnake.body) / 3)
        else:
            speed_clock.tick(110)


if __name__ == '__main__':
    screen = graph_init()
    speed_clock = pygame.time.Clock()
    run_single_new_game(screen, speed_clock, '张泽凌')
