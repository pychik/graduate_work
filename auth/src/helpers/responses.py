from http import client


MAIN_RESPONSES = {
    client.OK: 'Запрос выполнен успешно',
    client.NOT_FOUND: 'Запись не найдена',
    client.BAD_REQUEST: 'Переданы некорректные данные'
}
READ_RESPONSES = {
    client.OK: 'Запрос выполнен успешно',
    client.NOT_FOUND: 'Запись не найдена',
}
ADD_RESPONSES = {
    client.CREATED: 'Запись добавлена',
    client.NOT_FOUND: 'Запись не найдена',
}
DELETE_RESPONSES = {
    client.BAD_REQUEST: 'Переданы некорректные данные',
    client.NO_CONTENT: 'Запись удалена'
}
