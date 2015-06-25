#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, flash, url_for, render_template
from flask import request, redirect, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy import text

from datetime import datetime
import time
import copy
import string
import os, re
import sys

#搭建FLASK框架，配置SQLALCHEMY数据库
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
#app.config.from_pyfile('app.cfg')
#app.debug = True
app.debug = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/controls.sqlite3' % (os.path.dirname(__file__))
SQLALCHEMY_ECHO = False

'''
使用三个数据库

login 用来存储登录信息
request 用来存储用户请求记录
ServerState 用来存储中央空调状态
'''
databases = {
    'requests': 'sqlite:///requests.sqlite3',
    'login': 'sqlite:///login.sqlite3',
    'ServerState': 'sqlite:///ServerState.sqlite3'
}
app.config['SQLALCHEMY_BINDS'] = databases

db = SQLAlchemy(app)
app._static_folder = "/Users/macx/Desktop/大空调/myproject/static/"


#定义全局变量初始值如下

'''


'''
room_id = 724

client_state = "off"
client_mode = "cold"
client_power = 0.8
room_cost = 0

server_state = "off"
server_mode = "cold"
server_state_temp = "off"
server_mode_temp = "cold"
report_search = "day"

queue = []
def ClientWork(start, room_id):
    global queue
    if(start == "on/refresh"):
        for element in queue:
            temp_id = element
            if(temp_id == room_id):
                return "on"
        queue.append(room_id)
        if(len(queue) > 10):
            queue.pop(-1)
            return "waiting"
        else:
            return "on"
    if(start == "off"):
        for element in queue:
            temp_id = element
            if(temp_id == room_id):
                queue.remove(room_id)
                return "off"
        return "off"
    return "queue failure"


class login(db.Model):
    __tablename__ = "login"
    __bind_key__ = "login"
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(80))
    room_in_date = db.Column(db.DateTime)
    
    def __init__(self, room_id):
        self.room_id = room_id
        self.room_in_date = datetime.now()
    
    def __repr__(self):
        return '<room_id: %r>' % self.room_id

class requests(db.Model):
    
    __tablename__ = "requests"
    __bind_key__ = "requests"
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(80))
    room_cost = db.Column(db.String(80))
    room_temp = db.Column(db.String(80))
    room_state = db.Column(db.String(80))
    room_mode = db.Column(db.String(80))
    room_power = db.Column(db.String(80))
    room_date = db.Column(db.String(80))
    
    def __init__(self, room_id, room_cost, room_temp, room_state, room_mode, room_power, room_date):
        self.room_id = room_id
        self.room_cost = room_cost
        self.room_temp = room_temp
        self.room_state = room_state
        self.room_mode = room_mode
        self.room_power = room_power
        self.room_date = room_date

    def __repr__(self):
        return '<room_id: %r> <room_cost: %r> <room_temp: %r> <room_state: %r> <room_mode: %r> <room_power: %r> <room_date: %r>' % self.room_id, self.room_cost, self.room_temp, self.room_state, self.room_mode, self.room_power, self.room_date


class ServerState(db.Model):
    __tablename__ = "ServerState"
    __bind_key__ = "ServerState"
    
    id = db.Column(db.Integer, primary_key=True)
    room_state = db.Column(db.String(80))
    room_mode = db.Column(db.String(80))
    room_date = db.Column(db.String(80))

    def __init__(self, room_state, room_mode, room_date):
        self.room_state = room_state
        self.room_mode = room_mode
        self.room_date = room_date
    
    def __repr__(self):
        return '<room_state: %r> <room_mode: %r> <room_date: %r>' % self.room_state, self.room_mode, self.room_date

def restart():
     db.create_all()
     db.session.query(login).delete()
     db.session.commit()
     db.session.query(requests).delete()
     db.session.commit()
     db.drop_all()

#restart()

@app.route('/', methods = ['GET', 'POST'])
def index():
    global queue
    if request.method == 'POST':
        room_id = request.form['room_id']
    
        if(len(room_id) == 3 and (room_id.isdigit())):
            search_result = 1
            #db.create_all()
            search_a = login.query.all()
            #search_a = db.session.query(login).all()
            #db.session.query(login).delete()
            #db.session.commit()
            print search_a
            for query_room in search_a:
                if query_room.room_id == room_id:
                    search_result = 0
        
            if(search_result):
                #db.create_all()
                db.create_all()
                db.create_all(bind='login')
                logins = login(room_id)
                db.session.add(logins)
                db.session.commit()
                if room_id == '000':
                    return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state))
                else:
                    return redirect(url_for('client', room_cost = room_cost, room_id = room_id, client_state = client_state,client_mode = client_mode, client_power = client_power))
            else:
                return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/server/%<server_mode>%<server_state>%<room_id>', methods = ['GET', 'POST'])
