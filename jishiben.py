#-*-coding:utf-8-*-
# "My Journal version 1.0
# @kk 26-JAN-2023"
# 21-Nov-2023，修正部分中文字符无法输入的问题
# 20-Dec-2023，添加查找功能。添加快捷键
# 4-Jan-2024, 增加右键菜单；增加中文特殊符号输入

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import time  
import pyperclip

def open_file():
    global file_path
    file_path=filedialog.askopenfilename(filetype=[('Text files','*.txt')])
    load_file() # 加括号执行；不加括号引用。

# Initial display jishiben.txt
def load_file():  
    with open(file_path, "r") as f:  
        text = f.read()  
    text_box1.delete("1.0", tk.END)  
    text_box1.insert(tk.END, text)  
    text_box1.see("end-1c")  # 定位在最后一行 
    root.title("记事本 - " + file_path)

# RECORD input
def append_to_file():  
    input_text = text_box2.get("1.0", "end-1c")  
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
    with open(file_path, "a") as f:  
        f.write(timestamp + "\n" + input_text+"\n\n")  # 构造字符串：时间+换行+文本+换行
    load_file()  # 更新文本框1的内容  
    text_box2.delete("1.0", "end")  # 清空文本框2的内容  
    text_box2.focus_set()  # 将焦点设置为文本框2，以备下次输入
  
def return_to_append(self):  
    input_text = text_box2.get("1.0", "end-1c")  
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
    with open(file_path, "a") as f:  
        f.write(timestamp + "\n" + input_text+"\n\n")  
    load_file()  # 更新文本框1的内容  
    text_box2.delete("1.0", "end")  # 清空文本框2的内容  
    text_box2.focus_set()  # 将焦点设置为文本框2，以备下次输入
    return 'break'

def test():
    print('this is a test function')


def show_about():
    # about_info = "This is the about information of the software.\nFor more details, visit our website: http://abc.com"
    # messagebox.showinfo("About", about_info)
    # create textbox_about
    About_window=tk.Toplevel(root)  # 新建About 子窗口
    About_window.title("About")
    About_window.geometry("+250+250")
    About_font = tkFont.Font(family='Consolas', size=10)
    textbox_about = tk.Text(About_window, width=40, height=10, padx=5, pady=2, foreground="Black",background='#f3f3f3', font=About_font)  #新建一个文本框
    #textbox_about.configure(font=About_font,foreground="black",background='#f3f3f3') # 这句参数也可以写到上面一句里
    textbox_about.pack()  
    # open about.txt
    with open("about.txt", "r") as f:  
        text = f.read()  
    textbox_about.delete("1.0", "end")  
    textbox_about.insert("1.0", text)  
    #textbox_about.see("end-1c")  # 定位在最后一行 
    f.close()

def handle_event(event):
    if event.keysym == "o":
        open_file()
    elif event.keysym == "w":
        root.quit()
    elif event.keysym == "f":
        open_find_window()

def on_return_key(event):
    find_next()

# 查找功能
def open_find_window():
    # 查找
    find_window = Toplevel() 
    find_window.title("Find")
    find_window.geometry("300x100+450+200")
    label = Label(find_window, text="Find:")
    label.pack(side=LEFT)
    global entry
    global button
    entry=Entry(find_window)
    entry.pack(side=LEFT)
    button= Button(find_window, text="Find Next", command=find_next)
    button.pack(side=LEFT)
    entry.focus_set()
    find_window.bind("<Return>", on_return_key) # 绑定回车键。按回撤默认开始搜索。
    def on_closing():
        # Add any cleanup or refresh logic before closing the window
        # Call the refresh function before closing the window
        text_box1.tag_remove("found", "1.0", END) #从1.0到end，取消所有“found”结果的tag（高亮）
        find_window.destroy()  # Close the window
    find_window.protocol("WM_DELETE_WINDOW", on_closing)

