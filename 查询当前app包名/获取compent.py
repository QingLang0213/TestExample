#coding=utf-8
import os
import re


#通过adb shell dumpsys命令获得，这也是我准备主要介绍的方法
#我们使用windows选项，执行adb shell dumpsys window w，在输出结果中我们可以找到打开的当前应用的component，
#而component中总是含有斜杠“/”，所以我们可以使用这个命令得到输出（进入系统设置应用），
#adb shell dumpsys window w | findstr \/ ，需要转义斜杠“/”,在linux下需要把findstr换成grep，
#此时输出的内容还是会比较多，不容易查找，再结果分析，发现可以再查找字符串“name=”,
#接下来重新执行adb shell dumpsys window w | findstr \/ | findstr name= ，会输出下面的结果：
'''
C:\Users\admin>adb shell dumpsys window w | findstr \/ | findstr name=
      mSurface=Surface(name=com.samsung.android.app.cocktailbarservice/com.samsung.android.app.cockt
ailbarservice.CocktailBarService)
      mSurface=Surface(name=com.ss.android.article.news/com.ss.android.article.news.activity.MainAct
ivity)
个别机型会输出两个name，取最后一个[-1]
'''

def getFocusedPackageAndActivity():

        pattern = re.compile(r"[a-zA-Z0-9\.]+/[a-zA-Z0-9\.]+")
        out = os.popen("adb shell dumpsys window w | findstr \/ | findstr name=").read()
        list = pattern.findall(out)
        component = list[-1]

        return component

print getFocusedPackageAndActivity()

