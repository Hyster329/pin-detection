#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import shutil
import os
import time
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from checkpins import checkpin_main


class Toplevel:
    '''主窗口'''
    def __init__(self, top=None):
        # 配置窗口大小，位置，标题，背景颜色
        top.geometry("1400x750+246+156")
        top.minsize(120, 1)
        top.maxsize(3844, 1061)
        top.resizable(1,  1)
        top.title("针脚异常检测工具")
        top.configure(background="#d9d9d9")

        # 指定元素所在窗口
        self.top = top

        self.Image_show_Label = tk.Label(self.top)
        self.Image_show_Label.place(relx=0.017, rely=0.027, height=615, width=921)
        self.Image_show_Label.configure(activebackground="#f9f9f9")
        self.Image_show_Label.configure(anchor='w')
        self.Image_show_Label.configure(background="#ffffff")
        self.Image_show_Label.configure(compound='left')
        self.Image_show_Label.configure(disabledforeground="#a3a3a3")
        self.Image_show_Label.configure(foreground="#000000")
        self.Image_show_Label.configure(highlightbackground="#d9d9d9")
        self.Image_show_Label.configure(highlightcolor="black")
        self.Image_show_Label.configure(text="")

        self.Result_Label = tk.Label(self.top)
        self.Result_Label.place(relx=0.217, rely=0.893, height=43, width=634)
        self.Result_Label.configure(activebackground="#f9f9f9")
        self.Result_Label.configure(anchor='w')
        self.Result_Label.configure(background="#ffffff")
        self.Result_Label.configure(compound='center')
        self.Result_Label.configure(disabledforeground="#a3a3a3")
        self.Result_Label.configure(foreground="#000000")
        self.Result_Label.configure(highlightbackground="#d9d9d9")
        self.Result_Label.configure(highlightcolor="black")
        self.Result_Label.configure(text='')

        self.Label3 = tk.Label(self.top)
        self.Label3.place(relx=0.092, rely=0.893, height=43, width=137)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''当前图像检测结果：''')

        self.detect_mode = tk.StringVar()
        self.detect_mode.set('单例检测')  # 默认单例检测

        self.Single_button = tk.Radiobutton(self.top, text='单例检测', value='single', variable=self.detect_mode)
        self.Single_button.pack(side=tk.TOP, fill=tk.X)
        self.Single_button.place(relx=0.7, rely=0.04, relheight=0.036, relwidth=0.054)
        self.Single_button.configure(activebackground="beige")
        self.Single_button.configure(activeforeground="#000000")
        self.Single_button.configure(anchor='w')
        self.Single_button.configure(background="#d9d9d9")
        self.Single_button.configure(compound='left')
        self.Single_button.configure(disabledforeground="#a3a3a3")
        self.Single_button.configure(foreground="#000000")
        self.Single_button.configure(highlightbackground="#d9d9d9")
        self.Single_button.configure(highlightcolor="black")
        self.Single_button.configure(justify='left')

        self.Batch_button = tk.Radiobutton(self.top, text='批量检测', value='batch', variable=self.detect_mode)
        self.Batch_button.pack(side=tk.TOP, fill=tk.X)
        self.Batch_button.place(relx=0.8, rely=0.04, relheight=0.036, relwidth=0.054)
        self.Batch_button.configure(activebackground="beige")
        self.Batch_button.configure(activeforeground="#000000")
        self.Batch_button.configure(anchor='w')
        self.Batch_button.configure(background="#d9d9d9")
        self.Batch_button.configure(compound='left')
        self.Batch_button.configure(disabledforeground="#a3a3a3")
        self.Batch_button.configure(foreground="#000000")
        self.Batch_button.configure(highlightbackground="#d9d9d9")
        self.Batch_button.configure(highlightcolor="black")
        self.Batch_button.configure(justify='left')

        self.Input_directory_Entry = tk.Entry(self.top)
        self.Input_directory_Entry.place(relx=0.786, rely=0.107, height=28, relwidth=0.196)
        self.Input_directory_Entry.configure(background="white")
        self.Input_directory_Entry.configure(disabledforeground="#a3a3a3")
        self.Input_directory_Entry.configure(font="TkFixedFont")
        self.Input_directory_Entry.configure(foreground="#000000")
        self.Input_directory_Entry.configure(highlightbackground="#d9d9d9")
        self.Input_directory_Entry.configure(highlightcolor="black")
        self.Input_directory_Entry.configure(insertbackground="black")
        self.Input_directory_Entry.configure(selectbackground="#c4c4c4")
        self.Input_directory_Entry.configure(selectforeground="black")

        self.Select_Input_Button = tk.Button(self.top)
        self.Select_Input_Button.place(relx=0.693, rely=0.107, height=28, width=109)
        self.Select_Input_Button.configure(activebackground="beige")
        self.Select_Input_Button.configure(activeforeground="#000000")
        self.Select_Input_Button.configure(background="#d9d9d9")
        self.Select_Input_Button.configure(compound='left')
        self.Select_Input_Button.configure(disabledforeground="#a3a3a3")
        self.Select_Input_Button.configure(foreground="#000000")
        self.Select_Input_Button.configure(highlightbackground="#d9d9d9")
        self.Select_Input_Button.configure(highlightcolor="black")
        self.Select_Input_Button.configure(pady="0")
        self.Select_Input_Button.configure(text='''选择文件/文件夹''')

        self.Select_Output_Button = tk.Button(self.top)
        self.Select_Output_Button.place(relx=0.693, rely=0.173, height=28, width=109)
        self.Select_Output_Button.configure(activebackground="beige")
        self.Select_Output_Button.configure(activeforeground="#000000")
        self.Select_Output_Button.configure(background="#d9d9d9")
        self.Select_Output_Button.configure(compound='left')
        self.Select_Output_Button.configure(disabledforeground="#a3a3a3")
        self.Select_Output_Button.configure(foreground="#000000")
        self.Select_Output_Button.configure(highlightbackground="#d9d9d9")
        self.Select_Output_Button.configure(highlightcolor="black")
        self.Select_Output_Button.configure(pady="0")
        self.Select_Output_Button.configure(text='''选择结果存储目录''')

        self.Output_directory_Entry = tk.Entry(self.top)
        self.Output_directory_Entry.place(relx=0.786, rely=0.173, height=28, relwidth=0.196)
        self.Output_directory_Entry.configure(background="white")
        self.Output_directory_Entry.configure(cursor="fleur")
        self.Output_directory_Entry.configure(disabledforeground="#a3a3a3")
        self.Output_directory_Entry.configure(font="TkFixedFont")
        self.Output_directory_Entry.configure(foreground="#000000")
        self.Output_directory_Entry.configure(highlightbackground="#d9d9d9")
        self.Output_directory_Entry.configure(highlightcolor="black")
        self.Output_directory_Entry.configure(insertbackground="black")
        self.Output_directory_Entry.configure(selectbackground="#c4c4c4")
        self.Output_directory_Entry.configure(selectforeground="black")

        self.Begin_Button = tk.Button(self.top)
        self.Begin_Button.place(relx=0.693, rely=0.24, height=38, width=409)
        self.Begin_Button.configure(activebackground="beige")
        self.Begin_Button.configure(activeforeground="#000000")
        self.Begin_Button.configure(background="#d9d9d9")
        self.Begin_Button.configure(compound='left')
        self.Begin_Button.configure(disabledforeground="#a3a3a3")
        self.Begin_Button.configure(foreground="#000000")
        self.Begin_Button.configure(highlightbackground="#d9d9d9")
        self.Begin_Button.configure(highlightcolor="black")
        self.Begin_Button.configure(pady="0")
        self.Begin_Button.configure(text='''开始检测''')

        self.Padding_Label = tk.Label(self.top)
        self.Padding_Label.place(relx=0.693, rely=0.32, height=28, width=118)
        self.Padding_Label.configure(anchor='w')
        self.Padding_Label.configure(background="#d9d9d9")
        self.Padding_Label.configure(compound='left')
        self.Padding_Label.configure(disabledforeground="#a3a3a3")
        self.Padding_Label.configure(foreground="#000000")
        self.Padding_Label.configure(text='''图像边界填充高度：''')

        self.Padding_Entry = tk.Entry(self.top)
        self.Padding_Entry.place(relx=0.786, rely=0.32, height=28, relwidth=0.06)
        self.Padding_Entry.configure(background="white")
        self.Padding_Entry.configure(disabledforeground="#a3a3a3")
        self.Padding_Entry.configure(font="TkFixedFont")
        self.Padding_Entry.configure(foreground="#000000")
        self.Padding_Entry.configure(insertbackground="black")
        self.Padding_Entry.insert(0, "30")

        self.Padding_mes_Label = tk.Label(self.top)
        self.Padding_mes_Label.place(relx=0.857, rely=0.32, height=28, width=179)
        self.Padding_mes_Label.configure(anchor='w')
        self.Padding_mes_Label.configure(background="#d9d9d9")
        self.Padding_mes_Label.configure(compound='left')
        self.Padding_mes_Label.configure(disabledforeground="#a3a3a3")
        self.Padding_mes_Label.configure(foreground="#000000")
        self.Padding_mes_Label.configure(text='''(影响检测图像的上下边界)''')

        self.Threshold_Label = tk.Label(self.top)
        self.Threshold_Label.place(relx=0.693, rely=0.387, height=28, width=118)
        self.Threshold_Label.configure(anchor='w')
        self.Threshold_Label.configure(background="#d9d9d9")
        self.Threshold_Label.configure(compound='left')
        self.Threshold_Label.configure(disabledforeground="#a3a3a3")
        self.Threshold_Label.configure(foreground="#000000")
        self.Threshold_Label.configure(text='''阈值分割：''')

        self.Threshold_Entry = tk.Entry(self.top)
        self.Threshold_Entry.place(relx=0.786, rely=0.387, height=28, relwidth=0.06)
        self.Threshold_Entry.configure(background="white")
        self.Threshold_Entry.configure(disabledforeground="#a3a3a3")
        self.Threshold_Entry.configure(font="TkFixedFont")
        self.Threshold_Entry.configure(foreground="#000000")
        self.Threshold_Entry.configure(insertbackground="black")
        self.Threshold_Entry.insert(0, "130")

        self.Threshold_msg_Label = tk.Label(self.top)
        self.Threshold_msg_Label.place(relx=0.857, rely=0.387, height=28, width=176)
        self.Threshold_msg_Label.configure(anchor='w')
        self.Threshold_msg_Label.configure(background="#d9d9d9")
        self.Threshold_msg_Label.configure(compound='left')
        self.Threshold_msg_Label.configure(disabledforeground="#a3a3a3")
        self.Threshold_msg_Label.configure(foreground="#000000")
        self.Threshold_msg_Label.configure(text='''(输入图像阈值分割的低阈值)''')

        self.Median_kernel_Label = tk.Label(self.top)
        self.Median_kernel_Label.place(relx=0.693, rely=0.453, height=28, width=118)
        self.Median_kernel_Label.configure(anchor='w')
        self.Median_kernel_Label.configure(background="#d9d9d9")
        self.Median_kernel_Label.configure(compound='left')
        self.Median_kernel_Label.configure(disabledforeground="#a3a3a3")
        self.Median_kernel_Label.configure(foreground="#000000")
        self.Median_kernel_Label.configure(text='''中值滤波器大小：''')

        self.Median_kernel_Entry = tk.Entry(self.top)
        self.Median_kernel_Entry.place(relx=0.786, rely=0.453, height=28, relwidth=0.06)
        self.Median_kernel_Entry.configure(background="white")
        self.Median_kernel_Entry.configure(disabledforeground="#a3a3a3")
        self.Median_kernel_Entry.configure(font="TkFixedFont")
        self.Median_kernel_Entry.configure(foreground="#000000")
        self.Median_kernel_Entry.configure(insertbackground="black")
        self.Median_kernel_Entry.insert(0, "11")

        self.Median_kernel_msg_Label = tk.Label(self.top)
        self.Median_kernel_msg_Label.place(relx=0.857, rely=0.453, height=28, width=176)
        self.Median_kernel_msg_Label.configure(anchor='w')
        self.Median_kernel_msg_Label.configure(background="#d9d9d9")
        self.Median_kernel_msg_Label.configure(compound='left')
        self.Median_kernel_msg_Label.configure(disabledforeground="#a3a3a3")
        self.Median_kernel_msg_Label.configure(foreground="#000000")
        self.Median_kernel_msg_Label.configure(text='''(二值图像中值滤波降噪)''')

        self.Open_kernel_Label = tk.Label(self.top)
        self.Open_kernel_Label.place(relx=0.693, rely=0.52, height=28, width=118)
        self.Open_kernel_Label.configure(anchor='w')
        self.Open_kernel_Label.configure(background="#d9d9d9")
        self.Open_kernel_Label.configure(compound='left')
        self.Open_kernel_Label.configure(disabledforeground="#a3a3a3")
        self.Open_kernel_Label.configure(foreground="#000000")
        self.Open_kernel_Label.configure(text='''降噪开操作核心尺寸：''')

        self.Open_kernel_Entry = tk.Entry(self.top)
        self.Open_kernel_Entry.place(relx=0.786, rely=0.52, height=28, relwidth=0.06)
        self.Open_kernel_Entry.configure(background="white")
        self.Open_kernel_Entry.configure(disabledforeground="#a3a3a3")
        self.Open_kernel_Entry.configure(font="TkFixedFont")
        self.Open_kernel_Entry.configure(foreground="#000000")
        self.Open_kernel_Entry.configure(insertbackground="black")
        self.Open_kernel_Entry.insert(0, "30")

        self.Open_kernel_msg_Label = tk.Label(self.top)
        self.Open_kernel_msg_Label.place(relx=0.857, rely=0.52, height=28, width=176)
        self.Open_kernel_msg_Label.configure(anchor='w')
        self.Open_kernel_msg_Label.configure(background="#d9d9d9")
        self.Open_kernel_msg_Label.configure(compound='left')
        self.Open_kernel_msg_Label.configure(disabledforeground="#a3a3a3")
        self.Open_kernel_msg_Label.configure(foreground="#000000")
        self.Open_kernel_msg_Label.configure(text='''(矩形检测阶段开操作去噪)''')

        self.Channy_open_kernel_Label = tk.Label(self.top)
        self.Channy_open_kernel_Label.place(relx=0.693, rely=0.587, height=28, width=118)
        self.Channy_open_kernel_Label.configure(anchor='w')
        self.Channy_open_kernel_Label.configure(background="#d9d9d9")
        self.Channy_open_kernel_Label.configure(compound='left')
        self.Channy_open_kernel_Label.configure(disabledforeground="#a3a3a3")
        self.Channy_open_kernel_Label.configure(foreground="#000000")
        self.Channy_open_kernel_Label.configure(text='''轮廓开操作核心尺寸：''')

        self.Channy_open_kernel_Entry = tk.Entry(self.top)
        self.Channy_open_kernel_Entry.place(relx=0.786, rely=0.587, height=28, relwidth=0.06)
        self.Channy_open_kernel_Entry.configure(background="white")
        self.Channy_open_kernel_Entry.configure(disabledforeground="#a3a3a3")
        self.Channy_open_kernel_Entry.configure(font="TkFixedFont")
        self.Channy_open_kernel_Entry.configure(foreground="#000000")
        self.Channy_open_kernel_Entry.configure(insertbackground="black")
        self.Channy_open_kernel_Entry.insert(0, "13")

        self.Channy_open_kernel_Label = tk.Label(self.top)
        self.Channy_open_kernel_Label.place(relx=0.857, rely=0.587, height=28, width=176)
        self.Channy_open_kernel_Label.configure(anchor='w')
        self.Channy_open_kernel_Label.configure(background="#d9d9d9")
        self.Channy_open_kernel_Label.configure(compound='left')
        self.Channy_open_kernel_Label.configure(disabledforeground="#a3a3a3")
        self.Channy_open_kernel_Label.configure(foreground="#000000")
        self.Channy_open_kernel_Label.configure(text='''(开操作去除边界相连)''')

        self.Process_Label = tk.Label(self.top)
        self.Process_Label.place(relx=0.693, rely=0.653, height=28, width=417)
        self.Process_Label.configure(anchor='w')
        self.Process_Label.configure(background="#d9d9d9")
        self.Process_Label.configure(compound='left')
        self.Process_Label.configure(disabledforeground="#a3a3a3")
        self.Process_Label.configure(foreground="#000000")
        self.Process_Label.configure(text='''检测进程信息：''')

        self.Process_Text = tk.Text(self.top)
        self.scroll_bar = tk.Scrollbar(self.top)
        self.Process_Text.place(relx=0.693, rely=0.707, relheight=0.256, relwidth=0.289)
        self.scroll_bar.config(command=self.Process_Text.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Process_Text.config(yscrollcommand=self.scroll_bar.set)
        self.Process_Text.configure(background="white")
        self.Process_Text.configure(font="TkTextFont")
        self.Process_Text.configure(foreground="black")
        self.Process_Text.configure(highlightbackground="#d9d9d9")
        self.Process_Text.configure(highlightcolor="black")
        self.Process_Text.configure(insertbackground="black")
        self.Process_Text.configure(selectbackground="#c4c4c4")
        self.Process_Text.configure(selectforeground="black")
        self.Process_Text.configure(wrap="word")

        # 设置鼠标移到按钮上的事件，弹出提示
        CreateToolTip(self.Select_Input_Button, '选择文件（单例）或文件夹（批处理）')
        CreateToolTip(self.Select_Output_Button, '选择检测文件输出存放目录，程序将在该目录下新建子目录用于分类存储')

        # 绑定按钮事件
        self.Select_Input_Button.configure(command=self.choosepic)
        self.Select_Output_Button.configure(command=self.choose_outpath)
        self.Begin_Button.configure(command=self.check_main)

    def choosepic(self):
        if self.detect_mode.get() == "single":
            image_path = filedialog.askopenfilename(title='Select Image')
            self.Process_Text.insert('end', f"选择文件{image_path}\n")
            self.Process_Text.yview('end')
            self.Input_directory_Entry.delete(0, tk.END)
            self.Input_directory_Entry.insert(0, image_path)
            self.process_pic()
        elif self.detect_mode.get() == "batch":
            image_path = filedialog.askdirectory(title='Select Folder')
            self.Process_Text.insert('end', f"选择文件夹{image_path}\n")
            self.Process_Text.yview('end')
            self.Input_directory_Entry.delete(0, tk.END)
            self.Input_directory_Entry.insert(0, image_path)
        else:
            self.Process_Text.insert('end', "请选择有效路径!\n")
            self.Process_Text.yview('end')

    def choose_outpath(self):
        folder_path = filedialog.askdirectory(title='Select Folder')
        self.Process_Text.insert('end', f"选择文件夹{folder_path}\n")
        self.Process_Text.yview('end')
        self.Output_directory_Entry.delete(0, tk.END)
        self.Output_directory_Entry.insert(0, folder_path)
        if not os.path.exists(os.path.join(folder_path, "Normal")):
            os.mkdir(os.path.join(folder_path, "Normal"))
            self.Process_Text.insert('end', f"创建新文件夹{os.path.join(folder_path, 'Normal')}\n")
            self.Process_Text.yview('end')
        if not os.path.exists(os.path.join(folder_path, "Abnormal")):
            os.mkdir(os.path.join(folder_path, "Abnormal"))
            self.Process_Text.insert('end', f"创建新文件夹{os.path.join(folder_path, 'Abnormal')}\n")
            self.Process_Text.yview('end')

    def process_pic(self):
        image_path = self.Input_directory_Entry.get()
        if image_path == '' or not os.path.exists(image_path):
            messagebox.showerror('错误', '请输入有效路径！')
        img_open = Image.open(image_path)
        img_resize = img_open.resize((921, 614), Image.LANCZOS)
        image = ImageTk.PhotoImage(img_resize)
        self.Image_show_Label.config(image=image)
        self.Image_show_Label.image = image

    def check_main(self):
        image_path = self.Input_directory_Entry.get()
        out_path = self.Output_directory_Entry.get()
        if image_path == '' or not os.path.exists(image_path) or out_path == '' or not os.path.exists(out_path):
            messagebox.showerror('错误', '请输入有效路径！')
        else:
            self.Process_Text.insert('end', f"开始{self.detect_mode.get()}检测...\n")
            self.Process_Text.yview('end')

        padding = int(self.Padding_Entry.get())
        threshold = int(self.Threshold_Entry.get())
        median_kernel = int(self.Median_kernel_Entry.get())
        open_kernel = int(self.Open_kernel_Entry.get())
        channy_open_kernel = int(self.Channy_open_kernel_Entry.get())
        self.Process_Text.insert('end', f"当前主要参数{padding}，{threshold}，"
                                        f"{median_kernel}，{open_kernel}，{channy_open_kernel}.\n")
        self.Process_Text.yview('end')

        if self.detect_mode.get() == "single":
            result = checkpin_main(image_path, padding, threshold, median_kernel, open_kernel, channy_open_kernel)
            self.Process_Text.insert('end', f"当前检测图像文件名：{os.path.basename(image_path)}\n")
            self.Process_Text.insert('end', f"当前图像检测结果为：{result}\n")
            self.Process_Text.yview('end')
            self.Process_Text.update()
            if result:
                shutil.copyfile(image_path, os.path.join(out_path, "Normal", os.path.basename(image_path)))
                self.Result_Label.configure(text='''正常''')
                self.Result_Label.update()
            else:
                shutil.copyfile(image_path, os.path.join(out_path, "Abnormal", os.path.basename(image_path)))
                self.Result_Label.configure(text='''异常''')
                self.Result_Label.update()
        elif self.detect_mode.get() == "batch":
            for name in os.listdir(image_path):
                check_path = os.path.join(image_path, name)

                img_open = Image.open(check_path)
                img_resize = img_open.resize((921, 614), Image.LANCZOS)
                image = ImageTk.PhotoImage(img_resize)
                self.Image_show_Label.config(image=image)
                self.Image_show_Label.image = image
                self.Image_show_Label.update()

                result = checkpin_main(check_path, padding, threshold, median_kernel, open_kernel, channy_open_kernel)
                self.Process_Text.insert('end', f"当前检测图像文件名：{name}\n")
                self.Process_Text.insert('end', f"当前图像检测结果为：{result}\n")
                self.Process_Text.yview('end')
                self.Process_Text.update()
                if result:
                    shutil.copyfile(check_path, os.path.join(out_path, "Normal", name))
                    self.Result_Label.configure(text='''正常''')
                    self.Result_Label.update()
                else:
                    shutil.copyfile(check_path, os.path.join(out_path, "Abnormal", name))
                    self.Result_Label.configure(text='''异常''')
                    self.Result_Label.update()
        else:
            self.Process_Text.insert('end', "请选择检测模式!\n")
            self.Process_Text.yview('end')
    def destroy(self):
        '''窗口销毁函数'''
        self.destroy()


class ToolTip(object):
    '''设定鼠标停留事件'''
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "隐藏文本"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()+30
        y = y + cy + self.widget.winfo_rooty()+30
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="white", relief=tk.SOLID, borderwidth=1,
                      font=("黑体", "10"))
        label.pack(side=tk.BOTTOM)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    """实现鼠标移入移出事件"""
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class Application(tk.Tk):
    """定义主窗口逻辑"""
    def __init__(self):
        super(Application, self).__init__()
        # 实例化首页界面，并绑定按钮事件
        self.Toplevel = Toplevel(self)



if __name__ == '__main__':
    app = Application()  # 实例化主界面
    app.mainloop()  # 循环保持窗口开启