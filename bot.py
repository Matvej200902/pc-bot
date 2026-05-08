from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from wakeonlan import send_magic_packet
import paramiko
import os

TOKEN = os.getenv("8291688643:AAH3vPtYTn-9-P_fhxcHMz6Cd6ayMde3Fbc")
MAC = os.getenv("9c:6b:00:89:23:f4")
PC_IP = os.getenv("100.81.6.40")
USER = os.getenv("tabtabur")

keyboard = [
    ["🟢 Включить ПК", "🌙 Сон"],
    ["🔴 Выключить ПК", "📊 Статус"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def ssh_cmd(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PC_IP, username=USER)
    ssh.exec_command(cmd)
    ssh.close()

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🟢 Включить ПК":
        send_magic_packet(MAC)
        await update.message.reply_text("Отправил сигнал включения", reply_markup=markup)

    elif text == "🔴 Выключить ПК":
        ssh_cmd("sudo systemctl poweroff")
        await update.message.reply_text("Выключаю ПК", reply_markup=markup)

    elif text == "🌙 Сон":
        ssh_cmd("sudo systemctl suspend")
        await update.message.reply_text("ПК уходит в сон", reply_markup=markup)

    elif text == "📊 Статус":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(PC_IP, username=USER)
        stdin, stdout, stderr = ssh.exec_command("uptime")
        result = stdout.read().decode()
        ssh.close()
        await update.message.reply_text(result, reply_markup=markup)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.run_polling()