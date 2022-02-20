from source import *
from run_single_classic_game import run_single_classic_game
from run_single_new_game import run_single_new_game

if __name__ == "__main__":
    screen = graph_init()
    first_choice = second_choice = -1
    speed_clock = pygame.time.Clock()
    while true:
        first_choice = show_pages(screen, 0, 3)  # 显示1，2,3三个按钮，即开始界面
        if first_choice == single_button.button_flag:
            player_name='未登录'
            player_name=input_name()
            while true:
                second_choice = show_pages(screen, 3, 7,player_name=player_name)  # 显示3，4，5,6三个按钮，即单人模式选项界面
                if second_choice == single_return_button.button_flag:
                    break
                elif second_choice == single_classic_button.button_flag:
                    while true:
                        return_singal = run_single_classic_game(screen, speed_clock, player_name)
                        if return_singal == 'restart':
                            continue
                        elif return_singal == 'esc':
                            break
                elif second_choice == single_new_button.button_flag:
                    while true:
                        return_singal=run_single_new_game(screen,speed_clock,player_name)
                        if return_singal=='restart':
                            continue
                        elif return_singal=='esc':
                            break
                elif second_choice==single_rank_button.button_flag:
                    show_ranks()
        elif first_choice == double_button.button_flag:
            second_choice = show_pages(screen, 7, 10)  # 显示6，7，8三个按钮，表示双人模式选项界面
            if second_choice == 8:
                continue
        elif first_choice == quit_login_button.button_flag:
            terminate()

