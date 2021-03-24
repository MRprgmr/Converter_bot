import telebot
from telebot import types
import convertapi
import os
import time
import random
import string
from func_timeout import func_timeout, FunctionTimedOut


bot = telebot.TeleBot("token")


comment = False

exp_imp_typ = {
    973021229: ["", "", ""]
}

img_list1 = ["bmp","ico","jpeg","jpg","png","webp"]
img_list2 = ["jpg","pdf","png","webp"]
doc_list1 = ["csv", "doc", "docx", "ppt", "pptx","txt", "xls", "xlsx"]
doc_list2 = ["jpg", "pdf", "png", "txt"]
pdf_list = ["jpg", "png", "pptx", "txt"]
url_file = "https://api.telegram.org/file/bottoken/"

def get_random_string(length):
    letters = s
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def img_convert(img_url,id,msg):
        url = url_file + img_url
    
        bot.send_message(id, "⌛️  Converting file please wait...")
        name = get_random_string(4)
        convertapi.api_secret = 'W8JaOdZrK5YUOz2V'
        try:
            convertapi.convert(exp_imp_typ[id][1],{ 'File': url },from_format = exp_imp_typ[id][0]).save_files(name + "." + exp_imp_typ[id][1])
        except convertapi.exceptions.ApiError:
            bot.delete_message(id, msg+1)
            bot.send_message(id, f"❗️ We can't convert files from  <code>{exp_imp_typ[id][0]}</code>   to   <code>{exp_imp_typ[id][1]}</code>", parse_mode="HTML")
            exp_imp_typ[id][1] = ""
            exp_imp_typ[id][0] = ""
            exp_imp_typ[id][2] = ""
            return 0

        #bot.delete_message(id, msg)
        bot.delete_message(id, msg+1)
        bot.send_chat_action(id , "upload_document", timeout=4000)
        doc = open(name + '.' + exp_imp_typ[id][1], 'rb')
        bot.send_document(id, doc, caption=f"✅ Your file successfully converted from    <code>{exp_imp_typ[id][0]}</code>   to   <code>{exp_imp_typ[id][1]}</code>", parse_mode="HTML")
        doc.close()
        os.remove(name + "." + exp_imp_typ[id][1])
        exp_imp_typ[id][1] = ""
        exp_imp_typ[id][0] = ""
        exp_imp_typ[id][2] = ""

@bot.message_handler(commands = ['help'])
def help(msg):
    text = "You can convert your files to each other with this bot,\n In <b>Images</b> saction you can convert this formats of files:\n <code>bmp,ico, jpeg, jpg, png, webp</code>,\nIn <b>Microsoft office</b> you can covert your this format of files:\n<code>csv, doc, docx, ppt, pptx, xls, xlsx</code>, \n In <b>Pdf to</b> section you can covert your PDF files to other this files:\n<code>jpg, png, pptx, txt</code>\n📝 With Comment section you can add send your feedback to developer.\n<b>ALGORITHM GATEWAY</b> <code>Fintech & IT solution</code>"
    bot.send_message(msg.chat.id, text, parse_mode = "HTML")

@bot.message_handler(commands = ['start'])
def start(msg):
    exp_imp_typ.update({msg.from_user.id: ["", "", ""]})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("🏙 Images")
    btn2 = types.KeyboardButton("📘 Microsoft office")
    btn3 = types.KeyboardButton("📕 Pdf to")
    btn4 = types.KeyboardButton("🧑‍💻 About")
    btn5 = types.KeyboardButton("📝 Comment")
    markup.add(btn1,btn2,btn3)
    markup.add(btn4, btn5)
    help_text = f"Welcome   <b>{msg.from_user.first_name}</b>\nYou can convert your files with this bot,\nTo know how to use this bot send command /help"
    bot.send_message(msg.chat.id, help_text, reply_markup=markup, parse_mode="HTML")

  

