from flask import Flask, request, jsonify, send_from_directory
import csv
import os

app = Flask(__name__, static_folder='.')

CSV_FILE = 'registrations.csv'
CSV_HEADERS = ['name', 'squadName', 'mobileNumber', 'squadNo', 'timestamp']

# Ensure the CSV file exists and has headers
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

initialize_csv()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    squad_name = data.get('squadName')
    mobile_number = data.get('mobileNumber')
    squad_no = data.get('squadNo')
    timestamp = data.get('timestamp')

    if not all([name, squad_name, mobile_number, squad_no, timestamp]):
        return jsonify({'message': 'Missing data'}), 400

    # Check for duplicate mobile number
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['mobileNumber'] == mobile_number:
                return jsonify({'message': 'Mobile number already registered'}), 409

    # Append to CSV
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writerow({
            'name': name,
            'squadName': squad_name,
            'mobileNumber': mobile_number,
            'squadNo': squad_no,
            'timestamp': timestamp
        })

    return jsonify({'message': 'Registration successful', 'squadNo': squad_no}), 200

if __name__ == '__main__':
    app.run(debug=True)