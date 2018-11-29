
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf-8')
import pyshark
import os
import subprocess

#主要用于输出h225及h245协议流程，并简单判断开通通道及是否存在码流。


class h225_packet(object):
    '''
    过滤出h225协议数据包
    '''
    def __init__(self, file_path = None ):
        self.file_path = file_path
        
    def __filter_h225__(self):
        file_path =  self.file_path
        cap_225 = pyshark.FileCapture(file_path,display_filter="h225")
        return cap_225
#将h225信息放入字典中，方便输出
    def get_h225_info(self):
        cap_packte = h225_packet.__filter_h225__(self)
        h225_packets = []
        for cap in cap_packte :
            h225_packet_info = {} 
            #字典需要重置
            h225_packet_info["info"] = cap.h225.h323_message_body
            h225_packet_info["ip"] = cap.ip.src
            h225_packet_info["number"]  = cap.frame_info.number
            h225_packets.append(h225_packet_info)
        return h225_packets
 
def h245_packet(pcapfile = None):
    pcapfile = pcapfile
    h245_capabilityset_packet = []
    cap_245 = pyshark.FileCapture(pcapfile,display_filter="h245")
    for cap in cap_245:
        h245_capabilityset_info = {}
        h245_capabilityset_info["pdu_type"] =  cap.h245.pdu_type
        if h245_capabilityset_info["pdu_type"] == '0' :
            h245_capabilityset_info["info"] = cap.h245.request
        elif h245_capabilityset_info["pdu_type"] == '1' :
            h245_capabilityset_info["info"] = cap.h245.response
        elif h245_capabilityset_info["pdu_type"] == '3' :
            h245_capabilityset_info["info"] = cap.h245.indication
        elif h245_capabilityset_info["pdu_type"] == '2' :
            h245_capabilityset_info["info"] = cap.h245.command
        try:
            h245_capabilityset_info['data_type'] = cap.h245.datatype
            if cap.h245.datatype == '3':
                h245_capabilityset_info["data_info"] = cap.h245.audiodata
            elif cap.h245.datatype == '2':
                h245_capabilityset_info["data_info"] = cap.h245.videodata   
        except:
            pass
        try:
            h245_capabilityset_info['time'] = cap.sniff_time
        except:
            pass 
        try:
            h245_capabilityset_info['maximumbitrate'] = cap.h245.maximumbitrate
        except:
            pass         
        try:
            h245_capabilityset_info["seq_number"] = cap.h245.forwardlogicalchannelnumber
        except:
            pass 
        try:
            h245_capabilityset_info['network'] = cap.h245.network
        except:
            pass
        try:
            h245_capabilityset_info['rtcp_network'] = cap.h245.network2
        except:
            pass        
        try:
            port = cap.h245.tsapidentifier
            if int (port)%2 == 1:
                port = str(int(port)-1) 
            else:
                port = port
            h245_capabilityset_info['open_port'] = port
        except:
            pass
        #if hasattr(cap.h245, 'payloadtype'):
            #PT = cap.h245.payloadtype
        if hasattr(cap.h245, 'dynamicrtppayloadtype'):
            PT = cap.h245.dynamicrtppayloadtype
        try:
            h245_capabilityset_info['PT'] = PT
            PT = None
        except:
            pass

        h245_capabilityset_info["ip"] =cap.ip.src
        h245_capabilityset_info["number"] = cap.frame_info.number
        h245_capabilityset_packet.append(h245_capabilityset_info)
    return h245_capabilityset_packet

#输出单条数据包的详细信息
def frame_out(frame_list = [],file_path = None):
    os.chdir('C:\\Program Files (x86)\\Wireshark\\')
    for frame_number in frame_list:
        command = tshark_path+'  -Y frame.number==' +str(frame_number)+ ' -r ' +file_path+' -V   '
        b = os.popen(command,'r',-1)
        print b.read()
        
