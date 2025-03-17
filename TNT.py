import tkinter as tk

# 力度表数据
data_table = {
    20: [16, 21, 26, 32, 37, 42, 45, 47, 49, 52, 55, 58, 61, 64, 68, 71, 74, 77],
    30: [15, 21, 28, 30, 33, 35, 38, 41, 44, 47, 50, 53, 56, 59, 61, 63, 65, 67, 69, 71, 73, 75, 76],
    45: [17, 22, 26, 30, 33, 36, 40, 42, 45, 47, 50, 52, 55, 57, 59, 62, 64, 66, 68, 70, 72, 74, 76, 78],
    50: [16, 22, 27, 31, 34, 36, 39, 42, 45, 47, 50, 53, 55, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76],
    60: [18, 24, 29, 33, 37, 40, 44, 47, 50, 53, 56, 59, 62, 65, 67, 70, 73, 75, 78, 81, 83, 86, 88, 90],
    65: [20, 26, 31, 36, 40, 44, 48, 52, 55, 58, 62, 65, 67, 70, 73, 77, 80, 83, 86, 89, 92, 95, 97, 100],
    70: [22, 30, 35, 40, 45, 50, 53, 57, 62, 66, 70, 73, 77, 80, 84, 87, 91, 94, 98],
}

# 角度对应的风力调整系数
wind_adjustments = {
    20: 12,
    30: 5,
    45: 5,
    50: 4,
    60: 2.5,
    65: 2.5,
    70: 1,
}

selected_angle = None
selected_distance = None
selected_angle_button = None  # 记录被选中的角度按钮
selected_distance_button = None  # 记录被选中的距离按钮
selected_wind_button = None  # 记录被选中的风向按钮
wind_direction = "顺风"  # 初始状态

def lookup_force(angle, button):
    """ 选择角度并高亮按钮 """
    global selected_angle, selected_angle_button
    selected_angle = angle

    if selected_angle_button:
        selected_angle_button.config(bg="#f0f0f0")  # 恢复默认背景色
    button.config(bg="#4CAF50", fg="white")  # 高亮按钮
    selected_angle_button = button

def lookup_distance(distance, button):
    """ 选择距离并高亮按钮 """
    global selected_distance, selected_distance_button
    selected_distance = distance

    if selected_distance_button:
        selected_distance_button.config(bg="#f0f0f0")  # 恢复默认背景色
    button.config(bg="#4CAF50", fg="white")  # 高亮按钮
    selected_distance_button = button

def calculate_force():
    """ 计算最终力度 """
    if selected_angle is None or selected_distance is None:
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, "请先选择角度和距离！\n")
        return

    force_values = data_table[selected_angle]
    if selected_distance < 2 or selected_distance - 2 >= len(force_values):
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, "错误: 距离超出可查询范围！\n")
        return

    force = float(force_values[selected_distance - 2])

    # 获取风速，若为空则设置默认值为0
    wind_speed_input = wind_speed_var.get()
    wind_speed = float(wind_speed_input) if wind_speed_input != "" else 0.0

    if selected_angle in wind_adjustments:
        factor = wind_adjustments[selected_angle]
        adjustment = wind_speed / factor

        if wind_direction == "逆风":
            force += adjustment  # 逆风 → 增加力度
        else:
            force -= adjustment  # 顺风 → 减少力度

    # 清空风速输入框
    wind_speed_entry.delete(0, tk.END)

    # 显示最终结果在结果框中
    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, f"最终力度值: ")
    result_display.insert(tk.END, f"{force:.2f}", "highlight")
    result_display.insert(tk.END, f"\n风速: {wind_speed}")

def set_wind_direction(direction, button):
    """ 切换风向并高亮按钮 """
    global wind_direction, selected_wind_button
    wind_direction = direction
    wind_label.config(text=f"当前风向: {direction}")

    if selected_wind_button:
        selected_wind_button.config(bg="#f0f0f0")  # 恢复默认背景色
    button.config(bg="#4CAF50", fg="white")  # 高亮按钮
    selected_wind_button = button

# 创建主窗口
root = tk.Tk()
root.title("TNT屏距风速力度计算工具")
root.geometry("500x650")
root.config(bg="#e0f7fa")  # 设置背景色

# 角度选择
tk.Label(root, text="选择角度:", font=("Arial", 14), bg="#e0f7fa").pack(pady=5)
angle_frame = tk.Frame(root, bg="#e0f7fa")
angle_frame.pack()

# 调整按钮大小，使其更小
for angle in data_table.keys():
    btn = tk.Button(angle_frame, text=str(angle), font=("Arial", 10), width=3, height=1, relief="solid", borderwidth=2)
    btn.config(command=lambda a=angle, b=btn: lookup_force(a, b))
    btn.pack(side=tk.LEFT, padx=5, pady=5)

# 距离选择
tk.Label(root, text="选择距离:", font=("Arial", 14), bg="#e0f7fa").pack(pady=5)
distance_frame = tk.Frame(root, bg="#e0f7fa")
distance_frame.pack()

# 调整按钮的行数，分为 4 行，每行 6 个按钮
for i in range(4):
    row_frame = tk.Frame(distance_frame, bg="#e0f7fa")
    row_frame.pack()
    for j in range(6):
        btn_distance = i * 6 + j + 2
        if btn_distance <= 25:  # 确保按钮编号在合理范围内
            btn = tk.Button(row_frame, text=str(btn_distance), font=("Arial", 10), width=3, height=1, relief="solid", borderwidth=2)
            btn.config(command=lambda d=btn_distance, b=btn: lookup_distance(d, b))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

# 风速输入框
tk.Label(root, text="输入风速:", font=("Arial", 14), bg="#e0f7fa").pack(pady=5)
wind_speed_var = tk.StringVar()  # 改为StringVar，方便处理为空的情况
wind_speed_entry = tk.Entry(root, textvariable=wind_speed_var, font=("Arial", 12), width=20, relief="solid", borderwidth=2)
wind_speed_entry.pack(pady=10)

# 风向按钮
wind_frame = tk.Frame(root, bg="#e0f7fa")
wind_frame.pack()

btn_tailwind = tk.Button(wind_frame, text="顺风", font=("Arial", 10), width=6, height=1, relief="solid", borderwidth=2, command=lambda: set_wind_direction("顺风", btn_tailwind))
btn_tailwind.pack(side=tk.LEFT, padx=5, pady=5)

btn_headwind = tk.Button(wind_frame, text="逆风", font=("Arial", 10), width=6, height=1, relief="solid", borderwidth=2, command=lambda: set_wind_direction("逆风", btn_headwind))
btn_headwind.pack(side=tk.LEFT, padx=5, pady=5)

# 当前风向标签
wind_label = tk.Label(root, text=f"当前风向: {wind_direction}", font=("Arial", 12), bg="#e0f7fa")
wind_label.pack(pady=5)

# 计算按钮
calculate_button = tk.Button(root, text="计算", font=("Arial", 12), width=10, height=2, bg="#4CAF50", fg="white", command=calculate_force)
calculate_button.pack(pady=20)

# 结果显示框
result_display = tk.Text(root, font=("Arial", 12), height=5, width=30, wrap=tk.WORD, relief="solid", borderwidth=2)
result_display.pack(pady=10)

# 在结果框中添加高亮效果
result_display.tag_config("highlight", foreground="red")

root.mainloop()
