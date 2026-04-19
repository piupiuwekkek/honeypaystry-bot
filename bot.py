import telebot
import time
import json
import os
import gspread
from google.oauth2.service_account import Credentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8417510832:AAF9sScYaUtQ3lQ65erwGXFbJty_lVUHA24")
ADMIN_ID = 6911699137
ADMIN_USERNAME = "rhezzan"
OWNER_ID = 7307675541
OWNER_USERNAME = "dahneaa"
NAMA_TOKO = "HoneyPaystry"
CHANNEL_PAYMENT = "https://t.me/piementt"
CHANNEL_REVIEW_ID = "@HoneysttReview"
CHANNEL_REVIEW = "https://t.me/HoneysttReview"

SHEET_ID_PPOB = "1hlrp0OoNbAw9peNsLV3rIrVG4uIL8NOClbGzNen3qtU"
SHEET_ID_GAME = "1YDa8aafIeq2njVp_ePmlENUAyvJA8rtYR7mgzM3qg2I"
SHEET_ID_PREMIUM = "1F9etJEWCCooVh2pKBR-mKxSkEYsLNxOGVDfqz2G7klE"

GOOGLE_CREDS = json.loads(os.environ.get("GOOGLE_CREDS_JSON", "{}"))

bot = telebot.TeleBot(BOT_TOKEN)
sessions = {}
pending_review = {}

FORMAT_JOKI = (
    "```Silakan isi format order berikut, lalu kirim ke sini:\n\n"
    "Jenis Tugas: (jurnal/essay/makalah/laporan/PPT/proposal/skripsi/lainnya)\n"
    "Judul/Topik: \n"
    "Detail Tugas: \n"
    "Deadline: \n"
    "Jumlah Halaman/Kata: \n"
    "Referensi Khusus: (kosongkan jika tidak ada)\n"
    "Catatan Tambahan: (kosongkan jika tidak ada)```"
)

FORMAT_CONVERT = "https://t.me/honeypaystry/36"

PRICELIST = {
    "cv": "https://t.me/honeypaystry/18",
    "jaspin": "https://t.me/honeypaystry/17",
    "rekber": "https://t.me/honeypaystry/22",
    "jasget": "https://t.me/honeypaystry/23",
}

CHANNEL_TESTI = {
    "tugas": ("Testi Tugas", "https://t.me/resultmayo"),
    "transaksi": ("Testi Transaksi", "https://t.me/coneverts"),
    "game": ("Testi Game", "https://t.me/tasteplay"),
}

PROVIDER_PULSA = [
    ("Telkomsel", "pulsa_telkomsel"),
    ("XL", "pulsa_xl"),
    ("Three (3)", "pulsa_three"),
    ("Smartfren", "pulsa_smartfren"),
    ("Indosat", "pulsa_indosat"),
    ("By.U", "pulsa_byu"),
    ("Axis", "pulsa_axis"),
    ("Masa Aktif", "pulsa_masa_aktif"),
]

PROVIDER_KUOTA = [
    ("Telkomsel", "kuota_telkomsel"),
    ("XL", "kuota_xl"),
    ("Three (3)", "kuota_three"),
    ("Smartfren", "kuota_smartfren"),
    ("Indosat", "kuota_indosat"),
    ("By.U", "kuota_byu"),
    ("Axis", "kuota_axis"),
]

GAME_LIST = [
    ("Mobile Legends (Diamond)", "ml"),
    ("Free Fire (Diamond)", "ff"),
    ("PUBG (UC)", "pubg"),
    ("Honor of Kings (Token)", "hok"),
]


def get_sheet_data(sheet_id, tab_name):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).worksheet(tab_name)
        return sheet.get_all_records()
    except Exception as e:
        print(f"Error baca sheet {tab_name}: {e}")
        return []


def is_admin(uid):
    return uid in [ADMIN_ID, OWNER_ID]


def is_gangguan(produk):
    return str(produk.get("gangguan", "")).strip().lower() in ["1", "ya", "yes", "true", "gangguan"]


