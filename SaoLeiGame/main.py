import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from mineblock import *
from GUI import *

# 游戏屏幕的宽，根据方块宽度和尺寸常量计算得出
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
# 解释：通过方块宽度（BLOCK_WIDTH）和某个尺寸常量（SIZE）的乘积来确定游戏屏幕的宽度。
# 这里假设BLOCK_WIDTH和SIZE在其他地方已经被正确定义。

# 游戏屏幕的高，根据方块高度、额外行数和尺寸常量计算得出
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

# 定义游戏状态的枚举类
class GameStatus(Enum):
    """枚举类定义游戏的状态"""
    readied = 1   # 准备状态，游戏初始化完成，等待开始
    # 解释：表示游戏已经完成了初始化设置，例如加载了必要的资源等，现在处于等待玩家开始游戏的状态。
    started = 2   # 游戏进行中，玩家正在进行扫雷操作
    # 解释：当玩家开始进行扫雷相关的操作，如点击方块等，游戏就进入了这个正在进行的状态。
    over = 3     # 游戏结束，玩家触雷或其他导致游戏失败的情况
    # 解释：当玩家触发了地雷或者满足了其他导致游戏失败的条件时，游戏状态就变为结束状态。
    win = 4      # 游戏胜利，玩家成功标记出所有地雷或完成其他胜利条件
    # 解释：当玩家成功标记出所有的地雷，或者完成了其他预先设定的胜利条件时，游戏进入胜利状态。

# 在屏幕指定位置绘制文字的函数
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    """在屏幕指定位置绘制文字"""
    # 使用指定字体渲染文本内容，生成图像对象
    imgText = font.render(text, True, fcolor)
    # 解释：利用传入的字体（font）将指定的文本内容（text）渲染成一个可以在屏幕上显示的图像对象（imgText）。
    # True参数可能表示开启抗锯齿等优化效果，使文字显示更平滑。fcolor是文字的颜色，默认为白色。

    # 将生成的文本图像绘制到屏幕指定位置
    screen.blit(imgText, (x, y))
    # 解释：将刚刚渲染好的文本图像（imgText）绘制到屏幕（screen）上指定的坐标位置（x, y）。

# 重置游戏的函数
def reset_game(root, new_level):

    global level  # 假设 level 是全局变量，存储当前难度
    # 解释：这里声明要使用全局变量level，它用于记录当前游戏的难度级别。
    level = new_level  # 更新全局变量，表示设置新的游戏难度
    # 解释：将传入的新难度级别（new_level）赋值给全局变量level，从而更新游戏的难度设置。
    block = MineBlock(level=level)  # 重新初始化地雷块对象，传入新的难度级别
    # 解释：创建一个新的地雷块对象（MineBlock），并传入更新后的难度级别（level），以便重新初始化游戏中的地雷布局等相关设置。
    game_status = GameStatus.readied  # 重置游戏状态为准备状态
    # 解释：把游戏状态设置回初始的准备状态，意味着游戏将重新等待玩家开始操作。
    elapsed_time = 0  # 重置已过时间
    # 解释：将已经过去的游戏时间重置为0，就好像游戏刚刚开始一样。
    root.destroy()  # 关闭当前窗口，可能是游戏的主窗口或相关界面窗口
    # 解释：关闭传入的根窗口（root），这个窗口可能是游戏的主显示窗口或者与当前游戏场景相关的某个界面窗口。
    main(level)   # 重新启动游戏，传递新的难度级别进入游戏主逻辑
    # 解释：调用游戏的主函数（main）并传入更新后的难度级别（level），以重新启动游戏并进入新的一轮游戏流程。

