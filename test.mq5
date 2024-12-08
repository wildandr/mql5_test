// Variabel global untuk menyimpan ID magic terakhir yang diproses
int lastMagicID = -1;

// Fungsi untuk membuka posisi berdasarkan perintah dari file
void OpenPositionFromCommand() {
   string filename = "command.txt";  // Nama file yang berisi perintah
   int fileHandle = FileOpen(filename, FILE_READ | FILE_TXT);
   
   // Cek apakah file berhasil dibuka
   if (fileHandle != INVALID_HANDLE) {
      string command;
      // Baca satu baris perintah dari file
      command = FileReadString(fileHandle);
      
      // Tutup file setelah membaca
      FileClose(fileHandle);

      // Pisahkan perintah berdasarkan spasi
      string parts[];
      StringSplit(command, ' ', parts); // Memisahkan string berdasarkan spasi

      if (ArraySize(parts) >= 7) {
         string symbol = parts[0];
         string orderType = parts[1];
         double price = StringToDouble(parts[2]);
         int magicID = StringToInteger(parts[3]);  // Mengambil ID magic dari file
         double lotSize = StringToDouble(parts[4]); // Mengambil ukuran lot dari file
         double sl = StringToDouble(parts[5]);      // Mengambil nilai Stop Loss dari file
         double tp = StringToDouble(parts[6]);      // Mengambil nilai Take Profit dari file

         // Cek apakah ID magic berbeda dari yang terakhir diproses
         if (magicID != lastMagicID) {
            int orderAction = -1;

            // Tentukan aksi berdasarkan tipe order
            if (orderType == "ORDER_TYPE_BUY_LIMIT") {
               orderAction = ORDER_TYPE_BUY_LIMIT;
            } else if (orderType == "ORDER_TYPE_SELL_LIMIT") {
               orderAction = ORDER_TYPE_SELL_LIMIT;
            } else if (orderType == "ORDER_TYPE_BUY") {
               orderAction = ORDER_TYPE_BUY;
            } else if (orderType == "ORDER_TYPE_SELL") {
               orderAction = ORDER_TYPE_SELL;
            }

            // Cek jika tipe order valid dan buka posisi
            if (orderAction != -1) {
               // Pastikan tidak ada posisi terbuka sebelumnya
               if (PositionSelect(symbol) == false) {
                  MqlTradeRequest request = {};
                  request.action   = TRADE_ACTION_PENDING;   // Pending order (limit order)
                  request.symbol   = symbol;
                  request.volume   = lotSize;                 // Ukuran lot yang dibaca dari file
                  request.type     = orderAction;            // Tipe order (buy limit, sell limit, buy, sell)
                  request.price    = price;                  // Harga limit yang ditentukan
                  request.deviation= 3;                      // Slippage
                  request.magic    = magicID;                // ID magic untuk mengidentifikasi posisi
                  request.sl= sl;                     // Stop Loss (SL)
                  request.tp= tp;                    // Take Profit (TP)
                  request.comment  = "Open Position from Command"; // Komentar

                  MqlTradeResult result = {};
                  if (!OrderSend(request, result)) {
                     Print("Error membuka posisi: ", result.retcode);
                  } else {
                     Print("Posisi berhasil dibuka: ", result.order);
                     lastMagicID = magicID;  // Update lastMagicID setelah berhasil membuka posisi
                  }
               } else {
                  Print("Posisi sudah ada di pasar.");
               }
            } else {
               Print("Perintah tidak valid: ", command);
            }
         } else {
            Print("ID magic belum berubah, tidak perlu membuka posisi baru.");
         }
      } else {
         Print("Format perintah tidak benar di command.txt");
      }
   } else {
      Print("Error membuka file. Error code: ", GetLastError());
   }
}

// Fungsi utama untuk membaca perintah dari file dan membuka posisi
void OnTick() {
   static double lastCheckedTime = 0;

   // Cek setiap 0.1 detik (0.1 detik = 0.1 * 1000 ms = 100 ms)
   if (TimeCurrent() - lastCheckedTime >= 0.1) {
      OpenPositionFromCommand();
      lastCheckedTime = TimeCurrent();  // Update waktu terakhir pengecekan
   }
}
