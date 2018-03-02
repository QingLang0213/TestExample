#coding=utf-8
from Tkinter import *
import speed
import traceback


class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.root=master
        self.root.title('speed')
        self.root.geometry('720x460')
        self.root.resizable(0, 0)  # 禁止调整窗口大小
        self.root.protocol("WM_DELETE_WINDOW",self.close)


    def creatWidgets(self):
        frame_left = Frame(self.root, width=360, height=460, bg='#C1CDCD')
        frame_right = Frame(self.root, width=360, height=460, bg='#C1CDCD')
        frame_left.grid_propagate(0)
        frame_right.propagate(0)
        frame_right.grid_propagate(0)
        frame_left.grid(row=0, column=0)
        frame_right.grid(row=0, column=1)
            
        self.v1 = StringVar()
        self.v2 = StringVar()
            
            
        Label(frame_left, text=u"输入qlink账号或uid:", bg='#C1CDCD').grid(row=0, column=0, pady=10, padx=5)
        Entry(frame_left, width=25,textvariable=self.v1).grid(row=0,column=1,columnspan=2,padx=2,pady=10,ipady=2,sticky=W)

        self.b1=Button(frame_left, text=u"查询当前账号IP",command=self.test1, bg='#C1CDCD')
        self.b1.grid(row=1,rowspan=2,column=1,padx=5,pady=20)
        self.b2=Button(frame_left, text=u"查询当前账号GPS",command=self.test2, bg='#C1CDCD')
        self.b2.grid(row=3,column=1,padx=5,pady=20)    
        self.b1=Button(frame_left, text=u"查询手机端附近的人",command=self.test3, bg='#C1CDCD')
        self.b1.grid(row=4,column=1,padx=5,pady=20)
        self.b2=Button(frame_left, text=u"查询PC端附近的人",command=self.test4, bg='#C1CDCD')
        self.b2.grid(row=5,column=1,padx=5,pady=20)

            
           
            
        #Scrollbar
        scrollbar = Scrollbar(frame_right,bg='#C1CDCD')
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_msglist = Text(frame_right, yscrollcommand=scrollbar.set,bg='#C1CDCD')
        self.text_msglist.pack(side=RIGHT, fill=BOTH)
        scrollbar['command'] = self.text_msglist.yview
        self.text_msglist.tag_config('green', foreground='#008B00')
        self.text_msglist.tag_config('blue', foreground='#0000FF')
        self.text_msglist.tag_config('red', foreground='#FF3030')


    def test1(self):
        uid=self.v1.get()
        sp=speed.Speedrop(uid,1,app)
        sp.setDaemon(True)
        sp.start()
        
    def test2(self):
        uid=self.v1.get()
        sp=speed.Speedrop(uid,2,app)
        sp.setDaemon(True)
        sp.start()
        
    def test3(self):
        uid=self.v1.get()
        sp=speed.Speedrop(uid,3,app)
        sp.setDaemon(True)
        sp.start()
        
    def test4(self):
        uid=self.v1.get()
        sp=speed.Speedrop(uid,4,app)
        sp.setDaemon(True)
        sp.start()
        
    def close(self):
        self.root.quit()
        self.root.destroy()

            
if __name__ == "__main__":
    try:
        root=Tk()
        app=Application(root)
        app.creatWidgets()
        app.mainloop()
    except Exception,e:
        app.text_msglist.insert(END,traceback.format_exc(),'red')
  



            
