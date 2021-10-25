import datetime as dt
import re
import codecs as cds
import requests
import os.path

def time_func(timestm='now'):
    if timestm == "now":
        return dt.datetime.utcnow()
    else:
        return (dt.datetime.now()-timestm)

def info_load(*path):
    logg=()
    for x in path:
        if os.path.isfile(x): 
            with cds.open (x,'r','ANSI') as file_log:
                logg += (file_log.read(),)
    return logg

def info_extract(*info):
    extract=()
    for x in info:
        extract += (re.findall(r'<166>([^I]*)Internet',x),)
        extract += (re.findall(r'<166>([^d]*.)',x),)
        extract += (re.findall(r'<164>([^R]*\S*.\S*.\S*)',x),)
    return extract

def path_construct(path='c:\\ProgramData\\Paessler\\PRTG Network Monitor\\Trap Database\\sensor 2149\\', sensor_id='2149'):
    date_fold = [time_func('now'), time_func('now')-dt.timedelta(minutes=1)]
    if date_fold[0].hour == date_fold[1].hour:
        del date_fold[1]
    path_res=[]
    for x in date_fold:
        path_hour = (('0'+str(x.hour)) if x.hour <10 else str(x.hour))
        path_date = str(x.year)+str(x.month)+str(x.day)
        path_res.append(path+path_date+'\\'+sensor_id+'_'+path_date+path_hour+'.evl')
    return path_res   

def teleg_prep(*extract):
    for x in extract:
        for y in x:
            messa=re.findall(r'(^\S*.\S*.\S*.\S*)',y)
            for z in messa:
                differ=time_func(dt.datetime.strptime(z, '%b %d %Y %H:%M:%S'))
                if differ.seconds<70:
                    r = requests.get(f'https://api.telegram.org/bot2075871995:XXXX/sendMessage?chat_id=-1001715868802&text={y}')
                    

def runner():
    path=path_construct()
    logg=info_load(*path)
    extract=info_extract (*logg)
    message_teleg=teleg_prep(*extract)

if __name__== "__main__":
    runner()