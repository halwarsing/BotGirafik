import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import threading
import json
import ast
import sys
from halran import *
import youtube_api

ue4_blogers = ["UCVegZa_GdVut2-np7VWVU8w"]
youtube = youtube_api.Youtube()

tok = {}

def load_settings():
    out = {}
    text = open("config.halconf","r",encoding="utf-8").read().split(";")
    for i in text:
        args = i.split("=")
        out[args[0]] = args[1]
    return out

def list_gets(arr,index):
    out = []
    for i in arr:
        out.append(i[index])
    return out

def list_diagonale_gets(arr,left):
    out = []
    if left:
        c = 0
        for i in arr:
            out.append(i[c])
            c += 1

    else:
        c = len(arr[0]) - 1
        for i in arr:
            out.append(i[c])
            c -= 1
    return out

def check_win_toe(arr):
    out = False
    player = None
    if "".join(arr[0][:3]) == "xxx" or "".join(arr[1][:3]) == "xxx" or "".join(arr[2][:3]) == "xxx" or "".join(list_gets(arr,0)) == "xxx" or "".join(list_gets(arr,1)) == "xxx" or "".join(list_gets(arr,2)) == "xxx" or "".join(list_diagonale_gets(arr,False)) == "xxx" or "".join(list_diagonale_gets(arr,True)) == "xxx":
        out = True
        player = "p1"
    elif "".join(arr[0][:3]) == "ooo" or "".join(arr[1][:3]) == "ooo" or "".join(arr[2][:3]) == "ooo" or "".join(list_gets(arr,0)) == "ooo" or "".join(list_gets(arr,1)) == "ooo" or "".join(list_gets(arr,2)) == "ooo" or "".join(list_diagonale_gets(arr,False)) == "ooo" or "".join(list_diagonale_gets(arr,True)) == "ooo":
        out = True
        player = "p2"
    return (out,player)

settings_info = load_settings()
group_id = int(settings_info["group_id"])
nameGroup = settings_info["nameGroup"]
token = settings_info["token"]
greeting = settings_info["greeting"]
mati = open("маты.txt","r",encoding="utf-8").read().split(";")
facts = open("facts.txt","r",encoding="cp1251").read().split(";")[:-1]
def get_info():
    out = {}
    text = open("db.txt","r",encoding="cp1251").read().split("|")[:-1]
    for i in text:
        args = i.split("=")
        f = {}
        for g in args[1].split(";")[:-1]:
            if g.split(".")[0] == "keyboard":
                f["keyboard"] = g.split(".")[1]
            elif g.split(".")[0] == "mute":
                f["mute"] = g.split(".")[1].split(",")
            elif g.split(".")[0] == "users":
                f["users"] = ast.literal_eval(g.split(".")[1])
            else:
                f[g.split(".")[0]] = g.split(".")[1]
        out[args[0]] = f
    return out

def get_comments_info():
    out = []
    if len(open("cms.txt","r").read()) > 0:
        out = open("cms.txt","r",encoding="utf-8").read().split(";")[:-1]
    return out

info_chats = get_info()

def save_info():
    global info_chats
    out = ""

    for key in info_chats.keys():
        out += key+"="
        for k, v in info_chats[key].items():
            if k == "mute":
                out += "mute."+",".join(v)+";"
            else:
                out += k + "." + str(v) + ";"
        out += "|"

    open("db.txt","w").write(out)
            
save_info()
comments_ids = get_comments_info()

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id)
start = True

