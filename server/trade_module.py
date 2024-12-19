import MetaTrader5 as mt5

def trade(symbol, max_risk, stop_loss, order_type, order_price=None):
    """Fungsi untuk membuka trade (market atau limit) dengan validasi."""
    if not mt5.initialize():
        return {"success": False, "message": "Gagal menghubungkan ke MetaTrader 5"}

    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info or not symbol_info.visible:
        return {"success": False, "message": f"Simbol {symbol} tidak valid atau tidak terlihat"}

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        return {"success": False, "message": f"Gagal mendapatkan data tick untuk simbol {symbol}"}

    point = symbol_info.point
    min_distance = symbol_info.trade_stops_level * point

    # Debugging informasi harga pasar
    print(f"DEBUG: Harga Bid: {tick.bid}, Harga Ask: {tick.ask}, Minimum Distance: {min_distance}")

    # Tentukan harga untuk market order
    if order_type in ["buy", "sell"]:
        if order_type == "buy":
            order_price = tick.ask
        elif order_type == "sell":
            order_price = tick.bid
        print(f"DEBUG: Market order ({order_type}) pada harga {order_price}")

    # Validasi harga untuk limit orders
    elif order_type == "buy_limit":
        if order_price is None or order_price >= tick.bid - min_distance:
            print(f"DEBUG: Harga Buy Limit {order_price} terlalu dekat dengan Bid {tick.bid}, menyesuaikan...")
            order_price = tick.bid - min_distance - 10 * point  # Adjusting to a valid price
            print(f"DEBUG: Harga Buy Limit disesuaikan ke {order_price}")

    elif order_type == "sell_limit":
        if order_price is None or order_price <= tick.ask + min_distance:
            print(f"DEBUG: Harga Sell Limit {order_price} terlalu dekat dengan Ask {tick.ask}, menyesuaikan...")
            order_price = tick.ask + min_distance + 10 * point  # Adjusting to a valid price
            print(f"DEBUG: Harga Sell Limit disesuaikan ke {order_price}")

    # Hitung Stop Loss dalam poin
    sl_points = abs(order_price - stop_loss) / point
    pip_value = symbol_info.trade_contract_size * point
    lot_size = max_risk / (sl_points * pip_value)
    lot_size = round(min(max(lot_size, symbol_info.volume_min), symbol_info.volume_max), 2)

    # Debugging ukuran lot
    print(f"DEBUG: Lot Size: {lot_size}")

    # Siapkan request untuk order
    request = {
        "action": mt5.TRADE_ACTION_DEAL if order_type in ["buy", "sell"] else mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot_size,
        "type": {
            "buy": mt5.ORDER_TYPE_BUY,
            "sell": mt5.ORDER_TYPE_SELL,
            "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
            "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
        }.get(order_type),
        "price": order_price,
        "sl": stop_loss,
        "tp": 0.0,  # Anda bisa tambahkan TP jika diperlukan
        "deviation": 10,
        "magic": 234000,
        "comment": "Order dari Flask API",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Debugging request
    print(f"DEBUG: Request: {request}")

    # Kirim order
    result = mt5.order_send(request)
    if not result or result.retcode != mt5.TRADE_RETCODE_DONE:
        return {"success": False, "message": f"Order gagal: {result.comment if result else 'Kesalahan tidak diketahui'}"}

    return {
        "success": True,
        "message": "Order berhasil!",
        "order_price": order_price,
        "stop_loss": stop_loss,
        "lot_size": lot_size,
    }


def shutdown_mt5():
    """Menutup koneksi MetaTrader 5."""
    mt5.shutdown()
