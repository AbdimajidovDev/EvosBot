import methods
from methods import send_main_menu
from register import check, check_data_decorator
from database import Database
import globals
from telegram import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

db = Database("db-evos.db")


@check_data_decorator
def message_handler(update, context):
    message = update.message.text
    user = update.message.from_user
    state = context.user_data.get('state', 0)
    db_user = db.get_user_by_chat_id(user.id)

    if state == 0:
        check(update, context)

    elif state == 1:
        if not db_user['lang_id']:

            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id, "lang_id", 1)
                check(update, context)

            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id, 'lang_id', 2)
                check(update, context)

            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )

        elif not db_user['first_name']:
            db.update_user_data(user.id, 'first_name', message)
            check(update, context)

        elif not db_user['last_name']:
            db.update_user_data(user.id, 'last_name', message)
            buuttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']], request_contact=True)]
            ]
            check(update, context)

        elif not db_user['phone_number']:
            db.update_user_data(user.id, 'phone_number', message)
            check(update, context)

        else:
            check(update, context)

    elif state == 2:
        if message == globals.BTN_ORDER[db_user['lang_id']]:
            categories = db.get_categories_by_parent()
            print(categories)
            buttons = methods.send_category_buttons(categories=categories, lang_id=db_user['lang_id'])

            update.message.reply_text(
                text=globals.TEXT_ORDER[db_user['lang_id']],
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=buttons,
                )
            )

        elif message == globals.BTN_EVOS_FAMILY[db_user['lang_id']]:
            caption = globals.ABOUT_COMPANY[db_user['lang_id']]

            with open('images/evos.jpg', 'rb') as photo_file:
                update.message.reply_photo(
                    photo=photo_file,
                    caption=caption,
                    parse_mode='HTML'
                )

        elif message == globals.BTN_MY_ORDERS[db_user['lang_id']]:
            if context.user_data.get("carts", {}):
                carts = context.user_data.get("carts")
                text = "\n"
                lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
                total_price = 0

                for cart, val in carts.items():
                    product = db.get_product_for_cart(int(cart))
                    text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
                    total_price = product['price'] * val
                text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"

                update.message.reply_text(
                    text=f"<b>Ma'lumotlarim:</b>\n\n"
                         f"👤 <b>Ism-familiya:</b> {db_user['first_name']} {db_user['last_name']}\n"
                         f"📞 <b>Telefon raqam:</b> {db_user['phone_number']} \n\n"
                         f"📥 <b>Buyurtmalarim:</b> \n"
                         f"{text}",
                    parse_mode='HTML'
                )
            else:
                update.message.reply_text(
                    text=globals.NO_ZAKAZ[db_user['lang_id']])

        elif message == globals.BTN_COMMENTS[db_user['lang_id']]:
            update.message.reply_text(
                text="📝 Biror fikringiz yo taklifingiz bo'lsa yozib qoldiring!\nBiz albatta so'rovingizni ko'rib chiqamiz."
            )
            think = update.message.text
            print('think: ', think)

        elif message == globals.BTN_SETTINGS[db_user['lang_id']]:

            reply_markup = ReplyKeyboardMarkup([
                [KeyboardButton(text=globals.BTN_PERSONAL_SETTINGS[db_user['lang_id']]), KeyboardButton(text=globals.BTN_LANGUAGE_SETTINGS[db_user['lang_id']])],
                [KeyboardButton(text=globals.TEXT_MAIN_MENU[db_user['lang_id']])],
            ], resize_keyboard=True)
            context.bot.send_message(chat_id=update.message.from_user.id,text='⚙️ Sozlamalar menyusi', reply_markup=reply_markup)

        elif message == globals.TEXT_MAIN_MENU[db_user['lang_id']]:
            send_main_menu(context=context, chat_id=update.message.from_user.id, lang_id=db_user['lang_id'])

        elif message == globals.BTN_PERSONAL_SETTINGS[db_user['lang_id']]:
            info = db.info(chat_id=user.id)
            print('info = ', info)
            text = f"Isim: {info[0]['first_name']}\nFamilya: {info[0]['last_name']}\nTelefon raqam: {info[0]['phone_number']}"

            update.message.reply_text(text=text)

        elif message == globals.BTN_LANGUAGE_SETTINGS[db_user['lang_id']]:

            buttons = [
                [KeyboardButton(text=globals.BTN_LANG_UZ)],
                [KeyboardButton(text=globals.BTN_LANG_RU)],
            ]
            update.message.reply_text(
                text=globals.CHOOSE_LANG,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=buttons,
                    resize_keyboard=True
                )
            )

        if message == globals.BTN_LANG_UZ:
            db.update_user_data(user.id, "lang_id", 1)
            check(update, context)

        elif message == globals.BTN_LANG_RU:
            db.update_user_data(user.id, 'lang_id', 2)
            check(update, context)



    elif state == 3:
        if message == globals.BTN_LANG_UZ:
            db.update_user_data(db_user['chat_id'], 'lang_id', 1)
            context.user_data["state"] = globals.STATES['reg']
            check(update, context)

        elif message == globals.BTN_LANG_RU:
            db.update_user_data(db_user['chat_id'], 'lang_id', 2)
            context.user_data["state"] = globals.STATES['reg']
            check(update, context)

        else:
            update.message.reply_text(
                text=globals.TEXT_LANG_WARNING
            )

    else:
        update.message.reply_text("Salom")


