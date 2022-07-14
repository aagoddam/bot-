import  telebot
import psycopg2
from prettytable import PrettyTable
from telebot import types
from DB_functions import Database


IP = '"IsIndividual"'
LP = '"IsLegal"'
Emp = '"isEmployee"'

F_phone = "userphone"
F_name = "username"
F_TIN = "tin"
F_OrgName = "orgname"

#cursor.execute('SELECT item.partnumber, item.distrib, item.itemid, item.productname, location.quantity, price.value, price.currencyid FROM ((eureca.item JOIN eureca.location ON (((item.itemid)::text = (location.itemid)::text))) JOIN eureca.price ON (((item.itemid)::text = (price.itemid)::text)));')

#records = cursor.fetchall()
#print(records)


db = Database()

bot = telebot.TeleBot('5525614928:AAH3LrJPa5ZRRfZPwNmmL_cSREvblzTIlUs')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
RegButton = types.KeyboardButton('Зарегистрироваться')
markup.add(RegButton)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
IndividualPersonButton = types.KeyboardButton('?? Физ.лицо')
LegalPersonButton = types.KeyboardButton('?? Юр.лицо')
EmployeeButton = types.KeyboardButton('????? Сотрудник')
markup2.add(IndividualPersonButton, LegalPersonButton, EmployeeButton)

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MakeAnOrderButton = types.KeyboardButton('📦 Сделать заказ')
FindByIDButton = types.KeyboardButton('Поиск товара по ID')
ProfileButton = types.KeyboardButton('ℹ️ Мой профиль')
markup3.add(MakeAnOrderButton, ProfileButton, FindByIDButton)


markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
EditProfileButton = types.KeyboardButton('Редактировать свой профиль')
DeleteProfileButton = types.KeyboardButton('Удалить свой профиль')
markup4.add(EditProfileButton, DeleteProfileButton)

@bot.message_handler(commands = ['start'])
def start(message):

    #db.FieldDelete(message.chat.id)
    if not db.CheckID(message.chat.id):
        db.AddUser(message.chat.id)
        bot.send_message(message.chat.id,
                         'Для начала Вам необходимо зарегистрироваться',
                         parse_mode='html', reply_markup=markup)


        #db.FieldInput(message.chat.id, IP, 1)
        #db.FieldInput(message.chat.id, LP, 0)


        bot.register_next_step_handler(message, RegTypeChoice)
    else:
        # здесь должен быть список кнопок, доступных для каждых ролей отдельно

        bot.send_message(message.chat.id, 'Здравствуйте! Выберите одну из следующих функций:', reply_markup=markup3)
        bot.register_next_step_handler(message, ReggedUsers_Buttons)
    #Приветствие зареганого (хай ты крут ты принят)
    #Кнопка профиль (изменить свои данные, удалиться из бд, тд, тп)
    #В зависимости от флагов предлагать зарегаться как кто-то ещё
    #Функции просмотра бд (тоже кнопка)
    #Функция заказа (кнопппка)


def RegTypeChoice(message):
    if message.chat.type == 'private': #если сообщение не от бота, а от пользователя
        if message.text == 'Зарегистрироваться':
            bot.send_message(message.chat.id, '<b>Хто Вы?</b>', parse_mode='html', reply_markup=markup2)
            bot.register_next_step_handler(message, Roles)



def Roles(message):
    if message.text == '?? Физ.лицо':
        bot.send_message(message.chat.id,
                         'Для регистрации Вам необходимо ввести следующие данные: \n - <b>ФИО</b> \n - <b>Номер телефона</b>',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, 'Введите Ваше ФИО. Например: Иванов Иван Иванович')
        bot.register_next_step_handler(message, IP_get_FIO)
    elif message.text == '?? Юр.лицо':
        bot.send_message(message.chat.id,
                         'Для регистрации Вам необходимо ввести следующие данные: \n - <b>Наименование организации</b> \n - <b>ИНН</b>',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, 'Введите наименование Вашей организации. Например: ООО "ЭВРИКА"')
        bot.register_next_step_handler(message, LP_get_Name)
    elif message.text == '????? Сотрудник':
        bot.send_message(message.chat.id,
                         'Для регистрации Вам необходимо ввести <b>номер своего телефона</b>. Например: 88005553535',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, Emp_get_Phone)






#-------- Заносим ФИО физ.лица в БД --------#
def IP_get_FIO(message):
    # if (len(message.text) < 5 or len(message.text) > 70):
    #     bot.send_message(message.chat.id, 'Либо слишком мало символов, либо слишком много символов. Повторите попытку')
    # else:
        db.FieldInput(message.chat.id, F_name, message.text)
        bot.send_message(message.chat.id, 'Введите Ваш номер телефона. Например: 88005553535')
        bot.register_next_step_handler(message, IP_get_Phone)

#-------- Заносим номер телефона физ.лица в БД --------#
def IP_get_Phone(message):
    db.FieldInput(message.chat.id, F_phone, message.text)
    EndOfRegistration(message)








#-------- Заносим наименование юр.лица в БД --------#
def LP_get_Name(message):
    db.FieldInput(message.chat.id, F_OrgName, message.text)
    bot.send_message(message.chat.id, 'Введите ИНН. Например: 1234567890')
    bot.register_next_step_handler(message, LP_get_TIN)

#-------- Заносим ИНН юр.лица в БД --------#
def LP_get_TIN(message):
    db.FieldInput(message.chat.id, F_TIN, message.text)
    EndOfRegistration(message)








