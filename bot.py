# ============================================================
#  DATA PRODUK JOKI
# ============================================================
JOKI = {
    "joki_makalah":  "📄 Makalah / Esai",
    "joki_laporan":  "🔬 Laporan Praktikum",
    "joki_ppt":      "📊 Presentasi (PPT)",
    "joki_jurnal":   "📚 Resume / Resensi Jurnal",
    "joki_proposal": "📝 Proposal Penelitian",
    "joki_skripsi":  "🎓 Bab Skripsi / TA",
    "joki_lainnya":  "💬 Lainnya (diskusi dulu)",
}

# ============================================================
#  KEYBOARDS
# ============================================================

def kb_menu_utama():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📝 Joki Tugas", callback_data="kat_joki"))
    kb.add(InlineKeyboardButton("⚡ PPOB", callback_data="kat_ppob"))
    kb.add(InlineKeyboardButton("❓ Tanya Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb

def kb_joki():
    kb = InlineKeyboardMarkup()
    for key, label in JOKI.items():
        kb.add(InlineKeyboardButton(label, callback_data=key))
    kb.add(InlineKeyboardButton("🔙 Kembali", callback_data="back_menu"))
    return kb

def kb_ppob(produk_list):
    kb = InlineKeyboardMarkup()
    for p in produk_list:
        label = f"{p['nama']} — Rp{int(p['harga']):,}"
        kb.add(InlineKeyboardButton(label, callback_data=f"ppob_{p['kode']}"))
    kb.add(InlineKeyboardButton("🔙 Kembali", callback_data="back_menu"))
    return kb

def kb_kembali_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 Menu Utama", callback_data="back_menu"))
    return kb

# ============================================================
#  /start
# ============================================================

@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.from_user.id
    sessions[uid] = {"step": "menu", "order": {}}
    nama = msg.from_user.first_name or "Kak"
    teks = (
        f"👋 Halo, *{nama}!*\n\n"
        f"Selamat datang di *{NAMA_TOKO}* 🍯\n\n"
        f"Kami melayani:\n"
        f"• 📝 Joki tugas akademik\n"
        f"• ⚡ PPOB (pulsa, token, data)\n\n"
        f"Pilih layanan di bawah:"
    )
    bot.send_message(uid, teks, parse_mode="Markdown", reply_markup=kb_menu_utama())

@bot.message_handler(commands=["menu"])
def menu(msg):
    start(msg)

# ============================================================
#  COMMAND ADMIN
# ============================================================

def is_admin(uid):
    return uid == ADMIN_ID

@bot.message_handler(commands=["done"])
def cmd_done(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "Format: /done <user_id>")
        return
    try:
        target_id = int(parts[1])
        bot.send_message(
            target_id,
            f"✅ *Order kamu sudah selesai diproses!*\n\n"
            f"Terima kasih sudah order di *{NAMA_TOKO}* 🍯\n"
            f"Kalau ada pertanyaan, hubungi @{ADMIN_USERNAME}.",
            parse_mode="Markdown",
            reply_markup=kb_menu_utama()
        )
        bot.send_message(ADMIN_ID, f"✅ Notif selesai terkirim ke {target_id}.", parse_mode="Markdown")
    except:
        bot.send_message(ADMIN_ID, "❌ User ID tidak valid.")

@bot.message_handler(commands=["cancel"])
def cmd_cancel(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "Format: /cancel <user_id>")
        return
    try:
        target_id = int(parts[1])
        bot.send_message(
            target_id,
            f"❌ *Order kamu dibatalkan.*\n\n"
            f"Mohon maaf atas ketidaknyamanannya.\n"
            f"Hubungi @{ADMIN_USERNAME} untuk info lebih lanjut.",
            parse_mode="Markdown",
            reply_markup=kb_menu_utama()
        )
        bot.send_message(ADMIN_ID, f"✅ Notif cancel terkirim ke {target_id}.", parse_mode="Markdown")
    except:
        bot.send_message(ADMIN_ID, "❌ User ID tidak valid.")
@bot.message_handler(commands=["proses"])
def cmd_proses(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "Format: /proses <user_id>")
        return
    try:
        target_id = int(parts[1])
        bot.send_message(
            target_id,
            f"⚙️ *Order kamu sedang diproses!*\n\n"
            f"Kami akan segera menyelesaikannya. Mohon tunggu ya 🙏",
            parse_mode="Markdown"
        )
        bot.send_message(ADMIN_ID, f"✅ Notif proses terkirim ke {target_id}.", parse_mode="Markdown")
    except:
        bot.send_message(ADMIN_ID, "❌ User ID tidak valid.")

# ============================================================
#  CALLBACK
# ============================================================

@bot.callback_query_handler(func=lambda c: c.data == "back_menu")
def back_menu(call):
    uid = call.from_user.id
    sessions[uid] = {"step": "menu", "order": {}}
    bot.edit_message_text(
        "Pilih layanan:",
        uid, call.message.message_id,
        reply_markup=kb_menu_utama()
    )

@bot.callback_query_handler(func=lambda c: c.data == "kat_ppob")
def kat_ppob(call):
    bot.answer_callback_query(call.id, "Memuat produk...")
    uid = call.from_user.id
    produk_list = get_produk_ppob()
    if not produk_list:
        bot.edit_message_text(
            "⚡ *PPOB*\n\nGagal memuat produk. Hubungi admin:",
            uid, call.message.message_id,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💬 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME}"),
                InlineKeyboardButton("🔙 Kembali", callback_data="back_menu")
            ]])
        )
        return
    sessions[uid]["order"]["kategori"] = "ppob"
    bot.edit_message_text(
        "⚡ *PPOB*\n\nPilih produk:",
        uid, call.message.message_id,
        parse_mode="Markdown",
        reply_markup=kb_ppob(produk_list)
    )

