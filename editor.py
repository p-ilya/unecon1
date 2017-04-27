import sqlite3 as sq
from datetime import datetime, timedelta

con = sq.connect('db_test.sqlite3')

def data_input(l=None):
    if not l:
        base_date = datetime.strptime(input("Lesson date('%Y-%m-%d'): "),'%Y-%m-%d')
        name = input("Lesson name: ")
        ltime = input("Lesson time: ")
        group = input("Group: ")
        t_id = int(input("Teacher ID: "))
        aud = input("Place: ")
    else:
        ldate,name,ltime,group,t_id,aud = l
        base_date = datetime.strptime(ldate,'%Y-%m-%d')
    print("""Предварительные данные:
Дата/время: {0} {2}
Группа: {3} Место: {5}
ID преп: {4}
название: {1}""".format(base_date,name,ltime,group,t_id,aud))
    m = input("Looks right? Y/N")
    if m in ('Y','y'):
        return (base_date,name,ltime,group,t_id,aud)
    elif m in ('N','n'):
        data_input()
    else:
        print('shit happens')
        return 0
    
def new_lesson(l=None):
    with con:
        con.row_factory = sq.Row
        cur = con.cursor()

        if not l:
            base_date,name,ltime,group,t_id,aud = data_input()
        else:
            base_date,name,ltime,group,t_id,aud = data_input(l)

        cur.execute('INSERT INTO main_lesson(lDate,lName,lTime,lGroup_id,lTeacher_id,lAud) VALUES(?,?,?,?,?,?)',
                        (base_date.strftime('%Y-%m-%d'),
                         name,
                         ltime,
                         group,
                         t_id,
                         aud))
        
        m = input("Make regular? Y/N")
        if m in ("N", "n"):
            print("saved single lesson")
            return True
        elif m in ("Y","y"):
            stop = datetime.strptime(input("Stop date('%Y-%m-%d'): "),'%Y-%m-%d')
            iterdate = base_date + timedelta(days=14)
            
            while iterdate < stop:
                cur.execute('INSERT INTO main_lesson(lDate,lName,lTime,lGroup_id,lTeacher_id,lAud) VALUES(?,?,?,?,?,?)',
                            (iterdate.strftime('%Y-%m-%d'),
                             name,
                             ltime,
                             group,
                             t_id,
                             aud))
                iterdate += timedelta(days=14)
            print('saved regular lesson')
            return True
'''            
while 1:
    new_lesson()
    c = input('more? ')
    if c=='N': break
'''
is_1301 = [
    ('2017-02-16','Разработка программных приложений средствами mySAP','09:00 - 10:35','ИС-1301',5,'Г-2020'),
    ('2017-02-23','Разработка программных приложений средствами mySAP','09:00 - 10:35','ИС-1301',5,'Г-2020'),
    ('2017-02-16','Разработка программных приложений средствами mySAP','10:50 - 12:25','ИС-1301',5,'Г-2020'),
    ('2017-02-23','Разработка программных приложений средствами mySAP','10:50 - 12:25','ИС-1301',5,'Г-2020'),
    ('2017-02-16','Разработка программных приложений средствами mySAP','12:40 - 14:15','ИС-1301',5,'Г-2020'),
    ('2017-02-23','Разработка программных приложений средствами mySAP','12:40 - 14:15','ИС-1301',5,'Г-2020'),
    ('2017-02-20','Информационная безопасность и защита информации','12:40 - 14:15','ИС-1301',16,'Г-2064'),
    ('2017-02-20','Информационная безопасность и защита информации','14:30 - 16:00','ИС-1301',16,'Г-0001'),
    ('2017-02-20','Информационная безопасность и защита информации','16:10 - 17:40','ИС-1301',16,'Г-0001'),
    ('2017-02-27','Информационная безопасность и защита информации','12:40 - 14:15','ИС-1301',16,'Г-2064'),
    ('2017-02-27','Информационная безопасность и защита информации','14:30 - 16:00','ИС-1301',16,'Г-0001'),
    ('2017-02-27','Информационная безопасность и защита информации','16:10 - 17:40','ИС-1301',16,'Г-0001'),
    ('2017-02-21','Разработка программных приложений средствами mySAP','16:10 - 17:40','ИС-1301',5,'Г-2020'),
    ('2017-02-21','Разработка программных приложений средствами mySAP','17:50 - 19:20','ИС-1301',5,'Г-2020'),
    ('2017-02-28','Разработка программных приложений средствами mySAP','16:10 - 17:40','ИС-1301',5,'Г-2020'),
    ('2017-02-28','Разработка программных приложений средствами mySAP','17:50 - 19:20','ИС-1301',5,'Г-2020'),
    ('2017-02-22','Мультимедиа технологии','14:30 - 16:00','ИС-1301',6,'Г-2025'),
    ('2017-02-22','Мультимедиа технологии','16:10 - 17:40','ИС-1301',6,'Г-2025'),
    ('2017-02-22','Мультимедиа технологии','17:50 - 19:20','ИС-1301',6,'Г-2025'),
    
]

llrr = [('2017-03-01','Мультимедиа технологии','14:30 - 16:00','ИС-1301',6,'Г-2025'),
    ('2017-03-01','Мультимедиа технологии','16:10 - 17:40','ИС-1301',6,'Г-2025'),
    ('2017-03-01','Мультимедиа технологии','17:50 - 19:20','ИС-1301',6,'Г-2025'),]

for ls in llrr:
    new_lesson(l=ls)
