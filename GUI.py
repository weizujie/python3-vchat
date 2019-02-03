import pickle
import tkinter as tk
from tkinter import messagebox

# 第一个界面
home_window = tk.Tk()
home_window.title('取啥名好呢')
home_window.geometry('450x300')

# home window
canvas = tk.Canvas(home_window, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')
tk.Label(home_window, text='用户名').place(x=50, y=150)
tk.Label(home_window, text='密码').place(x=50, y=190)
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(home_window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(home_window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            # 测试用用户名和密码
            usrs_info = {
                'a': 'a',
            }
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            # 登录成功, 显示用户界面, 销毁主窗口
            home_window.destroy()

            user_window = tk.Tk()
            user_window.geometry('300x200')
            user_window.title('用户界面')
            tk.Label(user_window, text='欢迎你\n\n' + usr_name).place(x=10, y=30)

            tk.Label(user_window, text='请选择功能:\n1. 语音聊天: 正在完善中\n2. 成绩查询: 查询你的成绩').place(x=120, y=50)

            # 查询成绩按钮触发处理
            def get_score():
                score_listbox = tk.Listbox(user_window)
                score_dict = {
                    'a': '1',
                    'b': '2',
                    'c': '3',
                    'd': '4',
                    'e': '5',
                    'f': '6',
                    'g': '7',
                    'h': '8',
                    'i': '9',
                    'j': '23123',
                    'qdwd': '23123'
                }
                for eve_score in score_dict.items():
                    score_listbox.insert(1, eve_score)
                score_listbox.place(x=120, y=10)

            def tuling():
                pass

            # 聊天室按钮
            tk.Button(user_window, text='语音聊天', command=tuling).place(x=20, y=100)
            # 查询成绩按钮
            tk.Button(user_window, text='查询成绩', command=get_score).place(x=20, y=150)


        else:
            tk.messagebox.showerror('Error', '用户名或密码错误，请重试!')
    elif ((usr_name and usr_pwd) == ''):
        tk.messagebox.showerror('Error', '用户名和密码不能为空, 请重试!')
    else:
        tk.messagebox.showerror('Error', '用户名或密码错误，请重试!')


def usr_sign_up():
    def sign_up():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('Error', '输入的两次密码不一致!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', '该用户名已经被注册!')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Welcome', '注册成功!')
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(home_window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('用户注册界面')

    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='用户名 ').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码 ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码 ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_up)
    btn_comfirm_sign_up.place(x=150, y=130)


# login and sign up button
tk.Button(home_window, text='登录', command=usr_login).place(x=170, y=230)
tk.Button(home_window, text='注册', command=usr_sign_up).place(x=250, y=230)

home_window.mainloop()