def kirim_notif_admin(uid, order, username_buyer, tipe):
    notif = (
        f"ORDER {tipe} MASUK\n"
        f"Produk: {order.get('jenis', '-')}\n"
        f"Detail: {order.get('detail', '-')}\n"
        f"Harga: Rp{int(order.get('harga', 0)):,}\n"
        f"Ref: {order.get('ref', '-')}\n"
        f"Buyer: {username_buyer}\n"
        f"User ID: {uid}\n\n"
        f"/proses {uid}\n"
        f"/done {uid}\n"
        f"/cancel {uid}"
    )
    for admin in [ADMIN_ID, OWNER_ID]:
        try:
            bot.send_message(admin, notif)
        except Exception:
            pass


def minta_review(uid, order):
    pending_review[uid] = {"order": order, "step": "rating"}
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("1", callback_data="rate_1"),
        InlineKeyboardButton("2", callback_data="rate_2"),
        InlineKeyboardButton("3", callback_data="rate_3"),
        InlineKeyboardButton("4", callback_data="rate_4"),
        InlineKeyboardButton("5", callback_data="rate_5"),
    )
    bot.send_message(
        uid,
        f"Terima kasih sudah order di {NAMA_TOKO}!\n\n"
        f"Sebelum lanjut order berikutnya, mohon isi rating dulu ya (1-5):",
        reply_markup=kb
    )


