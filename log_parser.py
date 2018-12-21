#!/usr/bin/python3

# a-1. На входе:
# Имеются текстовые файлы с логами в таком формате:
# start_time | end_time | req_path | resp_code | resp_body
# start_time – точное время, когда запрос пришёл на веб-сервер, e.g. 24.05.2015 14:05:06
# end_time – точное время, когда запрос ушёл с веб-сервера
# req_path – запрашиваемый адрес, e.g. /index.html
# resp_code – код ответа, e.g. 200, 404, 500
# resp_body – тело ответа
#
# Что сделать:
# - написать скрипт на Python 3, которому на вход подаётся описанный выше
#   текстовой файл, а на выходе получаем следующие данные:
# - статистические характеристики времени обработки сервером всех запросов
#   (минимум, максимум, среднее арфиметическое, медиана)
# - Процент ошибочных запросов (ошибочные – если код вышее 400 или в теле
#   присутствует подстрока “error”)
# - Распределение числа вызовов по страницам (т.е. какую страницу сколько раз вызывали)

import datetime
import statistics

if len(sys.argv) < 2:
    sys.exit("No path file")

open_log_for_scan = open(sys.argv[1], 'r')

sessions_count = int(0)
error_requst = int(0)
request_processing_time = int(0)
timestatistic = []
requestpage = {}

# Подсчет ошибок
for session in open_log_for_scan:
    sessions_count += 1
    param = session.split(" | ")
    if 'error' in param[4] or 'Error' in param[4] or 'ERROR' in param[4] or int(param[3]) >= 400:
        error_requst += 1

# Сбор статистики времени обработки
    time_in = datetime.datetime.strptime(param[0], "%d.%m.%Y %H:%M:%S")
    time_out = datetime.datetime.strptime(param[1], "%d.%m.%Y %H:%M:%S")
    delta = time_out - time_in
    timestatistic.append (delta.seconds)

# Сбор статистики по вызываемым страницам
    if param[2] in requestpage:
        requestpage[param[2]] = requestpage[param[2]] + 1
    else:
        requestpage[param[2]] = 1

open_log_for_scan.close()

print ("СТАТИСТИКА ОБРАБОТКИ ЗАПРОСОВ")
print ("{0:>30}{1:<10}".format ("максимальное время (сек): ", max(timestatistic)))
print ("{0:>30}{1:<10}".format ("минимальное время (сек): ", min(timestatistic)))
print ("{0:>30}{1:<10}".format ("среднее время (сек): ", statistics.mean(timestatistic)))
print ("{0:>30}{1:<10}".format ("медиана (сек): ", statistics.median(timestatistic)))
print ("Ошибочных запросов: ", error_requst * 100 // sessions_count, "%")
print("\nРаспределение вызовов по страницам:")
for keys,values in requestpage.items():
    print(keys, ": ", values)

exit(0)
