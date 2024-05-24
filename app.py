from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from factory import Factory
from security import SecuritySystem
from device import Device
from data_collector import DataCollector
import data_analyzer
from door import Door
import json

with open('rooms.json') as f:
    data = json.load(f)

factory = Factory()
for room_info in data['rooms']:
    room = Device(room_info['name'])
    room.status = room_info['light']
    room.temperature = room_info['temperature']
    factory.add_room(room)

security_system = SecuritySystem()
door = Door()  # Создаем экземпляр класса Door

data_collector = DataCollector(factory, security_system, door)  # Передаем экземпляр SecuritySystem

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/factory'
mongo = PyMongo(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['factory']
state_collection = db['state']


@app.route('/')
def home():
    analysis_results = data_analyzer.analyze()
    return render_template('index.html', factory=factory, security_system=security_system, analysis_results=analysis_results)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        room_name = request.form['room']
        temperature = int(request.form['temperature'])
        light = 'light' in request.form
        room = factory.get_room_by_name(room_name)
        if room:
            room.temperature = temperature
            room.status = light
            state_collection.update_one({'name': room_name}, {'$set': {'temperature': temperature, 'light': light}}, upsert=True)
    return render_template('admin.html', factory=factory, security_system=security_system)

@app.route('/toggle_light/<room_name>')
def toggle_light(room_name):
    room = factory.get_room_by_name(room_name)
    if room:
        room.toggle()
        state_collection.update_one({'name': room_name}, {'$set': {'light': room.status}}, upsert=True)
    return redirect(url_for('admin_panel'))

@app.route('/turn_on_all_lights')
def turn_on_all_lights():
    for room in factory.rooms:
        room.status = True
        state_collection.update_one({'name': room.name}, {'$set': {'light': True}}, upsert=True)
    return redirect(url_for('admin_panel'))

@app.route('/turn_off_all_lights')
def turn_off_all_lights():
    for room in factory.rooms:
        room.status = False
        state_collection.update_one({'name': room.name}, {'$set': {'light': False}}, upsert=True)
    return redirect(url_for('admin_panel'))

@app.route('/toggle_alarm')
def toggle_alarm():
    security_system.toggle_alarm()
    state_collection.update_one({'name': 'security_system'}, {'$set': {'alarm_on': security_system.alarm_on}}, upsert=True)
    return redirect(url_for('admin_panel'))

@app.route('/toggle_door')
def toggle_door():
    door.toggle()
    state_collection.update_one({'name': 'door'}, {'$set': {'is_closed': door.is_closed}}, upsert=True)
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    data_collector.collect_data()
    app.run(debug=True)