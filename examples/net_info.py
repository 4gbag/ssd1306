#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#

import os
import sys
import time
if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

# import psutil

from demo_opts import device
from oled.render import canvas
from PIL import ImageFont

# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


def get_all_eth_traffic_info():
    '''
    获取所有网卡流量信息，该字段没有进行处理
    :return:
    '''
    with open("/proc/net/dev", "r") as f:
        return f.read().replace(":", "")

def get_all_eth_traffic_dict():
    '''
    获取所有网卡流量信息，返回json格式: [{"eth":"eth0","RX":"783333","TX":"17833344"} RX 接收， TX 发送]
    :return:
    '''
    import time
    traffic_info = get_all_eth_traffic_info().split('\n')
    # print(len(traffic_info))
    result = {}
    for eth_traffic in traffic_info:
        _t = eth_traffic.split(' ')
        _t = [x for x in _t if x != '']
        # 数据基于len=17 获取
        timestamp = int(time.time())
        if len(_t) != 17:
            continue
        result[_t[0]] = {"eth":_t[0], "RX":_t[1], "TX":_t[9], "timestamp": timestamp}

    # print(result)
    return result

def network(ifaces):
    if len(ifaces) == 0:
        return "no ifaces"
    # 获取开始流量
    traffic_info_start = get_all_eth_traffic_dict()
    time.sleep(1)
    # 获取结束流量，结束-开始=1秒内的流量，要精确的话，两个线程，一个线程获取，一个线程计算，或者协程,一个线程也行？
    traffic_info_end = get_all_eth_traffic_dict()



    for i in ifaces:
        # print('I='+i)
        traffic = traffic_info[i]
        print (traffic)
    # with open("/proc/net/dev", "r") as f:
    #     net_info = f.read()
    #     print(net_info)
    #     return f.read()
    # print("/usr/bin/traffic_monitor.sh %s" % iface)
    # os.system("/usr/bin/traffic_monitor.sh %s".format(iface))
    # with open("/tmp/tmp/%s" % iface, 'r') as f:
    #     return f.read()
    # stat = psutil.net_io_counters(pernic=True)[iface]
    # return "%s: Tx%s, Rx%s" % \
    #        (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))



def stats(oled):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 10)

    with canvas(oled) as draw:
        # draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        # if device.height >= 32:
        #     draw.text((0, 14), mem_usage(), font=font2, fill="white")
        #
        # if device.height >= 64:
        #     draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
        try:
            draw.text((0, 0), network("wlan0"), font=font2, fill="white")
            # draw.text((0, 0), "The python psutil library\n"
            #                   "(http://code.google.com/p/p\n"
            #                   "sutil/) packaged for OpenWRT.", font=font2, fill="white")
        except KeyError:
            # no wifi enabled/available
            pass


def main():
    network(["wlan0"])
    # while True:
    #     stats(device)
    #     time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
