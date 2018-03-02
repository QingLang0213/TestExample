#coding=utf-8

import redis
import threading
from Tkinter import *
from Geohash import geohash
from math import radians, cos, sin, asin, sqrt



def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000  


#纬线 latitude 经度 longitude


class Speedrop(threading.Thread):

    
    def __init__(self,uid,run_type,app):
        threading.Thread.__init__(self)
        self.uid=uid
        self.app=app
        self.type=run_type
        self.gsh_uid_list=[]
        self.ip_uid_list=[]
        self.pc_uid_list=[]
        

    def get_ip_info(self):
        user_ip=self.r.hget('user_status:'+self.uid,'user_ip')
        pc_wlan_ip=self.r.hget('user_status:'+self.uid,'pc_wlan_ip')
        self.app.text_msglist.insert(END,u'手机端IP地址:'+user_ip+'\n','blue')
        self.app.text_msglist.insert(END,u'PC端IP地址:'+pc_wlan_ip+'\n','blue')
 
    def get_gps_info(self):
        gsh=self.r.get('geohash_uid:'+self.uid)
        if gsh!=None:
            my_lats_lons=geohash.decode_exactly(gsh)
            my_lats=float(my_lats_lons[0])
            my_lons=float(my_lats_lons[1])
            self.app.text_msglist.insert(END,self.uid+u'geohash位置:'+gsh+'\n','blue')
            self.app.text_msglist.insert(END,self.uid+u'纬度:'+str(my_lats)+u',经度:'+str(my_lons)+'\n','blue')
        else:
           self.app.text_msglist.insert(END,self.uid+u'geohash位置为空'+'\n','blue')
            
    def get_gps_uid(self):
        self.gsh_uid_list[:]=[]
        gsh=self.r.get('geohash_uid:'+self.uid)
        if gsh==None:
            self.app.text_msglist.insert(END,self.uid+u'geohash位置为空'+'\n','blue')
            return 0
        
        my_lats_lons=geohash.decode_exactly(gsh)
        my_lats=float(my_lats_lons[0])
        my_lons=float(my_lats_lons[1])
        self.app.text_msglist.insert(END,self.uid+u'geohash位置:'+gsh+'\n','blue')

        geo_2000=gsh[:5]
        gh_list=self.r.keys('*%s*'%geo_2000)
        for gh in gh_list:
            fuid_list=self.r.smembers(gh)
            gh=gh.split(':')[1]
            lats_lons=geohash.decode(gh)
            lats=float(lats_lons[0])
            lons=float(lats_lons[1])
            dis=haversine(lons,lats,my_lons,my_lats)
            dis=round(dis,6)
            for fuid in fuid_list:
                self.gsh_uid_list.append(fuid)
                self.app.text_msglist.insert(END,'uid:'+fuid+u'  距离:'+str(dis)+'\n','green')  
        self.app.text_msglist.insert(END,u'手机端2000m范围内附近的人:%s\n'%len(self.gsh_uid_list),'blue')
        self.display(self.gsh_uid_list)
        

        
    def get_ip(self):
        self.ip_uid_list[:]=[]
        user_ip=self.r.hget('user_status:'+self.uid,'user_ip')
        self.ip_uid_list=list(self.r.smembers('spee_drop_ip:'+user_ip))
        self.app.text_msglist.insert(END,u'手机端相同IP附近的人:%s\n'%len(self.ip_uid_list),'blue')
        self.display(self.ip_uid_list)
       
        
    

    def get_pc(self):
        self.pc_uid_list[:]=[]
        pc_wlan_ip=self.r.hget('user_status:'+self.uid,'pc_wlan_ip')
        self.pc_uid_list=list(self.r.smembers('spee_drop_ip:'+pc_wlan_ip))
        self.app.text_msglist.insert(END,u'pc端相同IP下附近的人:%s\n'%len(self.pc_uid_list),'blue')
        self.display(self.pc_uid_list)


    def get_phone(self):
        self.get_gps_uid()
        self.get_ip()
        a=set(self.gsh_uid_list)
        b=set(self.ip_uid_list)
        c=list(a | b)
        self.app.text_msglist.insert(END,u'手机端GPS+IP合并后人数:%s\n'%len(c),'blue')
        self.display(c)
        

    def display(self,fu_list):
        for fu in fu_list:
            self.app.text_msglist.insert(END,fu+', ','green')
        self.app.text_msglist.insert(END,'\n\n')
        self.app.text_msglist.see(END)
        
        
    def run(self):
        self.r=redis.StrictRedis(host='58.60.230.238',port=6278,db=1,password='qhkj_redis_987',encoding='utf-8',socket_timeout=5)
        if self.type==1:
            self.get_ip_info()
        elif self.type==2:
            self.get_gps_info()
        elif self.type==3:
            self.get_phone()
        else:
            self.get_pc()
        





