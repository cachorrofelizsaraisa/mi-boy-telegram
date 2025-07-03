import telebot
import re

API_TOKEN = '7456361483:AAEbZNRtbh53bvgS6DfJXdE6zb46qiWShZc'
bot = telebot.TeleBot(API_TOKEN)

whitelist_urls = []
url_regex = r"(https?://\S+)"

@bot.message_handler(func=lambda message: True)
def check_message(message):
    try:
        if message.chat.type in ["group", "supergroup"]:
            text_to_check = message.text or message.caption or ""

            # Si es un mensaje reenviado, intenta obtener el texto original
            if message.forward_from and (message.forward_from_message and message.forward_from_message.text):
                text_to_check = message.forward_from_message.text

            if text_to_check:
                matches = re.findall(url_regex, text_to_check)
                if matches:  # Si hay URLs en el mensaje
                    for url in matches:
                        if url not in whitelist_urls:
                            try:
                                # Primero envía la advertencia
                                user_name = ""
                                if message.forward_from:
                                    user_name = message.forward_from.first_name or f"Usuario (ID: {message.forward_from.id})"
                                else:
                                    user_name = message.from_user.first_name or f"Usuario (ID: {message.from_user.id})"
                                
                                warning_msg = bot.send_message(
                                    message.chat.id, 
                                    f"¡Advertencia, {user_name}! Los enlaces no están permitidos en este grupo. Por favor, evita compartir URLs.",
                                    reply_to_message_id=message.message_id
                                )
                                
                                # Luego elimina el mensaje con URL
                                bot.delete_message(message.chat.id, message.message_id)
                                
                                # Opcional: eliminar el mensaje de advertencia después de un tiempo
                                # bot.delete_message(message.chat.id, warning_msg.message_id)
                                
                            except telebot.apihelper.ApiException as e:
                                if e.error_code == 403:
                                    bot.send_message(
                                        message.chat.id,
                                        "⚠️ No tengo permisos para eliminar mensajes. Por favor, otórgame permisos de administrador."
                                    )
                                else:
                                    print(f"Error de API: {e}")
                            except Exception as e:
                                print(f"Error inesperado: {e}")
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    print("Bot iniciado...")
    bot.polling(none_stop=True)