import requests
from time import *
#from easygui import *
import json
from tkinter import *
import gzip
from PIL import Image,ImageTk
import myKey
import webbrowser

#进行初始化

def get_location_by_ip():#通过ip接口获取大致位置
    #try:
    global city
    global lat
    global lon
        # 免费IP定位接口
        #resp = requests.get("http://ip-api.com/json/")
    resp = requests.get("https://myip.ipip.net/json")
    print(resp.text)
    data = resp.json()
        
    if data["ret"] == "ok":
            #lat = float(f"{data["lat"]:.2f}")   # 纬度
            #lon = float(f"{data["lon"]:.2f}")   # 经度
        city = data["data"]["location"][2] # 城市
        print(f"城市：{city}")
        #print(f"纬度：{lat}")
            #print(f"经度：{lon}")
            #return lat, lon
    else:
        print("获取失败")
    #except:
        #print("网络错误")


get_location_by_ip()
#placelat=str(lon)+','+str(lat)

#定义天气获取接口
headers={'X-QW-Api-Key':myKey.KEY,"Accept-Encoding": "gzip"}
geoapi='https://np6apvcawc.re.qweatherapi.com/geo/v2/city/lookup'
now='https://np6apvcawc.re.qweatherapi.com/v7/weather/now'
indice='https://np6apvcawc.re.qweatherapi.com/v7/indices/1d'
future='https://np6apvcawc.re.qweatherapi.com/v7/weather/'
paramsgeo={'location':city}
placenow=requests.get(geoapi,params=paramsgeo,headers=headers)#立即获取所在城市天气
print(placenow.text)
idnow=json.loads(placenow.text)

#错误页面
if placenow.status_code!=200:
    def more():
        webbrowser.open(idnow["error"]["type"])
    error=Tk()
    error.geometry('800x500+100+100')
    error.title('发生错误')
    Label(error,text='发生错误。请向您的管理员求助。以下信息可能可以帮到您。').pack()
    Label(error,text='状态码:'+str(placenow.status_code)).pack()
    Label(error,text='返回信息:'+idnow["error"]["detail"]).pack()
    Button(error,text='前往详情页面查看详情',command=more).pack()
    error.mainloop()

citynow=idnow["location"][0]["name"]
idnow=idnow["location"][0]["id"]
print(idnow)



paramsnow={'location':idnow}
paramsindice={'location':idnow,'type':"1,3"}
weathernow=requests.get(now,params=paramsnow,headers=headers)
wear=requests.get(indice,params=paramsindice,headers=headers)
print(weathernow.text)
print(wear.text)
#uncompressed_data = gzip.decompress(weathernow.content)
#json_str = uncompressed_data.decode("utf-8")  # 转文本
#json_data = json.loads(json_str)              # 转字典
weathernow_change=json.loads(weathernow.text)
wear_change=json.loads(wear.text)
print('当前位置：'+citynow)
print('天气：'+weathernow_change["now"]["text"])
print('温度：'+weathernow_change["now"]["temp"])
print('体感温度：'+weathernow_change["now"]["feelsLike"])

root=Tk()
root.title(citynow+'天气')
root.geometry('600x600+100+100')

var1=StringVar()

#iconid=weathernow_change["now"]["icon"]
#iconopen=Image.open('E:/学号随机/icons/'+iconid+'.svg')
#icon=ImageTk.PhotoImage(image=iconopen)

def anothercity():
    cityse=Toplevel()
    cityse.title('查询天气')
    cityse.geometry('300x300+100+100')
    Label(cityse,text='请输入要查询天气的城市').pack()
    Entry(cityse,textvariable=var1).pack()
    Button(cityse,text='确定',command=se).pack()

def se():
    global anidnow
    paramssec={'location':var1.get(),'lang':'zh'}
    anoplacenow=requests.get(geoapi,params=paramssec,headers=headers)
    print(anoplacenow.text)
    anidnow=json.loads(anoplacenow.text)
    ancitynow=anidnow["location"][0]["name"]
    anidnow=anidnow["location"][0]["id"]

    paramswease={'location':anidnow,'lang':'zh'}

    anoweathernow=requests.get(now,params=paramswease,headers=headers)
    print(anoweathernow)
    anoweathernow=json.loads(anoweathernow.text)
    print(anidnow)

    show=Toplevel()
    show.title('天气查询结果')
    show.geometry('400x400+100+100')
    Label(show,text=ancitynow+'天气',font=40).pack()
    Label(show,text='天气：'+anoweathernow["now"]["text"]).pack()
    Label(show,text='温度：'+anoweathernow["now"]["temp"]+'°C').pack()
    Label(show,text='体感温度：'+anoweathernow["now"]["feelsLike"]+'°C').pack()
    #Label(show,text=anoweathernow["daily"][0]["name"]+'：'+wear_change["daily"][0]["text"]).pack()
    #Label(show,text=anoweathernow["daily"][1]["name"]+'：'+wear_change["daily"][1]["text"]).pack()
    Button(show,text='查询本城市未来天气',command=anofuturedays).place(x=150,y=300)

