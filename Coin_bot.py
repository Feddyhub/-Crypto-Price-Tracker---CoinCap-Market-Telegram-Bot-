import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Telegram botunuzun token'ını buraya ekleyin
TOKEN = "7268436456:AAFXPpiYEAHN319bGrrMkzzYsysnst3i77M"

# CoinCap API endpoint'i
API_URL = "https://api.coincap.io/v2/assets"


async def get_crypto_price(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text('Lütfen bir kripto para simgesi belirtin. Örneğin: /price BTC')
        return

    crypto_symbol = context.args[0].upper()
    params = {
        'search': crypto_symbol,
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        if 'data' in data and data['data']:
            price = data['data'][0]['priceUsd']
            await update.message.reply_text(f'{crypto_symbol} fiyatı: ${price}')
        else:
            await update.message.reply_text(f'{crypto_symbol} için fiyat bilgisi bulunamadı.')
    except Exception as e:
        await update.message.reply_text(f'Hata: {e}')

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("price", get_crypto_price))

    app.run_polling()

if __name__ == '__main__':
    main()
