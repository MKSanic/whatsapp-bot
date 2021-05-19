import os
import whatsapp
import enchant
import pickle
import calendar
from pathlib import Path
from PyDictionary import PyDictionary
from datetime import datetime
from datetime import timedelta
from random import randint
os.chdir(str(Path(__file__).parent))
#os.chdir("C:/Users/Hansome/Desktop")
dictionary = PyDictionary()
ench = enchant.Dict("en-us")
dayOpts = ["upcoming","over","all"]
actions = ["create","remove","show"]
subjects = {"Higher Chinese":["hcl","higher_chinese","higher_china"],"Chinese":["cl","chinese","china"],"Geography":["geo","geog","geography"],"Integrated Science":["integrated_science","is","iscience","physics","phy","bio","biology"],
           "English":["english","england","el"],"Chemistry":["kemistry","chemistry","chem"],"D&T":["d_and_t","dandt","design_and_technology","d_and_t"],"Art":["art"],"Music":["music","sounds"],"Math":["meth","math","mathematics"],
           "Admin/Other":["admin","misc","miscellaneous","other"],"ACC":["acc"],"History":["history","hist"],"PE":["pe","physical_education"],"English Literature":["elit","lit","literature","english_leterature"]}
resources = [{"Timetable":["PDF: https://tinyurl.com/206tt2021pdf","PNG: https://tinyurl.com/206tt2021png","XLSX: https://tinyurl.com/206tt2021xlsx"]}]
def dump(data,file):
    f = open(file,"wb")
    pickle.dump(data,f)
    f.close()
def load(file):
    f = open(file,"rb")
    d = pickle.load(f)
    f.close()
    return d
def sub(check):
    for k,v in subjects.items():
        if(check.lower() in v):
            return [list(subjects.values()).index(v)]
    if(check.lower() == "all"):
        return list(subjects.keys())
    return ""
class info:
    def __init__(self,date,subject,content):
        self.date = date
        self.subject = subject
        self.content = content
def sort(saved,days):
    rt = []
    dates = set()
    for v in saved:
        if(v.date in days):
            dates.add(v.date)
    dates = list(sorted(dates))
    for i,d in enumerate(dates):
        rt.append([])
        a = rt[i]
        for v in saved:
            if(d == v.date):
                a.append(v)
    return rt
def findDays(arg):
    days = []
    try:
        day = arg
        #number dates
        if("/" in day):
            day = day.split("/")
            go = False
            for v in day:
                if(v.isdigit()):
                    go = True
                else:
                    print("numbers only for date pls im too lazy to implement word dates")
                    return
            if(go):
                days = [datetime(datetime.now().year,int(day[1]),int(day[0])).date()]
            else:
                print("sadge")
                return
        #tomorrow and others
        elif(day.lower() == "tomorrow" or day.lower() == "tmr"):
            days = [datetime.now().date() + timedelta(1,0)]
        elif(day == "today"):
            days = [datetime.now().date()]
        elif(day in dayOpts):
            saved = load("homework.txt")
            for v in saved:
                if(v.date >= datetime.now().date() and day == dayOpts[0]):
                    #date is upcoming
                    days.append(v.date)
                elif(v.date < datetime.now().date() and day == dayOpts[1]):
                    #date is over
                    days.append(v.date)
                elif(day == dayOpts[2]):
                    #all dates
                    days.append(v.date)
        else:
            print("invalid date")
            return
    except Exception as e:
        print(e)
        print("date not provided stoobid")
        return
    return days
client = whatsapp.client.WhatsappClient()
client.command_prefix = "/"
@client.command("quote","Gives a random quote!(sun tzu of course)")
def quote(args,msg):
    f = open("Sun Tzu.txt","r",encoding="utf8")
    l = -1
    s = []
    for line in f:
        s.append(line.replace("\n",""))
        l+=1
    f.close()
    client.send_message(s[randint(0,l)] + "\n-_Sun Tzu,_\n _The Art of War_")
@client.command("resources","Gives you a list of miscellaneous resources!")
def rsc(args,msg):
    rt = ""
    for d in resources:
        for k,l in d.items():
            rt += " *" + k + "*\n"
            for v in l:
                rt += "  " + v + "\n"
    client.send_message(rt)
@client.command("intro","gives self-introduction")
def intro(args,msg):
    client.send_message("Hello I am <unnamed bot(pls vote on name)>\n I am a slave dedicated to keeping track of things for you!\nDo /help for more info\nImportant note: I only work when my sister is connected to the internet")
@client.command("feedback","gives feedback to me, report bugs and request QOL changes here\n/feedback <text>\nEg.\n/feedback I want this feature...")
def feedback(args,msg):
    f = " ".join(args)
    saved = load("feedback.txt")
    saved.append(f)
    dump(saved,"feedback.txt")