def kb_menu_utama():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Joki Tugas", callback_data="kat_joki"))
    kb.add(InlineKeyboardButton("PPOB", callback_data="kat_ppob"))
    kb.add(InlineKeyboardButton("Top Up Game", callback_data="kat_game"))
    kb.add(InlineKeyboardButton("Aplikasi Premium", callback_data="kat_premium"))
    kb.row(
        InlineKeyboardButton("CV", callback_data="kat_cv"),
        InlineKeyboardButton("Jaspin", callback_data="kat_jaspin"),
    )
    kb.row(
        InlineKeyboardButton("Rekber", callback_data="kat_rekber"),
        InlineKeyboardButton("Jasget", callback_data="kat_jasget"),
    )
    kb.add(InlineKeyboardButton("Testi Tugas", url=CHANNEL_TESTI["tugas"][1]))
    kb.add(InlineKeyboardButton("Testi Transaksi", url=CHANNEL_TESTI["transaksi"][1]))
    kb.add(InlineKeyboardButton("Testi Game", url=CHANNEL_TESTI["game"][1]))
    kb.add(InlineKeyboardButton("Tanya Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb


def kb_ppob():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Pulsa", callback_data="ppob_kat_pulsa"))
    kb.add(InlineKeyboardButton("Kuota", callback_data="ppob_kat_kuota"))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
    return kb


def kb_provider(tipe):
    kb = InlineKeyboardMarkup()
    providers = PROVIDER_PULSA if tipe == "pulsa" else PROVIDER_KUOTA
    back = "ppob_kat_pulsa" if tipe == "pulsa" else "ppob_kat_kuota"
    for label, key in providers:
        kb.add(InlineKeyboardButton(label, callback_data=f"provider_{key}"))
    kb.add(InlineKeyboardButton("Kembali", callback_data=back))
    return kb


def kb_game():
    kb = InlineKeyboardMarkup()
    for label, key in GAME_LIST:
        kb.add(InlineKeyboardButton(label, callback_data=f"game_{key}"))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
    return kb


def kb_produk(produk_list, back_callback):
    kb = InlineKeyboardMarkup()
    for p in produk_list:
        if is_gangguan(p):
            label = f"[GANGGUAN] {p['nama']}"
        else:
            harga = int(p["harga"]) if p["harga"] else 0
            label = f"{p['nama']} - Rp{harga:,}"
        kb.add(InlineKeyboardButton(label, callback_data=f"beli_{p['kode']}"))
    kb.add(InlineKeyboardButton("Kembali", callback_data=back_callback))
    return kb


def kb_subkat(subkats, tab_name):
    kb = InlineKeyboardMarkup()
    for s in subkats:
        kb.add(InlineKeyboardButton(s, callback_data=f"subkat_{tab_name}_{s}"))
    kb.add(InlineKeyboardButton("Kembali", callback_data=f"provider_{tab_name}"))
    return kb


def kb_kembali(callback="back_menu"):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Menu Utama", callback_data=callback))
    return kb


def kb_convert(kat):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Lihat Pricelist", url=PRICELIST[kat]))
    kb.add(InlineKeyboardButton("Lihat Format Order", url=FORMAT_CONVERT))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
    return kb


def cek_pending_review(uid):
    if uid in pending_review:
        return True
    return False


@bot.message_handler(commands=["start", "menu"])
def start(msg):
    uid = msg.from_user.id
    if cek_pending_review(uid):
        bot.send_message(uid, "Kamu belum mengisi rating order sebelumnya.\nMohon isi rating dulu sebelum order lagi.")
        minta_review(uid, pending_review[uid]["order"])
        return
    sessions[uid] = {"step": "menu", "order": {}}
    nama = msg.from_user.first_name or "Kak"
    bot.send_message(
        uid,
        f"Halo {nama}! Selamat datang di {NAMA_TOKO}\n\nPilih layanan:",
        reply_markup=kb_menu_utama()
    )


@bot.message_handler(commands=["done"])
def cmd_done(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.from_user.id, "Format: /done <user_id>")
        return
    try:
        target = int(parts[1])
        sesi = sessions.get(target, {})
        order = sesi.get("order", {})
        bot.send_message(target, f"Order kamu sudah selesai! Terima kasih sudah order di {NAMA_TOKO}")
        minta_review(target, order)
        bot.send_message(msg.from_user.id, f"Notif selesai + review terkirim ke {target}")
    except Exception:
        bot.send_message(msg.from_user.id, "User ID tidak valid")


@bot.message_handler(commands=["cancel"])
def cmd_cancel(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.from_user.id, "Format: /cancel <user_id>")
        return
    try:
        target = int(parts[1])
        bot.send_message(
            target,
            f"Order kamu dibatalkan. Hubungi @{ADMIN_USERNAME} untuk info lebih lanjut.",
            reply_markup=kb_menu_utama()
        )
        bot.send_message(msg.from_user.id, f"Notif cancel terkirim ke {target}")
    except Exception:
        bot.send_message(msg.from_user.id, "User ID tidak valid")


@bot.message_handler(commands=["proses"])
def cmd_proses(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(msg.from_user.id, "Format: /proses <user_id>")
        return
    try:
        target = int(parts[1])
        bot.send_message(target, "Order kamu sedang diproses! Mohon tunggu ya.")
        bot.send_message(msg.from_user.id, f"Notif proses terkirim ke {target}")
    except Exception:
        bot.send_message(msg.from_user.id, "User ID tidak valid")


@bot.callback_query_handler(func=lambda c: c.data.startswith("rate_"))
def handle_rating(call):
    uid = call.from_user.id
    rating = int(call.data.replace("rate_", ""))
    stars = "⭐" * rating
    if uid not in pending_review:
        bot.answer_callback_query(call.id)
        return
    pending_review[uid]["rating"] = rating
    pending_review[uid]["step"] = "saran"
    bot.edit_message_text(
        f"Rating kamu: {stars}\n\nSekarang tulis kritik & saran kamu (boleh singkat):",
        uid, call.message.message_id
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data == "back_menu")
def back_menu(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    sessions[uid] = {"step": "menu", "order": {}}
    bot.edit_message_text("Pilih layanan:", uid, call.message.message_id, reply_markup=kb_menu_utama())


@bot.callback_query_handler(func=lambda c: c.data == "kat_joki")
def kat_joki(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    bot.answer_callback_query(call.id)
    sessions[uid] = {"step": "joki_detail", "order": {"jenis": "Joki Tugas"}}
    bot.edit_message_text(
        f"Joki Tugas\n\n{FORMAT_JOKI}\n\nSalin format di atas, isi, lalu kirim ke sini:",
        uid, call.message.message_id,
        reply_markup=kb_kembali()
    )


@bot.callback_query_handler(func=lambda c: c.data == "kat_ppob")
def kat_ppob(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_text("PPOB - Pilih kategori:", uid, call.message.message_id, reply_markup=kb_ppob())


@bot.callback_query_handler(func=lambda c: c.data == "kat_game")
def kat_game(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Top Up Game - Pilih game:", uid, call.message.message_id, reply_markup=kb_game())


@bot.callback_query_handler(func=lambda c: c.data == "kat_premium")
def kat_premium(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    bot.answer_callback_query(call.id, "Memuat produk...")
    produk_list = get_sheet_data(SHEET_ID_PREMIUM, "Sheet1")
    if not produk_list:
        bot.edit_message_text(
            "Produk tidak tersedia. Hubungi admin.",
            uid, call.message.message_id,
            reply_markup=kb_kembali()
        )
        return
    sessions[uid] = sessions.get(uid, {"step": "menu", "order": {}})
    sessions[uid]["order"]["tab"] = "premium"
    sessions[uid]["order"]["produk_list"] = produk_list
    bot.edit_message_text(
        "Aplikasi Premium - Pilih produk:",
        uid, call.message.message_id,
        reply_markup=kb_produk(produk_list, "back_menu")
    )


@bot.callback_query_handler(func=lambda c: c.data in ["kat_cv", "kat_jaspin", "kat_rekber", "kat_jasget"])
def kat_convert(call):
    uid = call.from_user.id
    if cek_pending_review(uid):
        bot.answer_callback_query(call.id, "Isi rating dulu ya!")
        return
    bot.answer_callback_query(call.id)
    kat = call.data.replace("kat_", "")
    label = {
        "cv": "CV (Convert)",
        "jaspin": "Jaspin",
        "rekber": "Rekber",
        "jasget": "Jasget"
    }.get(kat, kat.upper())
    sessions[uid] = {"step": f"convert_{kat}", "order": {"jenis": label, "harga": 0}}
    bot.edit_message_text(
        f"{label}\n\n"
        f"Lihat pricelist dan format order di bawah.\n"
        f"Setelah itu isi format order dan kirim ke sini:",
        uid, call.message.message_id,
        reply_markup=kb_convert(kat)
    )


@bot.callback_query_handler(func=lambda c: c.data == "ppob_kat_pulsa")
def ppob_pulsa(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Pulsa - Pilih provider:", call.from_user.id, call.message.message_id, reply_markup=kb_provider("pulsa"))


@bot.callback_query_handler(func=lambda c: c.data == "ppob_kat_kuota")
def ppob_kuota(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Kuota - Pilih provider:", call.from_user.id, call.message.message_id, reply_markup=kb_provider("kuota"))


@bot.callback_query_handler(func=lambda c: c.data.startswith("provider_"))
def pilih_provider(call):
    uid = call.from_user.id
    tab_name = call.data.replace("provider_", "")
    bot.answer_callback_query(call.id, "Memuat produk...")
    produk_list = get_sheet_data(SHEET_ID_PPOB, tab_name)
    if not produk_list:
        bot.edit_message_text(
            "Produk tidak tersedia atau belum diisi. Hubungi admin.",
            uid, call.message.message_id,
            reply_markup=kb_kembali("kat_ppob")
        )
        return
    sessions[uid] = sessions.get(uid, {"step": "menu", "order": {}})
    sessions[uid]["order"]["tab"] = tab_name
    subkats = list(dict.fromkeys([p["kategori"] for p in produk_list if p.get("kategori")]))
    if subkats:
        tipe_label = tab_name.replace("pulsa_", "").replace("kuota_", "").title()
        bot.edit_message_text(
            f"{tab_name.split('_')[0].title()} {tipe_label} - Pilih kategori:",
            uid, call.message.message_id,
            reply_markup=kb_subkat(subkats, tab_name)
        )
        return
    back = "ppob_kat_pulsa" if tab_name.startswith("pulsa_") else "ppob_kat_kuota"
    sessions[uid]["order"]["produk_list"] = produk_list
    bot.edit_message_text("Pilih produk:", uid, call.message.message_id, reply_markup=kb_produk(produk_list, back))


@bot.callback_query_handler(func=lambda c: c.data.startswith("subkat_"))
def pilih_subkat(call):
    uid = call.from_user.id
    raw = call.data.replace("subkat_", "")
    parts = raw.split("_", 2)
    tipe = parts[0]
    provider = parts[1]
    subkat = parts[2] if len(parts) > 2 else ""
    tab_name = f"{tipe}_{provider}"
    produk_list = get_sheet_data(SHEET_ID_PPOB, tab_name)
    filtered = [p for p in produk_list if p.get("kategori") == subkat]
    if not filtered:
        bot.answer_callback_query(call.id, "Produk tidak ditemukan.")
        return
    sessions[uid]["order"]["produk_list"] = filtered
    bot.edit_message_text(
        f"{tipe.title()} {provider.title()} - {subkat}:",
        uid, call.message.message_id,
        reply_markup=kb_produk(filtered, f"provider_{tab_name}")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("game_"))
def pilih_game(call):
    uid = call.from_user.id
    tab_name = call.data.replace("game_", "")
    bot.answer_callback_query(call.id, "Memuat produk...")
    produk_list = get_sheet_data(SHEET_ID_GAME, tab_name)
    if not produk_list:
        bot.edit_message_text(
            "Produk tidak tersedia. Hubungi admin.",
            uid, call.message.message_id,
            reply_markup=kb_kembali("kat_game")
        )
        return
    sessions[uid] = sessions.get(uid, {"step": "menu", "order": {}})
    sessions[uid]["order"]["tab"] = tab_name
    sessions[uid]["order"]["produk_list"] = produk_list
    bot.edit_message_text("Pilih nominal:", uid, call.message.message_id, reply_markup=kb_produk(produk_list, "kat_game"))


@bot.callback_query_handler(func=lambda c: c.data.startswith("beli_"))
def pilih_produk(call):
    uid = call.from_user.id
    kode = call.data.replace("beli_", "")
    sesi = sessions.get(uid, {})
    produk_list = sesi.get("order", {}).get("produk_list", [])
    produk = next((p for p in produk_list if str(p["kode"]) == kode), None)
    if not produk:
        bot.answer_callback_query(call.id, "Produk tidak ditemukan.")
        return
    if is_gangguan(produk):
        bot.answer_callback_query(call.id, "Produk ini sedang gangguan.")
        bot.send_message(uid, f"Maaf, {produk['nama']} sedang gangguan. Pilih produk lain atau hubungi admin.")
        return
    tab = sesi.get("order", {}).get("tab", "")
    if tab in ["ml", "ff", "pubg", "hok"]:
        step = "game_isi_id"
        prompt = "Masukkan ID game kamu:"
    elif tab == "premium":
        step = "ppob_isi_data"
        prompt = "Masukkan email akun kamu:"
    else:
        step = "ppob_isi_data"
        prompt = "Masukkan nomor HP / ID pelanggan:"
    sessions[uid] = {
        "step": step,
        "order": {"jenis": produk["nama"], "harga": produk["harga"], "kode": kode, "tab": tab}
    }
    bot.edit_message_text(
        f"Dipilih: {produk['nama']}\nHarga: Rp{int(produk['harga']):,}\n\n{prompt}",
        uid, call.message.message_id,
        reply_markup=kb_kembali()
    )


@bot.message_handler(content_types=["photo"])
def handle_foto(msg):
    uid = msg.from_user.id
    sesi = sessions.get(uid, {})
    if sesi.get("step") != "tunggu_bukpem":
        bot.send_message(uid, "Ketik /start untuk mulai order.")
        return
    order = sesi.get("order", {})
    bot.send_message(uid, "Bukti bayar diterima! Admin akan segera memverifikasi.")
    caption = (
        f"BUKTI BAYAR MASUK\n"
        f"Produk: {order.get('jenis', '-')}\n"
        f"Detail: {order.get('detail', '-')}\n"
        f"Harga: Rp{int(order.get('harga', 0)):,}\n"
        f"Ref: {order.get('ref', '-')}\n"
        f"Buyer: @{msg.from_user.username or 'no username'}\n"
        f"User ID: {uid}\n\n"
        f"/proses {uid}\n"
        f"/done {uid}\n"
        f"/cancel {uid}"
    )
    for admin in [ADMIN_ID, OWNER_ID]:
        try:
            bot.forward_message(admin, uid, msg.message_id)
            bot.send_message(admin, caption)
        except Exception:
            pass
    sessions[uid]["step"] = "selesai"


@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    uid = msg.from_user.id
    teks = msg.text.strip()

    if uid in pending_review:
        rev = pending_review[uid]
        if rev.get("step") == "saran":
            rating = rev.get("rating", 0)
            stars = "⭐" * rating
            order = rev.get("order", {})
            review_text = (
                f"REVIEW BARU\n"
                f"Produk: {order.get('jenis', '-')}\n"
                f"Rating: {stars} ({rating}/5)\n"
                f"Kritik & Saran: {teks}\n"
                f"Buyer: @{msg.from_user.username or 'no username'}"
            )
            try:
                bot.send_message(CHANNEL_REVIEW_ID, review_text)
            except Exception as e:
                print(f"Gagal kirim ke channel review: {e}")
            del pending_review[uid]
            sessions[uid] = {"step": "menu", "order": {}}
            bot.send_message(
                uid,
                f"Terima kasih atas review-nya! {stars}\n\n"
                f"Review kamu sudah dikirim ke {CHANNEL_REVIEW}\n"
                f"Kamu bisa order lagi sekarang.",
                reply_markup=kb_menu_utama()
            )
        return

    sesi = sessions.get(uid)
    if not sesi:
        start(msg)
        return

    step = sesi.get("step")
    order = sesi["order"]

    if step == "joki_detail":
        order["detail"] = teks
        order["ref"] = f"JKI{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\nJenis: {order['jenis']}\nRef: {order['ref']}\n\n"
            f"Detail order:\n{teks}\n\n"
            f"1. Tunggu admin konfirmasi harga\n"
            f"2. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "JOKI")

    elif step in ["convert_cv", "convert_jaspin", "convert_rekber", "convert_jasget"]:
        order["detail"] = teks
        order["ref"] = f"CVT{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\nLayanan: {order['jenis']}\nRef: {order['ref']}\n\n"
            f"Detail order:\n{teks}\n\n"
            f"1. Tunggu admin konfirmasi\n"
            f"2. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, order["jenis"].upper())

    elif step == "ppob_isi_data":
        order["detail"] = teks
        order["ref"] = f"PPB{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\nProduk: {order['jenis']}\nNo/ID: {teks}\nHarga: Rp{int(order['harga']):,}\nRef: {order['ref']}\n\n"
            f"1. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"2. Lakukan pembayaran\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "PPOB")

    elif step == "game_isi_id":
        order["detail"] = teks
        order["ref"] = f"GAME{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\nProduk: {order['jenis']}\nID Game: {teks}\nHarga: Rp{int(order['harga']):,}\nRef: {order['ref']}\n\n"
            f"1. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"2. Lakukan pembayaran\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "GAME")

    else:
        bot.send_message(uid, "Ketik /start untuk mulai order.")


if __name__ == "__main__":
    print(f"Bot {NAMA_TOKO} berjalan...")
    bot.infinity_polling()
    