# 游戏主函数，控制游戏的主要流程和逻辑
def main(difficulty_level=1):
    pygame.init() # 初始化Pygame库
    # 解释：这是使用Pygame进行游戏开发的第一步，初始化Pygame库，以便后续能够使用其提供的各种功能，如创建窗口、处理事件等。

    # 设置游戏窗口的显示模式，传入屏幕宽度和高度
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 解释：根据之前计算好的游戏屏幕宽度（SCREEN_WIDTH）和高度（SCREEN_HEIGHT）来设置游戏窗口的显示模式，
    # 这样就创建了一个具有特定尺寸的游戏窗口。
    pygame.display.set_caption('扫雷闯关') # 设置游戏窗口的标题
    # 解释：给游戏窗口设置一个标题，这里设置为“扫雷闯关”，以便在窗口的标题栏上显示该名称。

    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)
    # 解释：从指定的资源路径（'resources/a.TTF'）加载字体文件，并设置字体的大小为尺寸常量（SIZE）的两倍。
    # 这个字体可能会用于在游戏中绘制各种文本信息。

    fwidth, fheight = font1.size('999') # 获取特定文本的宽度和高度，可能用于后续布局
    # 解释：获取字符串“999”在刚刚加载的字体（font1）下的宽度（fwidth）和高度（fheight），
    # 这些尺寸信息可能会在后续的文本布局中起到参考作用，比如确定文本的显示位置等。

    red = (200, 40, 40) # 定义红色颜色值，可能用于绘制文本颜色等
    # 解释：定义了一个表示红色的颜色值元组（200, 40, 40），这个颜色可能会用于绘制一些特定的文本，
    # 比如显示剩余地雷数量、已过时间等信息时使用红色来突出显示。

    # 初始化地雷块，使用传入的 difficulty_level
    block = MineBlock(level=difficulty_level)
    # 解释：创建一个地雷块对象（MineBlock）并传入初始的难度级别（difficulty_level），
    # 这个对象可能负责管理游戏中的地雷布局、方块状态等相关信息。

    # 加载图片并缩放到合适大小的内部函数
    def load_image(file_name):
        """加载图片并缩放到合适大小"""
        try:
            # 加载指定路径下的图片文件，并转换为适合Pygame处理的格式
            img = pygame.image.load(f'resources/{file_name}').convert()
            # 解释：尝试从指定的资源路径（'resources/{file_name}'）加载图片文件，并将其转换为适合Pygame处理的格式。
            # 这样做是为了确保图片能够在Pygame环境中正确显示和处理。

            return pygame.transform.smoothscale(img, (SIZE, SIZE))
        # 解释：将加载好的图片（img）使用平滑缩放的方式缩放到指定的尺寸（SIZE, SIZE），
        # 以便在游戏中能够以统一的大小显示各种图片，比如方块图片、表情图片等。

        except pygame.error as e:
            print(f"图片 {file_name} 加载失败: {e}")
            sys.exit() # 如果加载失败，退出程序
            # 解释：如果在加载图片过程中出现了Pygame相关的错误（e），则打印出错误信息，告知用户图片加载失败，
            # 然后直接退出整个程序，因为图片可能是游戏正常运行所必需的资源。

    img_dict = {
        0: load_image('0.bmp'),
        1: load_image('1.bmp'),
        2: load_image('2.bmp'),
        3: load_image('3.bmp'),
        4: load_image('4.bmp'),
        5: load_image('5.bmp'),
        6: load_image('6.bmp'),
        7: load_image('7.bmp'),
        8: load_image('8.bmp'),
        "blank": load_image('blank.bmp'),
        "flag": load_image('flag.bmp'),
        "ask": load_image('ask.bmp'),
        "mine": load_image('mine.bmp'),
        "blood": load_image('blood.bmp'),
        "error": load_image('error.bmp')
    } # 创建一个字典，存储不同类型图片对应的加载和缩放后的图像对象
    # 解释：创建一个字典（img_dict），其中的键是不同的图片标识（如数字0-8表示周围地雷数量的图片，
    # "blank"表示空白方块图片等），值是通过调用load_image函数加载并缩放好的对应图片的图像对象。
    # 这样可以方便地根据需要获取相应的图片来在游戏屏幕上进行绘制。

    face_size = int(SIZE * 1.25)# 计算表情图片的尺寸
    # 解释：根据尺寸常量（SIZE）计算出表情图片的尺寸，这里将其设置为尺寸常量的1.25倍，
    # 可能是为了让表情图片在游戏屏幕上显示得更加突出或者符合某种设计需求。

    img_face_fail = pygame.transform.smoothscale(load_image('face_fail.bmp'), (face_size, face_size))
    img_face_normal = pygame.transform.smoothscale(load_image('face_normal.bmp'), (face_size, face_size))
    img_face_success = pygame.transform.smoothscale(load_image('face_success.bmp'), (face_size, face_size))
    # 解释：分别加载并缩放表示失败、正常、成功三种状态的表情图片（face_fail.bmp、face_normal.bmp、face_success.bmp）
    # 到之前计算好的表情图片尺寸（face_size, face_size），以便在游戏中根据不同的游戏状态显示相应的表情图片。

    face_pos_x = (SCREEN_WIDTH - face_size) // 2 # 计算表情图片在屏幕上的水平位置
    face_pos_y = (SIZE * 2 - face_size) // 2 # 计算表情图片在屏幕上的垂直位置
    # 解释：通过游戏屏幕的宽度（SCREEN_WIDTH）和表情图片的尺寸（face_size）计算出表情图片在屏幕上的水平位置（face_pos_x），
    # 以及通过尺寸常量（SIZE）和表情图片尺寸计算出表情图片在屏幕上的垂直位置（face_pos_y），
    # 这样就能准确地将表情图片放置在游戏屏幕的合适位置上。

    bgcolor = (225, 225, 225) # 定义游戏背景颜色
    # 解释：定义了一个表示游戏背景颜色的元组（225, 225, 225），这个颜色将用于填充整个游戏屏幕，
    # 为游戏提供一个统一的背景颜色。

    # 游戏变量初始化
    game_status = GameStatus.readied # 初始游戏状态设置为准备状态
    # 解释：将游戏的初始状态设置为准备状态，意味着游戏一开始是等待玩家开始操作的状态。

    start_time = None # 记录游戏开始时间，初始化为None
    # 解释：创建一个变量（start_time）用于记录游戏开始的时间，初始时将其设置为None，
    # 因为游戏还未开始，所以没有具体的开始时间。

    elapsed_time = 0 # 已过时间初始化为0
    # 解释：将已经过去的游戏时间初始化为0，因为游戏刚开始，还没有经过任何时间。

    save_file = "game_record.txt" # 保存游戏记录的文件名
    # 解释：定义一个字符串变量（save_file），用于指定保存游戏记录的文件名，这里设置为"game_record.txt"。

    # 检查是否有特定的命令行参数来跳过游戏
    if len(sys.argv) > 1 and sys.argv[1] == '--skip':
        # 直接设置游戏状态为胜利
        game_status = GameStatus.win
        # 解释：如果在命令行参数中检测到了"--skip"这个参数（并且命令行参数数量大于1），
        # 就直接将游戏状态设置为胜利状态，可能是用于测试或者某种特殊需求下快速进入胜利状态的情况。

        difficulty_level = 1  #假设胜利的难度级别
        # 解释：将难度级别设置为1，这里可能是一种默认的胜利难度设置，具体含义可能根据游戏的具体逻辑而定。

        elapsed_time = 0  # 设置经过时间为0
        # 解释：同时将已经过去的游戏时间也设置为0，就好像游戏刚刚开始就直接进入了胜利状态一样。

    else:
        while True:
            screen.fill(bgcolor) # 用背景颜色填充整个游戏屏幕
            # 解释：在每次游戏循环中，首先用之前定义的背景颜色（bgcolor）填充整个游戏屏幕，
            # 这样可以清除上一帧的画面内容，为绘制新的画面做好准备。
            for event in pygame.event.get(): #获取所有的游戏事件
            #  解释：通过Pygame的事件获取函数（pygame.event.get()）获取所有发生的游戏事件，
            #  这些事件可能包括鼠标点击、键盘按键按下等各种操作相关的事件。

                if event.type == QUIT: # 如果是退出事件
                    pygame.quit() # 退出Pygame
                    sys.exit() #退出程序
                    # 解释：如果获取到的事件类型是退出事件（QUIT），也就是玩家点击了游戏窗口的关闭按钮等情况，
                    # 就先退出Pygame库，然后再退出整个程序，以正常关闭游戏。

                elif event.type == MOUSEBUTTONDOWN: # 如果是鼠标按下事件
                    mouse_x, mouse_y = event.pos # 获取鼠标按下的位置坐标
                    # 解释：当检测到鼠标按下事件时，通过event.pos获取鼠标按下的位置坐标（mouse_x, mouse_y），
                    # 以便后续根据这个坐标来确定玩家点击的是游戏屏幕上的哪个位置。
                    x = mouse_x // SIZE # 计算鼠标所在方块的列索引
                    # 解释：将鼠标的横坐标（mouse_x）除以尺寸常量（SIZE），得到鼠标所在方块的列索引（x），
                    # 这样可以确定玩家点击的是游戏中的哪一列方块。
                    y = mouse_y // SIZE - 2 # 计算鼠标所在方块的行索引，减去额外的行数
                    # 解释：将鼠标的纵坐标（mouse_y）除以尺寸常量（SIZE）再减去2（可能是因为游戏布局中上方有预留的空间等原因），
                    # 得到鼠标所在方块的行索引（y），从而确定玩家点击的是游戏中的哪一行方块。
                    b1, b2, b3 = pygame.mouse.get_pressed() # 获取鼠标三个按键的按下状态
                    # 解释：通过Pygame的函数（pygame.mouse.get_pressed()）获取鼠标三个按键（通常是左键、右键、中键）的按下状态，
                    # 并分别赋值给b1、b2、b3三个变量，以便后续根据不同按键的按下情况来执行相应的操作。

                    if game_status == GameStatus.started: # 如果游戏正在进行中
                        if b1 and b3:  # 鼠标左右键同时按下
                            mine = block.getmine(x, y) # 获取指定位置的地雷对象
                            # 解释：当游戏正在进行中且鼠标左右键同时按下时，通过block.getmine(x, y)函数获取玩家点击位置（x, y）
                            # 对应的地雷对象（mine），以便后续对该地雷对象进行相关操作。

                            if mine.status == BlockStatus.opened: # 如果该方块已被打开
                                if not block.double_mouse_button_down(x, y): # 如果执行相关操作失败
                                    game_status = GameStatus.over # 设置游戏状态为结束
                                    # 解释：如果获取到的地雷对象的状态是已经被打开（opened），并且执行相关的双鼠标键按下操作（可能是某种特定功能）
                                    # 失败时，就将游戏状态设置为结束状态，意味着游戏失败了。

                elif event.type == MOUSEBUTTONUP: # 如果是鼠标松开事件
                    if y < 0: # 如果鼠标松开位置在特定区域（可能是顶部区域）
                        # 进一步判断鼠标松开的位置是否在表情图片所在的区域
                        if face_pos_x <= mouse_x <= face_pos_x + face_size \
                                and face_pos_y <= mouse_y <= face_pos_y + face_size:
                            # 点击表情重置关卡
                            game_status = GameStatus.readied
                            # 解释：重新初始化一个新的地雷块对象，传入当前的难度级别（difficulty_level），
                            # 这样可以重置游戏中的地雷布局等相关设置，为新的一局游戏做准备。
                            block = MineBlock(level=difficulty_level)
                            # 解释：获取当前的时间作为新一局游戏的开始时间，通过调用time.time()函数获取当前的时间戳。
                            start_time = time.time()
                            # 解释：将已经过去的游戏时间重置为0，因为是重新开始一局游戏，所以时间从0开始计算。
                            elapsed_time = 0
                            continue
                    # 解释：使用continue语句直接跳过本次循环的后续代码，回到循环的开头继续下一次循环，
                    # 这里可能是为了避免在重置关卡后执行一些不必要的后续操作。

                    # 如果游戏当前处于准备状态
                    if game_status == GameStatus.readied:
                        game_status = GameStatus.started
                        # 解释：将游戏状态从准备状态切换为开始状态，表明玩家已经准备好开始游戏，
                        # 此时游戏将正式进入玩家可以进行操作的阶段，比如点击方块等。

                        start_time = time.time()
                        # 解释：获取当前的时间作为游戏开始的时间，以便后续计算游戏已经进行的时间。

                        elapsed_time = 0
                    # 解释：将已经过去的游戏时间初始化为0，因为游戏刚刚从准备状态切换到开始状态，还没有经过实际的游戏操作时间。

                    # 如果游戏当前处于进行状态
                    if game_status == GameStatus.started:
                        mine = block.getmine(x, y)
                        # 解释：通过调用block.getmine(x, y)函数获取玩家鼠标松开位置（x, y）对应的地雷对象（mine），
                        # 这里的x和y是之前根据鼠标位置计算出来的方块行列索引，以便后续对该特定位置的地雷对象进行相关操作。

                        # 如果是左键点击（b1为True且b3为False，表示鼠标左键按下且右键未按下）
                        if b1 and not b3:  # 左键点击
                            if mine.status == BlockStatus.normal:
                                # 解释：如果获取到的地雷对象的状态是正常状态（即未被标记、未被打开等初始状态）
                                if not block.open_mine(x, y):
                                    game_status = GameStatus.over
                                    # 解释：尝试调用block.open_mine(x, y)函数来打开该位置的地雷方块，如果打开操作失败，
                                    # 就将游戏状态设置为结束状态，表示玩家触发了导致游戏失败的情况，比如可能是点击到了地雷。

                        # 如果是右键点击（b1为False且b3为True，表示鼠标左键未按下且右键按下）
                        elif not b1 and b3:  # 右键点击
                            if mine.status == BlockStatus.normal:
                                mine.status = BlockStatus.flag
                                # 解释：如果获取到的地雷对象的状态是正常状态，就将其状态设置为标记状态（flag），
                                # 通常表示玩家认为该位置可能是地雷并进行了标记操作。
                            elif mine.status == BlockStatus.flag:
                                mine.status = BlockStatus.ask
                                # 解释：如果该地雷对象的状态已经是标记状态，就将其状态更改为询问状态（ask），
                                # 可能表示玩家对之前的标记不太确定，想要进一步确认或者更改标记。
                            elif mine.status == BlockStatus.ask:
                                mine.status = BlockStatus.normal
                                # 解释：如果该地雷对象的状态是询问状态，就将其状态恢复为正常状态，
                                # 相当于取消了之前的标记或者询问操作，使其回到初始未操作的状态。

            # 渲染游戏区域
            flag_count = 0
            opened_count = 0
            for row in block.block:
                for mine in row:
                    pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                    # 解释：根据地雷对象的x和y坐标（这里的x和y可能是在游戏布局中的行列索引等相关信息）以及尺寸常量（SIZE），
                    # 计算出该地雷对象在游戏屏幕上的位置坐标（pos），以便后续在正确的位置绘制相应的图片。

                    if mine.status == BlockStatus.opened:
                        screen.blit(img_dict[mine.around_mine_count], pos)
                        opened_count += 1
                        # 解释：如果地雷对象的状态是已打开状态，就从之前创建的图片字典（img_dict）中获取对应周围地雷数量的图片，
                        # 并通过screen.blit函数将该图片绘制到计算好的屏幕位置（pos）上。同时，每绘制一个已打开的方块，就将opened_count加1，
                        # 用于后续判断游戏的胜负等逻辑。

                    elif mine.status == BlockStatus.bomb:
                        screen.blit(img_dict["blood"], pos)
                        # 解释：如果地雷对象的状态是炸弹状态（即已经触发了地雷），就从图片字典中获取表示爆炸的图片（"blood"），
                        # 并绘制到相应的屏幕位置上，以显示游戏失败时地雷爆炸的效果。

                    elif mine.status == BlockStatus.flag:
                        screen.blit(img_dict["flag"], pos)
                        flag_count += 1
                        # 解释：如果地雷对象的状态是标记状态，就从图片字典中获取表示标记的图片（"flag"），
                        # 并绘制到相应的屏幕位置上，以显示玩家标记的地雷位置。同时，每绘制一个标记的方块，就将flag_count加1，
                        # 用于后续判断游戏的胜负等逻辑。

                    elif mine.status == BlockStatus.ask:
                        screen.blit(img_dict["ask"], pos)
                        # 解释：如果地雷对象的状态是询问状态，就从图片字典中获取表示询问的图片（"ask"），
                        # 并绘制到相应的屏幕位置上，以显示玩家对该位置的不确定状态。

                    elif game_status == GameStatus.over and mine.value:
                        screen.blit(img_dict["mine"], pos)
                        # 解释：如果游戏状态已经是结束状态且该地雷对象的值表示它是一个地雷（这里的mine.value可能是用于判断是否是地雷的标识），
                        # 就从图片字典中获取表示地雷的图片（"mine"），并绘制到相应的屏幕位置上，以在游戏结束时显示所有未被标记的地雷位置。

                    elif mine.value == 0 and mine.status == BlockStatus.flag:
                        screen.blit(img_dict["error"], pos)
                        # 解释：如果地雷对象的值为0（表示不是地雷）但它的状态是标记状态，就从图片字典中获取表示错误标记的图片（"error"），
                        # 并绘制到相应的屏幕位置上，以显示玩家错误标记了非地雷位置的情况。

                    elif mine.status == BlockStatus.normal:
                        screen.blit(img_dict["blank"], pos)
            # 解释：如果地雷对象的状态是正常状态，就从图片字典中获取表示空白的图片（"blank"），
            # 并绘制到相应的屏幕位置上，以显示未被操作过的空白方块。

            # 在屏幕指定位置绘制剩余地雷数量的文本信息
            print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (block.mine_count - flag_count), red)
            # 解释：调用print_text函数在屏幕的指定位置（横坐标为30，纵坐标通过计算得到）绘制剩余地雷数量的文本信息。
            # 这里通过计算block.mine_count - flag_count得到剩余未标记的地雷数量，并将其格式化为两位数的字符串（'%02d'），
            # 使用之前定义的红色（red）作为文本颜色。

            if game_status == GameStatus.started:
                elapsed_time = int(time.time() - start_time)
                # 解释：如果游戏处于进行状态，通过计算当前时间（time.time()）减去游戏开始时间（start_time），
                # 得到游戏已经进行的时间，并将其转换为整数类型赋值给elapsed_time变量，以便后续显示和使用。

            # 在屏幕指定位置绘制已经过的游戏时间的文本信息
            print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)
            # 解释：调用print_text函数在屏幕的指定位置（横坐标为SCREEN_WIDTH - fwidth - 30，纵坐标通过计算得到）绘制已经过的游戏时间的文本信息。
            # 将elapsed_time变量的值格式化为三位数的字符串（'%03d'），使用红色作为文本颜色，以便在屏幕上清晰显示游戏进行的时间。

            # 判断胜负逻辑
            if flag_count + opened_count == BLOCK_WIDTH * BLOCK_HEIGHT:
                game_status = GameStatus.win
            # 解释：如果标记的方块数量（flag_count）加上已经打开的方块数量（opened_count）等于游戏中所有方块的总数（BLOCK_WIDTH * BLOCK_HEIGHT），
            # 就说明玩家已经成功标记出所有的地雷或者完成了其他胜利条件，此时将游戏状态设置为胜利状态。

            if game_status == GameStatus.over:
                screen.blit(img_face_fail, (face_pos_x, face_pos_y))
                # 解释：如果游戏状态是结束状态，就将之前加载并缩放好的表示失败的表情图片（img_face_fail）绘制到屏幕上计算好的位置（face_pos_x, face_pos_y），
                # 以显示游戏失败的效果。

                create_gui(difficulty_level,'over',block.mine_count - flag_count,None)
                # 解释：调用create_gui函数创建一个与游戏结束相关的图形用户界面（GUI），传入当前的难度级别（difficulty_level）、
                # 表示结束的状态字符串（'over'）、剩余未标记的地雷数量（block.mine_count - flag_count）以及None（可能是用于其他参数占位，
                # 具体取决于create_gui函数的定义）等参数，以便在游戏结束时向玩家展示相关信息。


                #关闭游戏窗口
                pygame.quit()
                return
            # 解释：先退出Pygame库，然后通过return语句结束当前函数（main函数）的执行，因为游戏已经结束，不需要再继续执行后续的游戏逻辑。

            elif game_status == GameStatus.win:
                screen.blit(img_face_success, (face_pos_x, face_pos_y))
                # 解释：如果游戏状态是胜利状态，就将之前加载并缩放好的表示胜利的表情图片（img_face_success）绘制到屏幕上计算好的位置（face_pos_x, face_pos_y），
                # 以显示游戏胜利的效果。

                save_record(save_file, difficulty_level, elapsed_time)

                # 解释：调用save_record函数保存游戏记录到指定的文件（save_file）中，传入当前的难度级别（difficulty_level）、
                # 游戏已经进行的时间（elapsed_time）等参数，以便记录玩家本次游戏的相关信息，如难度和通关时间等。

                if difficulty_level < 3:
                    #先进入结束界面，再选择接下来的操作
                    pygame.quit()  # 关闭 Pygame
                    create_gui(difficulty_level,'win',block.mine_count - flag_count,elapsed_time)
                    return
                    level += 1
                    block = MineBlock(level=difficulty_level)
                    game_status = GameStatus.readied
                    elapsed_time = 0
                    # 解释：如果当前的难度级别小于3，先关闭Pygame库，然后调用create_gui函数创建一个与游戏胜利相关的图形用户界面（GUI），
                    # 传入相关参数展示胜利信息。之后，将难度级别加1，重新初始化一个新的地雷块对象，将游戏状态设置为准备状态，
                    # 并将已经过去的游戏时间重置为0，准备进入下一个难度级别的游戏。
                else:
                    print("恭喜通关！游戏结束")
                    sys.exit()
                    # 解释：如果当前的难度级别大于等于3，就打印出恭喜通关的信息，然后直接退出整个程序，因为游戏已经全部通关完成。
            else:
                screen.blit(img_face_normal, (face_pos_x, face_pos_y))
                # 解释：如果游戏状态既不是结束状态也不是胜利状态，也就是游戏还在正常进行中，就将之前加载并缩放好的表示正常状态的表情图片（img_face_normal）
                # 绘制到屏幕上计算好的位置（face_pos_x, face_pos_y），以显示游戏正常进行的状态。
            pygame.display.update()
            # 解释：更新游戏屏幕的显示，将之前在本次循环中绘制的所有图片、文本等信息更新到屏幕上，以便玩家能够看到最新的游戏画面。
        pygame.quit()
        # 解释：在整个游戏循环结束后（正常情况下不会执行到这里，因为循环内有退出条件，如游戏结束或胜利等情况会提前退出循环），
        # 退出Pygame库，释放相关资源。

def save_record(file, difficulty_level, time_elapsed):
    """保存游戏记录到文件"""
    global level
    try:
        with open(file, 'a') as f:

            f.write(f"Level: {level}, Time: {time_elapsed} seconds\n")
            # 解释：尝试打开指定的文件（file），以追加模式（'a'）打开，这样可以在文件末尾添加新的记录而不覆盖原有记录。
            # 然后将当前的难度级别（level）和游戏已经进行的时间（time_elapsed）格式化为字符串写入到文件中，
            # 形成一条游戏记录，记录本次游戏的相关信息。
    except IOError as e:
        print(f"保存记录失败: {e}")
 # 解释：如果在打开文件或写入记录过程中出现了输入输出错误（IOError），就打印出错误信息，告知用户保存记录失败的原因。

if __name__ == '__main__':
    main()
#解释：当脚本作为主程序运行时（即__name__ == '__main__'），调用main函数开始执行游戏的主逻辑，启动整个游戏流程。

