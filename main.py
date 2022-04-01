import fake_useragent
import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

from auth_data import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет, напиши << Скидки >> для получения списка скидок!  ")

    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("скидки")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    @bot.message_handler(content_types=["text"])
    def send_discount(message):
        if message.text.lower() == "скидки":
            try:
                user = fake_useragent.UserAgent().random
                headers = {
                    "User-Agent": user,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

                }

                url = "https://5ka.ru/special_offers/"

                req = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(req.text, 'lxml')

                articles = soup.find("div", class_="items-list").find_all("div", class_="product-card item")

                for article in articles:
                    article_price_with_discount = article.find("div", class_="price-discount").find("span").text.strip()
                    article_price_with_out_discount = article.find("div", class_="price-discount").find("span",
                                                                                                        class_="price-regular").text.strip()
                    article_name = article.find("div", class_="image-cont").find("img").get("alt")
                    article_date = article.find("div", class_="item-date").text.strip()
                    bot.send_message(
                        message.chat.id,
                        f"Название товара: {article_name} \n Цена со скидкой: {article_price_with_discount} \n Цена без скидки: {article_price_with_out_discount} \n Дата действия: {article_date} ")
            except Exception:
                bot.send_message(message.chat.id, "Упс.. что то пошло не так")
        else:
            bot.send_message(message.chat.id, "Введите << Скидки >>")

    bot.polling()


def main():
    telegram_bot(token)


if __name__ == '__main__':
    main()
