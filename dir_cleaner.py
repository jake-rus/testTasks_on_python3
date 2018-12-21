#!/usr/bin/python3

# a-2. На входе: путь до директории
# Что сделать:
# - удалить всё содержимое директории кроме корневой папки
# - вывести информацию о том, сколько было удалено файлов того или иного типа
#   (папки считаем одним из типов файлов)
# - при удалении показывать прогресс-бар

import sys
import os
import progressbar

if len(sys.argv) < 2:
    sys.exit("No path directory")

dirPath = sys.argv[1]
counter_files = {}
quantity = sum(len(files) for root, dirs, files in os.walk(dirPath))

# Проверка прав на запись
if not os.access(dirPath,os.W_OK):
    sys.exit("Permission denid")

# Проверка не пустой директории
if quantity != 0:
    bar = progressbar.ProgressBar(maxval=quantity).start()
else:
    sys.exit("Directory is empty")

for root, dirs, files in os.walk(dirPath, topdown=False):
    i = 0
    for name in files:
        filePath = os.path.join(root, name)
        file_ext = os.path.splitext(filePath)[1]
        os.remove(filePath)
        i += 1
        bar.update(i)
        if file_ext in counter_files:
            counter_files[file_ext] = counter_files[file_ext] + 1
        else:
            counter_files[file_ext] = 1

    for name in dirs:
        os.rmdir(os.path.join(root, name))
        if 'dir' in counter_files:
            counter_files['dir'] = counter_files['dir'] + 1
        else:
            counter_files['dir'] = 1

bar.finish()
print("Удалены следующие файлы:")
print(counter_files)

exit(0)
