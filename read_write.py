import csv
import glob
from connect_db import cur


def read_write():
    # создаем таблицу с общими названиями столбцов для всех файлов csv, столбец OTKLONENIE для подсчетов отклонения
    # от планового времени
    cur.execute('''CREATE TABLE if not exists PLAN_TABLE
         (ID SERIAL PRIMARY KEY NOT NULL,
         PROJECT TEXT NOT NULL,
         LEADER TEXT NOT NULL,
         DATE_PERIOD DATE NOT NULL,
         OTKLONENIE TEXT NULL);'''
                )
    # Создаем таблицу работников
    cur.execute('''CREATE TABLE if not exists WORKER
            (ID SERIAL NOT NULL,
            PROJECT TEXT NOT NULL,
            WORKER TEXT NOT NULL,
            WORK_PLAN TEXT NOT NULL,
            PRIMARY KEY(ID));'''
                )
    # читаем все файлы с именем Plan* (Plan1, Plan2, Plan3...)
    for Files in glob.glob("Plan*.csv"):
        with open(Files, 'r', newline='') as File_read:
            reader = list(csv.reader(File_read, delimiter=';'))

            for i in range(1, len(reader)):  # будем считывать начиная со 2 строчки i=1
                # выгружаем общие данные в созданные столбцы таблиц
                cur.execute("INSERT INTO PLAN_TABLE ( PROJECT, LEADER, DATE_PERIOD) VALUES ('%s','%s','%s')" % (
                    reader[i][0], reader[i][1], reader[i][2]))
                for k in range(3, len(reader[1])):  # добавляем в таблицу WORKER проекты имена работников и рабочие часы
                    column = reader[0][k]
                    worker = str(column.replace(' ', '_'))  # заменяем пробелы в названиях столбцов на "_"
                    cur.execute("INSERT INTO WORKER (PROJECT, WORKER, WORK_PLAN) VALUES ('%s','%s','%s')" % (
                        reader[i][0], worker, reader[i][k].replace(',', '.')))
                x = 0  # переменная для подсчетов запланированных часов
                y = 0  # переменная для подсчетов затраченных часов
                z = '0'  # переменная для подсчета отклонения планируемых часов
                for j in range(3, len(reader[1])):  # считываем ячейки с плано-часами для конкретного проекта
                    row = reader[i][j]
                    if row == "":  # игнорируем пустую ячейку
                        continue
                    row2 = row.replace(',', '.').split('/')  # разбиваем данные из ячейки по слэшу
                    x += float(row2[0])
                    y += float(row2[1])
                if x != 0:
                    z = str(round(((y - x) / x * 100), 3)) + "%"  # возможно неправильная формула для подсчета
                    # процента отклонения
                row3 = reader[i][0]  # название проекта
                # загружаем подсчитанное отклонения планочасов проекта row3 в бд
                cur.execute("UPDATE PLAN_TABLE SET OTKLONENIE = '%s' WHERE PROJECT = '%s'" % (z, row3))
