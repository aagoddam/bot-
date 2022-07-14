import  telebot
import psycopg2
from prettytable import PrettyTable
conn = psycopg2.connect(dbname='eureca', user='postgres',
                        password='postgres', host='172.28.2.117')
cursor = conn.cursor()


#cursor.execute('SELECT item.partnumber, item.distrib, item.itemid, item.productname, location.quantity, price.value, price.currencyid FROM ((eureca.item JOIN eureca.location ON (((item.itemid)::text = (location.itemid)::text))) JOIN eureca.price ON (((item.itemid)::text = (price.itemid)::text)));')

#records = cursor.fetchall()
#print(records)





bot = telebot.TeleBot('5525614928:AAH3LrJPa5ZRRfZPwNmmL_cSREvblzTIlUs')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите код')

@bot.message_handler()
def start(message):
    cursor.execute(
        f"SELECT item.partnumber, item.distrib, item.itemid, location.quantity, price.value, price.currencyid FROM ((eureca.item JOIN eureca.location ON (((item.itemid)::text = (location.itemid)::text))) JOIN eureca.price ON (((item.itemid)::text = (price.itemid)::text))) WHERE partnumber = '{str(message.text)}';")

    #cursor.execute(f'SElECT * FROM mytable1 WHERE integers = {int(message.text)}')
    records = cursor.fetchall()

    my_list = []
    for x in records:
        myrow = str(x)[1: -1].split(",")
        for y in myrow:
            my_list.append(y)

    #my_str = ','.join(my_list)

    th = ['partnumber', 'distrib', 'itemid', 'quantity', 'value', 'currencyid']
    td = my_list
    columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

    table = PrettyTable(th)  # Определяем таблицу.

    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]


    bot.send_message(message.chat.id, f'<pre><b>{table}</b></pre>', parse_mode='html')
    #bot.send_message(message.chat.id, f'```{table}```', parse_mode='Markdown')

print("zxc")

bot.polling(none_stop= True)