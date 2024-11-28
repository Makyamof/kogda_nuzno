from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)
db_file = 'visit_data.json'

def read_visit_data():
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def write_visit_data(data):
    with open(db_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_robot', methods=['POST'])
def check_robot():
    real_ip = request.headers.get('X-Real-IP') or request.headers.get('X-Forwarded-For') or request.remote_addr
    visit_data = read_visit_data()
    visit = {
        'ip_address': real_ip,
        'visit_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'referrer': request.referrer,
        'user_agent': request.user_agent.string,
        'country': 'Unknown',
        'uuid': request.args.get('uuid')
    }
    visit_data.append(visit)
    write_visit_data(visit_data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
