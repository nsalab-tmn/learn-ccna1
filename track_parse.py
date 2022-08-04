#!/usr/bin/python3
import os, json, re, argparse

'''
для использования необходимо поместить каталог "templates" и этот скрипт в одно место
При запуске, по запросу, указать путь к каталогу, который надо запарсить (работает как относительный, так и абсолютный путь)
Также указать имя курса

!!!! применяется только для парсинга курсов и создания их метаданных! К материалам применять не стоит
!!!! ВАЖНО: если указывается относительный путь к каталогу с треком, то текущим каталогом является каталог, из которого пускается скрипт, а не где он лежит!
'''

def set_args():
    parser = argparse.ArgumentParser(description='Course parser')
    parser.add_argument('--path', type=str, help='path to course directory')
    parser.add_argument('--title', type=str, help='course title')
    parser.add_argument('--tag', type=str, help='course tag file')
    return parser


def get_dir(args_obj):
    args = args_obj.parse_args()
    if args.path:
        return args.path
    else:
        path_dir = input("Path to directory: ")
        return path_dir

def get_title(args_obj):
    args = args_obj.parse_args()
    if args.title:
        return args.title
    else:
        title = input("Course title: ")
        return title


def get_tag(args_obj):
    args = args_obj.parse_args()
    if args.tag:
        return args.tag
    else:
        tag = input("Path to tag file: ")
        return tag


# Создание списка материалов для размещения в ключе 'materials'
def create_materials(list_dir: list, materials=[]):
    if not list_dir:
        return materials
    if check_material(list_dir[0]):
        materials.append({ "$ref": f'./{list_dir[0]}/learn-metadata.json' })
    return create_materials(list_dir[1:], materials)
   
     
# Формирование контента метаданных из шаблолна
# title -  ожидается строка, приинимает RU в т.ч.
# materials - ожидается список из словарей с ref ссылками
# tags - ожидается строка .. или ../.. (в зависимости от относительного уровня расположения файла с тегами). Уровень указывается относительно metadata
def create_course_metadata(title:str, materials:list, tags: str):
    with open(f'{os.curdir}/templates/course-tpl.json','r') as c_tpl:
        json_content = json.load(c_tpl)

    json_content['materials'] = materials
    json_content['title'] = title
    json_content['tags'] = { "$ref": f'{tags}/material-tags.json'}
    
    return json_content

def check_material(material_name:str):
    if re.match(r'^\d\d\..+', material_name):
        return True
    return False

if __name__ == '__main__':
    
    # Пример применения функций
    args = set_args()
    parse_dir = get_dir(args)   # Например, ./01-icmp
    course_title = get_title(args)
    tag = get_tag(args)
    try:
        course_content = os.listdir(f'{parse_dir}')
        course_materials = create_materials(course_content)
        metadata = create_course_metadata(course_title, course_materials, tag)
   
        with open(f'{parse_dir}/learn-metadata.json', 'w', encoding='utf-8') as learn_metadata:
           json.dump(metadata, learn_metadata, indent=4, ensure_ascii=False)
    except:
       print('Directory not found')