def futuredays():
    global future15d
    future1=Toplevel()
    future1.title('查询未来天气')
    future1.geometry('300x300+100+100')
    futureget=future+'15d'
    paramsfuture={'location':idnow}
    future15d=requests.get(futureget,params=paramsfuture,headers=headers)
    print(future15d.text)
    Label(future1,text='请选择要查询的未来天气天数').pack()
    Button(future1,text='3天',command=future3).pack()
    Button(future1,text='7天',command=future7).pack()

def future3():
    future3dchange=json.loads(future15d.text)

    #第1天
    future1d_time=future3dchange["daily"][0]["fxDate"]
    future1d_tempmax=future3dchange["daily"][0]["tempMax"]
    future1d_tempmin=future3dchange["daily"][0]["tempMin"]
    future1d_weather=future3dchange["daily"][0]["textDay"]
    print(future1d_time,future1d_tempmax,future1d_tempmin,future1d_weather)

    #第2天
    future2d_time=future3dchange["daily"][1]["fxDate"]
    future2d_tempmax=future3dchange["daily"][1]["tempMax"]
    future2d_tempmin=future3dchange["daily"][1]["tempMin"]
    future2d_weather=future3dchange["daily"][1]["textDay"]
    print(future2d_time,future2d_tempmax,future2d_tempmin,future2d_weather)

    #第3天
    future3d_time=future3dchange["daily"][2]["fxDate"]
    future3d_tempmax=future3dchange["daily"][2]["tempMax"]
    future3d_tempmin=future3dchange["daily"][2]["tempMin"]
    future3d_weather=future3dchange["daily"][2]["textDay"]
    print(future3d_time,future3d_tempmax,future3d_tempmin,future3d_weather)


    futurew=Toplevel()
    futurew.title('未来天气')
    futurew.geometry('300x600+100+100')
    Label(futurew,text=future1d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future1d_weather).pack()
    Label(futurew,text='最高温度：'+future1d_tempmax).pack()
    Label(futurew,text='最低温度：'+future1d_tempmin).pack()

    Label(futurew,text=future2d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future2d_weather).pack()
    Label(futurew,text='最高温度：'+future2d_tempmax).pack()
    Label(futurew,text='最低温度：'+future2d_tempmin).pack()

    Label(futurew,text=future3d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future3d_weather).pack()
    Label(futurew,text='最高温度：'+future3d_tempmax).pack()
    Label(futurew,text='最低温度：'+future3d_tempmin).pack()

def future7():
    future5dchange=json.loads(future15d.text)

    #第1天
    future1d_time=future5dchange["daily"][0]["fxDate"]
    future1d_tempmax=future5dchange["daily"][0]["tempMax"]
    future1d_tempmin=future5dchange["daily"][0]["tempMin"]
    future1d_weather=future5dchange["daily"][0]["textDay"]
    print(future1d_time,future1d_tempmax,future1d_tempmin,future1d_weather)

    #第2天
    future2d_time=future5dchange["daily"][1]["fxDate"]
    future2d_tempmax=future5dchange["daily"][1]["tempMax"]
    future2d_tempmin=future5dchange["daily"][1]["tempMin"]
    future2d_weather=future5dchange["daily"][1]["textDay"]
    print(future2d_time,future2d_tempmax,future2d_tempmin,future2d_weather)

    #第3天
    future3d_time=future5dchange["daily"][2]["fxDate"]
    future3d_tempmax=future5dchange["daily"][2]["tempMax"]
    future3d_tempmin=future5dchange["daily"][2]["tempMin"]
    future3d_weather=future5dchange["daily"][2]["textDay"]
    print(future3d_time,future3d_tempmax,future3d_tempmin,future3d_weather)

    #第4天
    future4d_time=future5dchange["daily"][3]["fxDate"]
    future4d_tempmax=future5dchange["daily"][3]["tempMax"]
    future4d_tempmin=future5dchange["daily"][3]["tempMin"]
    future4d_weather=future5dchange["daily"][3]["textDay"]
    print(future4d_time,future4d_tempmax,future4d_tempmin,future4d_weather)

    #第5天
    future5d_time=future5dchange["daily"][4]["fxDate"]
    future5d_tempmax=future5dchange["daily"][4]["tempMax"]
    future5d_tempmin=future5dchange["daily"][4]["tempMin"]
    future5d_weather=future5dchange["daily"][4]["textDay"]
    print(future5d_time,future5d_tempmax,future5d_tempmin,future5d_weather)

    #第6天
    future6d_time=future5dchange["daily"][5]["fxDate"]
    future6d_tempmax=future5dchange["daily"][5]["tempMax"]
    future6d_tempmin=future5dchange["daily"][5]["tempMin"]
    future6d_weather=future5dchange["daily"][5]["textDay"]
    print(future6d_time,future6d_tempmax,future6d_tempmin,future6d_weather)

    #第7天
    future7d_time=future5dchange["daily"][6]["fxDate"]
    future7d_tempmax=future5dchange["daily"][6]["tempMax"]
    future7d_tempmin=future5dchange["daily"][6]["tempMin"]
    future7d_weather=future5dchange["daily"][6]["textDay"]
    print(future7d_time,future7d_tempmax,future7d_tempmin,future7d_weather)


    futurew=Toplevel()
    futurew.title('未来天气')
    futurew.geometry('300x700+100+50')
    Label(futurew,text=future1d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future1d_weather).pack()
    Label(futurew,text='最高温度：'+future1d_tempmax).pack()
    Label(futurew,text='最低温度：'+future1d_tempmin).pack()

    Label(futurew,text=future2d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future2d_weather).pack()
    Label(futurew,text='最高温度：'+future2d_tempmax).pack()
    Label(futurew,text='最低温度：'+future2d_tempmin).pack()

    Label(futurew,text=future3d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future3d_weather).pack()
    Label(futurew,text='最高温度：'+future3d_tempmax).pack()
    Label(futurew,text='最低温度：'+future3d_tempmin).pack()

    Label(futurew,text=future4d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future4d_weather).pack()
    Label(futurew,text='最高温度：'+future4d_tempmax).pack()
    Label(futurew,text='最低温度：'+future4d_tempmin).pack()

    Label(futurew,text=future5d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future5d_weather).pack()
    Label(futurew,text='最高温度：'+future5d_tempmax).pack()
    Label(futurew,text='最低温度：'+future5d_tempmin).pack()
    
    Label(futurew,text=future6d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future6d_weather).pack()
    Label(futurew,text='最高温度：'+future6d_tempmax).pack()
    Label(futurew,text='最低温度：'+future6d_tempmin).pack()

    Label(futurew,text=future7d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future7d_weather).pack()
    Label(futurew,text='最高温度：'+future7d_tempmax).pack()
    Label(futurew,text='最低温度：'+future7d_tempmin).pack()

