from flask import Flask, request, jsonify
import trade_module as trade_module  # Import modul yang telah dibuat sebelumnya
import requests

app = Flask(__name__)

# Daftar URL server lain yang ingin menerima order
other_servers = [
    # Tambahkan URL server lain jika diperlukan
]

@app.route('/')
def home():
    return "Flask Trading API is Running!"

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()

    # Validasi parameter input
    required_params = ['symbol', 'max_risk', 'stop_loss', 'order_type']
    for param in required_params:
        if param not in data:
            return jsonify({"success": False, "message": f"Parameter '{param}' tidak ditemukan."}), 400

    symbol = data['symbol']
    max_risk = data['max_risk']
    stop_loss = data['stop_loss']
    order_type = data['order_type'].lower()
    order_price = data.get('order_price')  # Opsional

    # Validasi tipe order
    valid_order_types = ['buy', 'sell', 'buy_limit', 'sell_limit']
    if order_type not in valid_order_types:
        return jsonify({"success": False, "message": "Tipe order tidak valid. Gunakan 'buy', 'sell', 'buy_limit', atau 'sell_limit'."}), 400

    # Eksekusi order di server utama
    result = trade_module.trade(symbol, max_risk, stop_loss, order_type, order_price)

    if result["success"]:
        # Kondisi khusus untuk simbol tertentu
        if data['symbol'] == "NDX100":
            data['symbol'] = "NAS100"
        data['symbol'] = f"{data['symbol']}.raw"

        # Kirimkan request ke server lain
        for server_url in other_servers:
            try:
                response = requests.post(server_url, json=data, timeout=5)  # Timeout 5 detik
                if response.status_code != 200:
                    print(f"Error saat mengirim request ke {server_url}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Exception saat mengirim request ke {server_url}: {e}")

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