def f():
    global start
    global info_chats
    threading.Timer(3600, f).start()  # Перезапуск через 60 минут
    if start == False:
        for i in info_chats.keys():
            keyboard = info_chats[i]["keyboard"]
            if info_chats[i]["ue4"] == "t":
                vk.method("messages.send",{
                    'peer_id': i,
                    'random_id': get_random_id(),
                    'message': "Последнее видео Marco Ghislanzoni - "+ youtube.get_last_video(ue4_blogers[0]),
                    'keyboard': keyboard
                })
            vk.method("messages.send",{
                'peer_id': i,
                'random_id': get_random_id(),
                'message': "А вы знали, что " + random.randelem(facts),
                'keyboard': keyboard
            })
    else:
        for i in info_chats.keys():
            keyboard = VkKeyboard(one_time=False)
            if info_chats[i]["ue4"] == "t":
                keyboard.add_button("!скажи факт",color=VkKeyboardColor.POSITIVE)
                keyboard.add_button("!покажи документацию",color=VkKeyboardColor.NEGATIVE)
                keyboard.add_button("!настройки",color=VkKeyboardColor.SECONDARY)
                keyboard.add_button("!новости ue4",color=VkKeyboardColor.PRIMARY)

            else:
                
                keyboard.add_button("!скажи факт",color=VkKeyboardColor.POSITIVE)
                keyboard.add_button("!покажи документацию",color=VkKeyboardColor.NEGATIVE)
                keyboard.add_button("!настройки",color=VkKeyboardColor.SECONDARY)
            keyboard = keyboard.get_keyboard()
            info_chats[i]["keyboard"] = keyboard
            if info_chats[i]["greeting?"] == "t":
                vk.method("messages.send",{
                    'peer_id': i,
                    'random_id': get_random_id(),
                    'message': greeting,
                    'keyboard': info_chats[i]["keyboard"]
                })
        start = False

threading.Thread(target=f).start()

