from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Daftar URL cabang (Server Flask cabang)
BRANCH_SERVERS = [
    "http://branch_server_1:5000/send-command",  # Ganti dengan alamat cabang yang sesuai
    "http://branch_server_2:5000/send-command",  # Ganti dengan alamat cabang yang sesuai
    "http://branch_server_3:5000/send-command"   # Ganti dengan alamat cabang yang sesuai
]

# Fungsi untuk mengirimkan data ke server cabang
def send_to_branch_server(data):
    responses = []
    for server_url in BRANCH_SERVERS:
        try:
            # Mengirimkan data ke server cabang dengan metode POST
            response = requests.post(server_url, json=data)
            responses.append({
                'server': server_url,
                'status_code': response.status_code,
                'response': response.json()
            })
        except Exception as e:
            responses.append({
                'server': server_url,
                'status_code': 'Failed',
                'error': str(e)
            })
    return responses

# Endpoint untuk menerima perintah dari klien dan meneruskannya ke server cabang
@app.route('/send-command-to-branches', methods=['POST'])
def send_command_to_branches():
    # Ambil data JSON yang dikirimkan oleh klien
    data = request.get_json()

    # Pastikan data yang diperlukan ada
    if all(k in data for k in ('symbol', 'orderType', 'price', 'lotSize', 'stopLoss', 'takeProfit')):
        # Kirim perintah ke server cabang
        branch_responses = send_to_branch_server(data)

        return jsonify({
            'status': 'success',
            'message': 'Command sent to all branch servers.',
            'responses': branch_responses
        }), 200
    else:
        return jsonify({"status": "error", "message": "Missing required fields in the request."}), 400

# Endpoint untuk mengecek apakah server utama berjalan
@app.route('/')
def home():
    return "Main Flask Server is running."

if __name__ == '__main__':
    # Jalankan server utama di localhost dengan port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)