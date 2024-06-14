from flask import Flask, request, render_template, jsonify
import json
app = Flask(__name__, template_folder='templates')
data = {'temp': [], 'hum': []}

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        content = request.get_json()

        temp = content['temp']
        hum = content['hum']

        data['temp'] = temp
        data['hum'] = hum

        print(f"Received data: temperature = {temp}, humidity = {hum}")
        return jsonify({'success': True})
    except Exception as e:
        print(f'Error receiving data : {str(e)}')
        return jsonify({'success': False, 'error':str(e)})

@app.route('/')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)