@client.command("meaning","Gets meaning of word\n*Example:*\n/meaning <word>\n/Eg.\nmeaning exasperated")
def mean(args,msg):
    if(args != []):
        search = args[0]
    else:
        client.send_message("/help meaning")
        return
    reply = ""
    if(ench.check(search)):
        try:
            m = dictionary.meaning(search)
            for k,v in m.items():
                reply += "*" + k + ":* "
                for im in v:
                    reply += im + ", "
                reply = reply[:-2] + "\n"
        except:
            reply = "Invalid word"
    else:
        reply = "Invalid word"
    client.send_message(reply)
def homework(args,msg):
    try:
        action = args[0]
    except:
        return "/help homework"
    rt = ""
    try:
        l = lambda s=args[0]: True if(s in actions) else False
        if(l()):
            opt = actions.index(action)
            if(opt == 0):
                #create
                days = findDays(args[1])
                if(days == None):
                    rt += "invalid date"
                    return rt
                else:
                    #day found
                    if(len(days) != 1):
                        rt += "one date for create only thx"
                        return rt
                    else:
                        saved = load("homework.txt")
                        #goal: append saved with appropiate info, dump
                        try:
                            subject = sub(args[2])[0]
                            if(subject == ""):
                                rt += "invalid subject"
                                return rt
                        except:
                            rt += "invalid subject"
                            return rt
                        try:
                            content = " ".join(args[3:])
                        except:
                            rt += "no content found"
                            return rt
                        saved.append(info(days[0],list(subjects)[subject],content))
                        dump(saved,"homework.txt")
                        rt += "successfully added \"" + content + "\" to " + list(subjects)[subject] + " due on " + str(days[0])
                        return rt
            elif(opt == 1):
                #remove
                days = findDays(args[1])
                if(days == None):
                    rt += "invalid date"
                    return rt
                else:
                    #day found
                    if(len(days) != 1):
                        rt += "one date for remove only thx"
                        return rt
                    else:
                        saved = load("homework.txt")
                        #goal: find the one that is gonna be deleted, del(list[593])]
                        try:
                            subject = sub(args[2])[0]
                            if(subject == ""):
                                rt += "invalid subject"
                                return rt
                        except:
                            rt += "invalid subject"
                            return rt
                        try:
                            content = " ".join(args[3:])
                        except:
                            rt += "no content found"
                            return rt
                        #real shit
                        deleted = False
                        for i,v in enumerate(saved):
                            if(v.date == days[0] and v.subject == list(subjects)[subject] and v.content.lower() == content.lower()):
                                del saved[i]
                                deleted = True
                                rt += "successfully deleted\n" + v.subject + ": \"" + v.content + "\" due on " + str(days[0])
                                break
                        if(deleted):
                            dump(saved,"homework.txt")
                        else:
                            rt += "no homework with such criteria were found"
                        return rt
            elif(opt == 2):
                #show
                if(len(args) >= 3):
                    days = findDays(args[1])
                    if(days == None):
                        print("invalid date")
                        return rt
                    else:
                        #day found
                        try:
                            subject = sub(args[2])
                            if(subject == ""):
                                rt += "invalid subject"
                                return rt
                        except:
                            rt +=  "invalid subject"
                            return rt
                        #real shit
                        saved = load("homework.txt")
                        final = []
                        dated = sort(saved,days)
                        for l in dated:
                            a = {}
                            for v in l:
                                try:
                                    a[v.subject]
                                except:
                                    a[v.subject] = []
                                a[v.subject].append(v)
                            final.append(a)
                        for d in final:
                            rt += "\n*Submit on: " + str(d[list(d.keys())[0]][0].date) + "*"
                            for s,vl in d.items():
                                rt += "\n*" + s + "*\n"
                                for v in vl:
                                    rt += "-" + v.content + "\n"
                        if(rt != ""):
                            rt = rt[:-1]
                        else:
                            rt = "No homework!(yet)"
                        return rt
                else:
                    rt += "insufficient arguments"
                    return rt
        else:
            rt += "invalid action stoobid"
            return rt
    except:
        rt += "action not found stoobid"
        return rt
    return rt
@client.command("homework","*Homework command*\nHow to use:\nTo add homework to the system, do \n/homework create <date> <subject> <name>\nEg.\n/homework create 18/1 admin sign forms\nIf you need to remove an entry for whatever reason, do \n/homework remove <date> <subject> <content>\nEg.\n/homework remove 18/1 admin sign form\nLastly, to show saved homework, do\n/homework show <date> <subject>\nEg.\n/homework show upcoming all\n the 'show' command allows 'upcoming','over','all as dates, in case you want more than a day's worth of homework.\nfor <subject> 'all' gives all subjects, and specific subject give their respective subjects\n please replace spaces in <subject> with an underscore(_)\n\nSidenote: I spent forever on this project, since the start of the year, please use it.\nAlso, report bugs with /feedback :)")
def hw(args,msg):
    client.send_message(homework(args,msg))
@client.on_ready
def change_chat():
    #client.set_chat("Hansome")
    client.set_chat("206 2k21 without cher")
    print("Ready")
client.run()
