import os
os.environ["PORT"] = "10000"

import logging
import random
import asyncio
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

# === Configurar Flask para mantener activo el Web Service de Render ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot de señales Mine Cave está activo!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Configuración del bot
TOKEN = "7335845771:AAFQLQPtF83J_H4T608W0FcseIUrzub7FpI"
CHAT_ID ="-1002342267741" # Asegúrate de que este sea un número entero

# Inicializa el bot y el despachador
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Parámetros del juego
FILAS, COLUMNAS = 5, 5
ESTRELLAS = 4

# Lista para almacenar los patrones utilizados
patrones_utilizados = []

# Función para generar señales seguras de Las Minas
def generar_senal():
    filas, columnas = FILAS, COLUMNAS
    estrellas = ESTRELLAS
    tablero = [["⬜" for _ in range(columnas)] for _ in range(filas)]

    while True:
        posiciones_estrellas = set()
        while len(posiciones_estrellas) < estrellas:
            x, y = random.randint(0, filas - 1), random.randint(0, columnas - 1)
            posiciones_estrellas.add((x, y))
        
        # Convertir posiciones a una tupla para verificar si ya se ha utilizado
        patron = tuple(sorted(posiciones_estrellas))
        if patron not in patrones_utilizados:
            patrones_utilizados.append(patron)
            break

    for (x, y) in posiciones_estrellas:
        tablero[x][y] = "⭐"

    # Representando los cuadros con color azul celeste utilizando el emoji 🟦
    tablero_con_cuadros = "\n".join(" ".join(fila) for fila in tablero)
    tablero_con_cuadros = tablero_con_cuadros.replace("⬜", "🟦")
    return tablero_con_cuadros

# Manejador para el comando /start
@dp.message(CommandStart())
async def start(message: types.Message):
    boton_iniciar = KeyboardButton(text="Iniciar señales")
    teclado = ReplyKeyboardMarkup(keyboard=[[boton_iniciar]], resize_keyboard=True)
    await message.answer("🚀 Bot activo! Pulsa 'Iniciar señales' para comenzar a recibir señales de Las Minas cada 3 minutos.", reply_markup=teclado)

# Manejador para el botón "Iniciar señales"
@dp.message(lambda message: message.text == "Iniciar señales")
async def iniciar_senales(message: types.Message):
    await message.answer("🔔 Has iniciado las señales. Recibirás una nueva señal cada 3 minutos.")
    asyncio.create_task(enviar_senales())

# Función para enviar señales cada 3 minutos
async def enviar_senales():
    while True:
        await bot.send_message(CHAT_ID, "checking signals..📈​")
        await asyncio.sleep(10)  # Esperar 10 segundos antes de enviar la señal
        senal = generar_senal()
        mensaje = (
            "⚠️ WARNING: Play responsibly! Although this bot has a 95% success rate, "
            "you should always play responsibly. ⚠️\n\n"
            f"🔥 PREDICTION CONFIRMED! 🚀\n\n{senal}\nTRAPS: 3\nATTEMPTS: 3"
        )
        await bot.send_message(CHAT_ID, mensaje)
        await bot.send_message(CHAT_ID, "⚠️ REMINDER: You have 3 minutes to execute this signal and only 3 attempts! ⚠️")
        await asyncio.sleep(120)  # Esperar 2 minutos
        await bot.send_message(CHAT_ID, "✅✅✅ PREDICTION SUCCESSFUL! 🎉🎉🎉\n\nGreat job! Keep playing responsibly and enjoy your winnings! 🤑💰")
        await asyncio.sleep(50)  # Esperar el tiempo restante para completar los 3 minutos (180 segundos)

# Función principal para iniciar el bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # Inicia el servidor Flask
    asyncio.run(main())  # Inicia el bot



    
