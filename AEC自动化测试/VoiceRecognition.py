#coding=utf-8 
from aip import AipSpeech
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#""" 你的 APPID AK SK """
APP_ID = '10627199'
API_KEY = 'P7Z7arYUxSNkl0zrkQomeL3W'
SECRET_KEY = 'ebAoPIkM9yg01uUjig3wLYOvvYSy3PeD'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def VoiceRecognition(filepath):
    Voiceresult = client.asr(get_file_content(filepath), 'wav', 8000, {
        'lan': 'zh',})
    Voiceresult_json = json.dumps(Voiceresult)
    text = json.loads(Voiceresult_json)
    if text.has_key('result'):
        s = text['result'][0] #取result后字段，表示识别的字
        ResultStr = s.decode('utf-8')
        ResultStr = ResultStr.replace('，','').replace('！','').replace('？','')
        ResultStrLen=len(ResultStr)
        return (ResultStr,ResultStrLen)
    else:
        ResultStr = 'Recognition Failed! '
        ResultStrLen = 0
        return (ResultStr,ResultStrLen)
if __name__ == "__main__":
    (ResultStr,ResultStrLen) = VoiceRecognition(r"D:\AEC_sop\CapAudio_all\Cap_Audio_file1\2018_01_23_20_04_00\capaec8.pcm")
    print ResultStr
    print ResultStrLen


