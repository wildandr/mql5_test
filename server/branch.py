from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Path ke file command.txt dan magic_id_counter.txt
COMMAND_FILE_PATH = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\command.txt"
MAGIC_ID_COUNTER_PATH = 'magic_id_counter.txt'

# Fungsi untuk membaca magicID terakhir dari file
def read_last_magic_id():
    if os.path.exists(MAGIC_ID_COUNTER_PATH):
        with open(MAGIC_ID_COUNTER_PATH, 'r') as file:
            magic_id = file.read().strip()
            return int(magic_id) if magic_id.isdigit() else 0
    else:
        return 0

# Fungsi untuk menyimpan magicID terbaru ke file
def write_last_magic_id(magic_id):
    with open(MAGIC_ID_COUNTER_PATH, 'w') as file:
        file.write(str(magic_id).zfill(5))  # Menyimpan magicID dengan 5 digit (contoh: 00001)

# Fungsi untuk menulis perintah ke file command.txt dengan encoding UTF-8
def write_to_command_file(command):
    try:
        print(f"Menulis perintah ke file: {command}")  # Debugging: Menampilkan perintah yang akan ditulis
        with open(COMMAND_FILE_PATH, 'w', encoding='utf-16') as file:
            file.write(command + '\n')
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

# Endpoint untuk menerima perintah dan menulis ke command.txt
@app.route('/send-command', methods=['POST'])
def send_command():
    # Ambil data JSON yang dikirimkan oleh client
    data = request.get_json()

    # Debugging: Tampilkan data yang diterima
    print(f"Data yang diterima di server cabang: {data}")

    # Cek apakah data yang diperlukan ada
    if all(k in data for k in ('symbol', 'orderType', 'price', 'lotSize', 'stopLoss', 'takeProfit')):
        # Ambil magicID terakhir dan increment
        last_magic_id = read_last_magic_id()
        magic_id = last_magic_id + 1

        # Pastikan magicID tidak melebihi 99999
        if magic_id > 99999:
            return jsonify({"status": "error", "message": "Magic ID limit reached (99999)."}), 400

        # Format perintah sesuai dengan struktur EA
        command = f"{data['symbol']} {data['orderType']} {data['price']} {magic_id} {data['lotSize']} {data['stopLoss']} {data['takeProfit']}"

        # Debugging: Menampilkan perintah yang akan ditulis
        print(f"Perintah yang akan ditulis: {command}")

        # Tulis perintah ke file command.txt
        if write_to_command_file(command):
            # Simpan magicID terbaru
            write_last_magic_id(magic_id)
            return jsonify({"status": "success", "message": "Command added to file."}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to write to file."}), 500
    else:
        print("Data tidak lengkap di server cabang.")
        return jsonify({"status": "error", "message": "Missing required fields in the request."}), 400

# Endpoint untuk mengecek apakah server berjalan
@app.route('/')
def home():
    return "Flask Server is running."

if __name__ == '__main__':
    # Jalankan server di localhost dengan port 5005
    app.run(debug=True, host='0.0.0.0', port=5005)