for event in longpoll.listen():
    if event.type == VkBotEventType.WALL_REPLY_NEW:
        mat = False
        for i in mati:
            if i in event.obj["text"]:
                if event.obj["id"] not in comments_ids:
                    vk.method("wall.createComment",{
                        'owner_id': -group_id,
                        'post_id': event.obj["post_id"],
                        'message': "Аяяй, материться нельзя",
                        'reply_to_comment': event.obj["id"],
                        'guid': get_random_id()
                    })
                    comments_ids.append(event.obj["id"])
                    open("cms.txt","a").write(str(event.obj["id"])+";")
                    mat = True
        if "reply_to_comment" not in event.obj.keys() and mat == False:
            if event.obj["id"] not in comments_ids:
                vk.method("wall.createComment",{
                    'owner_id': -group_id,
                    'post_id': event.obj["post_id"],
                    'message': "А вы знали, что "+random.randelem(facts),
                    'reply_to_comment': event.obj["id"],
                    'guid': get_random_id()
                })
                comments_ids.append(event.obj["id"])
                open("cms.txt","a").write(str(event.obj["id"])+";")
    elif event.type == VkBotEventType.MESSAGE_NEW:
        if len(event.obj["message"]["text"].split(f"[club{group_id}|@{nameGroup}] ")) > 1:
            event.obj["message"]["text"] = event.obj["message"]["text"].split("[club203377245|@intfactshal] ")[1]
        
        if event.obj["message"]["text"] == "!start" and str(event.obj["message"]["peer_id"]) not in info_chats.keys():
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("!скажи факт",color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("!покажи документацию",color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("!настройки",color=VkKeyboardColor.PRIMARY)
            keyboard = keyboard.get_keyboard()
            users = vk.method("messages.getConversationMembers",{
                'peer_id': event.obj['message']['peer_id']
            })
            users_dict = {}
            for user in users['items']:
                if user ['member_id'] > 0:
                    users_dict[str(user['member_id'])] = {'awards':[],'money':100}
            info_chats[str(event.obj["message"]["peer_id"])] = {"ue4":"f","mute":["infactshal"],"greeting?":"t","keyboard":keyboard,'users':users_dict}
            save_info()
            vk.method("messages.send", {
                'peer_id': event.obj["message"]["peer_id"],
                'random_id': get_random_id(),
                'message': 'Вот мои команды - https://botgirafik.peopletok.ru/commands.php',
                'keyboard': keyboard
            })
        
        if str(event.obj["message"]["peer_id"]) not in info_chats.keys():
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("!start",color=VkKeyboardColor.POSITIVE)
            keyboard = keyboard.get_keyboard()
            vk.method("messages.send", {
                'peer_id': event.obj["message"]["peer_id"],
                'random_id': get_random_id(),
                'message': 'Если хотите начать напишите !start',
                'keyboard': keyboard
            })

        id_user = event.obj["message"]["from_id"]
        if str(event.obj["message"]["peer_id"]) in info_chats.keys():
            if str(id_user) not in info_chats[str(event.obj["message"]["peer_id"])]["mute"]:
                keyboard = info_chats[str(event.obj["message"]["peer_id"])]["keyboard"]
                if event.obj["message"]["text"].startswith("!скажи факт"):
                    if len(event.obj["message"]["text"].split(" ")) == 3 and int(event.obj["message"]["text"].split("!скажи факт")[1]) < len(facts):
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': "А вы знали, что " + facts[int(event.obj["message"]["text"].split("!скажи факт")[1])],
                            'keyboard': keyboard
                        })
                        
                    else:
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': "А вы знали, что " + random.randelem(facts),
                            'keyboard': keyboard
                        })

                if event.obj["message"]["text"].startswith('!добавь факт'):
                    new_fact = event.obj["message"]["text"].split("!добавить факт")[1]
                    facts.append(new_fact)
                    open("facts.txt","a").write(new_fact+";")
                    vk.method("messages.send",{
                        'peer_id': event.obj["message"]["peer_id"],
                        'random_id': get_random_id(),
                        'message': "факт добавлен",
                        'keyboard': keyboard
                    })

                if event.obj["message"]["text"].startswith('!покажи документацию'):
                    vk.method("messages.send",{
                        'peer_id': event.obj["message"]["peer_id"],
                        'random_id': get_random_id(),
                        'message': "Вот мой сайт - https://botgirafik.peopletok.ru",
                        'keyboard': keyboard 
                    })
                if event.obj["message"]["text"].startswith("!замуть"):
                    user = event.obj["message"]["text"].split("!замуть ")[1].split("id")[1].split("|")[0]
                    user_name = event.obj["message"]["text"].split("!замуть ")[1].split("|")[1].split("]")[0] 
                    result = f"{user_name} уже замучен"
                    if user not in info_chats[str(event.obj["message"]["peer_id"])]["mute"]:
                        info_chats[str(event.obj["message"]["peer_id"])]["mute"].append(user)
                        result = f'Ща замучу {user_name}'
                        save_info()
                    
                    vk.method("messages.send",{
                        'peer_id':event.obj['message']['peer_id'],
                        'random_id':get_random_id(),
                        'message': result,
                        'keyboard': keyboard
                    })

                if event.obj["message"]["text"].startswith("!размуть"):
                    user = event.obj["message"]["text"].split("!размуть ")[1].split("id")[1].split("|")[0]
                    result = f"{user} уже размучен"
                    if user in info_chats[str(event.obj["message"]["peer_id"])]["mute"]:
                        info_chats[str(event.obj["message"]["peer_id"])]["mute"].remove(user)
                        result = f'Ща размучу {user}'
                        save_info()
                    
                    vk.method("messages.send",{
                        'peer_id':event.obj['message']['peer_id'],
                        'random_id':get_random_id(),
                        'message': result,
                        'keyboard': keyboard
                    })
                str(event.obj["message"]["peer_id"]) not in tok.keys()
                if event.obj["message"]["text"].startswith('!крестики-нолики') and str(event.obj["message"]["peer_id"]) not in tok.keys():
                    players = event.obj["message"]["text"].split("!крестики-нолики ")[1].split(" ")
                    tok[str(event.obj["message"]["peer_id"])] = {
                        "p1":players[0].split("id")[1].split("|")[0],
                        "p1_name":players[0].split("|")[1].split("]")[0],
                        "p2":players[1].split("id")[1].split("|")[0],
                        "p2_name":players[1].split("|")[1].split("]")[0],
                        "tok":[
                            [" "," "," "],
                            [" "," "," "],
                            [" "," "," "]
                        ],
                        "round": "1"
                    }
                    vk.method("messages.send",{
                        'peer_id':event.obj['message']['peer_id'],
                        'random_id':get_random_id(),
                        'message': "⛔️|⛔️|⛔️\n⛔️|⛔️|⛔️\n⛔️|⛔️|⛔️",
                        'keyboard': keyboard
                    })

                elif str(event.obj["message"]["peer_id"]) in tok.keys():
                    user = str(event.obj["message"]["from_id"])
                    o = ""
                    try:
                        coord = (int(event.obj["message"]["text"].split("-")[0])-1,int(event.obj["message"]["text"].split("-")[1])-1)
                        isDraw = True
                        if tok[str(event.obj["message"]["peer_id"])]["round"] == "1" and user == tok[str(event.obj["message"]["peer_id"])]["p1"]:
                            if tok[str(event.obj["message"]["peer_id"])]["tok"][coord[0]][coord[1]] == " ":
                                tok[str(event.obj["message"]["peer_id"])]["tok"][coord[0]][coord[1]] = "x"
                                tok[str(event.obj["message"]["peer_id"])]["round"] = "2"
                            else:
                                 o += "Там уже поставлено\n"

                        elif tok[str(event.obj["message"]["peer_id"])]["round"] == "2" and user == tok[str(event.obj["message"]["peer_id"])]["p2"]:
                            if tok[str(event.obj["message"]["peer_id"])]["tok"][coord[0]][coord[1]] == " ":
                                tok[str(event.obj["message"]["peer_id"])]["tok"][coord[0]][coord[1]] = "o"
                                tok[str(event.obj["message"]["peer_id"])]["round"] = "1"
                                
                            else:
                                 o += "Там уже поставлено\n"
                        for i in tok[str(event.obj["message"]["peer_id"])]["tok"]:
                            ou = ""
                            for k in i:
                                out = "⛔️"
                                if k == "x":
                                    out = "❌"
                                elif k == "o":
                                    out = "🅾️"
                                else:
                                    isDraw = False
                                    
                                ou += f"{out}|"
                            ou = ou[:-1]
                            o += ou+"\n"

                        if isDraw:
                            o += "Ничья :-(\n"
                        
                        checkwintoe = check_win_toe(tok[str(event.obj["message"]["peer_id"])]["tok"])
                        if checkwintoe[1] == "p1":
                            o += "Победил "+tok[str(event.obj["message"]["peer_id"])]["p1_name"] + "!!!"

                        if checkwintoe[1] == "p2":
                            o += "Победил "+tok[str(event.obj["message"]["peer_id"])]["p2_name"] + "!!!"
                            
                        vk.method("messages.send",{
                            'peer_id':event.obj['message']['peer_id'],
                            'random_id':get_random_id(),
                            'message': o,
                            'keyboard': keyboard
                        })
                        if checkwintoe[0]:
                            del tok[str(event.obj["message"]["peer_id"])]

                        elif isDraw:
                            del tok[str(event.obj["message"]["peer_id"])]
                    except:
                        pass
                    

                if event.obj["message"]["text"].startswith('!настройки'):
                    info = event.obj["message"]["text"].split(" ")
                    if len(info) == 3:
                        info_chats[str(event.obj["message"]["peer_id"])][info[1]] = info[2]
                        if info[1] == "ue4":
                            keyboard = VkKeyboard(one_time=False)
                            keyboard.add_button("!скажи факт",color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button("!покажи документацию",color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_button("!настройки",color=VkKeyboardColor.SECONDARY)
                            if info[2] == "t":
                                keyboard.add_button("!новости ue4",color=VkKeyboardColor.PRIMARY)
                            keyboard = keyboard.get_keyboard()
                            info_chats[str(event.obj["message"]["peer_id"])]["keyboard"] = keyboard
                            
                        keyboard = info_chats[str(event.obj["message"]["peer_id"])]["keyboard"]
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': "Настройки обновлены: "+info[1]+"="+info[2],
                            'keyboard': keyboard 
                        })
                        save_info()
                    else:
                        ue4 = info_chats[str(event.obj["message"]["peer_id"])]["ue4"]
                        mute = ",".join(info_chats[str(event.obj["message"]["peer_id"])]["mute"])
                        greeting = info_chats[str(event.obj["message"]["peer_id"])]["greeting?"]
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': f"""Настройки
ue4={ue4},
mute={mute}
greeting?={greeting}""",
                        'keyboard': keyboard
                    })
                if event.obj["message"]["text"].startswith("!новости ue4"):
                    vk.method("messages.send",{
                        'peer_id': event.obj["message"]["peer_id"],
                        'random_id': get_random_id(),
                        'message': "Последнее видео Marco Ghislanzoni - https://youtube.com/watch?v="+ youtube.get_last_video(ue4_blogers[0]),
                        'keyboard': keyboard
                    })

                if event.obj['message']['text'].startswith('!больше-меньше'):
                    info = event.obj['message']['text'].split(" ")
                    if len(info) == 1:
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': "Напишите !больше-меньше {больше или меньше} {дополнительно ставка}. Больше 99999 или меньше 100000 :-)",
                            'keyboard': keyboard
                        })
                    elif len(info) == 2:
                        random_num = random.randint(0,199999,1)
                        result = ""
                        if random_num > 99999:
                            if info[1] == "больше":
                                result = "Правильно!"
                            else:
                                result = "Неправильно!"
                        elif random_num < 100000:
                            if info[1] == "меньше":
                                result = "Правильно!"
                            else:
                                result = "Неправильно!"
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': f"{result} число - {random_num}",
                            'keyboard': keyboard
                        })
                    
                    elif len(info) == 3:
                        random_num = random.randint(0,199999,1)
                        money = int(info[2])
                        result = ""
                        curMoney = int(info_chats[str(event.obj['message']['peer_id'])]['users'][str(event.obj['message']['from_id'])]['money'])
                        if curMoney >= money:
                            if random_num > 99999:
                                if info[1] == "больше":
                                    result = f"Правильно! +{money},"
                                    info_chats[str(event.obj['message']['peer_id'])]['users'][str(event.obj['message']['from_id'])]['money'] = curMoney + money
                                else:
                                    result = f"Неправильно!"
                                    info_chats[str(event.obj['message']['peer_id'])]['users'][str(event.obj['message']['from_id'])]['money'] = curMoney - money
                            elif random_num < 100000:
                                if info[1] == "меньше":
                                    result = f"Правильно! +{money},"
                                    info_chats[str(event.obj['message']['peer_id'])]['users'][str(event.obj['message']['from_id'])]['money'] = curMoney + money
                                else:
                                    info_chats[str(event.obj['message']['peer_id'])]['users'][str(event.obj['message']['from_id'])]['money'] = curMoney - money
                                    result = f"Неправильно!"
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': f"{result} число - {random_num}",
                                'keyboard': keyboard
                            })
                        else:
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': f"У вас недостаточно монет. У вас {curMoney}, а нужно {money}",
                                'keyboard': keyboard
                            })

                if event.obj["message"]["text"].startswith("!инфо"):
                    info = event.obj["message"]["text"].split(" ")
                    if len(info) == 1:
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': "Пользователи: "+str(info_chats[str(event.obj['message']['peer_id'])]['users']),
                            'keyboard': keyboard
                        })

                    elif len(info) == 2:
                        user = info[1].split("id")
                        if len(user) > 1:
                            user = user[1].split("|")[0]
                            user_name = info[1].split("|")[1].split("]")[0]
                            user_info = info_chats[str(event.obj['message']['peer_id'])]['users'][user]
                            money = user_info['money']
                            awards = ", ".join(user_info["awards"])
                            if len(user_info['awards']) > 0:
                                awards = f"Награды: {awards}\n"
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': f"Пользователь {user_name}:\n{awards}Монет: {money}",
                                'keyboard': keyboard
                            })

                if event.obj['message']['text'].startswith('!наградить'):
                    user = event.obj['message']['text'].split('!наградить ')[1].split(' ')[0]
                    award_name = event.obj['message']['text'].split(user+" ")[1]
                    user_name = user.split("|")[1].split("]")[0]
                    user_id = user.split("id")[1].split("|")[0]
                    info_chats[str(event.obj['message']['peer_id'])]['users'][user_id]['awards'].append(award_name)
                    vk.method("messages.send",{
                        'peer_id': event.obj["message"]["peer_id"],
                        'random_id': get_random_id(),
                        'message': f'{user_name} получил награду "{award_name}" :-)',
                        'keyboard': keyboard
                    })

                if event.obj['message']['text'].startswith('!рандом'):
                    info = event.obj['message']['text'].split(" ")
                    if len(info) == 1:
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': str(random.randint(0,500,1,difficult=random.randint(0,5,1)))+" - от 0 до 500, с шагом 1",
                            'keyboard': keyboard
                        })
                    if len(info) == 2:
                        if info[1] == "float":
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': str(random.randint(0.0,100.0,0.01,difficult=random.randint(0,5,1)))+" - от 0.0 до 100.0, с шагом 0.01, примерно 10000 вариантов :)",
                                'keyboard': keyboard
                            })
                        elif info[1] == "int":
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': str(random.randint(0,100,1,difficult=random.randint(0,5,1)))+" - от 0 до 100, с шагом 1, примерно 100 вариантов :)",
                                'keyboard': keyboard
                            })
                        elif info[1] == "array":
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': str(random.randelem(['hi','hello','bye','goodbye','goodmorning']))+" - рандомный элемент из массива ['hi','hello','bye','goodbye','goodmorning'] :)",
                                'keyboard': keyboard
                            })
                        elif info[1] == "инфо":
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': "Это новый рандомный алгоритм об нём можно узнать на github: https://github.com/halwarsing/HalwarsingRandom и можно установить в python на сайте PyPi: https://pypi.org/project/halran/ :)",
                                'keyboard': keyboard
                            })
                        elif len(info[1].split(",")) > 1:
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': str(random.randelem(info[1].split(",")))+" - рандомный элемент из массива "+str(info[1].split(","))+" :)",
                                'keyboard': keyboard
                            })

                        else:
                            if len(info[1].split(".")) > 1:
                                count = float(info[1])
                            else:
                                count = int(info[1])
                            vk.method("messages.send",{
                                'peer_id': event.obj["message"]["peer_id"],
                                'random_id': get_random_id(),
                                'message': str(random.randint(0,count,1,difficult=random.randint(0,5,1)))+f" - рандомное число от 0 до {count}, с шагом 1 :)",
                                'keyboard': keyboard
                            })
                    elif len(info) == 3:
                        if len(info[1].split(".")) > 1:
                            start = float(info[1])
                        else:
                            start = int(info[1])
                        if len(info[2].split(".")) > 1:
                            end = float(info[2])
                        else:
                            end = int(info[2])
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': str(random.randint(start,end,1,difficult=random.randint(0,5,1)))+f" - рандомное число от {start} до {end}, с шагом 1 :)",
                            'keyboard': keyboard
                        })    
                    elif len(info) == 4:
                        if len(info[1].split(".")) > 1:
                            start = float(info[1])
                        else:
                            start = int(info[1])
                        if len(info[2].split(".")) > 1:
                            end = float(info[2])
                        else:
                            end = int(info[2])
                        if len(info[3].split(".")) > 1:
                            step = float(info[3])
                        else:
                            step = int(info[3])
                        vk.method("messages.send",{
                            'peer_id': event.obj["message"]["peer_id"],
                            'random_id': get_random_id(),
                            'message': str(random.randint(start,end,step,difficult=random.randint(0,5,1)))+f" - рандомное число от {start} до {end}, с шагом {step} :)",
                            'keyboard': keyboard
                        })
