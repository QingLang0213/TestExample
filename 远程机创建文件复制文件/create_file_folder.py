#coding=utf-8
import sys,os
import time

ip_list=['192.168.219.10','192.168.219.12','192.168.219.13',\
         '192.168.219.14','192.168.219.15','192.168.219.16']


folder_list=['Home_page','New','Communicate','Life','Mediaplay','Entertain',\
             'Readnews','Trip','Study','Finance','System','Download_Count_Add',\
             'APP_Details','APP_Score','APP_TOP10','Request_Timestamp','Whether_Robot_Online',\
             'Whether_Buy_APP','Not_Buy_APP']


os.popen('md D:\\sanbo_market')

for folder in folder_list:
    os.popen('md D:\\sanbo_market\\'+folder)



#os.popen('rd/s/q D:\\sanbo_market')


file_name='D:\\sanbo_market'

for ip in ip_list:
    cmd='net use \\\\%s abc321/user:admin && echo F|xcopy %s \\\\%s\D$\\sanbo_market /E /Y /D'%(ip,file_name,ip)
    os.popen(cmd)
