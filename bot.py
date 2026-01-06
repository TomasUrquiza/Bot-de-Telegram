
import telebot
import requests
import random
import string

TOKEN = 'Tu Token Aquí'
bot = telebot.TeleBot(TOKEN)
tareas = {} 

@bot.message_handler(commands=['start', 'menu'])
def enviar_menu(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn_dolar = InlineKeyboardButton("💵 Dólar", callback_data="btn_dolar")
    btn_pass = InlineKeyboardButton("🔐 Generar Pass", callback_data="btn_pass")

    btn_ver_tareas = InlineKeyboardButton("📝 Ver mis Tareas", callback_data="btn_ver_tareas")
    btn_borrar_tareas = InlineKeyboardButton("🗑️ Borrar Todo", callback_data="btn_borrar_tareas")
    
    markup.add(btn_dolar, btn_pass, btn_ver_tareas, btn_borrar_tareas)
    
    mensaje_intro = (
        "🤖 **Sistema V4.0 Online**\n\n"
        "💡 **NUEVO:** Para agregar una tarea, escribe:\n"
        "`/tarea Comprar leche`\n"
        "`/tarea Estudiar Python`"
    )
    
    bot.reply_to(message, mensaje_intro, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['tarea'])
def agregar_tarea(message):

    texto_usuario = message.text.replace("/tarea", "").strip()
    id_usuario = message.chat.id

    if len(texto_usuario) > 0:
        
        if id_usuario not in tareas:
            tareas[id_usuario] = []
            
        
        tareas[id_usuario].append(texto_usuario)
        bot.reply_to(message, f"✅ Guardado: *{texto_usuario}*", parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ Escribe algo después del comando. Ej: `/tarea Ir al gym`", parse_mode="Markdown")


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: True)
def procesar_botones(call):
    chat_id = call.message.chat.id
    
    if call.data == "btn_ver_tareas":
        
        if chat_id in tareas and len(tareas[chat_id]) > 0:
            lista_texto = "📝 **Tus Tareas Pendientes:**\n\n"
            
            for i, tarea in enumerate(tareas[chat_id], 1):
                lista_texto += f"{i}. {tarea}\n"
            
            bot.send_message(chat_id, lista_texto, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "🤷‍♂️ No tienes tareas pendientes.")

    elif call.data == "btn_borrar_tareas":
        if chat_id in tareas:
            tareas[chat_id] = [] 
            bot.answer_callback_query(call.id, "¡Lista vaciada!")
            bot.send_message(chat_id, "🗑️ Todas las tareas fueron eliminadas.")
        else:
            bot.answer_callback_query(call.id, "Nada que borrar.")

    
    elif call.data == "btn_dolar":
        try:
            data = requests.get("https://dolarapi.com/v1/dolares/blue").json()
            bot.send_message(chat_id, f"💵 Blue Venta: ${data['venta']}")
        except: pass
        
    elif call.data == "btn_pass":
        chars = string.ascii_letters + string.digits
        pwd = ''.join(random.choice(chars) for i in range(10))
        bot.send_message(chat_id, f"🔐 Clave: `{pwd}`", parse_mode="Markdown")

    try: bot.answer_callback_query(call.id)
    except: pass

print("💾 Sistema de Memoria Activo...")
bot.infinity_polling()