#输出h225协议  
def h225_output():
    for  test_paket in  h225_test.get_h225_info():
        if test_paket["ip"] == src_ip:
            txt =  "                 "+h225_info_drct[test_paket["info"]]      
            txt1 = src_ip+"---------------------------------------------------------------->"+dst_ip
            ftxt.write(txt+'\n'+txt1+'\n'+'\n')
        if test_paket["ip"] == dst_ip:
            txt2 =  "                "+h225_info_drct[test_paket["info"]]+"      "      
            txt3 =dst_ip+ "<----------------------------------------------------------------" +src_ip  
            ftxt.write(txt2+'\n'+txt3+'\n'+'\n')

            
#输出h245协议 
def h245_output(packet_dict=[]):
    for  test1_paket in  packet_dict:  
        try: 
            data_type = H245_data_type_dict[test1_paket['data_type']]
            data_info = H245_data_info_dict[test1_paket['data_type']][test1_paket['data_info']]
        except:
            data_type = ''    
            data_info = ''
        try:
            number= 'seq_number:'+test1_paket['seq_number']
        except:
            number = ''
        try:
            open_port = test1_paket['open_port']
        except:
            open_port = ''
        try:
            PT = ' PT: '+test1_paket['PT']
        except:
            PT = ''
        if test1_paket["ip"] == src_ip:
            try:
                txt =  "                "+h245_pdu_type_dict[test1_paket["pdu_type"]][test1_paket["info"]]+" "+data_type+" "+data_info+number+" "+open_port+PT 
                txt1 = src_ip+"---------------------------------------------------------------->"+dst_ip
                ftxt.write(txt+'\n'+txt1+'\n'+'\n') 
            except:
                pass
        if test1_paket["ip"] == dst_ip:
            try:
                txt2 = "                "+h245_pdu_type_dict[test1_paket["pdu_type"]][test1_paket["info"]]+" "+data_type+" "+data_info+number+" "+open_port+PT
                txt3 = dst_ip+"<----------------------------------------------------------------"+src_ip
                ftxt.write(txt2+'\n'+txt3+'\n'+'\n')
            except:
                pass
            
#判断主流通道开通情况
def judge_mianVideo_port(src_ip = None,packet_dict = []):
    #判断ACK回应情况
    mianVideo_ack = []
    video_open_port_list = []
    for  test1_paket in  packet_dict:
        video_open_port = {}
        try: 
            data_type = H245_data_type_dict[test1_paket['data_type']]
            data_info = H245_data_info_dict[test1_paket['data_type']][test1_paket['data_info']]
        except:
            data_type=''       
        video_open_port['ip'] = src_ip
        if  data_type=='video' and test1_paket['ip'] == video_open_port['ip'] and test1_paket['data_info'] == '5' :
            video_open_port['number']= test1_paket['seq_number']
            video_open_port['open_port'] = test1_paket['open_port']
            video_open_port['PT'] = test1_paket['PT']
            video_open_port_list.append(video_open_port)
    for video_open_port in video_open_port_list:
        #ACK回应的标记
        ack_tag = 0
        for test2_paket in  packet_dict:
            try: 
                data_type = h245_pdu_type_dict[test2_paket["pdu_type"]][test2_paket["info"]]
            except:
                data_type=''
            try:
                seq_number = test2_paket['seq_number']
            except:
                seq_number = ''
            try:
                dst_port = test2_paket['open_port']
            except:
                dst_port = ''
            try:
                dst_PT = test2_paket['PT']
            except:
                dst_PT = 'None'   
            dst_ip = test2_paket['ip']
            src_PT = video_open_port['PT']
            src_port = video_open_port['open_port']
            src_ip = video_open_port['ip']
            if src_ip != dst_ip:
                if data_type == 'openlogicalchannelack' and seq_number == video_open_port['number'] :
                    #对端回复ACK，将标记置1
                    ack_tag = 1
                    if src_PT == dst_PT or dst_PT == None:
                        txt =  '主流视频通道开通成功。  \n主流视频码流流向：src_ip '+src_ip+' src_port: ' +src_port +' >>>>>>>>>>> dst_ip '+dst_ip+' dst_port:'+ dst_port+' PT: '+ src_PT
                    else:
                        txt = '主流视频通道开通失败！！！\n原因：PT值不一致： src_PT = '+src_PT+' dst_PT = '+str(dst_PT)
        if ack_tag==0 :
            if data_type == 'openlogicalChannelReject' and seq_number == video_open_port['number'] :
                txt ='主流通道开通失败！！！\n原因：开通通道被拒   '+ src_ip +'>>>>>>>>>>>'+dst_ip
            elif data_type == 'openlogicalChannelReject' and seq_number != video_open_port['number']:    
                txt ='主流通道开通失败！！！\n原因：ACK未回复   '+ src_ip +'>>>>>>>>>>>'+dst_ip
        return src_port,src_PT,txt
    
