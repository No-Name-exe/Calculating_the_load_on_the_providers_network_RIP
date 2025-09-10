from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
Database={}
Database["data"]={
        'routers': [
            {'img':'1.png','title': 'Маршрутизатор провайдера','desc':'Роутер TP-Link Archer C7 — высокопроизводительный роутер с поддержкой Gigabit Ethernet и мощным процессором', 'id': 1},
            {'img':'2.png','title': 'Маршрутизатор промежуточный','desc':'Роутер Asus RT-AC66U — надёжный роутер среднего класса с двумя диапазонами и функцией Mesh.', 'id': 2},
            {'img':'3.png','title': 'Маршрутизатор жилого дома','desc':'Роутер D-Link DIR-615 — компактный и недорогой роутер для домашнего использования с базовыми функциями', 'id': 3},
            {'img':'4.jpg','title': 'Маршрутизатор запасной','desc':'Роутер Netgear R6220 — резервный роутер с простым управлением и стабильной работой.', 'id': 4},
            {'img':'5.png','title': 'Маршрутизатор школы','desc':'Роутер Cisco RV340 — корпоративное устройство с усиленной безопасностью и поддержкой VPN.', 'id': 5},
            {'img':'6.jpg','title': 'Маршрутизатор почты','desc':'Роутер MikroTik hAP ac2 — роутер со встроенным файерволом и возможностями контроля трафика.', 'id': 6},
        ]
    }

Application={}
Application={
    "ListOfApplic":[
            {
            "id":"3", 
            "Date":"",
            "Price":"21 Руб",
            "Comment":" ",
            "ListRouter":[1,3,5]
            },
            {
            "id":"5", 
            "Date":"",
            "Price":"",
            "Comment":"",
            "ListRouter":[3,4]
            },
        ]
    }

def report(request):
    return HttpResponse('Hello world!')

def main(request):
    return render(request, 'site.html')

def result(request):
    return render(request, 'router.html')

def sendSearch(request):
    input_text = request.POST.get("search")
    data={}
    final={}
    found=[]
    routers = Database["data"]["routers"]
    for var in routers:
        print(str(var["title"]).find(input_text))
        if str(var["title"]).find(input_text) >= 0:
            print(var)
            found.append(var)
    print(found) 
    print({'data':{1}})
    data["routers"]=found
    data["req"]=input_text
    final["data"]=data
    print(final)
    # return HttpResponse(input_text)	
    return render(request, 'selection.html',final)	

def GetRouters(request):
    context = {}
    context.update(Database)       # добавляем ключи из Database
    context.update(Application)    # добавляем ключи из Application
    print(context)
    return render(request, 'selection.html', context)


def GetRouter(request, id):
    result=next(item for item in Database["data"]["routers"] if item["id"] == id)
    print(result)
    data={}
    data["data"]=result
    return render(request, 'router.html', data)

def GetApplication(request, id):
    res=[]
    fin={}
    context={}
    ThisApplic={}
    for item in Application['ListOfApplic']: 
        if int(item["id"])==id:
            ThisApplic=item
    # next(item for item in Application['ListOfApplic'] if item["id"] == id)
    context=dict(ThisApplic)
    for item in ThisApplic["ListRouter"]:
        for base in Database["data"]["routers"]:
            if base["id"]==item:
                res.append(base)
    fin["routers"]=res
    context["data"]=fin
    print(context)
    return render(request, 'application.html', context)