# FUNCTION FIND_NEXT 01 一次高亮标记所有符合条件的结果；
# def find_next():
#     text_box1.tag_remove("found", "1.0", END) #从1.0到end，取消所有“found”结果的tag（高亮）
#     count=0; start="1.0"  #start 是查找的起始位置；end是末尾位置。大写END是变量，
#     keyword=entry.get()
#     if keyword:
#         while True:
#             start=text_box1.search(keyword,start,stopindex=END,nocase=True) #nocase=true 不区分大小写
#             if not start:
#                 break
#             end=f"{start}+{len(keyword)}c"
#             text_box1.tag_add("found",start,end)
#             text_box1.see(start)
#             count += 1; start=end
#         text_box1.tag_configure("found",background="yellow", foreground="red")
#         entry.focus_set()

# FUNCTION FIND NEXT 02 一次只高亮显示一个结果，点击查找下一个，继续显示下一个，循环往复。
start="1.0"
def find_next():
    global start
    text_box1.tag_remove("found", "1.0", END) #从1.0到end，取消所有“found”结果的tag（高亮）
    count=0; 
    #start="1.0"  #start 是查找的起始位置；end是末尾位置。大写END是变量，
    keyword=entry.get()
    if keyword:
        start=text_box1.search(keyword,start,stopindex=END,nocase=True) #nocase=true 不区分大小写
        if start:
            end=f"{start}+{len(keyword)}c"
            text_box1.tag_add("found",start,end)
            text_box1.see(start)
            count += 1; start=end
            text_box1.tag_configure("found",background="yellow", foreground="red")
            entry.focus_set()
        else:
            start="1.0"
            find_next()

# 定义鼠标右键项目
def callback1(event=None):
    global root
    text_box2.event_generate('<<Cut>>')
    
def callback2(event=None):
    global root
    text_box2.event_generate('<<Copy>>')
    
def callback3(event=None):
    global root
    text_box2.event_generate('<<Paste>>')
         

# initial
file_path="jishiben.txt"
#file2="about.txt"

root = tk.Tk()  
root.title("记事本 - " + file_path)  
root.geometry("+100+100")
myfont = tkFont.Font(family='consolas', size=11)


# create a menu bar
menubar = Menu(root)
# create the "File" menu and add the "Open File" menu item
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Open File', command = open_file, accelerator='Ctrl+o') #函数不能加括号，加括号表示调用；不加括号表示引用
filemenu.add_separator # split line
filemenu.add_command(label='Exit', command = root.quit, accelerator='Ctrl+w') 
#create the 'Edit' menu and add the 'search' menu item
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_command(label='Find', command=open_find_window, accelerator='Ctrl+f')
# create the "Help" menu and add the 'About' menu item
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About', command = show_about) 
# Creat mouse-right-click-menu
rightclickmenu = Menu(root,
            tearoff=False,
            #bg="black",
            )
rightclickmenu.add_command(label="剪切", command=callback1)
rightclickmenu.add_command(label="复制", command=callback2)
rightclickmenu.add_command(label="粘贴", command=callback3)
# config the root to use the menubar
root.config(menu=menubar)

# create window - textbox1 for DISPLAY(UP) and textbox2 for INPUT(DOWN)
# text box1 - DISPLAY Box
text_box1 = tk.Text(root, width=100, height=30, borderwidth=1, padx=4, pady=4, font=myfont)  
#text_box1.configure(font=("宋体", 11),foreground="black", charset='UTF-8')
text_box1.pack(padx=0,pady=0) 
# text box2 - INPUT box
text_box2 = tk.Text(root, width=100, height=10, borderwidth=1, padx=4, pady=4, font=myfont)  
#text_box2.configure(font=("宋体", 11),foreground="black")
text_box2.pack(padx=0,pady=0)  
# SEND button  
button = tk.Button(root, text="发布 (Ctrl+Enter)", command=append_to_file, width=15, height=1)  #pady padx 写在这里是内边距；
button.pack(pady=5)  # padx，pady 写在pack里代表外边距

# Keyboard shortcut
# 绑定回车键事件，实现点击回车键发布文本框2的内容  
text_box2.bind("<Control-Return>", return_to_append)  
root.bind_all("<Control-o>", handle_event)
root.bind_all("<Control-w>", handle_event)
root.bind_all("<Control-f>", handle_event)
# text_box1 右键鼠标事件
def popup(event):
    rightclickmenu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单
text_box2.bind("<Button-3>", popup)  

load_file()  # 重新加载test.txt文件并显示在文本框1中 
text_box2.focus_set()  # 将焦点设置为文本框2，以备下次输入
root.mainloop()