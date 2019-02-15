#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-2-15 下午10:32
# @Author  : Jie
# @Site    : https://www.jianshu.com/u/ce9c158c2fa4
# @File    : config.py
# @Software: PyCharm Community Edition

import pyaudio
APP_ID = '15179831'
API_KEY = 'R93YzrozkK8VLeACtVGm4wMc'
SECRET_KEY = 'jGHEw8v29Tr5UFuQTokQLKMI8yTXPpMM'
TULING_APIKEY = "d66e74574d564824a05463341a124829"

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "audio.wav"