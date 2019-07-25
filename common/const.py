# coding=utf-8
from django.db import connection
from django.utils.translation import ugettext_lazy as _
__author__ = 'June'

DB_CHAR_CODE_2 = 2
DB_CHAR_CODE_4 = 4
DB_CHAR_CODE_6 = 6
DB_CHAR_CODE_8 = 8
DB_CHAR_CODE_10 = 10

DB_CHAR_NAME_20 = 20
DB_CHAR_NAME_40 = 40
DB_CHAR_NAME_60 = 60
DB_CHAR_NAME_80 = 80
DB_CHAR_NAME_120 = 120
DB_CHAR_NAME_200 = 200


STATUS_ON_OFF = (
    (0,_('OFF')),
    (0,_('ON')),
)

import itchat
#itchat.auto_login(hotReload=True)
def getMsgFormat(user, host, command_no, message):
    import random
    return "1:%d:%s:%s:%d:%s" % (

        random.randint(1, 1000),
        user,
        host,
        command_no,
        message
    )

def get_value_list(group):
    """
    获取值列表信息
    """
    if group:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT code,name FROM basedata_valuelistitem WHERE group_code=%s AND status=1',[group])
            rows = cursor.fetchall()
            return tuple([(code,name) for code,name in rows])
        except Exception as e:
            return None
    else:
        return None

def send_ipmsg(name):
    import xlrd
    import socket
    workbook = xlrd.open_workbook('static/wechat.xlsx')
    table = workbook.sheets()[0]
    ip = None
    for i in range(table.nrows):
        if name == table.row_values(i)[0]:
            ip = table.row_values(i)[2]
    if ip is None:
        print("ip获取失败")
    command_no = 32
    source_host = 'localhost'

    # Set ipaddress
    ipaddress = ip

    # Set port
    port = 2425

    # Set source_user
    source_user = b'admin'

    # Set message
    message = b'192.168.1.15'

    # Send message
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.sendto(getMsgFormat(source_user, source_host, command_no, message).encode(encoding='utf-8'), (ipaddress, port))
    except Exception:
        print('Sending error')

def send_wechat(name,msg):

    import xlrd
    workbook = xlrd.open_workbook('static/wechat.xlsx')
    table = workbook.sheets()[0]
    for i in range(table.nrows):
        if name == table.row_values(i)[0]:
            itchat.get_friends(update=True)
            tosend = itchat.search_friends(nickName=table.row_values(i)[1])
            if len(tosend) == 0:
                print('微信名' + table.row_values(i)[1] + '不存在')
            else:
                tosend[0].send(msg)







