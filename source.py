import sys

import pygame
import random
from pygame.locals import *
import time
from tkinter import *
import tkinter.font as tkfont
from tkinter import ttk
import pymysql
from socket import gethostname

true = True
false = False
player_name = ''
player1_name = ''
player2_name = ''
font_path = 'C:\\Windows\\Fonts\\Dengb.ttf'
# 窗口与像素大小
window_width = 900
window_height = 600
ceil = 15  # 单个方块大小
map_width = int(window_width / ceil)
map_height = int(window_height / ceil)
# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (216, 191, 216)
green = (0, 255, 0)
dark_green = (0, 155, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
cyan = (0, 188, 212)
yellow = (255, 235, 59)
amber = (255, 193, 7)
dark_blue = (0, 0, 139)
# 游戏背景颜色
BG_color = black
# 定义方向
up = 1
down = 2
left = 3
right = 4
stay = 5
# 头部下标
head = 0
font_size = 40  # 字符大小
# 点中的是哪个按钮
button_flag = -1  # 不指向任何一个button
single_classic_data_unit = {
    "player_name": '',
    'score': int,
    'from_computer': '',
    'time': ''
}

class block():
    def __init__(self, x, y, size, direction):
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction

    def move(self):
        if self.direction == up:
            self.y -= 1
        elif self.direction == down:
            self.y += 1
        elif self.direction == left:
            self.x -= 1
        elif self.direction == right:
            self.x += 1
        elif self.direction == stay:
            return

    def is_out(self):
        if self.x < 0 or self.x >= map_width or self.y < 0 or self.y >= map_height:
            return true

    def is_in(self):
        return not self.is_out()

class food_block(block):
    def __init__(self, x, y, size, color, direction=stay):
        block.__init__(self, x, y, size,
                       direction)  # 等价于super(food_block,self).__init__(x, y, size, direction),里面没有self
        self.color = color  # 食物都是纯色
        self.point=4-self.size #越大的食物分越小长得越长 越小的食物分越大长的越小

    def show(self, screen):
        x = self.x * ceil
        y = self.y * ceil
        arect = pygame.Rect(x, y, ceil * self.size, ceil * self.size)
        pygame.draw.rect(screen, self.color, arect)

    def random_direction(self):
        self.direction = random.randint(1, 5)

    def deal_out(self):
        if self.x < 0:
            self.x += 1
        elif self.x + self.size >= map_width:
            self.x -= self.size
        if self.y < 0:
            self.y += 1
        elif self.y + self.size >= map_height:
            self.y -= self.size

    def move(self):
        self.deal_out()
        self.random_direction()
        super(food_block, self).move()

    def change_size(self):
        self.size += random.randint(-1, 1)
        if self.size <= 0:
            self.size += 1
        elif self.size >= 4:
            self.size -= 1

class star_block(block):
    def __init__(self, x, y, size, direction=stay, color=red):
        super(star_block, self).__init__(x, y, size, direction)
        self.color = color
    def show(self,screen):
        x=self.x*ceil
        y=self.y*ceil
        points=[(x+ceil/3*1,y),(x+ceil/3*2,y),(x+ceil,y+ceil/3*1),(x+ceil,y+ceil/3*2),(x+ceil/3*2,y+ceil),(x+ceil/3*1,y+ceil),(x,y+ceil/3*2),(x,y+ceil/3*1)]
        #顶点要是顺时针
        pygame.draw.polygon(screen,self.color,points)

class snake_block(block):
    def __init__(self, x, y, direction, size=1, in_color=gray, outer_color=black):
        super(snake_block, self).__init__(x, y, size, direction)
        self.inner_color = in_color
        self.outer_color = outer_color

    def show(self, screen):
        x = self.x * ceil
        y = self.y * ceil
        outer_rect = pygame.Rect(x, y, ceil * self.size, ceil * self.size)
        inner_rect = pygame.Rect(x + 4, y + 4, ceil - 8, ceil - 8)
        pygame.draw.rect(screen, self.outer_color, outer_rect)
        pygame.draw.rect(screen, self.inner_color, inner_rect)

    def move(self):
        super(snake_block, self).move()
        self.deal_out()

    def deal_out(self,sequence_number=1):
        if self.x < 0:
            self.x = map_width - sequence_number
        elif self.x >= map_width:
            self.x = sequence_number-1
        if self.y < 0:
            self.y = map_height - sequence_number
        elif self.y >= map_height:
            self.y = sequence_number-1

class snake():
    def __init__(self):
        start_x = random.randint(5, map_width - 8)
        start_y = random.randint(3, map_height - 3)
        self.body = []
        outer_number=0
        for i in range(0, 3):
            asnake_block=snake_block(start_x - i, start_y, right)
            if asnake_block.is_out():
                asnake_block.deal_out(outer_number+1)
                outer_number+=1#防止生成出界
            self.body.append(asnake_block)
        self.lenth = 3
        self.score = self.lenth - 3

    def reverse_direction(self):
        for ablock in self.body:
            if ablock.direction == up:
                ablock.direction = down
            elif ablock.direction == down:
                ablock.direction = up
            elif ablock.direction == left:
                ablock.direction = right
            elif ablock.direction == right:
                ablock.direction = left
        self.body.reverse()

    def is_reverse(self, direction):
        if self.body[0].direction == up and direction == down:
            return true
        elif self.body[0].direction == down and direction == up:
            return true
        elif self.body[0].direction == left and direction == right:
            return true
        elif self.body[0].direction == right and direction == left:
            return true
        return false

    def move(self, direction):
        if direction == stay:
            direction = self.body[0].direction
        if self.is_reverse(direction):
            self.reverse_direction()
            for ablock in self.body:
                ablock.move()
        else:
            for i in range(len(self.body) - 1, 0, -1):  # 从最后一个元素（len(self.body)-1），到除了第一个元素0，每次减一
                self.body[i].direction = self.body[i - 1].direction
                self.body[i].move()
            if self.body[0].direction != down and direction == up:
                self.body[0].direction = up
            elif self.body[0].direction != up and direction == down:
                self.body[0].direction = down
            elif self.body[0].direction != left and direction == right:
                self.body[0].direction = right
            elif self.body[0].direction != right and direction == left:
                self.body[0].direction = left
            self.body[0].move()

    def is_eating_food(self, afood: food_block):
        if self.body[0].x in range(afood.x, afood.x + afood.size) and self.body[0].y in range(afood.y,afood.y + afood.size):
            return true

    def deal_eating_food(self, afood: food_block):
        self.score += afood.point
        outer_number=0
        for i in range(afood.size):
            self.add_one()
            if self.body[-1].is_out():
                self.body[-1].deal_out(outer_number+1)
                outer_number+=1 #防止生成出界

    def add_one(self):
        direction = self.body[-1].direction  # 蛇最后一个方块的方向
        x = self.body[-1].x
        y = self.body[-1].y
        if direction==up:
            self.body.append(snake_block(x,y+1,direction))
        elif direction==down:
            self.body.append(snake_block(x,y-1,direction))
        elif direction==left:
            self.body.append(snake_block(x+1,y,direction))
        elif direction==right:
            self.body.append(snake_block(x-1,y,direction))
    def minus_one(self):
        del self.body[-1]

    def show(self, screen):
        for ablock in self.body:
            ablock.show(screen)

    def is_alive(self):
        head=self.body[0]
        for i in range(1,len(self.body)):
            if head.x==self.body[i].x and head.y==self.body[i].y:
                return false
        return true




class button():  # 封装按钮类
    def __init__(self, button_flag, pos, text, is_enabled=false, back_color=gray, font_color=black,
                 font_path='C:\\Windows\\Fonts\\Dengb.ttf', font_size=40, bias=10):
        self.button_flag = button_flag
        self.pos = pos
        self.text = text
        self.bias = bias
        self.font_size = font_size
        self.back_color = back_color
        self.font_color = font_color
        self.font_path = font_path
        self.is_enabled = is_enabled

    def show_background_rect(self, screen):
        background_rect = pygame.Rect(self.pos[0] - self.bias, self.pos[1] - self.bias,
                                      len(self.text) * self.font_size + 2 * self.bias, self.font_size + 2 * self.bias)
        pygame.draw.rect(screen, self.back_color, background_rect)

    def show_text(self, screen):
        if self.is_enabled == true:
            font = pygame.font.Font(self.font_path, self.font_size)
            text = font.render(self.text, true, self.font_color)
            screen.blit(text, self.pos)

    def is_over_button(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + len(self.text) * self.font_size and self.pos[1] <= pos[1] <= self.pos[
            1] + 1 * self.font_size and self.is_enabled == true:
            return True
        else:
            return False

    def mouse_down_change(self, screen):
        if self.is_enabled == true:
            self.back_color = dark_gray
            self.show_background_rect(screen)
            self.show_text(screen)

    def mouse_up_change(self, screen):
        if self.is_enabled == true:
            self.back_color = gray
            self.show_text(screen)





def get_random_color():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color


def graph_init():
    pygame.init()
    screen = pygame.display.set_mode(size=(window_width, window_height), flags=HWSURFACE)
    pygame.display.set_caption("python贪吃蛇")
    return screen


def terminate():
    pygame.quit()
    sys.exit(0)


def deal_mouse_move(mouse_pos, screen, player_name, button_start):
    for abutton in buttons:
        if abutton.is_over_button(mouse_pos):
            abutton.show_background_rect(screen)
            abutton.show_text(screen)
            pygame.display.update()
            return
    screen.fill(white)
    for abutton in buttons:
        abutton.show_text(screen)
    if button_start == 3 or button_start == 7:
        show_player_name(screen, player_name)
    pygame.display.update()


def deal_mouse_down(mouse_pos, screen):
    global button_flag
    for abutton in buttons:
        if abutton.is_over_button(mouse_pos):
            abutton.mouse_down_change(screen)
            button_flag = abutton.button_flag
            pygame.display.update()
            return


def deal_mouse_up(mouse_pos, screen):
    global button_flag  # 使用全局
    for abutton in buttons:
        if button_flag == abutton.button_flag:
            if abutton.is_over_button(mouse_pos):
                abutton.back_color = gray
                return abutton.button_flag  # 鼠标按键抬起来的时候在哪个按钮上，也就是点击了哪个按钮，返回按钮编号
            else:
                abutton.mouse_up_change(screen)
    button_flag = -1
    pygame.display.update()


def show_pages(screen, button_start, button_end, player_name='未登录'):
    screen.fill(white)
    for abutton in buttons[button_start:button_end]:
        abutton.is_enabled = true
        abutton.show_text(screen)
    pygame.display.update()
    if button_start == 3 or button_start == 7:
        show_player_name(screen, player_name)
    while true:
        time.sleep(0.015)
        mouse_pos = pygame.mouse.get_pos()
        deal_mouse_move(mouse_pos, screen, player_name, button_start)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    deal_mouse_down(mouse_pos, screen)
            if event.type == MOUSEBUTTONUP:
                choice = -1
                if event.button == 1:
                    choice = deal_mouse_up(mouse_pos, screen)
                if choice != -1:
                    for abutton in buttons[button_start:button_end]:
                        abutton.is_enabled = false
                    return choice


def show_player_name(screen, player_name):
    font = pygame.font.Font(font_path, font_size)
    tip1 = font.render('你好！%s' % player_name, true, green)
    screen.blit(tip1, (20, 20))


def get_rank(rank_datas):
    db = pymysql.connect(host='175.24.100.167', user='root',passwd= '000815', database='snake')
    cursor = db.cursor()
    sql = 'select * from single_classic_top10'
    cursor.execute(sql)
    datas = cursor.fetchall()
    for unit in datas:
        single_classic_data_unit['player_name'] = unit[0]
        single_classic_data_unit['score'] = unit[1]
        single_classic_data_unit['from_computer'] = unit[2]
        single_classic_data_unit['time'] = unit[3]
        temp = single_classic_data_unit.copy()
        rank_datas.append(temp)
    rank_datas = sorted(rank_datas, key=lambda i: (i['score'], i['player_name']), reverse=true)
    db.close()
    return rank_datas


def update_rank(player_name, score):
    if player_name == '未登录':
        return
    rank_datas = get_rank([])
    single_classic_data_unit['player_name'] = player_name;
    single_classic_data_unit['score'] = score
    single_classic_data_unit['from_computer'] = get_computer_name()
    single_classic_data_unit['time'] = get_current_time()
    unit = single_classic_data_unit.copy()
    db = pymysql.connect(host='175.24.100.167', user='root', passwd='000815', database='snake')
    cursor = db.cursor()
    for rank_data in rank_datas:
        if player_name.strip() == rank_data['player_name']:
            if score > rank_data['score']:
                root = Tk()
                root.title('')
                font = tkfont.Font(size=20)

                sql_update_score = "update single_classic_top10 set score='" + str(
                    unit['score']) + "', from_computer='" + str(unit['from_computer']) + "',time='" + str(
                    unit['time']) + "' where player_name='" + str(unit['player_name']) + "'"
                cursor.execute(sql_update_score)
                db.commit()
                db.close()
                message = Message(root, text="恭喜您打破纪录！您的成绩已上传。", font=font, width=450)
                message.pack()
                mainloop()
            return
    if len(rank_datas) < 10:
        sql_update_rank = "insert into single_classic_top10 values('%s',%s,'%s','%s')" \
                          % (unit['player_name'], unit['score'], unit['from_computer'], unit['time'])
        cursor.execute(sql_update_rank)
        db.commit()
        db.close()
        root = Tk()
        root.title('')
        font = tkfont.Font(size=20)
        message = Message(root, text="恭喜您打破纪录！您的成绩已上传。", font=font, width=450)
        message.pack()
        mainloop()
        return
    elif len(rank_datas) >= 10 and score > rank_datas[-1]['score']:
        sql_delete_min = "delete from single_classic_top10 order by score limit 1"
        cursor.execute(sql_delete_min)
        sql_update_rank = "insert into single_classic_top10 values('%s',%s,'%s','%s')" \
                          % (unit['player_name'], unit['score'], unit['from_computer'], unit['time'])
        cursor.execute(sql_update_rank)
        db.commit()
        db.close()
        root = Tk()
        root.title('')
        font = tkfont.Font(size=20)
        message = Message(root, text="恭喜您打破纪录！您的成绩已上传。", font=font, width=450)
        message.pack()
        mainloop()
        return


def get_computer_name():
    name = gethostname()
    return name


def get_current_time():
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return date


def show_end_info(screen):
    font = pygame.font.Font(font_path, 40)
    tip1 = font.render('游戏结束', true, black)
    tip2 = font.render('按R重新开始', true, black)
    tip3 = font.render('按ESC返回主界面', true, black)
    screen.blit(tip1, (380, 200))
    screen.blit(tip2, (340, 300))
    screen.blit(tip3, (300, 400))
    pygame.display.update()
    while true:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return "restart"
                elif event.key == K_ESCAPE:
                    return 'esc'

def show_ranks():
    rank_datas = get_rank([])
    root = Tk()
    font = tkfont.Font(size=20)
    root.title('排行榜')
    tree = ttk.Treeview(root, show='headings')  # 这样就不会显示讨厌的第一列
    tree['columns'] = ('排名', '玩家名字', '得分', '时间', '玩家使用的电脑名称')
    tree.column('排名', width=50)
    tree.column('玩家名字', width=110)
    tree.column('得分', width=50)
    tree.column('时间', width=200)
    tree.column('玩家使用的电脑名称', width=200)
    tree.heading('排名', text='排名')
    tree.heading('玩家名字', text='玩家名称')
    tree.heading('得分', text='得分')
    tree.heading('时间', text='时间')
    tree.heading('玩家使用的电脑名称', text='玩家使用的电脑名称')
    for i in range(len(rank_datas)):
        tree.insert(parent='', index=i, values=(
            i + 1, rank_datas[i]['player_name'], rank_datas[i]['score'], rank_datas[i]['time'],
            rank_datas[i]['from_computer']))
    tree.grid(row=0, column=0)
    mainloop()


def pause_game(screen):
    font = pygame.font.Font(font_path, font_size)
    tip1 = font.render('游戏已暂停', true, black)
    tip2 = font.render('按SPACE键继续游戏', true, black)
    tip3 = font.render('按ESC退出返回至主页面', true, black)
    screen.blit(tip1, (360, 200))
    screen.blit(tip2, (280, 300))
    screen.blit(tip3, (240, 400))
    pygame.display.update()
    while true:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
                elif event.key == K_ESCAPE:
                    return 'ecs'


def input_name():
    root = Tk()
    name = Entry(root)
    name.focus()
    name.grid(row=0, column=1, ipadx=30, ipady=3)

    def get_name():
        global player1_name
        player1_name = name.get()
        root.destroy()
        root.quit()

    butt = Button(root, text='确定', width=10, command=get_name)
    butt.grid(row=0, column=3, ipadx=5)
    root.title('登录游戏')
    font = tkfont.Font(size=15)
    Label(root, text="请输入您的大名:", font=font).grid(row=0, column=0, ipadx=5, ipady=5)
    Label(root, text='本程序已实现联网，为保证您的成绩时时处处有效，请输入您唯一的名字，无名的成绩将不会进入排行榜！').grid(row=1, column=0, columnspan=4)
    mainloop()
    if player1_name == '':
        return '未登录'
    return player1_name

def draw_score(screen, score):
    font = pygame.font.Font('C:\\Windows\\Fonts\\Dengb.ttf', 40)
    score_surf = font.render('得分：%s' % score, True, green)
    screen.blit(score_surf, (20, 20))

# 用到的几个按钮
single_pos = (370, 300)  # 改这一个就行
double_pos = (single_pos[0], single_pos[1] + font_size * 2)
quit_pos = (single_pos[0] + font_size, single_pos[1] + font_size * 4)
rank_pos = (20, 540)

single_button = button(button_flag=0, pos=single_pos, text='单人游戏', font_size=font_size)
double_button = button(button_flag=1, pos=double_pos, text='双人游戏', font_size=font_size)
quit_login_button = button(button_flag=2, pos=quit_pos, text='退出', font_size=font_size)
single_classic_button = button(button_flag=3, pos=single_pos, text='经典模式', font_size=font_size)  # 放在single_button的原位置
single_new_button = button(button_flag=4, pos=double_pos, text='道具模式', font_size=font_size)
single_return_button = button(button_flag=5, pos=(quit_pos[0] - font_size, quit_pos[1]), text='退出登录',
                              font_size=font_size)
single_rank_button = button(button_flag=6, pos=rank_pos, text='排行榜', font_size=font_size)
double_classic_button = button(button_flag=7, pos=single_pos, text='竞技模式', font_size=font_size)
double_taichi_button = button(button_flag=8, pos=double_pos, text='太极模式', font_size=font_size)
doble_return_button = button(button_flag=9, pos=(quit_pos[0] - font_size, quit_pos[1]), text='退出登录',
                             font_size=font_size)
buttons = [single_button, double_button, quit_login_button, \
           single_classic_button, single_new_button, single_return_button, single_rank_button, \
           double_classic_button, double_taichi_button, doble_return_button, ]  # 三个为一个界面
rank_datas = get_rank([])
