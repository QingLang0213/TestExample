#encoding=utf-8
import sys
import MySQLdb
import paramiko
import hashlib
import random
import time
from sshtunnel import SSHTunnelForwarder  


unit=1000 #批量插入单元
num=100 #数值倍数(实际插入数量为num*count)


#connect SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("10.10.25.20",23,"root",",./ZxcvB123",timeout=2000)
cmd1='cd /var/www/html/sanbomarket/images/tubiao'
cmd2='cd /var/www/html/sanbomarket/images/tubiao/launcher'
cmd3='cd /var/www/html/sanbomarket/images/jietu'
cmd_list=[cmd1,cmd2,cmd3]
#新品推荐/社交通讯/生活实用/影音播放/游戏娱乐/资讯阅读/旅游出行/办公学习/投资理财/系统工具。
type_list=['new','communicate','life','mediaplay','entertain','readnews','trip','study','finance','system']

def creat_images(number):
    for i in range(3):
        for j in range(2,number+1):
            cmd=cmd_list[i]+";cp Test1.png Test%s.png"%j
            #print cmd
            ssh.exec_command(cmd)
    print 'creat images ok'


def delete_images(number):
    for i in range(3):
        for j in range(2,number+1):
            cmd=cmd_list[i]+";rm -rf Test%s.png"%(j)
            ssh.exec_command(cmd)            
    print 'delete images ok'




# connect Databse
conn = MySQLdb.connect(host='10.10.25.20',user='root',passwd='qhkj_mysql_987',port=3306,charset='utf8')
# 使用cursor()方法获取操作游标 
cur = conn.cursor()


def create_data(index1,index2):
    values=[]
    for i in range(index1,index2+1):
        app_name='TestApp'+str(i)
        status=random.choice([0,1,4294967295])
        priority=i
        price=random.randint(0,100)
        key1=key2=key3='KEY'+str(i)
        app_size=str(random.randint(0,100))+'M'
        download_count=random.randint(0,1000)
        app_version='1.1.'+str(random.randint(0,9))
        version_code=random.randint(1,1000)
        min_os_version='4.4.0'
        app_type=app_subtype=random.choice(type_list)
        app_image='/sanbomarket/images/tubiao/Test'+str(i)+'.png'  
        launcher_image='/sanbomarket/images/tubiao/launcher/Test'+str(i)+'.png'
        app_link='/download/APK/Test'+str(i)+'.apk'
        app_brief=app_news=app_name
        #生成下载路径md5值
        my_md5=hashlib.md5()
        my_md5.update(app_link)
        app_md5=my_md5.hexdigest()
        package='com.android.qihantest'+str(i)
        app_data=random.choice(['#198fcb','#FFFFFF','#FFFF00','#FF3030'])
        lang=random.choice([u'中文',u'英文',u'中英文'])
        company='Company'+str(i)
        jietu='http://10.10.25.20:22280/sanbomarket/images/jietu/Test'+str(i)+'.png;'  
        app_id=random.randint(0,10)
        one=two=three=four=five=random.randint(0,1000)
        average=round(random.uniform(0,3),1)
        fabu_time=time.strftime("%Y-%m-%d",time.localtime())
        fabu_time='2017-'+str(random.randint(1,12))+'-'+str(random.randint(1,29))
        values.append((i,app_name,status,priority,price,key1,key2,key3,app_size,download_count,\
                       app_version,version_code,min_os_version,app_type,app_subtype,app_image,\
                       launcher_image,app_link,app_brief,app_news,app_md5,package,app_data,lang,company,\
                       jietu,app_id,one,two,three,four,five,average,fabu_time))
    
    return values

def insert(name,values):
    try:  
        cur.executemany('insert into '+name+' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)
    except MySQLdb.Error, e:  
        print "Mysql Error",e
       

def insert_large(count):
    for i in range(count):
        values=create_data(i*unit+1,(i+1)*unit)
        insert('app_list',values)
        conn.commit()


def getCount(name):  
    count = 0  
    try:  
        count = cur.execute('select * from '+name)  
    except MySQLdb.Error, e:  
        count = 0  
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])  
  
    return count


def deleteAll(name):  
    try:  
        cur.execute('delete from ' + name)  
    except MySQLdb.Error, e:  
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def update(name):
    #更新真实数据，随机插入到数据库中
    real_id=[]
    cur.execute('select * from app_list')       
    result=cur.fetchall()
    conn.select_db('sanbo_market')
    
    for r in result:
        t=list(r)
        if t[25]!=None:
            if '58.60.230.238' in t[25]:
                tmp=t[25].replace('58.60.230.238:22280','10.10.25.20:80')
        t[25]=tmp
        t[32]=random.randint(1,6)
        t.pop(0)
        value=tuple(t)
        update_id=str(random.randint(1,num*unit))
        real_id.append(update_id)
        
        cur.execute('update '+name+' set app_name=%s,status=%s,priority=%s,price=%s,key1=%s,key2=%s,key3=%s,\
                    app_size=%s,download_count=%s,app_version=%s,version_code=%s,min_os_version=%s,app_type=%s,\
                    app_subtype=%s,app_image=%s,launcher_image=%s,app_link=%s,app_brief=%s,app_news=%s,app_md5=%s,\
                    package=%s,app_data=%s,lang=%s,company=%s,jietu=%s,app_id=%s,one=%s,two=%s,three=%s,four=%s,\
                    five=%s,average=%s,fabu_time=%s where id='+update_id,value)

    print real_id
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    
    conn.select_db('sanbo_market')
    deleteAll('app_list')
    #insert('app_list',create_data(1,1000))# index1--index2
    insert_large(num)#count=num*unit

    count=getCount('app_list')
    print 'app_list data count is:',count
    conn.select_db('sanbo_market_test')
    update('app_list')
    
    print 'creat images....'
    #creat_images(num*unit)
    print 'delete images....'
    #delete_images(num*unit)
    
        
    








