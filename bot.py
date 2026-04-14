import telebot
import time
import gspread
from google.oauth2.service_account import Credentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8417510832:AAF9sScYaUtQ3lQ65erwGXFbJty_lVUHA24"
ADMIN_ID = 6911699137
ADMIN_USERNAME = "rhezzan"
NAMA_TOKO = "HoneyPaystry"
CHANNEL_PAYMENT = "https://t.me/piementt"
SHEET_ID_PPOB = "1hlrp0OoNbAw9peNsLV3rIrVG4uIL8NOClbGzNen3qtU"
SHEET_ID_GAME = "1YDa8aafIeq2njVp_ePmlENUAyvJA8rtYR7mgzM3qg2I"

GOOGLE_CREDS = {
    "type": "service_account",
    "project_id": "honeypaystry-bot",
    "private_key_id": "b757f75b4c2beb597dc29bd1ebdf6feda535a2a6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCljmfLbP9wnPD0\nIb2IM7TiOeMUlX0JUS0QrSvYvsCiK2P/xZN31QaGhLKoYBolySdBZ44iWl333pED\nedrI/e+AbyS2thDhk7mjU5o4SnTJw2Dm1fhndlFhAfhbmVX+Xyk/Ns+8oDEKuhwD\ngzFcrgdLVGszFi34QzzC2mTo+D9RvlJRU/oAEBEbEg+1Y+KNlJZB6ukbHkLrLCEX\nnEbdif5z9zNaOqA+ly9yhzvieF1CDvrVSc74jVaoJM5geElDwZij7UZLWNoRQKuf\nfDZ4JMLvJqPjinAjAYTomshU4Ppd1+pNQokFTvdmBeuE4J9Wvc8q/zwB513Jh9/3\ncThVv46DAgMBAAECggEAL6G+pC0KezR0MNEqTi8OOk5MUqZF0LHtxNAF/vi2xJG2\nVibarE36cCZqnn3z1+49YJhyMNkOExwSXc0n0M8aormXdwf/6F7PuLl7c/mcC1au\noQtryhylAkOGWJhPwP1RCTJ0Z0ExivQLzkjnIVKin548r3iQpk52A1vBT7Pox9QD\nNaMXXB/O3ZoLJ22XEAhsyR6+M03GwGaMxaDTrQi+scK3Y+cG6uuIaDyh7cswttUT\n/1tpTq5fnAHqZVjtjYf9iHHBn1llrVAFawAMWexYCAG4sbaMntFWdTaGAKBlIaFC\nVGBVBqvizOiq2pMjA0ZfJmkt423oH3Dy3NNrVMgimQKBgQDN33UjFAb0tAPm1gWb\nNwLeyPxnV5R13PajMVNKX/Yw/04SwpzqFMX9jajtRsZP8mjDUdmwefiQPYogtuzt\nuil+mAm9bglqjl8P5ooftkk+WPRx6fY7t3cJd/BiNIYH7vfotG+yENJsgg1vlgFD\n1fISUPHrIUN1F2Qr0O4xTjdnSQKBgQDN3esgcC84t+8zZSG7gDP75IyEi+S9FG/J\n8Qsh5ZrdwvQK9msNOegRTkJD2XZR9LGCJZF3+NbLuEcNcau9a8WVaEvb4tQ88qhU\nscOQD5G6VULMDcA+a9qRngo+Dw2HHSSxSZtTK5+nI972crfhnEwpumuJLD1M77yw\n+7hjta1LawKBgDS6I5UdXv6zUECB1iO/viNzFHofSy24rw5y5qMo2rQH32Yco/Wr\n5l2fN4G127rEGiLURs3VH11J9aOVVi84u8HpjK0QjqbU2fIHmJ6woCewvsKiKmd3\nAKzTJCTy0NUdVi8qb2UKu+oAkRJgN+i41evtAVi4Rz+pAwXZ1/eW0cfJAoGBAMOz\nrBqJKwrTKAyGnjudk01pJf+28Tqh2+dwQrH1kHQyKUbmnDvViXwyFiJj7uvYHorn\nZdNT9fVx9/Ga1rVaZ1kx7bNZfYN29niVCKDBfDpTZQ2QIOn2I7B8OaZnLuf7127F\n12eIN9xu6D0GLzHFIE4mzqV3LcseuBTTJqV7BwODAoGAcbkyOPttp1FY4s87tidF\nO8NN3JAQHhxYO+u5uPbsq+yQ9f1yLLgT+VCiIzNtjxjVdkUVcvWaTPNeTHMXHjzs\ntlX2s4HmxHUZt1X8OeEliXpP0YOeV8NxLA8/Nnc6uPIjpjAqc3726aGlqrG/UDrx\npHu1w4dODAHj2/Ih7IqUgmA=\n-----END PRIVATE KEY-----\n",
    "client_email": "honeypaystry-bot@honeypaystry-bot.iam.gserviceaccount.com",
    "client_id": "114508117228448871347",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/honeypaystry-bot%40honeypaystry-bot.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

bot = telebot.TeleBot(BOT_TOKEN)
sessions = {}

JOKI = {
    "joki_makalah": "Makalah / Esai",
    "joki_laporan": "Laporan Praktikum",
    "joki_ppt": "Presentasi PPT",
    "joki_jurnal": "Resume / Resensi Jurnal",
    "joki_proposal": "Proposal Penelitian",
    "joki_skripsi": "Bab Skripsi / TA",
    "joki_lainnya": "Lainnya"
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


def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scopes)
    return gspread.authorize(creds)


def get_sheet_data(sheet_id, tab_name):
    try:
        client = get_gspread_client()
        sheet = client.open_by_key(sheet_id).worksheet(tab_name)
        return sheet.get_all_records()
    except Exception as e:
        print(f"Error baca sheet {tab_name}: {e}")
        return []


def kb_menu_utama():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Joki Tugas", callback_data="kat_joki"))
    kb.add(InlineKeyboardButton("PPOB", callback_data="kat_ppob"))
    kb.add(InlineKeyboardButton("Top Up Game", callback_data="kat_game"))
    kb.add(InlineKeyboardButton("Tanya Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb


def kb_joki():
    kb = InlineKeyboardMarkup()
    for key, label in JOKI.items():
        kb.add(InlineKeyboardButton(label, callback_data=key))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
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


def is_admin(uid):
    return uid == ADMIN_ID


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
    bot.send_message(ADMIN_ID, notif)


@bot.message_handler(commands=["start", "menu"])
def start(msg):
    uid = msg.from_user.id
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
        bot.send_message(ADMIN_ID, "Format: /done <user_id>")
        return
    try:
        target = int(parts[1])
        bot.send_message(
            target,
            f"Order kamu sudah selesai! Terima kasih sudah order di {NAMA_TOKO}",
            reply_markup=kb_menu_utama()
        )
        bot.send_message(ADMIN_ID, f"Notif selesai terkirim ke {target}")
    except Exception:
        bot.send_message(ADMIN_ID, "User ID tidak valid")


@bot.message_handler(commands=["cancel"])
def cmd_cancel(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "Format: /cancel <user_id>")
        return
    try:
        target = int(parts[1])
        bot.send_message(
            target,
            f"Order kamu dibatalkan. Hubungi @{ADMIN_USERNAME} untuk info lebih lanjut.",
            reply_markup=kb_menu_utama()
        )
        bot.send_message(ADMIN_ID, f"Notif cancel terkirim ke {target}")
    except Exception:
        bot.send_message(ADMIN_ID, "User ID tidak valid")


@bot.message_handler(commands=["proses"])
def cmd_proses(msg):
    if not is_admin(msg.from_user.id):
        return
    parts = msg.text.split()
    if len(parts) < 2:
        bot.send_message(ADMIN_ID, "Format: /proses <user_id>")
        return
    try:
        target = int(parts[1])
        bot.send_message(target, "Order kamu sedang diproses! Mohon tunggu ya.")
        bot.send_message(ADMIN_ID, f"Notif proses terkirim ke {target}")
    except Exception:
        bot.send_message(ADMIN_ID, "User ID tidak valid")


@bot.callback_query_handler(func=lambda c: c.data == "back_menu")
def back_menu(call):
    uid = call.from_user.id
    sessions[uid] = {"step": "menu", "order": {}}
    bot.edit_message_text(
        "Pilih layanan:",
        uid,
        call.message.message_id,
        reply_markup=kb_menu_utama()
    )


@bot.callback_query_handler(func=lambda c: c.data == "kat_joki")
def kat_joki(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "Joki Tugas - Pilih jenis:",
        call.from_user.id,
        call.message.message_id,
        reply_markup=kb_joki()
    )


@bot.callback_query_handler(func=lambda c: c.data == "kat_ppob")
def kat_ppob(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "PPOB - Pilih kategori:",
        call.from_user.id,
        call.message.message_id,
        reply_markup=kb_ppob()
    )


@bot.callback_query_handler(func=lambda c: c.data == "kat_game")
def kat_game(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "Top Up Game - Pilih game:",
        call.from_user.id,
        call.message.message_id,
        reply_markup=kb_game()
    )


@bot.callback_query_handler(func=lambda c: c.data == "ppob_kat_pulsa")
def ppob_pulsa(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "Pulsa - Pilih provider:",
        call.from_user.id,
        call.message.message_id,
        reply_markup=kb_provider("pulsa")
    )


@bot.callback_query_handler(func=lambda c: c.data == "ppob_kat_kuota")
def ppob_kuota(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        "Kuota - Pilih provider:",
        call.from_user.id,
        call.message.message_id,
        reply_markup=kb_provider("kuota")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("provider_"))
def pilih_provider(call):
    uid = call.from_user.id
    tab_name = call.data.replace("provider_", "")
    bot.answer_callback_query(call.id, "Memuat produk...")

    produk_list = get_sheet_data(SHEET_ID_PPOB, tab_name)

    if not produk_list:
        bot.edit_message_text(
            "Produk tidak tersedia atau belum diisi. Hubungi admin.",
            uid,
            call.message.message_id,
            reply_markup=kb_kembali("kat_ppob")
        )
        return

    sessions[uid] = sessions.get(uid, {"step": "menu", "order": {}})
    sessions[uid]["order"]["tab"] = tab_name

    if tab_name.startswith("kuota_"):
        subkats = list(dict.fromkeys([
            p["kategori"] for p in produk_list if p.get("kategori")
        ]))
        if subkats:
            bot.edit_message_text(
                f"Kuota {tab_name.replace('kuota_', '').title()} - Pilih kategori:",
                uid,
                call.message.message_id,
                reply_markup=kb_subkat(subkats, tab_name)
            )
            return

    back = "ppob_kat_pulsa" if tab_name.startswith("pulsa_") else "ppob_kat_kuota"
    sessions[uid]["order"]["produk_list"] = produk_list
    bot.edit_message_text(
        "Pilih produk:",
        uid,
        call.message.message_id,
        reply_markup=kb_produk(produk_list, back)
    )


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
        f"Kuota {provider.title()} - {subkat}:",
        uid,
        call.message.message_id,
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
            uid,
            call.message.message_id,
            reply_markup=kb_kembali("kat_game")
        )
        return

    sessions[uid] = sessions.get(uid, {"step": "menu", "order": {}})
    sessions[uid]["order"]["tab"] = tab_name
    sessions[uid]["order"]["produk_list"] = produk_list

    bot.edit_message_text(
        "Pilih nominal:",
        uid,
        call.message.message_id,
        reply_markup=kb_produk(produk_list, "kat_game")
    )


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

    tab = sesi.get("order", {}).get("tab", "")
    if tab in ["ml", "ff", "pubg", "hok"]:
        step = "game_isi_id"
        prompt = "Masukkan ID game kamu:"
    else:
        step = "ppob_isi_data"
        prompt = "Masukkan nomor HP / ID pelanggan:"

    sessions[uid] = {
        "step": step,
        "order": {
            "jenis": produk["nama"],
            "harga": produk["harga"],
            "kode": kode,
            "tab": tab
        }
    }

    bot.edit_message_text(
        f"Dipilih: {produk['nama']}\nHarga: Rp{int(produk['harga']):,}\n\n{prompt}",
        uid,
        call.message.message_id,
        reply_markup=kb_kembali()
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("joki_"))
def pilih_joki(call):
    uid = call.from_user.id
    key = call.data
    label = JOKI.get(key, "Joki Tugas")
    sessions[uid] = {"step": "joki_detail", "order": {"jenis": label}}
    bot.edit_message_text(
        f"Dipilih: {label}\n\nKetik detail tugas kamu (judul, deadline, instruksi):",
        uid,
        call.message.message_id,
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
    bot.send_message(
        uid,
        "Bukti bayar diterima! Admin akan segera memverifikasi.",
        reply_markup=kb_kembali()
    )
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
    bot.forward_message(ADMIN_ID, uid, msg.message_id)
    bot.send_message(ADMIN_ID, caption)
    sessions[uid]["step"] = "selesai"


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
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\n"
            f"Jenis: {order['jenis']}\n"
            f"Detail: {teks}\n"
            f"Ref: {order['ref']}\n\n"
            f"1. Tunggu admin konfirmasi harga\n"
            f"2. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)
            ]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "JOKI")

    elif step == "ppob_isi_data":
        order["detail"] = teks
        order["ref"] = f"PPB{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\n"
            f"Produk: {order['jenis']}\n"
            f"No/ID: {teks}\n"
            f"Harga: Rp{int(order['harga']):,}\n"
            f"Ref: {order['ref']}\n\n"
            f"1. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"2. Lakukan pembayaran\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)
            ]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "PPOB")

    elif step == "game_isi_id":
        order["detail"] = teks
        order["ref"] = f"GAME{uid}{int(time.time())}"
        sessions[uid]["step"] = "tunggu_bukpem"
        bot.send_message(
            uid,
            f"Order diterima!\n"
            f"Produk: {order['jenis']}\n"
            f"ID Game: {teks}\n"
            f"Harga: Rp{int(order['harga']):,}\n"
            f"Ref: {order['ref']}\n\n"
            f"1. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"2. Lakukan pembayaran\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)
            ]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "GAME")

    else:
        bot.send_message(uid, "Ketik /start untuk mulai order.")


if __name__ == "__main__":
    print(f"Bot {NAMA_TOKO} berjalan...")
    bot.infinity_polling()