@bot.callback_query_handler(func=lambda c: c.data == "kat_joki")
def kat_joki(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "📝 *Joki Tugas*\n\nPilih jenis tugas kamu:",
        call.from_user.id, call.message.message_id,
        parse_mode="Markdown",
        reply_markup=kb_joki()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("ppob_"))
def pilih_ppob(call):
    uid = call.from_user.id
    kode = call.data.replace("ppob_", "")
    produk_list = get_produk_ppob()
    produk = next((p for p in produk_list if str(p["kode"]) == kode), None)
    if not produk:
        bot.answer_callback_query(call.id, "Produk tidak ditemukan.")
        return

    sessions[uid] = {
        "step": "ppob_isi_data",
        "order": {
            "kategori": "ppob",
            "jenis": produk["nama"],
            "harga": produk["harga"],
            "kode": kode
        }
    }

    bot.edit_message_text(
        f"✅ Dipilih: *{produk['nama']}*\n"
        f"Harga: *Rp{int(produk['harga']):,}*\n\n"
        f"Ketik *nomor HP / ID pelanggan* kamu:",
        uid, call.message.message_id,
        parse_mode="Markdown",
        reply_markup=kb_kembali_menu()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("joki_"))
def pilih_joki(call):
    uid = call.from_user.id
    key = call.data
    label = JOKI.get(key, "Joki Tugas")
    sessions[uid] = {
        "step": "joki_detail",
        "order": {"jenis": label, "key": key}
    }
    bot.edit_message_text(
        f"✅ Dipilih: *{label}*\n\n"
        f"Ceritain detail tugasnya — judul/topik, deadline, dan instruksi khusus kalau ada.\n\n"
        f"_Ketik sekarang:_",
        uid, call.message.message_id,
        parse_mode="Markdown",
        reply_markup=kb_kembali_menu()
    )