def judge_extendVideo_port(src_ip = None,packet_dict = []):
    #判断ACK回应情况
    mianVideo_ack = []
    video_open_port_list = []
    for  test1_paket in  packet_dict:
        video_open_port = {}
        try: 
            data_type = H245_data_type_dict[test1_paket['data_type']]
            data_info = H245_data_info_dict[test1_paket['data_type']][test1_paket['data_info']]
        except:
            data_type=''       
        video_open_port['ip'] = src_ip
        if  data_type=='video' and test1_paket['ip'] == video_open_port['ip'] and test1_paket['data_info'] == '6' :
            video_open_port['number']= test1_paket['seq_number']
            video_open_port['open_port'] = test1_paket['open_port']
            video_open_port['PT'] = test1_paket['PT']
            video_open_port_list.append(video_open_port)
    print video_open_port_list
    #ACK回应的标记
    for video_open_port in video_open_port_list:
        ack_tag = 0
        for test2_paket in  packet_dict:
            try: 
                data_type = h245_pdu_type_dict[test2_paket["pdu_type"]][test2_paket["info"]]
            except:
                data_type=''
            try:
                seq_number = test2_paket['seq_number']
            except:
                seq_number = ''
            try:
                dst_port = test2_paket['open_port']
            except:
                dst_port = ''
            try:
                dst_PT = test2_paket['PT']
            except:
                dst_PT = 'None' 
            dst_ip = test2_paket['ip']
            src_PT = video_open_port['PT']
            src_port = video_open_port['open_port']
            src_ip = video_open_port['ip']
            if  dst_ip != src_ip:
                if data_type == 'openlogicalchannelack' and seq_number == video_open_port['number'] :
                    #对端回复ACK，将标记置1
                    ack_tag = 1
                    if dst_PT == src_PT or dst_PT == None:
                        txt =  '辅流视频通道开通成功。  \n辅流视频码流流向：src_ip '+src_ip+' src_port: ' +src_port +' >>>>>>>>>>> dst_ip '+dst_ip+' dst_port:'+ dst_port+' PT: '+ str(src_PT)
                    else:
                        txt = '辅流视频通道开通失败！！！\n原因：PT值不一致： src_PT = '+src_PT+' dst_PT = '+str(dst_PT)
        
            if ack_tag==0 and dst_ip != src_ip: 
                if data_type == 'openlogicalChannelReject' and seq_number == video_open_port['number'] :
                    txt ='辅流通道开通失败！！！\n原因：开通通道被拒   '+ src_ip +'>>>>>>>>>>>'+dst_ip
                elif data_type == 'openlogicalChannelReject' and seq_number != video_open_port['number']:  
                    txt ='辅流通道开通失败！！！\n原因：ACK未回复   '+ src_ip +'>>>>>>>>>>>'+dst_ip
        return src_port,src_PT,txt

