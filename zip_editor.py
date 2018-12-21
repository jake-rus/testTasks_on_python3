#!/usr/bin/python3

# a-3.На входе: zip архив.
# структура архива:
# - директория "test" содержащая файл - "файл1.xml" и директорию - "dir"
# - файл "главный.xml"
# - файл "не совсем главный.xml"
# Что сделать:
# -директорию dir переименовать в dir1
# -в файле "главный.xml" у всех тэгов <tag> атрибуту "name" к существующему значению дописать "1"
# -в файле "главный.xml" у всех тэгов <tag1> атрибуту "name" к существующему значению дописать "1"
# -в файле "не совсем главный.xml" у всех тэгов <tag1> атрибуту "name" к существующему значению дописать "1"
# -упаковать в архив с тем же именем.

import sys
import os
import zipfile
import xml.etree.ElementTree as etree

def xml_modify (filePath, element, attribute, addvalue):
    tree = etree.parse(filePath) #синтаксический анализ
    root = tree.getroot() # получение корневого элемента
    all_entries = tree.findall(element) #поиск элемента любой вложенности
    for entries in all_entries: #замена значения атрибута
        entries.attrib[attribute] = entries.attrib[attribute] + addvalue
    modFile = open(filePath, 'w')
    tree.write(modFile, encoding="unicode", xml_declaration=True, method="xml")
    modFile.close()

# проверка аргументов и файла
if len(sys.argv) < 2:
    sys.exit("No path file")
zipFile = sys.argv[1]

if not zipfile.is_zipfile(zipFile):
    sys.exit("is not zip file")

if not os.access(zipFile,os.W_OK):
    sys.exit("Permission denid")

# Распаковка во временную директорию
dirTemp = os.path.splitext(zipFile)[0] + "~18"
os.mkdir(dirTemp)
z = zipfile.ZipFile(zipFile, 'r')
z.extractall(dirTemp)
z.close()
os.remove(zipFile)

# Внесение изменений
os.rename((dirTemp + "/test/dir"), (dirTemp + "/test/dir1"))
xml_modify(dirTemp + "/главный.xml", './/tag', 'name', '1')
xml_modify(dirTemp + "/главный.xml", './/tag1', 'name', '1')
xml_modify(dirTemp + "/не совсем главный.xml", './/tag1', 'name', '1')

#Добавление в архив
os.chdir(dirTemp)
z = zipfile.ZipFile(zipFile, 'w')
for root, dirs, files in os.walk('.', topdown=False):
    for file in dirs:
        z.write(os.path.join(root, file))
    for file in files:
        if file != zipFile:
            z.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))
    for file in dirs:
        os.rmdir(os.path.join(root, file))

z.close()
os.chdir('..')
os.rename(dirTemp + '/' + zipFile, zipFile)
os.rmdir(dirTemp)
exit(0)
