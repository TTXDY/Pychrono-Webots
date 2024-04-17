from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import webbrowser
from tkinter import messagebox
from TerrainBuilder.controllers.my_controller.Build.TerrainChrono import (
    Terrain_Pychrono,
)
import time
import numpy as np

sign = 1
Obj_show = False
Obj_file_path = ""
Obj_file_path2 = ""
Texture_file_path = ""
Texture_file_path2 = ""
Noise_file_path = ""
dimensions = []
values1 = []
values2 = []

# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
world_dir = current_dir + "\TerrainBuilder\worlds"
controller_dir = (
    current_dir + r"\TerrainBuilder\controllers\my_controller\my_controller.py"
)
print("当前路径：" + world_dir)


def get_obj_dimensions(obj_file_path):
    vertices = []

    with open(obj_file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("v "):
                vertex = line.strip().split()[1:]
                vertex = [float(coord) for coord in vertex]
                vertices.append(vertex)

    vertices = np.array(vertices)
    min_vertex = np.min(vertices, axis=0)
    max_vertex = np.max(vertices, axis=0)
    dimensions = max_vertex - min_vertex

    return dimensions


# 示例使用
# obj_file_path = "path_to_obj_file.obj"
# dimensions = get_obj_dimensions(obj_file_path)
# print("Dimensions:", dimensions)


def get_Texture():
    Texture_file_path = filedialog.askopenfilename()
    new_file = []
    with open("TerrainBuilder/controllers/my_controller/my_controller.py", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "texture_image_path=" in line:
                replace = (
                    "            texture_image_path=" + '"' + Texture_file_path + '",'
                )
                line = replace + "\n"
            new_file.append(line)

    with open("TerrainBuilder/controllers/my_controller/my_controller.py", "w") as f:
        for line in new_file:
            f.write(line)
    if Texture_file_path:
        print(Texture_file_path)


def replace_line(file_path, line_number, new_code):
    # 读取文件内容
    with open(file_path, "r") as file:
        lines = file.readlines()

    # 替换指定行的代码
    if line_number <= len(lines):
        lines[line_number - 1] = new_code + "\n"  # 注意行号从1开始，而列表索引从0开始

    # 将修改后的内容写回文件
    with open(file_path, "w") as file:
        file.writelines(lines)


def Print_member():
    global sign
    global Obj_show

    if sign:
        sign = 1 - sign
        _var2.set(
            "An unstructured terrain modeling and generation method\n Webots are used for rigid terrain and Pychrono for deformable terrain")
        var1.set("Webots")
        var2.set("PyChrono")
        yes_var.set("Run Pychrono")

    else:
        sign = 1 - sign
        Obj_show = False
        _var2.set("")
        var1.set("")
        var2.set("")
        yes_var.set("")
        SOF_button.config(state="disabled")
        STF_button.config(state="disabled")
        SNF_button.config(state="disabled")
        obj_var.set("")
        obj_button_var.set("")
        texture_button_var.set("")
        noise_button_var.set("")
        tp_label_var.set("")
        t1_var.set("")
        t2_var.set("")
        texture_var.set("")
        noise_var.set("")


def Click_Box():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir

    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildBox"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    boxDir = world_dir + r"\randomBox.wbt"
    webbrowser.open(boxDir)


def Click_Slope():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir
    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildSlope"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Slope_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "xyz = " in line:
                    replace = "        xyz = [np.random.uniform(2, 5, 1),np.random.uniform(0.05, 0.2, 1),np.random.uniform(2, 5, 1), ]"
                    line = replace + "\n"
                if "rad1 = " in line:
                    replace = "        rad1 = 3.14 / float(np.random.randint(6, 12))"
                    line = replace + "\n"
                if "rad2 = " in line:
                    replace = "        rad2 = 3.14 / float(np.random.randint(6, 12))"
                    line = replace + "\n"
                if "high_slope = " in line:
                    replace = "        high_slope = np.random.uniform(0.5, 2, 1)"
                    line = replace + "\n"

                if "x_decay = " in line:
                    replace = "        x_decay = np.random.uniform(2, 3, 1)"
                    line = replace + "\n"

                if "h_decay = " in line:
                    replace = "        h_decay = np.random.uniform(0.99, 1.01, 1)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        slopeDir = world_dir + r"\randomSlopes.wbt"
        webbrowser.open(slopeDir)

    def Click_Slope_yes():
        popupSlope = tk.Toplevel(window)
        # popupSlope.geometry("400x400")

        LabelSlope = [
            "x[2, 5] : ",
            "y[0.05, 0.2]: ",
            "z[2, 5]: ",
            "rad1[0.2, 1.57]: ",
            "rad2[0.2, 1.57]: ",
            "high[0.5, 2]: ",
            "x_decay[2, 3]: ",
            "h_decay[0.99, 1.01]: ",
            # "texture_image_path",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=2, to=5, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=0.05, to=0.2, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=2, to=5, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        for i in range(3, 5):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=0.2, to=1.57, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        for i in range(5, 6):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=0.5, to=2, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        for i in range(6, 7):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=2, to=3, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        for i in range(7, 8):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=0.99, to=1.01, increment=0.001)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        for i in range(8, 10):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupSlope, text=LabelSlope[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupSlope, from_=0, to=1, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "xyz = " in line:
                        replace = (
                            "        xyz = ["
                            + values[0]
                            + ", "
                            + values[1]
                            + ", "
                            + values[2]
                            + "]"
                        )
                        line = replace + "\n"
                    if "rad1 = " in line:
                        replace = "        rad1 = " + values[3]
                        line = replace + "\n"
                    if "rad2 = " in line:
                        replace = "        rad2 = " + values[4]
                        line = replace + "\n"
                    if "high_slope = " in line:
                        replace = "        high_slope = " + values[5]
                        line = replace + "\n"

                    if "x_decay = " in line:
                        replace = "        x_decay = " + values[6]
                        line = replace + "\n"

                    if "h_decay = " in line:
                        replace = "        h_decay = " + values[7]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[8] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[9] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)
            slopeDir = world_dir + r"\randomSlopes.wbt"

            webbrowser.open(slopeDir)

        labell = tk.Label(popupSlope, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popupSlope, text="Select texture file", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popupSlope, text="OK", command=get_values).grid(
            row=12, column=0
        )
        btn = tk.Button(popupSlope, text="Close", command=popupSlope.destroy).grid(
            row=12, column=1
        )

    popupSlopeYesNo = tk.Toplevel(window)
    label = tk.Label(
        popupSlopeYesNo,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="Select a way to open",
    ).pack(pady=10)
    btn = tk.Button(
        popupSlopeYesNo,
        text="Custom",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Slope_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popupSlopeYesNo,
        text="Random",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Slope_no,
    ).pack(side=LEFT, padx=20, pady=20)


def Click_Stairs():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir

    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildStair"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Stairs_yes():
        popupStairs = tk.Toplevel(window)

        LabelStair = [
            "width[1, 4]: ",
            "high[0.01, 1]: ",
            "lenth[1, 10]: ",
            "pattern[0, 2]: ",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupStairs, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupStairs, from_=1, to=4, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupStairs, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupStairs, from_=0.01, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupStairs, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupStairs, from_=1, to=10, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(3, 4):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupStairs, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupStairs, from_=0, to=2, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(4, 6):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupStairs, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupStairs, from_=0, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "width_stair = " in line:
                        replace = "        width_stair = " + values[0]
                        line = replace + "\n"
                    if "high_stair = " in line:
                        replace = "        high_stair = " + values[1]
                        line = replace + "\n"
                    if "lenth_stair = " in line:
                        replace = "        lenth_stair = " + values[2]
                        line = replace + "\n"
                    if "pattern_stair = " in line:
                        replace = "        pattern_stair = " + values[3]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[4] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[5] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)
            starisDir = world_dir + r"\randomStairs.wbt"
            webbrowser.open(starisDir)

        labell = tk.Label(popupStairs, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popupStairs, text="Select texture file: ", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popupStairs, text="Ok", command=get_values).grid(
            row=12, column=0
        )
        btn = tk.Button(popupStairs, text="Close", command=popupStairs.destroy).grid(
            row=12, column=1
        )

    def Click_Stairs_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "width_stair = " in line:
                    replace = "        width_stair = np.random.uniform(1, 4, 1)"
                    line = replace + "\n"
                if "high_stair = " in line:
                    replace = "        high_stair = np.random.uniform(0.01, 1, 1)"
                    line = replace + "\n"
                if "lenth_stair = " in line:
                    replace = "        lenth_stair = np.random.uniform(1, 10, 1)"
                    line = replace + "\n"
                if "pattern_stair = " in line:
                    replace = "        pattern_stair = np.random.randint(0, 2, 1)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        starisDir = world_dir + r"\randomStairs.wbt"
        webbrowser.open(starisDir)

    popupStairsYesNo = tk.Toplevel(window)
    label = tk.Label(
        popupStairsYesNo,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="选择一种方式打开",
    ).pack(pady=10)
    btn = tk.Button(
        popupStairsYesNo,
        text="自定义",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Stairs_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popupStairsYesNo,
        text="随机",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Stairs_no,
    ).pack(side=LEFT, padx=20, pady=20)


def Click_Ditch():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir

    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildDitch"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Ditch_yes():
        # pass
        popupditch = tk.Toplevel(window)

        LabelStair = [
            "width[0.5, 1]: ",
            "high[0.01, 0.5]: ",
            "lenth[5, 10]: ",
            "distance[0.5, 1]: ",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupditch, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupditch, from_=0.5, to=1, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupditch, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupditch, from_=0.01, to=0.5, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupditch, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupditch, from_=5, to=10, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(3, 4):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupditch, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupditch, from_=0.5, to=1, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(4, 6):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupditch, text=LabelStair[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupditch, from_=0, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "width_ditch = " in line:
                        replace = "        width_ditch = " + values[0]
                        line = replace + "\n"
                    if "high_ditch = " in line:
                        replace = "        high_ditch = " + values[1]
                        line = replace + "\n"
                    if "lenth_ditch = " in line:
                        replace = "        lenth_ditch = " + values[2]
                        line = replace + "\n"
                    if "distance_ditch = " in line:
                        replace = "        distance_ditch = " + values[3]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[4] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[5] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)

            ditchDir = world_dir + r"\randomDitch.wbt"
            webbrowser.open(ditchDir)

        labell = tk.Label(popupditch, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popupditch, text="Select texture file: ", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popupditch, text="确定", command=get_values).grid(
            row=12, column=0
        )
        btn = tk.Button(popupditch, text="关闭", command=popupditch.destroy).grid(
            row=12, column=1
        )

    def Click_Ditch_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "width_ditch = " in line:
                    replace = "        width_ditch = np.random.uniform(0.5, 1, 1)"
                    line = replace + "\n"
                if "high_ditch = " in line:
                    replace = "        high_ditch = np.random.uniform(0.01, 0.5, 1)"
                    line = replace + "\n"
                if "lenth_ditch = " in line:
                    replace = "        lenth_ditch = np.random.uniform(5, 10, 1)"
                    line = replace + "\n"
                if "distance_ditch = " in line:
                    replace = "        distance_ditch = np.random.uniform(0.5, 1, 1)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        ditchDir = world_dir + r"\randomDitch.wbt"
        webbrowser.open(ditchDir)

    popup = tk.Toplevel(window)
    label = tk.Label(
        popup,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="选择一种方式打开",
    ).pack(pady=10)
    btn = tk.Button(
        popup,
        text="自定义",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Ditch_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popup,
        text="随机",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Ditch_no,
    ).pack(side=LEFT, padx=20, pady=20)

    # ditchDir = world_dir + r"\randomDitch.wbt"
    # webbrowser.open(ditchDir)


def Click_Rough():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir
    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildRough"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Rough_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "size = " in line:
                    replace = "        size = np.random.randint(20, 30)"
                    line = replace + "\n"
                if "a = " in line:
                    replace = "        a = np.random.uniform(0.1, 0.2)"
                    line = replace + "\n"
                if "b = " in line:
                    replace = "        b = np.random.uniform(0.05, 0.1)"
                    line = replace + "\n"
                if "c = " in line:
                    replace = "        c = np.random.uniform(0.01, 0.05)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        roughDir = world_dir + r"\randomRough.wbt"
        webbrowser.open(roughDir)

    def Click_Rough_yes():
        # pass
        popupRough = tk.Toplevel(window)

        LabelRough = [
            "size [24, 30]: ",
            "a [0.1, 0.2]: ",
            "b [0.05, 0.1]: ",
            "c[0.01, 0.05]: ",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupRough, text=LabelRough[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupRough, from_=24, to=30, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupRough, text=LabelRough[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupRough, from_=0.1, to=0.2, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupRough, text=LabelRough[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupRough, from_=0.05, to=0.1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(3, 4):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupRough, text=LabelRough[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupRough, from_=0.01, to=0.05, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(4, 6):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popupRough, text=LabelRough[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popupRough, from_=0, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "size = " in line:
                        replace = "        size = " + values[0]
                        line = replace + "\n"
                    if "a = " in line:
                        replace = "        a = " + values[1]
                        line = replace + "\n"
                    if "b = " in line:
                        replace = "        b = " + values[2]
                        line = replace + "\n"
                    if "c = " in line:
                        replace = "        c = " + values[3]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[4] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[5] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)

            roughDir = world_dir + r"\randomRough.wbt"
            webbrowser.open(roughDir)

        labell = tk.Label(popupRough, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popupRough, text="Select texture file: ", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popupRough, text="确定", command=get_values).grid(
            row=12, column=0
        )
        btn = tk.Button(popupRough, text="关闭", command=popupRough.destroy).grid(
            row=12, column=1
        )

    popup = tk.Toplevel(window)
    label = tk.Label(
        popup,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="选择一种方式打开",
    ).pack(pady=10)
    btn = tk.Button(
        popup,
        text="自定义",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Rough_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popup,
        text="随机",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Rough_no,
    ).pack(side=LEFT, padx=20, pady=20)


def Click_Hilly():
    # file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    file_path = controller_dir

    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildHilly"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Ditch_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "bianchang = " in line:
                    replace = "        bianchang = 24"
                    line = replace + "\n"
                if "montainNum = " in line:
                    replace = "        montainNum = np.random.randint(0, 10)"
                    line = replace + "\n"
                if "minHeight = " in line:
                    replace = "        minHeight = np.random.uniform(0.01, 0.1)"
                    line = replace + "\n"
                if "maxHeight = " in line:
                    replace = "        maxHeight = np.random.uniform(1, 3)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        hillyDir = world_dir + r"\randomHilly.wbt"
        webbrowser.open(hillyDir)

    def Click_Ditch_yes():
        # pass
        popuphilly = tk.Toplevel(window)

        Labelhilly = [
            "bianchang[24, 30]: ",
            "montainNum[0, 10]: ",
            "minHeight[0.01, 0.1]: ",
            "maxHeight[1, 13: ",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuphilly, text=Labelhilly[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuphilly, from_=24, to=30, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuphilly, text=Labelhilly[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuphilly, from_=0, to=10, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuphilly, text=Labelhilly[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuphilly, from_=0.01, to=0.1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(3, 4):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuphilly, text=Labelhilly[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuphilly, from_=1, to=3, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(4, 6):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuphilly, text=Labelhilly[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuphilly, from_=0, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "bianchang = " in line:
                        replace = "        bianchang = " + values[0]
                        line = replace + "\n"
                    if "montainNum = " in line:
                        replace = "        montainNum = " + values[1]
                        line = replace + "\n"
                    if "minHeight = " in line:
                        replace = "        minHeight = " + values[2]
                        line = replace + "\n"
                    if "maxHeight = " in line:
                        replace = "        maxHeight = " + values[3]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[4] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[5] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)

            ditchHilly = world_dir + r"\randomHilly.wbt"
            webbrowser.open(ditchHilly)

        labell = tk.Label(popuphilly, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popuphilly, text="Select texture file: ", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popuphilly, text="确定", command=get_values).grid(
            row=12, column=0
        )
        btn = tk.Button(popuphilly, text="关闭", command=popuphilly.destroy).grid(
            row=12, column=1
        )

    popup = tk.Toplevel(window)
    label = tk.Label(
        popup,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="选择一种方式打开",
    ).pack(pady=10)
    btn = tk.Button(
        popup,
        text="自定义",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Ditch_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popup,
        text="随机",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Ditch_no,
    ).pack(side=LEFT, padx=20, pady=20)
    # hillyDir = world_dir + r"\randomHilly.wbt"
    # webbrowser.open(hillyDir)


def Click_Pit():
    file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildPit"'  # 新的代码
    replace_line(file_path, line_number, new_code)

    def Click_Pit_no():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "xx = " in line:
                    replace = "        xx = np.random.randint(10, 20)"
                    line = replace + "\n"
                if "yy = " in line:
                    replace = "        yy = np.random.randint(3, 7)"
                    line = replace + "\n"
                if "zz = " in line:
                    replace = "        zz = np.random.randint(10, 20)"
                    line = replace + "\n"
                if "xDimension = " in line:
                    replace = "        xDimension = np.random.randint(10, 40)"
                    line = replace + "\n"
                if "zDimension = " in line:
                    replace = "        zDimension = np.random.randint(10, 40)"
                    line = replace + "\n"
                if "roughness=" in line:
                    replace = "            roughness=0.2,"
                    line = replace + "\n"
                if "metalness=" in line:
                    replace = "            metalness=0.8,"
                    line = replace + "\n"
                new_file.append(line)

        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        pitDir = world_dir + r"\randomPit.wbt"
        webbrowser.open(pitDir)

    def Click_Pit_yes():
        # pass
        popuppit = tk.Toplevel(window)

        Labelpit = [
            "x[24, 30]: ",
            "y[0, 10]: ",
            "z[0.01, 0.1]: ",
            "xDimension[10, 40]: ",
            "zDimension[10, 40]: ",
            "roughness[0, 1]: ",
            "metalness[0, 1]: ",
        ]

        # 创建6个组合
        i = 0
        spinboxes = []  # 存储Spinbox控件的列表
        for i in range(1):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=10, to=20, increment=0.1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(1, 2):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=3, to=7, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(2, 3):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=10, to=20, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(3, 4):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=10, to=40, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(4, 5):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=10, to=40, increment=1)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)
        for i in range(5, 7):
            # 创建Label和Spinbox，并使用grid布局放置在不同的行上
            label = tk.Label(popuppit, text=Labelpit[i])
            label.grid(row=i, column=0)

            spinbox = tk.Spinbox(popuppit, from_=0, to=1, increment=0.01)
            spinbox.grid(row=i, column=1)
            spinboxes.append(spinbox)

        def get_values():
            values = [spinbox.get() for spinbox in spinboxes]
            new_file = []
            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
            ) as f:
                lines = f.readlines()
                for line in lines:
                    if "xx = " in line:
                        replace = "        xx = " + values[0]
                        line = replace + "\n"
                    if "yy = " in line:
                        replace = "        yy = " + values[1]
                        line = replace + "\n"
                    if "zz = " in line:
                        replace = "        zz = " + values[2]
                        line = replace + "\n"
                    if "xDimension = " in line:
                        replace = "        xDimension = " + values[3]
                        line = replace + "\n"
                    if "zDimension = " in line:
                        replace = "        zDimension = " + values[4]
                        line = replace + "\n"
                    if "roughness=" in line:
                        replace = "            roughness=" + values[5] + ","
                        line = replace + "\n"
                    if "metalness=" in line:
                        replace = "            metalness=" + values[6] + ","
                        line = replace + "\n"
                    new_file.append(line)

            with open(
                "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
            ) as f:
                for line in new_file:
                    f.write(line)

            pitDir = world_dir + r"\randomPit.wbt"
            webbrowser.open(pitDir)

        labell = tk.Label(popuppit, text="Select texture: ").grid(row=11, column=0)
        btnSelect = tk.Button(popuppit, text="Select texture file: ", command=get_Texture).grid(
            row=11, column=1
        )
        btn = tk.Button(popuppit, text="确定", command=get_values).grid(row=12, column=0)
        btn = tk.Button(popuppit, text="关闭", command=popuppit.destroy).grid(
            row=12, column=1
        )

    popup = tk.Toplevel(window)
    label = tk.Label(
        popup,
        height=2,
        width=30,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="选择一种方式打开",
    ).pack(pady=10)
    btn = tk.Button(
        popup,
        text="自定义",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Pit_yes,
    ).pack(side=LEFT, padx=20, pady=20)
    btn = tk.Button(
        popup,
        text="随机",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_Pit_no,
    ).pack(side=LEFT, padx=20, pady=20)

    # pitDir = world_dir + r"\randomPit.wbt"
    # webbrowser.open(pitDir)


def Click_3DModel():
    file_path = "TerrainBuilder/controllers/my_controller/my_controller.py"  # 文件路径
    line_number = 18  # 要替换的行号
    new_code = 'choose = "buildTerrainFrom3DModel"'  # 新的代码
    replace_line(file_path, line_number, new_code)
    popup = tk.Toplevel(window)
    label = tk.Label(
        popup,
        height=2,
        width=36,
        font=("Consolas", 20),
        fg="black",
        # bg="yellow",
        text="请选择一个Obj格式的地形文件和纹理文件",
    ).pack(pady=10)
    btn = tk.Button(
        popup,
        text="Obj格式文件",
        height=2,
        width=15,
        font=("consolas", 16),
        command=SelectObjFile2,
    ).pack(padx=20, pady=20)
    btn = tk.Button(
        popup,
        text="纹理文件",
        height=2,
        width=15,
        font=("consolas", 16),
        command=SelectTextureFile2,
    ).pack(padx=20, pady=20)
    # popuppit = tk.Toplevel(window)

    Labelpit = [
        "roughness[0, 1]: ",
        "metalness[0, 1]: ",
    ]
    # 创建6个组合
    i = 0
    spinboxes = []  # 存储Spinbox控件的列表
    for i in range(2):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(
            popup,
            text=Labelpit[i],
            font=("consolas", 16),
        )
        label.pack()

        spinbox = tk.Spinbox(popup, from_=0, to=1, increment=0.01, width=25)
        spinbox.pack()
        spinboxes.append(spinbox)
    values = [spinbox.get() for spinbox in spinboxes]

    def Click_d_yes():
        new_file = []
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "r"
        ) as f:
            lines = f.readlines()
            for line in lines:
                if "builder.buildFrom3DModel(" in line:
                    replace = (
                        "    builder.buildFrom3DModel("
                        + '"'
                        + Obj_file_path2
                        + '"'
                        + ","
                        + '"'
                        + Texture_file_path2
                        + '"'
                        + ","
                        + values[0]
                        + ","
                        + values[1]
                        + ")"
                    )
                    line = replace + "\n"
                new_file.append(line)
        with open(
            "TerrainBuilder/controllers/my_controller/my_controller.py", "w"
        ) as f:
            for line in new_file:
                f.write(line)
        if (
            Obj_file_path2 != None
            and Obj_file_path2 != None
            and values[0] != None
            and values[1] != None
        ):
            modelDir = world_dir + r"\empty.wbt"
            webbrowser.open(modelDir)

    btn = tk.Button(
        popup,
        text="确定",
        height=2,
        width=15,
        font=("consolas", 16),
        command=Click_d_yes,
    ).pack(padx=20, pady=20)
    # pass


def Print_Webots():
    popup = tk.Toplevel(window)
    popup.geometry("400x750")
    label = tk.Label(
        popup,
        height=2,
        width=30,
        font=("Consolas", 22),
        fg="black",
        # bg="yellow",
        text="RANDOM",
    )
    label.pack(pady=(5, 5))
    Box_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Box",
        command=Click_Box,
    )
    Box_button.pack(padx=10, pady=10)

    Slope_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Slope",
        command=Click_Slope,
    )
    Slope_button.pack(padx=10, pady=10)

    Stairs_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Stairs",
        command=Click_Stairs,
    )
    Stairs_button.pack(padx=10, pady=10)

    Ditch_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Ditch",
        command=Click_Ditch,
    )
    Ditch_button.pack(padx=10, pady=10)

    Rough_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Rough",
        command=Click_Rough,
    )
    Rough_button.pack(padx=10, pady=10)

    Hilly_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Hilly",
        command=Click_Hilly,
    )
    Hilly_button.pack(padx=10, pady=10)

    Pit_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="Pit",
        command=Click_Pit,
    )
    Pit_button.pack(padx=10, pady=10)

    DModel_button = tk.Button(
        popup,
        height=1,
        width=12,
        font=("Consolas", 18),
        bg="white",
        fg="blue",
        text="3D Model",
        command=Click_3DModel,
    )
    DModel_button.pack(padx=10, pady=10)

    btn = tk.Button(
        popup,
        text="Close",
        height=2,
        font=("Consolas", 14),
        width=10,
        command=popup.destroy,
    ).pack(pady=10)

    # webbrowser.open(
    #     r"d:\sunjieqiang\webots\2-4-6 - new\model2-4-6_obstacles_6_random_step_include_test\worlds\model_10_0.06.wbt"
    # )
    # var1.set("Webots")
    # pass


def Print_Pychrono():
    global Obj_show
    if Obj_show:
        Obj_show = False
        SOF_button.config(state="disabled")
        STF_button.config(state="disabled")
        SNF_button.config(state="disabled")
        obj_var.set("")
        obj_button_var.set("")
        texture_button_var.set("")
        noise_button_var.set("")
        tp_label_var.set("")
        t1_var.set("")
        t2_var.set("")
        texture_var.set("")
        noise_var.set("")
    else:
        Obj_show = True
        SOF_button.config(state="normal")
        STF_button.config(state="normal")
        SNF_button.config(state="normal")
        obj_var.set("Obj:")
        texture_var.set("Texture:")
        noise_var.set("Noise:")
        obj_button_var.set("Obj file")
        texture_button_var.set("Texture file")
        noise_button_var.set("noise file")
        tp_label_var.set("Terrain param setting")
        t1_var.set("The first one")
        t2_var.set("The second one")


def SelectTextureFile2():
    global Texture_file_path2
    Texture_file_path2 = filedialog.askopenfilename()
    if Texture_file_path2:
        print(Texture_file_path2)


def SelectObjFile2():
    global Obj_file_path2, dimensions
    Obj_file_path2 = filedialog.askopenfilename()

    if Obj_file_path2:
        # webbrowser.open(Obj_file_path)
        print(Obj_file_path2)


def SelectObjFile():
    global Obj_file_path, dimensions
    Obj_file_path = filedialog.askopenfilename()

    if Obj_file_path:
        # webbrowser.open(Obj_file_path)
        print(Obj_file_path)


def SelectTextureFile():
    global Texture_file_path
    Texture_file_path = filedialog.askopenfilename()
    if Texture_file_path:
        print(Texture_file_path)


def SelectNoiseFile():
    global Noise_file_path
    Noise_file_path = filedialog.askopenfilename()

    if Noise_file_path:
        print(Noise_file_path)


def RunPychrono():
    global Obj_file_path, Texture_file_path, Noise_file_path, dimensions, values1, values2

    if values1 == [] or values2 == []:
        messagebox.showwarning("警告", "您需要将地形参数补全")
    terrain_p = [values1, values2]
    # terrain_p.append[values1]
    # terrain_p.append[values2]
    if Obj_file_path == "" or Texture_file_path == "" or Noise_file_path == "":
        # 彈出窗口提示不能運行
        # messagebox.showwarning("你需要首先输入Obj文件和纹理文件")
        messagebox.showwarning("警告", "您需要首先输入Obj文件、纹理文件和噪声文件")
    else:
        dimensions = get_obj_dimensions(Obj_file_path)
        print("Dimensions:", dimensions)
        if dimensions[2] > dimensions[0] or dimensions[2] > dimensions[1]:
            messagebox.showwarning("警告", "Obj地形的高大于宽和长，请重新设置")
        else:
            env = Terrain_Pychrono(
                IsCarSystem=True,
                dimensions=dimensions,
                noise_path=Noise_file_path,
                texture_path=Texture_file_path,
                obj_path=Obj_file_path,
                terrain_para=terrain_p,
            )
            env.Run()


window = tk.Tk()
window.geometry("1180x750")
window.title("TERRAIN")
frame = tk.LabelFrame(
    window, text="Terrain", font=("Consolas", 24), bg="white", fg="blue"
)
frame.pack(padx=10, pady=(20, 0))

_var2 = tk.StringVar()
var1 = tk.StringVar()
var2 = tk.StringVar()
yes_var = tk.StringVar()
obj_var = tk.StringVar()
texture_var = tk.StringVar()
noise_var = tk.StringVar()
obj_button_var = tk.StringVar()
texture_button_var = tk.StringVar()
noise_button_var = tk.StringVar()
tp_label_var = tk.StringVar()
t1_var = tk.StringVar()
t2_var = tk.StringVar()

the_button = tk.Button(
    frame,
    height=1,
    width=20,
    font=("Consolas", 18),
    bg="white",
    fg="blue",
    text="Welcome",
    command=Print_member,
)
the_button.pack(padx=10, pady=10)

the2_label = tk.Label(
    frame,
    height=3,
    width=72,
    font=("Consolas", 14),
    fg="black",
    bg="yellow",
    textvariable=_var2,
)
the2_label.pack(padx=50, pady=10)

button1 = tk.Button(
    frame,
    height=1,
    width=14,
    font=("consolas", 16),
    textvariable=var1,
    command=Print_Webots,
)
button1.pack(padx=10, pady=10)

#
button2 = tk.Button(
    frame,
    height=1,
    width=14,
    font=("consolas", 16),
    textvariable=var2,
    command=Print_Pychrono,
)
button2.pack(padx=10, pady=10)

the3_label = tk.Label(
    frame,
    height=3,
    width=5,
    font=("Consolas", 14),
    fg="black",
    bg="white",
    textvariable=obj_var,
)
the3_label.pack(side=LEFT, padx=(35, 0), pady=0)
SOF_button = tk.Button(
    frame,
    height=1,
    width=14,
    font=("consolas", 16),
    # text="Select obj file",
    textvariable=obj_button_var,
    command=SelectObjFile,
)
SOF_button.pack(side=LEFT, padx=0, pady=0)
SOF_button.config(state="disabled")

the4_label = tk.Label(
    frame,
    height=3,
    width=8,
    font=("Consolas", 14),
    fg="black",
    bg="white",
    textvariable=texture_var,
)
the4_label.pack(side=LEFT, padx=(40, 0), pady=0)
STF_button = tk.Button(
    frame,
    height=1,
    width=14,
    font=("consolas", 16),
    # text="Select Texture file",
    textvariable=texture_button_var,
    command=SelectTextureFile,
)
STF_button.pack(side=LEFT, padx=10, pady=0)
STF_button.config(state="disabled")

the5_label = tk.Label(
    frame,
    height=3,
    width=8,
    font=("Consolas", 14),
    fg="black",
    bg="white",
    textvariable=noise_var,
)
the5_label.pack(side=LEFT, padx=(40, 0), pady=0)
SNF_button = tk.Button(
    frame,
    height=1,
    width=14,
    font=("consolas", 16),
    # text="Select Texture file",
    textvariable=noise_button_var,
    command=SelectNoiseFile,
)
SNF_button.pack(side=LEFT, padx=10, pady=0)
SNF_button.config(state="disabled")


frame2 = tk.LabelFrame(
    window,
    text="Terrain Para",
    font=("Consolas", 24),
    bg="white",
    fg="blue",
)
frame2.pack(padx=10, pady=(20, 0))

the2_label = tk.Label(
    frame2,
    height=2,
    width=22,
    font=("Consolas", 16),
    fg="black",
    bg="yellow",
    # text="地形参数的设置",
    textvariable=tp_label_var,
)
the2_label.pack(padx=50, pady=10)


def t1_para():
    global values1
    popuppit = tk.Toplevel(window)

    Labelpit = [
        "k_c[40, 5000](e^3): ",
        "k_ψ[1, 100](e^3): ",
        "n[0.2, 1.6]: ",
        "c[1, 70](e^3): ",
        "ψ[5, 40]: ",
        "shear[1, 3](e^(-2)): ",
        "K[4, 4.5](e^8): ",
        "R[3, 3.5](e^4): ",
    ]

    # 创建6个组合
    i = 0
    spinboxes = []  # 存储Spinbox控件的列表
    for i in range(1):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=40, to=1500, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(1, 2):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=100, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(2, 3):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=0.2, to=1.6, increment=0.1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(3, 4):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=70, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(4, 5):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=5, to=40, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(5, 6):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=3, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(6, 7):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=4, to=4.5, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(7, 8):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=3, to=3.5, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)

    def getValue1():
        global values1
        values = [spinbox.get() for spinbox in spinboxes]
        # print(type(int(values[0])), int(values[0]))
        values1 = [
            float(values[0]) * 1e3,
            float(values[1]) * 1e3,
            float(values[2]),
            float(values[3]) * 1e3,
            float(values[4]),
            float(values[5]) * 1e-2,
            float(values[6]) * 1e8,
            float(values[7]) * 1e4,
        ]
        popuppit.destroy()

    btnClose = tk.Button(
        popuppit,
        width=6,
        text="确定",
        height=2,
        font=("consolas", 10),
        command=getValue1,
    ).grid(
        column=1,
    )


def t2_para():
    global values2
    popuppit = tk.Toplevel(window)

    Labelpit = [
        "k_c[40, 5000](e^3): ",
        "k_ψ[1, 100](e^3): ",
        "n[0.2, 1.6]: ",
        "c[1, 70](e^3): ",
        "ψ[5, 40]: ",
        "shear[1, 3](e^(-2)): ",
        "K[4, 4.5](e^8): ",
        "R[3, 3.5](e^4): ",
    ]

    # 创建6个组合
    i = 0
    spinboxes = []  # 存储Spinbox控件的列表
    for i in range(1):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=40, to=1500, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(1, 2):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=100, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(2, 3):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=0.2, to=1.6, increment=0.1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(3, 4):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=70, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(4, 5):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=5, to=40, increment=1)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(5, 6):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=1, to=3, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(6, 7):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=4, to=4.5, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)
    for i in range(7, 8):
        # 创建Label和Spinbox，并使用grid布局放置在不同的行上
        label = tk.Label(popuppit, text=Labelpit[i])
        label.grid(row=i, column=0)

        spinbox = tk.Spinbox(popuppit, from_=3, to=3.5, increment=0.01)
        spinbox.grid(row=i, column=1)
        spinboxes.append(spinbox)

    def getValue2():
        global values2
        values = [spinbox.get() for spinbox in spinboxes]
        print(values)
        values2 = [
            float(values[0]) * 1e3,
            float(values[1]) * 1e3,
            float(values[2]),
            float(values[3]) * 1e3,
            float(values[4]),
            float(values[5]) * 1e-2,
            float(values[6]) * 1e8,
            float(values[7]) * 1e4,
        ]
        popuppit.destroy()

    btnClose = tk.Button(
        popuppit,
        width=6,
        text="确定",
        height=2,
        font=("consolas", 10),
        command=getValue2,
    ).grid(
        column=1,
    )


t1_btn = tk.Button(
    frame2,
    width=14,
    # text="第一组地形参数",
    textvariable=t1_var,
    height=1,
    font=("consolas", 14),
    command=t1_para,
).pack(side=LEFT, padx=(60, 10), pady=(10))

t2_btn = tk.Button(
    frame2,
    width=14,
    # text="第二组地形参数",
    textvariable=t2_var,
    height=1,
    font=("consolas", 14),
    command=t2_para,
).pack(side=LEFT, padx=(60, 40), pady=(10))

btnYes = tk.Button(
    window,
    width=12,
    textvariable=yes_var,
    height=1,
    font=("consolas", 16),
    command=RunPychrono,
).pack(pady=5)


btnClose = tk.Button(
    window,
    width=6,
    text="Close",
    height=1,
    font=("consolas", 16),
    command=window.destroy,
).pack()
# 进入主事件循环
window.mainloop()
