import sys,os
import MySQLdb
import random
import time
import hashlib

txt_number=5#设置生成txt文本数量

ip_list=['192.168.219.10','192.168.219.12','192.168.219.13','192.168.219.14','192.168.219.15','192.168.219.16']

devid_list=[]
did_list=[]
token_list=[]
dev_card_dict={}
# connect Databse
conn = MySQLdb.connect(host='10.10.25.20',user='root',passwd='qhkj_mysql_987',port=3306,charset='utf8')
# 使用cursor()方法获取操作游标
cur = conn.cursor()
conn.select_db('sanbo_market')
cur.execute('select * from robot_token_list')       
result=cur.fetchall()
cur.execute('select * from devid_card_list')
dev_card_list=cur.fetchall()
for dev_card in dev_card_list:
        dev_card_dict[dev_card[1]]=dev_card[2]

conn.commit()
cur.close()
conn.close()

for r in result:
        devid_list.append(r[1])
        did_list.append(r[2])
        token_list.append(r[4])

num=len(devid_list)/txt_number
    
for t in range(txt_number):
    ip=ip_list[t]
    filename='D:\\csv_data\\token%s.txt'%(t+1)
    cmd='net use \\\\%s abc321/user:admin && echo F|xcopy %s \\\\%s\D$\\csv_data\\token.txt /E /Y /D'%(ip,filename,ip)
    f=open(filename,'w')
    for i in range(num*t,(t+1)*num):
        package='com.android.qihantest'+str(i+1)
        app_name='TestApp'+str(i+1)
        card=dev_card_dict[devid_list[i]]
        if token_list[i]==None:continue
        token=str(did_list[i])+','+devid_list[i]+','+token_list[i]+','+package+','+card+','+app_name+'\n'
        f.write(token)
    f.close()
    os.popen(cmd)
    print u'账户写入完成,位置%s\\D:\\token.txt'%ip
os.popen('copy D:\\csv_data\\token1.txt D:\\csv_data\\token.txt')
print 'copy D:\\csv_data\\token1.txt to D:\\csv_data\\token.txt'






    