# ============================================================
#  PHOTO HANDLER — bukti bayar
# ============================================================
@bot.message_handler(content_types=["photo"])
def handle_foto(msg):
    uid = msg.from_user.id
    sesi = sessions.get(uid, {})

    if sesi.get("step") == "tunggu_bukpem":
        order = sesi.get("order", {})
        bot.send_message(
            uid,
            f"✅ *Bukti bayar diterima!*\n\n"
            f"Admin akan memverifikasi dan memproses ordermu segera. Tunggu ya 🙏",
            parse_mode="Markdown",
            reply_markup=kb_kembali_menu()
        )
        caption = (
            f"💰 *BUKTI BAYAR MASUK*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Produk  : {order.get('jenis', '-')}\n"
            f"Detail  : {order.get('detail', '-')}\n"
            f"Harga   : Rp{int(order.get('harga', 0)):,}\n"
            f"Ref     : {order.get('ref', '-')}\n"
            f"Buyer   : @{msg.from_user.username or 'no username'}\n"
            f"User ID : {uid}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"/proses {uid} — sedang diproses\n"
            f"/done {uid} — selesai\n"
            f"/cancel {uid} — dibatalkan"
        )
        bot.forward_message(ADMIN_ID, uid, msg.message_id)
        bot.send_message(ADMIN_ID, caption, parse_mode="Markdown")
        sessions[uid]["step"] = "selesai"
    else:
        bot.send_message(uid, "Ketik /start untuk mulai order. 😊")

# ============================================================
#  TEXT HANDLER
# ============================================================

@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    uid = msg.from_user.id
    teks = msg.text.strip()
    sesi = sessions.get(uid)

    if not sesi:
        start(msg)
        return

    step = sesi.get("step")
    order = sesi["order"]

    # PPOB — isi nomor/ID pelanggan
    if step == "ppob_isi_data":
        order["detail"] = teks
        order["ref"] = f"PPB{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"

        bot.send_message(
            uid,
            f"✅ *Order PPOB diterima!*\n\n"
            f"Produk : {order['jenis']}\n"
            f"No/ID  : {teks}\n"
            f"Harga  : *Rp{int(order['harga']):,}*\n"
            f"Ref    : {order['ref']}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Cek info pembayaran → {CHANNEL_PAYMENT}\n"
            f"2️⃣ Lakukan pembayaran\n"
            f"3️⃣ Kirim bukti bayar *di sini* (foto)\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💳 Info Payment", url=CHANNEL_PAYMENT)
            ]])
        )

        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else f"ID: {uid}"
        notif = (
            f"🔔 *ORDER PPOB MASUK*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Produk  : {order['jenis']}\n"
            f"No/ID   : {teks}\n"
            f"Harga   : Rp{int(order['harga']):,}\n"
            f"Ref     : {order['ref']}\n"
            f"Buyer   : {username_buyer}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"➡️ [DM Buyer](tg://user?id={uid})"
        )
        bot.send_message(ADMIN_ID, notif, parse_mode="Markdown")

    # JOKI — isi detail tugas
    elif step == "joki_detail":
        order["detail"] = teks
        order["ref"] = f"JKI{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"

        bot.send_message(
            uid,
            f"✅ *Order diterima!*\n\n"
            f"Jenis  : {order['jenis']}\n"
            f"Detail : {teks}\n"
            f"Ref    : {order['ref']}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Tunggu admin konfirmasi harga via DM\n"
            f"2️⃣ Cek info pembayaran → {CHANNEL_PAYMENT}\n"
            f"3️⃣ Kirim bukti bayar *di sini* (foto)\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💳 Info Payment", url=CHANNEL_PAYMENT)
            ]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else f"ID: {uid}"
        notif = (
            f"🔔 *ORDER JOKI MASUK*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Jenis   : {order['jenis']}\n"
            f"Detail  : {teks}\n"
            f"Ref     : {order['ref']}\n"
            f"Buyer   : {username_buyer}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"➡️ [DM Buyer](tg://user?id={uid})"
        )
        bot.send_message(ADMIN_ID, notif, parse_mode="Markdown")

    else:
        bot.send_message(uid, "Ketik /start untuk mulai order. 😊")

# ============================================================
#  RUN
# ============================================================

if name == "main":
    print(f"✅ Bot {NAMA_TOKO} berjalan...")
    bot.infinity_polling()
