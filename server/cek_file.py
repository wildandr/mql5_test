import os

# Path ke file command.txt
COMMAND_FILE_PATH = r"C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files\command.txt"

# Fungsi untuk mencoba berbagai encoding dan membaca file
def test_read_file_with_encodings():
    encodings_to_test = ['utf-8', 'utf-16', 'ISO-8859-1', 'latin1', 'cp1252', 'windows-1252', 'ascii']
    successful_encodings = []

    # Cek apakah file ada
    if os.path.exists(COMMAND_FILE_PATH):
        for encoding in encodings_to_test:
            try:
                # Coba buka dan baca file dengan encoding yang diuji
                with open(COMMAND_FILE_PATH, 'r', encoding=encoding) as file:
                    lines = file.readlines()  # Membaca semua baris di file
                    
                    if lines:
                        # Jika file berhasil dibaca, print hasilnya
                        print(f"Berhasil membaca file dengan encoding: {encoding}")
                        for line in lines:
                            print(f"Perintah yang dibaca: {line.strip()}")
                        successful_encodings.append(encoding)
                        
            except UnicodeDecodeError:
                print(f"Error: Tidak dapat membaca file dengan encoding {encoding}")
            except Exception as e:
                print(f"Error dengan encoding {encoding}: {e}")
        
        # Jika ada encoding yang berhasil, tampilkan
        if successful_encodings:
            print("\nEncodings yang berhasil digunakan untuk membaca file:")
            for encoding in successful_encodings:
                print(f"- {encoding}")
        else:
            print("\nTidak ada encoding yang berhasil membaca file.")
    else:
        print(f"File {COMMAND_FILE_PATH} tidak ditemukan.")

# Menjalankan fungsi untuk menguji berbagai encoding
test_read_file_with_encodings()
