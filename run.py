import pickle
import tkinter as tk
import wave
import json
import time
import requests
import numpy as np
from aip import AipSpeech
from tkinter import messagebox
from config import *


class Iting:

    def __init__(self):

        # home window
        self.home_window = tk.Tk()
        self.home_window.title('iTing v0.0.1')
        self.home_window.geometry('450x300')

        # welcome image
        self.canvas = tk.Canvas(self.home_window, height=200, width=500)
        self.image_file = tk.PhotoImage(file='welcome.gif')
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.image_file)
        self.canvas.pack(side='top')

        # username and password label
        self.l1 = tk.Label(self.home_window, text='用户名').place(x=50, y=150)
        self.l2 = tk.Label(self.home_window, text='密码').place(x=50, y=190)
        self.var_usr_name = tk.StringVar()
        self.entry_usr_name = tk.Entry(self.home_window, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=160, y=150)
        self.var_usr_pwd = tk.StringVar()
        self.entry_usr_pwd = tk.Entry(self.home_window, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=190)

        # login and sign up button
        self.login_bt = tk.Button(self.home_window, text='登录', command=self.usr_login).place(x=170, y=230)
        self.sign_up_bt = tk.Button(self.home_window, text='注册', command=self.usr_sign_up).place(x=250, y=230)

        self.home_window.mainloop()

    def usr_login(self):

        global usr_window
        global lb

        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()

        try:
            with open('usrs_info.pickle', 'rb') as fp:
                usrs_info = pickle.load(file=fp)

        except FileNotFoundError as e:
            with open('usrs_info.pickle', 'wb') as fp:
                usrs_info = {'a': 'a'}
                # 将usrs_info封装到usrs.info.pickle文件里
                pickle.dump(obj=usrs_info, file=fp)  # obj表示要封装的对象, file表示obj要写入的对象, file必须以wb形式打开

        if usr_name == '' or usr_pwd == '':
            messagebox.showerror(title='Error', message='用户名或密码不能为空!')
        elif usr_name in usrs_info:
            if usr_pwd in usrs_info:
                # messagebox.showinfo(title='Welcome', message='欢迎')
                self.home_window.destroy()
                usr_window = tk.Tk()
                usr_window.title('User window')
                usr_window.geometry('500x300')


                lb = tk.Listbox(usr_window, width=70, height=14, font=('软体雅黑', 10))
                tk.Button(usr_window, text='开始聊天', font=('软体雅黑', 12), command=self.tuling).place(x=10, y=250)


            elif usr_pwd not in usrs_info:
                messagebox.showerror(title='Error', message='用户名或密码错误!')
        else:
            messagebox.showerror(title='Error', message='用户名或密码错误!')

    def usr_sign_up(self):
        def sign_up():
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()

            with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
            if np != npf:
                tk.messagebox.showerror(title='Error', message='输入的两次密码不一致!')
            elif nn == '' or np == '' or npf == '':
                tk.messagebox.showerror(title='Error', message='三者不能为空!')
            elif nn in exist_usr_info:
                tk.messagebox.showerror(title='Error', message='该用户名已经被注册!')
            else:
                exist_usr_info[nn] = np
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo(title='Successful', message='注册成功!')
                window_sign_up.destroy()

        def clear():
            entry_new_name.delete(first=0, last=8)
            entry_usr_pwd.delete(first=0, last=16)
            entry_usr_pwd_confirm.delete(first=0, last=16)

        window_sign_up = tk.Toplevel(self.home_window)
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

        btn_clear = tk.Button(window_sign_up, text='重新输入', command=clear)
        btn_clear.place(x=200, y=130)

    def record_wave(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def tuling(self):
        res = aipSpeech.asr(self.get_file_content(WAVE_OUTPUT_FILENAME), 'wav', 16000, {'lan': 'zh', })
        if res["err_msg"] == "success.":
            tk.Label(usr_window, text=res["result"][0], font=('软体雅黑', 12)).place(x=100, y=250)
            cont = requests.get(
                'http://www.tuling123.com/openapi/api?key=' + TULING_APIKEY + '&info=%s' % (res["result"][0],)).content
            m = json.loads(cont)
            var = m['text']
            #tk.Label(usr_window, text=var, font=('软体雅黑', 12)).pack()
            lb.insert(0, var)
            lb.pack()
            # print("iTing: ", m['text'])

    def monitor(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        rec = []
        flag = False
        print('-' * 20)
        while 1:
            data = stream.read(CHUNK)
            if flag == True:
                rec.append(data)
            frames.append(data)
            audio_data = np.fromstring(data, dtype=np.short)
            large_sample_count = np.sum(audio_data > 2000)
            temp = np.max(audio_data)

            if temp > 2000:
                flag = True

            if temp <= 2000:
                if flag == True:
                    flag = False
                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(rec))
                    wf.close()
                    rec = []
                    self.tuling()

        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    # create admin user
    with open('usrs_info.pickle', 'wb') as fp:
        usrs_info = {'admin': 'admin'}
        pickle.dump(obj=usrs_info, file=fp)

    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    iting = Iting()