#其他城市未来天气查询函数
def anofuturedays():
    global anofuture15d
    future1=Toplevel()
    future1.title('查询未来天气')
    future1.geometry('300x300+100+100')
    futureget=future+'3d'
    paramsfuture={'location':anidnow,'lang':'zh'}
    anofuture15d=requests.get(futureget,params=paramsfuture,headers=headers)
    print(anofuture15d.text)
    Label(future1,text='请选择要查询的未来天气天数').pack()
    Button(future1,text='3天',command=anofuture3).pack()

def anofuture3():
    future3dchange=json.loads(anofuture15d.text)

    #第1天
    future1d_time=future3dchange["daily"][0]["fxDate"]
    future1d_tempmax=future3dchange["daily"][0]["tempMax"]
    future1d_tempmin=future3dchange["daily"][0]["tempMin"]
    future1d_weather=future3dchange["daily"][0]["textDay"]
    print(future1d_time,future1d_tempmax,future1d_tempmin,future1d_weather)

    #第2天
    future2d_time=future3dchange["daily"][1]["fxDate"]
    future2d_tempmax=future3dchange["daily"][1]["tempMax"]
    future2d_tempmin=future3dchange["daily"][1]["tempMin"]
    future2d_weather=future3dchange["daily"][1]["textDay"]
    print(future2d_time,future2d_tempmax,future2d_tempmin,future2d_weather)

    #第3天
    future3d_time=future3dchange["daily"][2]["fxDate"]
    future3d_tempmax=future3dchange["daily"][2]["tempMax"]
    future3d_tempmin=future3dchange["daily"][2]["tempMin"]
    future3d_weather=future3dchange["daily"][2]["textDay"]
    print(future3d_time,future3d_tempmax,future3d_tempmin,future3d_weather)


    futurew=Toplevel()
    futurew.title('未来天气')
    futurew.geometry('300x600+100+100')
    Label(futurew,text=future1d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future1d_weather).pack()
    Label(futurew,text='最高温度：'+future1d_tempmax).pack()
    Label(futurew,text='最低温度：'+future1d_tempmin).pack()

    Label(futurew,text=future2d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future2d_weather).pack()
    Label(futurew,text='最高温度：'+future2d_tempmax).pack()
    Label(futurew,text='最低温度：'+future2d_tempmin).pack()

    Label(futurew,text=future3d_time+'天气',font=15).pack()
    Label(futurew,text='天气：'+future3d_weather).pack()
    Label(futurew,text='最高温度：'+future3d_tempmax).pack()
    Label(futurew,text='最低温度：'+future3d_tempmin).pack()

Label(root,text=citynow+'天气',font=40).pack()
Label(root,text='天气：'+weathernow_change["now"]["text"]).pack()
Label(root,text='温度：'+weathernow_change["now"]["temp"]+'°C').pack()
Label(root,text='体感温度：'+weathernow_change["now"]["feelsLike"]+'°C').pack()
Label(root,text=wear_change["daily"][0]["name"]+'：'+wear_change["daily"][0]["text"]).pack()
Label(root,text=wear_change["daily"][1]["name"]+'：'+wear_change["daily"][1]["text"]).pack()
Button(root,text='查询其他城市天气',command=anothercity).place(x=400,y=550)
Button(root,text='查询未来天气',command=futuredays).place(x=150,y=550)

root.mainloop()