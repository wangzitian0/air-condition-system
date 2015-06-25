#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, flash, url_for, render_template
from flask import request, redirect, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
app._static_folder = "/Users/macx/Desktop/大空调/myproject/static/"

#imagepath = os.path.join(os.getcwd(), "static/images")

room_id = 724
server_mode = "cold"
client_state = "off"
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



class controls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(80))
    room_in_date = db.Column(db.DateTime)
    
    def __init__(self, room_id, room_user):
        self.room_id = room_id
        self.room_in_date = datetime.now()
    
    def __repr__(self):
        return '<User %r>' % self.room_id


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        room_id = request.form['room_id']
        '''
            db.create_all()
            control = controls(room_id, room_user
            db.session.add(control)
            db.session.commit()
        '''
        if(len(room_id) == 3 and (room_id.isdigit())):
            if room_id == '000'  :
                #print "sadasd"
                return redirect(url_for('server', room_id = room_id))
            else:
                return redirect(url_for('client', room_id = room_id, client_state = client_state,client_mode = client_mode, client_power = client_power))
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/server/<room_id>', methods = ['GET', 'POST'])
def server(room_id=room_id):
    
    if request.method == 'POST':
        server_mode = request.form.get('mode', None)
        start = request.form.get('start', None)
        temp_value = request.form.get('temp', 'form1')
        print temp_value
        
        return render_template('server.html', room_id=room_id)
    else:
        return render_template('server.html', room_id=room_id)

@app.route('/log')
def log():
    return render_template('log.html')


@app.route('/client/%<client_mode>%<client_power>%<client_state>%<room_id>', methods = ['GET', 'POST'])
def client(room_id=room_id, client_state=client_state, client_mode = client_mode, client_power = client_power):
    #client_state = "off"
    #client_mode = "cold"
    client_temp = 25
    client_start = "off"
    #client_power = 0.8
    if request.method == 'POST':
        
        client_power = request.form.get('power', 'form')
        client_mode = request.form.get('mode', 'form')
        client_temp = request.form.get('temp', 'form')
        client_start = request.form.get('start', 'form')
        date = request.form.get('date', 'form')
        
        if(client_mode != server_mode):
            client_state = "off_mode"
            return render_template('client.html', room_id=room_id, client_state=client_state,client_mode = client_mode, client_power = client_power)
        else:
            client_state =ClientWork(client_start, room_id)
            client_mode = client_mode
            client_power = client_power
            
            #return render_template('client.html', room_id=room_id, client_state=client_state)
            return redirect(url_for('client', room_id = room_id, client_state = client_state,client_mode = client_mode, client_power = client_power))
    else:
        return render_template('client.html', room_id=room_id, client_state=client_state,client_mode = client_mode, client_power = client_power)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
























