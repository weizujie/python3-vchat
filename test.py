# -*- coding: utf-8 -*-
import os
import wave
import json
import requests
import numpy as np
from aip import AipSpeech
from config import *

class iTing:
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
        res = aipSpeech.asr(iting.get_file_content(WAVE_OUTPUT_FILENAME), 'wav', 16000, {'lan': 'zh', })
        if res["err_msg"] == "success.":
            print('   我:', res["result"][0])

            cont = requests.get(
                'http://www.tuling123.com/openapi/api?key=' + TULING_APIKEY + '&info=%s' % (res["result"][0],)).content
            m = json.loads(cont)
            print("iTing: ", m['text'])
            print('-'*20)
    def Monitor(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        rec = []
        flag = False
        print('-'*20)
        while (True):
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
                    iting.tuling()

        stream.stop_stream()
        stream.close()
        p.terminate()



if __name__ == "__main__":

    # 初始化
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    iting = iTing()


    # 启动 iting
    iting.Monitor()

