import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 🔐 API Keys (User Provided)
RAPIDAPI_KEY = "55ad50313cmsh406dd1e39526ebcp1a81e2jsn8f74b5f30e3c"
BOT_TOKEN = "7696662096:AAHs9koeTREwB_qA2y2WWAGPEQqrgWf6HCU"

def get_vehicle_info(number):
    url = "https://rto-vehicle-information-india.p.rapidapi.com/getVehicleInfo"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "rto-vehicle-information-india.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    payload = {
        "vehicle_no": number,
        "consent": "Y",
        "consent_text": "I hereby give my consent for Eccentric Labs API to fetch my information"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()

        if "result" in data:
            r = data["result"]
            return (
                f"🚗 *Owner:* {r.get('owner_name', 'N/A')}\n"
                f"🛻 *Vehicle Class:* {r.get('vehicle_class', 'N/A')}\n"
                f"⛽ *Fuel Type:* {r.get('fuel_type', 'N/A')}\n"
                f"📅 *Reg. Date:* {r.get('registration_date', 'N/A')}\n"
                f"🛡️ *Insurance:* {r.get('insurance_upto', 'N/A')}\n"
                f"🔰 *RC Status:* {r.get('rc_status', 'N/A')}"
            )
        else:
            return "❌ No valid data found. Please check the vehicle number."

    except Exception as e:
        return f"⚠️ Error occurred: {str(e)}"

def start(update, context):
    update.message.reply_text("👋 Welcome! Send me a vehicle number like *RJ09AB1234*", parse_mode='Markdown')

def handle_message(update, context):
    vehicle_number = update.message.text.strip().upper()
    info = get_vehicle_info(vehicle_number)
    update.message.reply_text(info, parse_mode='Markdown')

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
