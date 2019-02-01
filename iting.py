#!/usr/bin/python3

import os
import re
import sys
import json
import time
import urllib
import base64
import requests
import tempfile
import urllib.request
import speech_recognition
from bs4 import BeautifulSoup

r = speech_recognition.Recognizer()
tuling_apikey = "d66e74574d564824a05463341a124829"

class iTing:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.request.urlopen(token_url).read()
        token_data = json.loads(r_str)
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)

        # voice_data = urllib.request.urlopen(get_url).read()
        voice_data = requests.get(get_url).content
        # 3.处理返回数据
        voice_fp = open(filename,'wb+')
        voice_fp.write(voice_data)
        voice_fp.close()
        pass

    def getText(self, filename):
        # 2. 向Rest接口提交数据
        data = {}
        # 语音的一些参数
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read()
        # 3.处理返回数据
        return json.loads(r_data)['result']

    def lisenTo(self):
        with speech_recognition.Microphone() as sorce:
            r.adjust_for_ambient_noise(sorce)
            audio = r.listen(sorce)
            return r.recognize_google(audio, language="zh-TW")

    def speak(self, sentence):
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            bdr.getVoice(text=sentence, filename='{}.wav'.format(fp.name))
            print('回答：' + sentence)
            os.system("start {}.wav".format(fp.name))

    def get_score(self, textUserID, textPasswd):
        login_URL = 'http://222.30.63.15/NKEMIS/SystemLogin.aspx'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        response = requests.get(login_URL, headers=headers)
        bsObj = BeautifulSoup(response.text, 'lxml')
        __VIEWSTATE = bsObj.find('input').attrs['value']
        __EVENTVALIDATION = bsObj.find('input', id='__EVENTVALIDATION').attrs['value']
        from_data = {
            "__VIEWSTATE": __VIEWSTATE,
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "txtUserID": textUserID,
            "txtPasswd": textPasswd,
            "ImageButton1.x": 1,
            "ImageButton1.y": 1,
        }
        session = requests.session()
        session.post(login_URL, data=from_data)
        score_url = "http://222.30.63.15/nkemis/Student/ScoreQuery.aspx"
        score_html = session.get(score_url)

        # 课程名称
        title = re.compile('<tr align="center">.*?<td align="left">.*?<a.*?>(.*?)</a>', re.S)
        title_items = re.findall(title, score_html.text)

        # 总成绩
        score = re.compile(
            '<tr align="center">.*?<td align="left">.*?<a.*?>.*?</a>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>(.*?)<td>',
            re.S)
        score_items = re.findall(score, score_html.text)


        score_list = []
        for title_item, score_item in zip(title_items, score_items):
            score_list.append(title_item.replace("\r", "").replace("\t", "").replace("\n", "") + score_item.replace("</td>", ""))

        return score_list
            
    def tuling(self, info):
        url = 'http://www.tuling123.com/openapi/api?key=' + tuling_apikey + '&info=' + info
        res = requests.get(url)
        res.encoding = 'utf-8'
        jd = json.loads(res.text)
        print('iTing: '+jd['text'])

if __name__ == "__main__":
    # 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的key和secert
    api_key = "R93YzrozkK8VLeACtVGm4wMc" 
    api_secert = "jGHEw8v29Tr5UFuQTokQLKMI8yTXPpMM"
    # 初始化
    bdr = iTing("iTing v0.0.1", api_key, api_secert)
    
    while True:
        print("----请说话----")
        lisen = bdr.lisenTo()
        print('我:' + lisen)
        bdr.tuling(lisen)
        time.sleep(3)
        if (lisen == '再见'):
            sys.exit()