@bot.message_handler(func=lambda msg: msg.text == "🏙 Images")
def image(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    exp_imp_typ.update({msg.from_user.id: ["", "", "img_1"]})
    markup = types.InlineKeyboardMarkup()
    for i in range(0, len(img_list1), 2):
        markup.add(types.InlineKeyboardButton(img_list1[i], callback_data=img_list1[i]), 
        types.InlineKeyboardButton(img_list1[i+1], callback_data=img_list1[i+1]))
    markup.add(types.InlineKeyboardButton("🏘 Home", callback_data="home"))
    bot.send_message(msg.chat.id, "Choose your image type:", reply_markup=markup)
    
    
@bot.message_handler(func=lambda msg: msg.text == "📘 Microsoft office")
def office(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    exp_imp_typ.update({msg.from_user.id: ["", "", "doc_1"]})
    markup = types.InlineKeyboardMarkup()
    for i in range(0, len(doc_list1), 2):
        markup.add(types.InlineKeyboardButton(doc_list1[i], callback_data=doc_list1[i]), 
        types.InlineKeyboardButton(doc_list1[i+1], callback_data=doc_list1[i+1]))
    markup.add(types.InlineKeyboardButton("🏘 Home", callback_data="home"))
    bot.send_message(msg.chat.id, "Choose your document type:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "📕 Pdf to")
def pdf_to(msg):
    exp_imp_typ.update({msg.from_user.id: ["pdf", "", "pdfto_select"]})
    bot.delete_message(msg.chat.id, msg.message_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, 4, 2):
        markup.add(types.InlineKeyboardButton(pdf_list[i], callback_data=pdf_list[i]), 
        types.InlineKeyboardButton(pdf_list[i+1], callback_data=pdf_list[i+1]))
    markup.add(types.InlineKeyboardButton("🏘 Home", callback_data="home"))
    bot.send_message(msg.chat.id, "🖍 Select your file format to covert from PDF format..", reply_markup=markup, parse_mode="HTML")
    

@bot.message_handler(content_types = ['text'])
def abcom(msg):
    global comment
    if msg.text == "🧑‍💻 About":
        bot.send_location(msg.chat.id, 40.783789, 72.3315272)
        about = "<b>Algorithm Gateway</b> <code>Fintech & IT solution:</code>\nTelegram: https://t.me/algorithmgate_way\nFacebook: https://www.facebook.com/algorithmgateway \n Website: http://algorithmgateway.com"
        bot.send_message(msg.chat.id, about, parse_mode="HTML")
    elif msg.text == "📝 Comment":
        comment = True
        bot.send_message(msg.chat.id, "📝 Send your commant to developer, it may add contribution for this program.")
    elif comment:
        comment = False
        text = "Username:  @" + msg.from_user.username + "\n" + msg.text
        bot.send_message(973021229, text)
        bot.send_message(msg.chat.id, "😁 Thank you for your commands")
    elif msg.text == "len(dict)":
        bot.send_message(973021229, len(exp_imp_typ))
    




@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    if call.data == "home":
        exp_imp_typ.update({call.from_user.id: ["", "", ""]})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton("🏙 Images")
        btn2 = types.KeyboardButton("📘 Microsoft office")
        btn3 = types.KeyboardButton("📕 Pdf to")
        btn4 = types.KeyboardButton("🧑‍💻 About")
        btn5 = types.KeyboardButton("📝 Comment")
        markup.add(btn1,btn2,btn3)
        markup.add(btn4, btn5)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Home page:", reply_markup=markup)

    if exp_imp_typ[call.from_user.id][2] == "img_1":
        exp_imp_typ[call.from_user.id][0] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        for i in range(0, len(img_list2), 2):
            markup.add(types.InlineKeyboardButton(img_list2[i], callback_data=img_list2[i]), 
        types.InlineKeyboardButton(img_list2[i+1], callback_data=img_list2[i+1]))
        markup.add(types.InlineKeyboardButton("🏘 Home", callback_data="home"))
        exp_imp_typ[call.from_user.id][2] = "img_2"
        bot.send_message(call.message.chat.id, "Choose your image type that you want will be convert:", reply_markup=markup)
    elif exp_imp_typ[call.from_user.id][2] == "img_2":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
        exp_imp_typ[call.from_user.id][1] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Send me your image in  👉 <code>{exp_imp_typ[call.from_user.id][0]}</code> 👈  type:",reply_markup=markup, parse_mode = "HTML")
        exp_imp_typ[call.from_user.id][2] = "import_img"
    elif exp_imp_typ[call.from_user.id][2] == "doc_1":
        exp_imp_typ[call.from_user.id][2] = "doc_2"
        exp_imp_typ[call.from_user.id][0] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        for i in range(0, len(img_list2), 2):
            markup.add(types.InlineKeyboardButton(doc_list2[i], callback_data=doc_list2[i]), 
            types.InlineKeyboardButton(doc_list2[i+1], callback_data=doc_list2[i+1]))
        markup.add(types.InlineKeyboardButton("🏘 Home", callback_data="home"))
        bot.send_message(call.message.chat.id, "Choose your document type that you want will be convert:", reply_markup=markup)
    elif exp_imp_typ[call.from_user.id][2] == "doc_2":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
        exp_imp_typ[call.from_user.id][1] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Send me your document in  👉 <code>{exp_imp_typ[call.from_user.id][0]}</code> 👈  type:", reply_markup=markup, parse_mode = "HTML")
        exp_imp_typ[call.from_user.id][2] = "import_doc"
    elif exp_imp_typ[call.from_user.id][2] == "pdfto_select":
        exp_imp_typ[call.from_user.id][2] = "import_pdf"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
        exp_imp_typ[call.from_user.id][1] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Send me your file type in  <code>PDF</code>  format\n❗️ It must be less than   <code>5 MB</code>", reply_markup=markup, parse_mode = "HTML")



@bot.message_handler(content_types = ['photo'])
def importphoto(msg):
    if exp_imp_typ[msg.from_user.id][2] == "import_img":
        try:
            bot.delete_message(msg.chat.id, msg.message_id-1)
        except telebot.apihelper.ApiException:
            pass
        fileid = msg.photo[0].file_id
        img_url = bot.get_file(fileid).file_path
        try:
            func_timeout(30, img_convert, args=(img_url, msg.chat.id, msg.message_id))
        except FunctionTimedOut:
            bot.send_message(msg.chat.id, "🕔 Sorry we coodn't covert your file, becouse run time")
    elif (exp_imp_typ[msg.from_user.id][2] == "import_doc") or (exp_imp_typ[msg.from_user.id][2] == "import_pdf"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
        bot.send_message(msg.chat.id, "⁉️ You have entered invailed type of file.\nPlease re-enter your file..", reply_markup=markup)



@bot.message_handler(content_types = ['document'])
def importphoto2(msg):
    if exp_imp_typ[msg.from_user.id][2] == "import_img":
        try:
            bot.delete_message(msg.chat.id, msg.message_id-1)
        except telebot.apihelper.ApiException:
            pass
        fileid = msg.document.file_id
        img_url = bot.get_file(fileid).file_path
        img_convert(img_url, msg.chat.id, msg.message_id)
    elif exp_imp_typ[msg.from_user.id][2] == "import_doc":
        if msg.document.file_size > 5000000:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("❌ Cancel converting", callback_data="home"))
            bot.delete_message(msg.chat.id, msg.message_id-1)
            bot.send_message(msg.chat.id, "❗️ This bot can only convert files less than <code>5 MB</code>,\nPlease resend your file..", reply_markup=markup, parse_mode="HTML")
        else:
            try:
                bot.delete_message(msg.chat.id, msg.message_id-1)
            except telebot.apihelper.ApiException:
                pass
            fileid = msg.document.file_id
            img_url = bot.get_file(fileid).file_path
            if img_url.endswith(exp_imp_typ[msg.from_user.id][0]):
                try:
                    func_timeout(60, img_convert, args=(img_url, msg.chat.id, msg.message_id))
                except FunctionTimedOut:
                    bot.send_message(msg.chat.id, "🕔 Sorry we coodn't covert your file, becouse run time")
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
                bot.send_message(msg.chat.id, "⁉️ You have entered invailed type of file.\nPlease re-enter your file..", reply_markup=markup)

    elif exp_imp_typ[msg.from_user.id][2] == "import_pdf":
        if msg.document.file_size > 5000000:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("❌ Cancel converting", callback_data="home"))
            bot.delete_message(msg.chat.id, msg.message_id-1)
            bot.send_message(msg.chat.id, "❗️ This bot can only convert files less than <code>5 MB</code>,\nPlease resend your file..", reply_markup=markup, parse_mode="HTML")
        else:
            try:
                bot.delete_message(msg.chat.id, msg.message_id-1)
            except telebot.apihelper.ApiException:
                pass
            fileid = msg.document.file_id
            img_url = bot.get_file(fileid).file_path
            if img_url.endswith(exp_imp_typ[msg.from_user.id][0]):
                try:
                    func_timeout(60, img_convert, args=(img_url, msg.chat.id, msg.message_id))
                except FunctionTimedOut:
                    bot.send_message(msg.chat.id, "🕔 Sorry we coodn't covert your file, becouse run time")

            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="home"))
                bot.send_message(msg.chat.id, "⁉️ You have entered invailed type of file.\nPlease re-enter your file..", reply_markup=markup)

        
        
bot.polling()