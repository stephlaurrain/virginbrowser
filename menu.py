import os
import sys
import gc
from virginbrowser import Bot
from datetime import datetime


class Menuitem:
    def __init__(self, command, label, nb_params, ret):
        self.command = command
        self.label = label        
        self.nb_params = nb_params        
        self.ret = ret

root_app = os.getcwd()

hardgreen = "\033[32m\033[1m"
normalgreen = "\033[32m\033[2m"
normalcolor = "\033[0m"


def mencol(nb, fonc, comment):
    return f"{hardgreen}{nb} - {fonc} {normalgreen} - {comment}{normalcolor}"

def drkcol(str):
    return f"{hardgreen}{str}{normalcolor}"

def clear():
    return os.system('clear')

nb_args = len(sys.argv)

jsonfile_from_arg = "default" if (nb_args == 1) else sys.argv[1]
mode_menu = "default" if (nb_args < 3) else sys.argv[2]

clear()

bot = Bot()
while True:
    print(drkcol("\nHi Neo, I'm your pure browser"))    
    print(drkcol("Your wish is my order\n"))
    print(drkcol("What I can do for you :\n"))

    menulist = []
    menulist.append(Menuitem("browse", "browse", nb_params=0, ret=True))    
    # menulist.append(Menuitem("resetprofile", "resetprofile", nb_params=0, ret=True))  
    

    for idx, menuitem in enumerate(menulist):
        print (mencol(idx, menuitem.command, menuitem.label))
        if menuitem.ret:
            print(drkcol("#####"))

    
    print(drkcol("#####"))
    print(mencol("93", "edit_params", "edit default.json"))        
    print(mencol("99", "exit", "exit this menu"))

    dothat = input(drkcol("\n\nReady to browse : "))

    today = datetime.now()
    dnow = today.strftime(r"%y%m%d")

    if dothat == "93":
        print(drkcol("\edit params -r\n"))
        os.system("nano data/conf/default.json")
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        del bot
        gc.collect
        quit()
    try:
        if int(dothat) < 50:
            cmdstr = "nop"

            item = menulist[int(dothat)]
            cmd = item.command
            print (cmd)
            prms = int(item.nb_params)
            prmcmdlist = []
            for i in range(prms):
                prmcmdlist.append(input(drkcol(f"enter param {i} :")))
            bot.main(cmd, jsonfile_from_arg, prmcmdlist)

    except Exception as e:
        print (e)
        print(f"\n{hardgreen}bad command (something went wrong){normalcolor}\n")
