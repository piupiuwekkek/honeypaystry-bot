import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============================================================
#  KONFIGURASI
# ============================================================
BOT_TOKEN       = "8417510832:AAF9sScYaUtQ3lQ65erwGXFbJty_lVUHA24"
ADMIN_ID        = 6911699137
ADMIN_USERNAME  = "rhezzan"
NAMA_TOKO       = "HoneyPaystry"
CHANNEL_PAYMENT = "https://t.me/piementt"
# ============================================================

bot = telebot.TeleBot(BOT_TOKEN)
sessions = {}

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
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "⚡ *PPOB*\n\nLayanan PPOB sedang dalam persiapan.\nHubungi admin untuk order manual:",
        call.from_user.id, call.message.message_id,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💬 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("🔙 Kembali", callback_data="back_menu")
        ]])
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

    if step == "joki_detail":
        order["detail"] = teks
        order["ref"] = f"JKI{uid}{int(time.time())}"
        sessions[uid]["step"] = "selesai"

        # Konfirmasi ke buyer
        bot.send_message(
            uid,
            f"✅ *Order diterima!*\n\n"
            f"Jenis  : {order['jenis']}\n"
            f"Detail : {teks}\n"
            f"Ref    : {order['ref']}\n\n"
            f"Admin akan segera menghubungi kamu untuk diskusi harga dan pengerjaan. Tunggu ya! 🙏",
            parse_mode="Markdown",
            reply_markup=kb_kembali_menu()
        )

        # Notif ke admin
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
        bot.send_message(uid, "Ketik /start untuk mulai. 😊")

# ============================================================
#  RUN
# ============================================================

if __name__ == "__main__":
    print(f"✅ Bot {NAMA_TOKO} berjalan...")
    bot.infinity_polling()