#判断音频通道开通情况
def judge_mianAudio_port(src_ip = None,packet_dict = []):
    audio_open_port_list =[]
    for  test1_paket in  packet_dict:
        audio_open_port = {}
        try: 
            data_type = H245_data_type_dict[test1_paket['data_type']]
            data_info = H245_data_info_dict[test1_paket['data_type']][test1_paket['data_info']]
        except:
            data_type='' 
        audio_open_port['ip'] = src_ip
        if  data_type=='audio' and test1_paket['ip'] == audio_open_port['ip']:
            audio_open_port['number']= test1_paket['seq_number']
            audio_open_port['open_port'] = test1_paket['open_port']
            audio_open_port['PT'] = test1_paket['PT']
            audio_open_port_list.append(audio_open_port)
    ack_tag = 0
    for audio_open_port in audio_open_port_list:
        for test2_paket in  packet_dict:
            try: 
                data_type = h245_pdu_type_dict[test2_paket["pdu_type"]][test2_paket["info"]]
            except:
                data_type=''
            try:
                seq_number = test2_paket['seq_number']
            except:
                seq_number = ''
            try:
                dst_port = test2_paket['open_port']
            except:
                dst_port = ''
            try:
                dst_PT = test2_paket['PT']
            except:
                dst_PT = 'None'  
            dst_ip = test2_paket['ip']
            src_port = audio_open_port['open_port']
            src_PT =  audio_open_port['PT'] 
            src_ip = audio_open_port['ip']
            if audio_open_port['ip'] != dst_ip:
                if data_type == 'openlogicalchannelack' and seq_number == audio_open_port['number']:
                    ack_tag = 1
                    if dst_PT == src_PT or  dst_PT == None :
                        txt = '音频通道开通成功。 \n音频码流流向： src_ip: '+src_ip+' src_port: ' +src_port +' >>>>>>>>>>> dst_ip: '+dst_ip+' dst_port:'+ dst_port+' PT: '+ str(src_PT)
                    else:
                        txt = '音频通道开通失败！！！\n原因：PT值不一致：src_PT = '+str(src_PT)+' dst_PT = '+str(dst_PT)
        if ack_tag==0:
            if data_type == 'openlogicalChannelReject' and seq_number == audio_open_port['number'] :
                txt ='音频通道开通失败！！！\n原因：开通通道被拒   '+ src_ip +'>>>>>>>>>>>'+dst_ip
            elif data_type == 'openlogicalChannelReject' and seq_number != audio_open_port['number']:  
                txt ='音频通道开通失败！！！\n原因：ACK未回复   '+ src_ip +'>>>>>>>>>>>'+dst_ip
        return src_port,src_PT,txt

#判断是通道开通之后是否存在该条码流
def judge_bit_stream(src_ip=None,src_port=None):
    display = 'ip.src=='+str(src_ip)+'&&udp.srcport=='+str(src_port)
    cap = pyshark.FileCapture(pcapfile,display_filter=display)

    num_packat= 0
    for udp_pcaket in cap:
        num_packat = num_packat+1
        break
    if num_packat>=1:
        txt = src_ip+ ' 发送码流成功。'+'\n'+'\n'
    else :
        txt = src_ip+ ' 发送码流失败！！！'+'\n'+'\n'
    return txt


#码流判断输出
def mianVideo_out(src_ip=None,packet_dict=[]):
    src_port,src_PT,txt = judge_mianVideo_port(src_ip=src_ip,packet_dict=packet_dict)
    txt1 = judge_bit_stream(src_ip=src_ip, src_port=src_port)
    ftxt.write(txt+'\n'+txt1)    
def extendVideo_out(src_ip=None,packet_dict=[]):
    src_port,src_PT,txt = judge_extendVideo_port(src_ip=src_ip,packet_dict=packet_dict)
    txt1 = judge_bit_stream(src_ip=src_ip, src_port=src_port)
    ftxt.write(txt+'\n'+txt1)    
