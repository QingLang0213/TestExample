#coding=utf-8
import os,sys, subprocess
import random
import time
import MySQLdb

txt_number=5#设置生成txt文本数量
number= 10000#设置每个txt文本包含的账户数量
#设置远程机IP地址，也可以添加本机IP地址
ip_list=['192.168.219.10','192.168.219.12','192.168.219.13','192.168.219.14','192.168.219.15','192.168.219.16']

dev=['e1a33ecbf7e22d3bf536f3e78e','e2e32d7844980d01687d88c1b3','e31f6e5de66313bea828295177','e418ebaa15fb428d440e14260b'\
    ,'e5e18155e7ed676c30b0d2194a','e6e9b502af3d77104248fc23b8','e7d0c6bed956c399a41670b877']

dev_list=[]
os.popen('md D:\\csv_data\\')
def create_device():
    for t in range(txt_number):
        ip=ip_list[t]
        filename='D:\\csv_data\\dev_did%s.txt'%(t+1)
        cmd='net use \\\\%s abc321/user:admin && echo F|xcopy %s \\\\%s\D$\\csv_data\\dev_did.txt /E /Y /D'%(ip,filename,ip)
        f=open(filename,'w')
        for i in range(number):
            devid=dev[t]+str(100000+i+1)
            dev_list.append(devid)
            did=i+1
            dev_did=devid+','+str(did)+'\n'
            f.write(dev_did)
        f.close()
        os.popen(cmd)
        os.popen('copy ')
        print u'账户写入完成,位置%s\\D:\\csv_data\\dev_did.txt'%ip
    os.popen('copy D:\\csv_data\\dev_did1.txt D:\\csv_data\\dev_did.txt')
    print 'copy D:\\csv_data\\dev_did1.txt to D:\\csv_data\\dev_did.txt'
   
def create_card():
    values=[]
    # connect Databse
    conn = MySQLdb.connect(host='10.10.25.20',user='root',passwd='qhkj_mysql_987',port=3306,charset='utf8')
    # 使用cursor()方法获取操作游标
    cur = conn.cursor()
    conn.select_db('sanbo_market')
    cur.execute('delete from robot_token_list')
    print 'delete table robot_token_list'

    cur.execute('delete from devid_card_list')
    print 'create card to device'
    length=number*txt_number
    for i in range(length):
        uid=i+1
        devid=dev_list[i]
        card='qihantest'+str(1000000+i+1)
        download_package=None
        status=0
        used_time=None
        values.append((uid,devid,card,download_package,status,used_time))
    cur.executemany('insert into devid_card_list values(%s,%s,%s,%s,%s,%s)',values)  
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_device()
    create_card()

