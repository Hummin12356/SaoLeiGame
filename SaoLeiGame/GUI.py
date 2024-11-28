import tkinter as tk
from tkinter import font


file_path = "game_record.txt"

def set_difficulty_label(root, difficulty_level):
    difficulty_levels = {1: "初级", 2: "中级", 3: "高级"}
    difficulty_text = f"当前难度：{difficulty_levels.get(difficulty_level, '未知')}"
    difficulty_label = tk.Label(root, text=difficulty_text, font=("Arial", 14))
    difficulty_label.pack()

def read_records(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        times = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                parts = stripped_line.split(', Time: ')
                if len(parts) > 1:
                    time_str = parts[1].split(' ')[0]  # 获取 "X" 秒
                    try:
                        times.append(int(time_str))
                    except ValueError:
                        pass  # 如果转换失败，则忽略这一行
        min_time = min(times) if times else 0
        return min_time

# 将秒数转换为分钟和秒数的形式
def convert_time(time_in_seconds):
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
    return f"{minutes}分{seconds}秒"

def create_gui(difficulty_level,game_result,remaining_mines,elapsed_time):
    from main import reset_game
    global level  # 假设 level 是全局变量，存储当前难度
    level = difficulty_level  # 更新全局变量
    # 创建主窗口
    root = tk.Tk()
    root.title("结束界面")
    # 获取屏幕分辨率
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口位置
    win_width = 600
    win_height = 360
    x = (screen_width - win_width) // 2
    y = (screen_height - win_height) // 2

    # 设置窗口大小和位置
    root.geometry(f"{win_width}x{win_height}+{x}+{y}")
    root.geometry("600x360")  # 设置窗口大小

    # 设置标题

    # 设置标题
    if game_result == "win" and level == 3:
        title_text = "您已通关！🎉"
        title_color = "green"
    elif game_result == "win":
        title_text = "挑战成功！🎉"
        title_color = "green"
    else:
        title_text = "挑战失败！💥"
        title_color = "red"
    title_label = tk.Label(root, text=title_text, font=("Arial", 24, "bold"), fg=title_color)
    title_label.pack(pady=10)

    # 设置难度标签
    set_difficulty_label(root, difficulty_level)

    # 设置字体
    record_label_font = font.Font(family="Arial", size=14)
    # 创建通关时间标签
    if game_result == "win"and elapsed_time is not None:
        time_label = tk.Label(root, text=f"通关时间：{elapsed_time} 秒", font=record_label_font)
        time_label.pack()


    # 读取并转换最佳纪录时间
    min_time = read_records(file_path)
    best_time = convert_time(min_time)
    record_label = tk.Label(root, text=f"最佳纪录：{best_time}", font=record_label_font)
    record_label.pack()

    # 剩余雷数
    mines_label = tk.Label(root, text=f"剩余雷数：{remaining_mines}", font=("Arial", 14))
    mines_label.pack()

    # 按钮框架
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(side=tk.BOTTOM, pady=20)

    # 再玩一局按钮
    replay_button = tk.Button(buttons_frame, text="再玩一局", font=("Arial", 12), command=lambda current_level=difficulty_level: reset_game(root,difficulty_level))
    replay_button.pack(side=tk.LEFT, padx=(20, 10))

    # 联机对战按钮
    battle_button = tk.Button(buttons_frame, text="联机对战", font=("Arial", 12), command=lambda: print("联机对战,还在开发中"))
    battle_button.pack(side=tk.LEFT, padx=(10, 20))

    # 提升难度按钮
    if difficulty_level < 3:
        increase_difficulty_button = tk.Button(buttons_frame, text="提升难度", font=("Arial", 12), command=lambda current_level=level: reset_game( root,level+1))
        increase_difficulty_button.pack(side=tk.LEFT, padx=(10, 20))

    # 运行主循环
    root.mainloop()