#-------- Заносим номер телефона сотрудника в БД --------#
def Emp_get_Phone(message):
    db.FieldInput(message.chat.id, F_phone, message.text)
    EndOfRegistration(message)








#-------- Завершение регистрации --------#
def EndOfRegistration(message):
    bot.send_message(message.chat.id,
                     'Регистрация окончена. \n<b>Ждите подтверждения.</b>', parse_mode='html')
    bot.send_message(message.chat.id, 'Выберите одну из следующих функций:', reply_markup=markup3)
    bot.register_next_step_handler(message, ReggedUsers_Buttons)


def ReggedUsers_Buttons(message):
    if message.chat.type == 'private':
        if message.text == '📦 Сделать заказ':
            if db.CheckAccess(message.chat.id, IP):
                bot.send_message(message.chat.id, 'Введите ID товара')
                bot.register_next_step_handler(message, OrderInputID)
            else:
                bot.send_message(message.chat.id, 'У вас недостаточно прав, ожидайте подтверждения регистрации', reply_markup=markup3)
                bot.register_next_step_handler(message, ReggedUsers_Buttons)
            #bot.send_message(message.chat.id, 'Функция "Сделать заказ" пока что не доработана. Подождите пару дней', reply_markup=types.ReplyKeyboardRemove())
            # + добавить кнопку назад
        elif message.text == 'ℹ️ Мой профиль':
            # здесь должна выводиться инфа о пользователе (в зависимости от ролей):
            # — ФИО + телефон (если физик)
            # — Наименование организации + ИНН (если юрик)
            # — номер телефона (если сотрудник)
            # bot.send_message(message.chat.id, 'Функция "Мой профиль" пока что не доработана. Подождите пару дней')

            bot.send_message(message.chat.id, 'Ниже представлена информация о Вас:', reply_markup=markup4)
            bot.send_message(message.chat.id, db.GetRow(message.chat.id))
            bot.register_next_step_handler(message, EditOrDeleteProfile)

        elif message.text == 'Поиск товара по ID':
            bot.send_message(message.chat.id, "Введите ID товара", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, FindByID)
            # + добавить кнопку назад


def EditOrDeleteProfile(message):
    if message.chat.type == 'private':
        if message.text == 'Редактировать свой профиль':

            # здесь должны быть кнопки с выбором того, что хочется редактировать.
            # это нужно будет уже согласовывать с БД как-то
            # то есть на кнопках писать те параметры, кому они принадлежат (физику, юрику или сотруднику)
            # + добавить кнопку назад
            bot.send_message(message.chat.id, '<b>Выберете роль в которой хотите изменить (добавить) данные</b>', parse_mode='html', reply_markup=markup2)
            bot.register_next_step_handler(message, Roles)
            pass
        elif message.text == 'Удалить свой профиль':
            markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            YesDeleteButton = types.KeyboardButton('Да, хочу удалить свои данные')
            markup5.add(YesDeleteButton)
            # пока что будет одна кнопка "Да, удалить", но должна быть еще кнопка "назад"
            bot.send_message(message.chat.id, 'Вы действительно хотите удалить свои данные?', reply_markup=markup5)
            db.FieldDelete(message.chat.id)
            bot.register_next_step_handler(message, DeleteProfile)


def DeleteProfile(message):
    if message.chat.type == 'private':
        if message.text == 'Да, хочу удалить свои данные':
            # SQL запрос чтобы удалить данные
            bot.send_message(message.chat.id, 'Вы успешно удалили свои данные.\nЕсли в будущем Вам понадобится пользоваться ботом, <b>необходима будет повторная регистрация</b>', parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        start(message)
        # elif message.text == 'Назад'


def OrderInputID(message):
    db.MakeOrder(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'Введите количество товара')
    bot.register_next_step_handler(message, OrderInputQuantity)

def OrderInputQuantity(message):
    db.OrderFieldInput(message.chat.id, "quantity", message.text)

    bot.send_message(message.chat.id, 'Информация о заказе принята', reply_markup=markup3)
    bot.register_next_step_handler(message, ReggedUsers_Buttons)


def FindByID(message):
    db.cursor.execute(
        f"SELECT item.distrib, item.itemid, location.quantity, price.value, price.currencyid FROM ((eureca.item JOIN eureca.location ON (((item.itemid)::text = (location.itemid)::text))) JOIN eureca.price ON (((item.itemid)::text = (price.itemid)::text))) WHERE partnumber = '{str(message.text)}';")


    records = db.cursor.fetchall()

    my_list = []
    for x in records:
        myrow = str(x)[1: -1].split(",")
        for y in myrow:
            my_list.append(y)

    #my_str = ','.join(my_list)

    th = ['distrib', 'itemid', 'quantity', 'value', 'currencyid']
    td = my_list
    columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

    table = PrettyTable(th)  # Определяем таблицу.

    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]


    bot.send_message(message.chat.id, f'<pre><b>{table}</b></pre>', parse_mode='html', reply_markup=markup3)

    bot.register_next_step_handler(message, ReggedUsers_Buttons)
    #bot.send_message(message.chat.id, f'```{table}```', parse_mode='Markdown')




@bot.message_handler(commands = ['help'])
def button1(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Я хачю пуэрчик", url="https://vk.com/m7k7r"))
    bot.send_message(message.chat.id, 'посоветуйте аниме подростку', reply_markup=markup)
print("zxc")


bot.polling(none_stop= True)





