import sys
from io import BytesIO
from find_spn_param import find_spn
import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

deltax, deltay = find_spn(toponym_to_find)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([deltax, deltay]),
    "l": "map",
    'pt': ",".join([toponym_longitude, toponym_lattitude]) + ',pm2dbm'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
a={'response': {'GeoObjectCollection': {'metaDataProperty': {
    'GeocoderResponseMetaData': {'request': 'Москва, ул. Ак. Королева, 12', 'results': '10', 'found': '1'}},
                                      'featureMember': [{'GeoObject': {'metaDataProperty': {
                                          'GeocoderMetaData': {'precision': 'exact',
                                                               'text': 'Россия, Москва, улица Академика Королёва, 12',
                                                               'kind': 'house', 'Address': {'country_code': 'RU',
                                                                                            'formatted': 'Россия, Москва, улица Академика Королёва, 12',
                                                                                            'postal_code': '127427',
                                                                                            'Components': [
                                                                                                {'kind': 'country',
                                                                                                 'name': 'Россия'},
                                                                                                {'kind': 'province',
                                                                                                 'name': 'Центральный федеральный округ'},
                                                                                                {'kind': 'province',
                                                                                                 'name': 'Москва'},
                                                                                                {'kind': 'locality',
                                                                                                 'name': 'Москва'},
                                                                                                {'kind': 'street',
                                                                                                 'name': 'улица Академика Королёва'},
                                                                                                {'kind': 'house',
                                                                                                 'name': '12'}]},
                                                               'AddressDetails': {'Country': {
                                                                   'AddressLine': 'Россия, Москва, улица Академика Королёва, 12',
                                                                   'CountryNameCode': 'RU', 'CountryName': 'Россия',
                                                                   'AdministrativeArea': {
                                                                       'AdministrativeAreaName': 'Москва',
                                                                       'Locality': {'LocalityName': 'Москва',
                                                                                    'Thoroughfare': {
                                                                                        'ThoroughfareName': 'улица Академика Королёва',
                                                                                        'Premise': {
                                                                                            'PremiseNumber': '12',
                                                                                            'PostalCode': {
                                                                                                'PostalCodeNumber': '127427'}}}}}}}}},
                                                                       'name': 'улица Академика Королёва, 12',
                                                                       'description': 'Москва, Россия', 'boundedBy': {
                                              'Envelope': {'lowerCorner': '37.602175 55.820566',
                                                           'upperCorner': '37.610386 55.825189'}},
                                          'Point': {'pos': '37.606281 55.822878'}}}]}}}