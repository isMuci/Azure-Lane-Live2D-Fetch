import json
import os
import random
import re

import requests
from time import sleep

# jsonheaders =  {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Origin": "https://blhx.willlan.net",
#     "Referer": "https://blhx.willlan.net/",
#     "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "Windows",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-site",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 LBBROWSER"
# }
#
# pngheaders =  {
#     "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Origin": "https://blhx.willlan.net",
#     "Referer": "https://blhx.willlan.net/",
#     "Sec-Ch-Ua": "Google Chrome;v=119, Chromium;v=119, Not?A_Brand;v=24",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "Windows",
#     "Sec-Fetch-Dest": "image",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-site",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
# }

master="https://blhx.willlan.net/json/live2dMaster.json?1026"
fetchurl="https://game.cdn.willlan.net/AzurLane/Live2d/"
header={"User-Agent": "Mozilla/5.0","Referer": "https://blhx.willlan.net/"}

session_obj = requests.Session()

live2dMaster=session_obj.get(master).json()['Master']

for character in live2dMaster:
    live2d=character['live2d']
    for model in live2d:
        model3path=model['path']
        print(model3path)
        wait_time = random.uniform(1, 5)
        sleep(0.5)
        model3 = session_obj.get(model3path,headers={"User-Agent": "Mozilla/5.0","Referer": "https://blhx.willlan.net/"})
        # model3=requests.post(model3path,jsonheaders)
        if model3.reason == "OK":

            foldername=re.search(r'/Live2d/([^/]+)/', model3path).group(1)
            print(foldername)
            folder_path = os.path.join("./res/", foldername)
            os.makedirs(folder_path, exist_ok=True)

            filename = os.path.basename(model3path)
            try:
                with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as json_file:
                    json.dump(model3.json(), json_file, ensure_ascii=False, indent=4)
            except Exception as e:
                print("\033[91m{}\033[0m".format(e))

            print(filename)

            fileReferences=model3.json()['FileReferences']

            moc=fileReferences['Moc']
            mocfile = session_obj.get(fetchurl+"/"+foldername+"/"+moc,headers={"User-Agent": "Mozilla/5.0", "Cookie:": "https://blhx.willlan.net/"})
            try:
                with open(os.path.join(folder_path, moc), 'wb') as file:
                    file.write(mocfile.content)
            except Exception as e:
                print("\033[91m{}\033[0m".format(e))
            print(moc)
            sleep(0.5)

            textures = fileReferences['Textures']
            os.makedirs(folder_path + "/textures", exist_ok=True)
            for texture in textures:
                texturefile = session_obj.get(fetchurl + "/" + foldername + "/" + texture,headers={"User-Agent": "Mozilla/5.0","Referer": "https://blhx.willlan.net/"})
                try:
                    with open(folder_path + "/" + texture, 'wb') as file:
                        file.write(texturefile.content)
                except Exception as e:
                    print("\033[91m{}\033[0m".format(e))
                print(texture)
                sleep(0.5)

            physics=fileReferences['Physics']
            physicsfile = session_obj.get(fetchurl + "/" + foldername + "/" + physics,headers={"User-Agent": "Mozilla/5.0", "Referer": "https://blhx.willlan.net/"})
            try:
                with open(os.path.join(folder_path, physics), 'w', encoding='utf-8') as json_file:
                    json.dump(physicsfile.json(), json_file, ensure_ascii=False, indent=4)
            except Exception as e:
                print("\033[91m{}\033[0m".format(e))
            print(physics)
            sleep(0.5)

            expressions=fileReferences['Expressions']
            os.makedirs(folder_path+"/expressions", exist_ok=True)
            for expression in expressions:
                expressionpath=expression['File']
                expressionfile = session_obj.get(fetchurl + "/" + foldername + "/" +expressionpath ,headers={"User-Agent": "Mozilla/5.0","Referer": "https://blhx.willlan.net/"})
                try:
                    with open(folder_path+"/"+expressionpath, 'w', encoding='utf-8') as json_file:
                        json.dump(expressionfile.json(), json_file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print("\033[91m{}\033[0m".format(e))
                print(expressionpath)
                sleep(0.5)
                
            motions = fileReferences['Motions'][""]
            os.makedirs(folder_path + "/motions", exist_ok=True)
            for motion in motions:
                motionpath = motion['File']
                motionfile = session_obj.get(fetchurl + "/" + foldername + "/" + motionpath,headers={"User-Agent": "Mozilla/5.0","Referer": "https://blhx.willlan.net/"})
                try:
                    with open(folder_path + "/" + motionpath, 'w', encoding='utf-8') as json_file:
                        json.dump(motionfile.json(), json_file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print("\033[91m{}\033[0m".format(e))
                print(motionpath)
                sleep(0.5)
            print(fileReferences)
        elif model3.reason == "Frequency Capped":
            print(model3.reason)



