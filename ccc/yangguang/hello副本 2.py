#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, flash, url_for, render_template
from flask import request, redirect, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy import text
import os, re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
#app.config.from_pyfile('app.cfg')


app.debug = True
'''
databases = {
    'login': 'sqlite:///login.db',
    'requests': 'sqlite:///requests.db',
    'ServerState': 'sqlite:///ServerState.db'
}
'''
databases = {
    'login': 'sqlite:///login.sqlite3',
    'requests': 'sqlite:///requests.sqlite3',
    'ServerState': 'sqlite:///ServerState.sqlite3'
}
app.config['SQLALCHEMY_BINDS'] = databases


db = SQLAlchemy(app)
app._static_folder = "/Users/macx/Desktop/大空调/myproject/static/"

room_id = 724
server_mode = "cold"
client_state = "off"
server_state = "off"

server_state_temp = "off"
server_mode_temp = "cold"
client_mode = "cold"
client_power = 0.8

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
        return "off failure"
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
    room_temp = db.Column(db.String(80))
    room_state = db.Column(db.String(80))
    room_mode = db.Column(db.String(80))
    room_power = db.Column(db.String(80))
    #room_date = db.Column(db.String(80))
    
    
    def __init__(self, room_id, room_temp, room_state, room_mode, room_power):
        #def __init__(self, room_id, room_temp, room_state, room_mode, room_power, room_date):
        self.room_id = room_id
        self.room_temp = room_temp
        self.room_state = room_state
        self.room_mode = room_mode
        self.room_power = room_power
    #self.room_date = room_date
    
    def __repr__(self):
        return '<room_id: %r> <room_temp: %r> <room_state: %r> <room_mode: %r> <room_power: %r> ' % self.room_id, self.room_temp, self.room_state, self.room_mode, self.room_power
    '''
    def __repr__(self):
        return '<room_id: %r> <room_temp: %r> <room_state: %r> <room_mode: %r> <room_power: %r> <room_date: %r>' % self.room_id, self.room_temp, self.room_state, self.room_mode, self.room_power, self.room_date
    '''

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

restart()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        room_id = request.form['room_id']
    
        if(len(room_id) == 3 and (room_id.isdigit())):
            search_result = 1
            db.create_all()
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
                logins = login(room_id)
                db.session.add(logins)
                db.session.commit()
                if room_id == '000':
                    return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state))
                else:
                    return redirect(url_for('client', room_id = room_id, client_state = client_state,client_mode = client_mode, client_power = client_power))
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
    
    db.create_all(bind='requests')
    room_requests=requests.query.all()
    db.drop_all(bind='requests')
    
    if request.method == 'POST':
        
        server_mode = request.form.get('mode', 'form')
        server_state = request.form.get('start', 'form')

        if server_state == "on" or server_state == "waiting":
            if len(queue) == 0 or len(queue) >= 10:
                server_state = "waiting"
            else:
                server_state = "on"
    
        db.create_all(bind='ServerState')
        date = str(datetime.now())
        serverstates = ServerState(server_state, server_mode, date)
        db.session.add(serverstates)
        db.session.commit()
        db.drop_all(bind='ServerState')
        
        #return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state))
        #return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state, room_request=requests.query.all()))
        return redirect(url_for('server', room_id=room_id, server_mode=server_mode, server_state= server_state, room_request=room_requests))
    else:
        #return render_template('server.html', room_id=room_id, server_mode=server_mode, server_state= server_state)
        #return render_template('server.html', room_id=room_id, server_mode=server_mode, server_state= server_state, room_request=requests.query.all())
        return render_template('server.html', room_id=room_id, server_mode=server_mode, server_state= server_state, room_request=room_requests)

@app.route('/log')
def log():
    return render_template('log.html')


@app.route('/client/%<client_mode>%<client_power>%<client_state>%<room_id>', methods = ['GET', 'POST'])
def client(room_id=room_id, client_state=client_state, client_mode = client_mode, client_power = client_power):
    #client_state = "off"
    #client_mode = "cold"
    client_temp = 25
    client_start = "off"
    global server_state_temp
    global server_mode_temp
    #client_power = 0.8
    
    if request.method == 'POST':
        client_power = request.form.get('power', 'form')
        client_mode = request.form.get('mode', 'form')
        client_temp = request.form.get('temp', 'form')
        client_start = request.form.get('start', 'form')
        date = request.form.get('date', 'form')
        
        db.create_all(bind='ServerState')
        #db.create_all()
        query_desc = ServerState.query.order_by(desc(ServerState.room_date)).limit(3).all()
        db.session.commit()
        server_state_temp = query_desc[0].room_state
        server_mode_temp = query_desc[0].room_mode
        db.drop_all(bind='ServerState')
        
        
        if(server_state_temp == "waiting" or server_state_temp == "on"):
            if(client_mode != server_mode_temp):
                client_state = "off_mode"
            else:
                client_state=ClientWork(client_start, room_id)
    
        db.create_all(bind='requests')
        #request_room = requests(room_id, client_temp, client_state, client_mode, client_power, date)
        request_room = requests(room_id, client_temp, client_state, client_mode, client_power)
        db.session.add(request_room)
        db.session.commit()
        db.drop_all(bind='requests')

        return redirect(url_for('client', room_id = room_id, client_state = client_state,client_mode = client_mode, client_power = client_power))
        
    else:
        return render_template('client.html', room_id=room_id, client_state=client_state,client_mode = client_mode, client_power = client_power)


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, host = '0.0.0.0', port = 5000)
























