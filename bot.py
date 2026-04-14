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
SHEET_ID = "1hlrp0OoNbAw9peNsLV3rIrVG4uIL8NOClbGzNen3qtU"

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


def get_produk_ppob():
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        return sheet.get_all_records()
    except Exception as e:
        print(f"Error baca sheet: {e}")
        return []


def kb_menu_utama():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Joki Tugas", callback_data="kat_joki"))
    kb.add(InlineKeyboardButton("PPOB", callback_data="kat_ppob"))
    kb.add(InlineKeyboardButton("Tanya Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
    return kb
def kb_joki():
    kb = InlineKeyboardMarkup()
    for key, label in JOKI.items():
        kb.add(InlineKeyboardButton(label, callback_data=key))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
    return kb


def kb_ppob(produk_list):
    kb = InlineKeyboardMarkup()
    for p in produk_list:
        label = f"{p['nama']} - Rp{int(p['harga']):,}"
        kb.add(InlineKeyboardButton(label, callback_data=f"ppob_{p['kode']}"))
    kb.add(InlineKeyboardButton("Kembali", callback_data="back_menu"))
    return kb


def kb_kembali():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Menu Utama", callback_data="back_menu"))
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
        bot.send_message(target, f"Order kamu sudah selesai! Terima kasih sudah order di {NAMA_TOKO}", reply_markup=kb_menu_utama())
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
        bot.send_message(target, f"Order kamu dibatalkan. Hubungi @{ADMIN_USERNAME} untuk info lebih lanjut.", reply_markup=kb_menu_utama())
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
    bot.edit_message_text("Pilih layanan:", uid, call.message.message_id, reply_markup=kb_menu_utama())


@bot.callback_query_handler(func=lambda c: c.data == "kat_joki")
def kat_joki(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Joki Tugas - Pilih jenis:", call.from_user.id, call.message.message_id, reply_markup=kb_joki())


@bot.callback_query_handler(func=lambda c: c.data == "kat_ppob")
f"1. Cek info payment: {CHANNEL_PAYMENT}\n"
            f"2. Lakukan pembayaran\n"
            f"3. Kirim bukti bayar di sini (foto)",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Info Payment", url=CHANNEL_PAYMENT)]])
        )
        username_buyer = f"@{msg.from_user.username}" if msg.from_user.username else str(uid)
        kirim_notif_admin(uid, order, username_buyer, "PPOB")

    else:
        bot.send_message(uid, "Ketik /start untuk mulai order.")


if name == "main":
    print(f"Bot {NAMA_TOKO} berjalan...")
    bot.infinity_polling()