def audio_out(src_ip=None,packet_dict=[]):
    src_port,src_PT,txt = judge_mianAudio_port(src_ip=src_ip,packet_dict=packet_dict)
    txt1 = judge_bit_stream(src_ip=src_ip, src_port=src_port)
    ftxt.write(txt+'\n'+txt1)  
    

#返回数据包号给frame_out()函数，返回terminalcapabilityset的数据包序号，用于Tshark查看数据包的详细内容。
def return_frame(packet_dict=None):
    terminalcapabilityset_framelist = []
    for packet in packet_dict:
        try: 
            data_type = h245_pdu_type_dict[packet["pdu_type"]][packet["info"]]
        except:
            data_type=''
        if data_type == 'terminalcapabilityset':
            frame_number = packet['number']
            terminalcapabilityset_framelist.append(frame_number)
    return terminalcapabilityset_framelist


if __name__ == '__main__':
    
    tshark_path ='tshark.exe'
    #科达定义的 PT值对应的音视频协议
    #audio_PT_dict = {'98':'G7221C','127':'opus','8':'G711A ','0':'G711U ','99':'G719 ','9':'G722','15':'G728 ','18':'G729','96':'MP3 ','102':'AAC-LC','103':'AAC-LD'}
    #video_PT_dict = {'106':'h.264','108':'h.265 ','97':'MPEG-4 ','34':'h.263','31':'h.261'}
    
    #Wireshark中部分字段输出的数字值对应的字符串含义
    H245_audio_info_dict = {"0":"understand","20":"generic"}
    H245_video_info_dict = {"5":"mainvideo",'6':'extendvideo'}
    H245_data_info_dict = {"2":H245_video_info_dict,"3":H245_audio_info_dict,"4":"data"}
    
    h225_info_drct = {"0":"setup","1":"callprocceding","2":"connect","3":"alftering","5":"releseCompelet",'6':'facility'}
    H245_data_type_dict = {"2":"video","3":"audio","4":"data"}
    
    h245_request_dict = {"0":"","1":"masterSlaveDetermination","2":"terminalcapabilityset","3":"openlogicalchannel"}
    h245_response_dict = {'3':'terminalcapabilitysetAck','1':'masterSlaveDeterminationAck','7':'closelogicalchannel','16':'roundTripDelayResponse',"5":"openlogicalchannelack",'6':'openlogicalChannelReject'}
    h245_indication_dict = {'13':'userInput','21':'flowcontrolIndication'}
    h245_conmand_dict = {'4':'flowcontrolCommand','6':'miscellaneousIndication'}
    
    h245_pdu_type_dict = {"0":h245_request_dict, "1":h245_response_dict,"2":h245_conmand_dict,"3":h245_indication_dict}
    
    ftxt = open('result.txt','w')
    #数据包路径输入
    pcapfile = r'D:\wyc\suju\5.5.pcap'
    #输入主呼与被呼ip
    src_ip = "172.16.178.15"
    dst_ip = "172.16.178.121"
    
    #输出h.225协议,呼叫流程
    h225_test= h225_packet(file_path = pcapfile)
    h225_output()
    
    #输出h.245协议数据包的列表
    packet_dict = h245_packet(pcapfile = pcapfile)
    h245_output(packet_dict=packet_dict)
    
    #主流视频判断输出
    mianVideo_out(src_ip=src_ip,packet_dict=packet_dict)
    mianVideo_out(src_ip=dst_ip,packet_dict=packet_dict)
    
    #辅流判断输出
    #extendVideo_out(src_ip=src_ip,packet_dict=packet_dict)
    #extendVideo_out(src_ip=dst_ip,packet_dict=packet_dict) 
    
    #音频判断输出
    #audio_out(src_ip=src_ip,packet_dict=packet_dict)
    #audio_out(src_ip=dst_ip,packet_dict=packet_dict)
    
    #输出terminalcapabilityset数据包详细内容
    #frame_list = return_frame(packet_dict=packet_dict)
    #frame_out(frame_list =frame_list,file_path = pcapfile)