def server(room_id=room_id, server_mode=server_mode, server_state=server_state):
    global queue
    global server_state_temp
    global server_mode_temp
    
    if request.method == 'POST':

        server_mode = request.form.get('mode', 'form')
        server_state = request.form.get('start', 'form')
        
        server_restart = request.form.get('restart', 'form1')
        if server_restart == "restart":
            restart()
            server_state = "off"
            server_mode = "cold"

        #print "server_state:::" + server_state

        if server_state != "off":
            if len(queue) == 0 or len(queue) >= 10:
                server_state = "waiting"
            else:
                check_waiting = 1
                for element in queue:
                    watch_room = requests.query.filter_by(room_id = element).all()
                    if watch_room[len(watch_room) -1].room_state != "waiting":
                        check_waiting = 0
                if check_waiting == 1 :
                    server_state = "waiting"
                else:
                    server_state = "on"
    
        db.create_all()
        db.create_all(bind='ServerState')
        #date = str(datetime.now())
        date = datetime.now()
        serverstates = ServerState(server_state, server_mode, date)
        db.session.add(serverstates)
        db.session.commit()
        
        db.create_all()
        db.create_all(bind='requests')
        #room_requestss = db.session.query(requests).all()
        #query_desc = ServerState.query.order_by(desc(ServerState.room_date)).limit(3).all()
        room_requestss = requests.query.order_by(requests.room_date.desc()).limit(10).all()
        db.session.commit()
        
        if len(room_requestss) == 0:
            room_requestss.append(requests('000', '0', '0', server_state, server_mode, '0', datetime.now()))

        return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state, room_requestss=room_requestss[0].room_id))#wocaolozheshiwei
    else:
        db.create_all()
        db.create_all(bind='requests')
        room_requestss = db.session.query(requests).all()
        db.session.commit()
        
        if len(room_requestss) == 0:
            room_requestss.append(requests('000', '0', '0', server_state, server_mode, '0', datetime.now()))
        
        return render_template('server.html', room_id=room_id, server_mode=server_mode, server_state= server_state, room_requestss=room_requestss)

@app.route('/watch/', methods = ['GET', 'POST'])
def watch():

    room_watch = []
    for element in queue:
        watch_room = requests.query.filter_by(room_id = element).all()
        watch_room = watch_room[len(watch_room) -1]
        
        room_last_time = watch_room.room_date
        room_last_time= datetime.strptime(room_last_time, "%Y-%m-%d %H:%M:%S.%f")
        if (datetime.now() - room_last_time).seconds > 20 :
            client_state = ClientWork("off", room_id)
            db.create_all()
            db.create_all(bind='requests')
            watch_room.room_state = client_state
            db.session.add(watch_room)
            db.session.commit()
    
            logins = login.query.filter_by(room_id = watch_room.room_id).all()
            for element in logins:
                db.session.delete(element)
            db.session.commit()
        
        room_watch.append(watch_room)
    
    return render_template('watch.html', room_watch=room_watch)

#@app.route('/reportsheet/%<report_search>%', methods = ['GET', 'POST'])
#def reportsheet(report_search = report_search):

