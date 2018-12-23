import tkinter #импорт модуля оконного
import tkinter.ttk as ttk #движок для создания виджетов
import json #все данные базы в этом формеате чтобы работать с ней
from tinydb import TinyDB
import datetime
import time
import smtplib #связано с матаном
from email.mime.multipart import MIMEMultipart #(реализация в функциии  send_message)(*1*)
from email.mime.text import MIMEText


try:                                            # проверка подключения к серверу google чтобы проверить подключение к интернету.
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
if have_internet() == True:

    window = tkinter.Tk()#вызов окна
    frame = tkinter.Frame (window)#рамка
    frame.pack()
    
    maintext=''
    r = tkinter.Text(wrap=tkinter.NONE)
    dateY = tkinter.IntVar()
    dateM = tkinter.IntVar() #доп. переменные
    dateD = tkinter.IntVar()
    timeH = tkinter.IntVar()
    timeM = tkinter.IntVar()
    
    label = tkinter.Label(frame, text='Желаемая дата и время\n(год, месяц, день, час, минута)')
    label.grid(row=6,column=1)
    entrydateY = tkinter.Entry(frame, textvariable=dateY)
    entrydateY.grid(row=6,column=2)
    entrydateM = tkinter.Entry(frame, textvariable=dateM)
    entrydateM.grid(row=6,column=3)
    entrydateD = tkinter.Entry(frame, textvariable=dateD)#Переменные для даты и времени
    entrydateD.grid(row=6,column=4)
    entrytimeH = tkinter.Entry(frame, textvariable=timeH)
    entrytimeH.grid(row=6,column=5)
    entrytimeM = tkinter.Entry(frame, textvariable=timeM)
    entrytimeM.grid(row=6,column=6)
    
    label = tkinter.Label(frame, text='Введите текст заметки:')#заполняем информацией строчки
    label.grid(row=0,column=1)
    entry = tkinter.Entry(frame, textvariable=r)
    entry.grid(row=0,column=2)
    label = tkinter.Label(frame, text='Выберите категорию: ')
    label.grid(row=3,column=1)
    combobox = ttk.Combobox(frame, values=[u'Срочно', u'Саморазвитие',u'Учеба'],height=2)
    combobox.set(u'Срочно')
    combobox.grid(row=3,column=2)# 
    labelRek = tkinter.Label(frame, text='Выберите рекомендацию: ')
    labelRek.grid(row=4,column=1)
    comboboxRek = ttk.Combobox(frame, values=[u'Единоразовая', u'Раз в неделю',u'Раз в месяц'],height=2)
    comboboxRek.set(u'Единоразовая')
    comboboxRek.grid(row=4,column=2)
    

    def sendmail():#отправка сообщения на почту
        fromaddr = ""#моя почта
        mypass = ""#мой пароль
        toaddr = ""#кому отправлять 
     
        msg = MIMEMultipart()#(*1*)
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Напоминание "+str(combobox.get())
     
        body = str(entry.get())#тело письма
        msg.attach(MIMEText(body, 'plain'))
     
        server = smtplib.SMTP('smtp.mail.ru', 587)#подключение к mail серверу через порт
        server.starttls()
        server.login(fromaddr, mypass)# мы логинимся 
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)#отправим письмо с адреса на адрес с текстом
        server.quit()
    
        
    db = TinyDB('db.json')
    def read_table():# функция которая смотрит все напоминания которые были сохранены в базе. (*2*)
        maintext=''
        i=0
        while i<len(db):
            i=i+1
            maintext=maintext+db.get(eid=i)['Напоминание']+' '+db.get(eid=i)['категория']+' '+db.get(eid=i)['рекомендация']+'\n'
        return maintext
    def button():#кнопка
        try:
            sendtime=datetime.datetime(int(entrydateY.get()), int(entrydateM.get()), int(entrydateD.get()), int(entrytimeH.get()), int(entrytimeM.get())) 
            db.insert({'Напоминание': str(entry.get()), 'категория': str(combobox.get()), 'рекомендация': str(comboboxRek.get())}) #вставляем в tinydb нашу новую напоминалку (*2*)
            labelRes = tkinter.Label(frame, text=read_table())#вывод предыдущих напоминаний из tinydb 
            labelRes.grid(row=8,column=1)
        except:
            labelExcept = tkinter.Label(frame, text='Неверно введены данные, проверьте заполнение')#обработка исключений
            labelExcept.grid(row=10,column=3)
        time.sleep((sendtime - datetime.datetime.now()).seconds) #ожидание питона до назначенного времени отправки сообщения
        sendmail()
    button = tkinter.Button(frame, text='Добавить',command=button)
    button.grid(row=7,column=3)
    labelRes = tkinter.Label(frame, text=read_table())
    labelRes.grid(row=8,column=1)
    window.mainloop()
else:
    print("you are not connected to the internet!")

