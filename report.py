import csv
from connect_db import cur, con


# report() создает отчет о существующих проектах
def report():
    # получаем из бд строки PROJECT, LEADER, DATE_PERIOD, OTKLONENIE отсортированные по DATE_PERIOD в порядке
    # вострастания
    cur.execute("SELECT PROJECT, LEADER, DATE_PERIOD, OTKLONENIE from PLAN_TABLE ORDER BY DATE_PERIOD")
    rows = cur.fetchall()
    with open('Report.csv', 'w', newline='') as File:  # создаем файл для записи
        File_write = csv.writer(File, delimiter=';')
        name = ('Название проекта', 'Руководитель', 'Дата сдачи', 'Отклонение')
        File_write.writerow(name)  # записываем в файл названия столбцов
        for row in rows:
            File_write.writerow(row)  # записываем по столбцам данные из бд
    con.commit()
    con.close()