@app.route('/reportsheet/', methods = ['GET', 'POST'])
def reportsheet():
    
    if request.method == 'POST':
        
        report_search = request.form.get('search', 'form')
        search_date = datetime.now()
        
        room_requestss = requests.query.order_by(requests.room_id).all()
        if report_search == "month":
            for element in room_requestss:
                element_time = element.room_date
                element_time = datetime.strptime(element_time, "%Y-%m-%d %H:%M:%S.%f")
                if element_time.month != search_date.month:
                    room_requestss.remove(element)
        elif report_search == "week":
            for element in room_requestss:
                element_time = element.room_date
                element_time = datetime.strptime(element_time, "%Y-%m-%d %H:%M:%S.%f")
                if element_time.isocalendar()[1] != search_date.isocalendar()[1]:
                    room_requestss.remove(element)
        elif report_search == "day":
            for element in room_requestss:
                element_time = element.room_date
                element_time = datetime.strptime(element_time, "%Y-%m-%d %H:%M:%S.%f")
                if element_time.isocalendar()[1] != search_date.isocalendar()[1] or element_time.isocalendar()[2] != search_date.isocalendar()[2]:
                    room_requestss.remove(element)
        
        room_new_request = []
        for element in room_requestss:
            if len(room_new_request) > 0 :
                element_new = room_new_request[len(room_new_request) - 1]
                if element_new.room_state == "on":
                    if element.room_cost != element_new.room_cost or element.room_temp != element_new.room_temp:
                        room_new_request.append(element)
                elif element_new.room_state == "waiting":
                    if element.room_state == "on" or element.room_state == "off":
                        room_new_request.append(element)
                elif element_new.room_state == "off":
                    if element.room_state == "on" or element.room_state == "waiting":
                        room_new_request.append(element)
            else:
                room_new_request.append(element)
        room_requestss = room_new_request

        total_report = []
        room_report = []
        turn_on = 0
        cost_sum = 0
        for element in room_requestss:
            if len(room_report) > 0 :
                if element.room_id != room_report[0]:
                    room_report[1] = cost_sum
                    total_report.append(room_report)
                    room_report = []
                    cost_sum = 0
                    turn_on = 0
                    if element.room_state == "on" or element.room_state == "off":
                        turn_on = turn_on + 1
                    room_report.append(element.room_id)
                    room_report.append(cost_sum)
                    room_report.append(turn_on)
                else:
                    room_request_cost = string.atof(element.room_cost)
                    if (room_request_cost - room_report[1]) >= 0:
                        cost_sum = cost_sum + room_request_cost - room_report[1]
                        room_report[1] = room_request_cost
                    else :
                        room_report[1] = room_request_cost
                    
                    if element.room_state == "on" or element.room_state == "off":
                        turn_on = turn_on + 1
                    room_report[2] = turn_on
                
                if element.room_date == room_requestss[len(room_requestss) - 1].room_date:
                    total_report.append(room_report)
            else:
                room_report.append(element.room_id)
                room_report.append(cost_sum)
                if element.room_state == "on" or element.room_state == "off":
                    turn_on = turn_on + 1
                room_report.append(turn_on)

        #return redirect(url_for('reportsheet', report_search=report_search, room_requestss=room_requestss, report=report))
        return render_template('reportsheet.html', room_requestss=room_requestss, report=total_report, report_search = report_search)
       
    else:
        db.create_all()
        db.create_all(bind='requests')
        room_requestss = requests.query.order_by(requests.room_date.desc()).limit(100).all()
        db.session.commit()
        
        #return render_template('reportsheet.html', room_requestss=room_requestss)
        return render_template('reportsheet.html')


@app.route('/roomstatic/', methods = ['GET', 'POST'])
def roomstatic():
    if request.method == 'POST':
        search_scope = request.form.get('search', 'form')
        
        db.create_all()
        db.create_all(bind='requests')
        room_requestss = requests.query.order_by(requests.room_date.desc()).limit(100).all()
        db.session.commit()

        return render_template('static.html', room_requestss=room_requestss)
    else:
        
        db.create_all()
        db.create_all(bind='requests')
        room_requestss = requests.query.order_by(requests.room_date.desc()).limit(100).all()
        db.session.commit()
        
        return render_template('static.html', room_requestss=room_requestss)

@app.route('/client/$<room_cost>%<client_mode>%<client_power>%<client_state>%<room_id>', methods = ['GET', 'POST'])
def client(room_id=room_id, room_cost=room_cost, client_state=client_state, client_mode = client_mode, client_power = client_power):
    
    client_temp = 25
    client_start = "off"
    global server_state_temp
    global server_mode_temp
    
    if request.method == 'POST':
        room_cost = request.form.get('client_cost', 'form')
        client_power = request.form.get('power', 'form')
        client_mode = request.form.get('mode', 'form')
        client_temp = request.form.get('temp', 'form')
        client_aim_temp = request.form.get('aim_temp', 'form')
        client_state = request.form.get('room_state', 'form')
        client_start = request.form.get('start', 'form')
        date = str(datetime.now())
        #date_close = request.form.get('date', 'form')

        db.create_all()
        db.create_all(bind='ServerState')
        query_desc = ServerState.query.order_by(desc(ServerState.room_date)).limit(3).all()
        db.session.commit()
        
        if len(query_desc) == 0:
            client_state = "off"
        else:
            server_state_temp = query_desc[0].room_state
            server_mode_temp = query_desc[0].room_mode
            
            if(server_state_temp == "waiting" or server_state_temp == "on"):
                if(client_mode != server_mode_temp):
                    client_state = "off_mode"
                elif client_start == 'form':
                    if client_mode == "cold" and client_temp <= client_aim_temp and client_state == "on":
                        client_state = "waiting"
                    elif client_mode == "warm" and client_temp >= client_aim_temp and client_state == "on":
                        client_state = "waiting"
                elif(client_start != 'form'):
                    client_state=ClientWork(client_start, room_id)
                else:
                    client_state = "off"
            else:
                client_state = "off"

        db.create_all()
        db.create_all(bind='requests')
        request_room = requests(room_id, room_cost, client_temp, client_state, client_mode, client_power, date)
        db.session.add(request_room)
        db.session.commit()
    
        return redirect(url_for('client', room_id = room_id, room_cost = room_cost, client_state = client_state,client_mode = client_mode, client_power = client_power))
        
    else:
        return render_template('client.html', room_id=room_id, room_cost = room_cost, client_state=client_state,client_mode = client_mode, client_power = client_power)


if __name__ == '__main__':
        app.run(debug = False, host = '0.0.0.0', port = 5000)
























