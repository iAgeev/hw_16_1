# import json
# import os
# import main
#
#
# def load_json(file_json):
#     """Чтение данных из json-файла"""
#     with open(file_json, mode='r', encoding='utf-8') as file:
#         data = json.load(file)
#         return data
#
#
# def users_db_load(db_table):
#     """Загрузка данных в БД"""
#     users = load_json(os.path.join('data', 'users.json'))
#     for user in users:
#         db.session.add(
#             db_table(
#                 id=user.id,
#                 first_name=user.first_name,
#                 last_name=user.last_name,
#                 age=user.age,
#                 email=user.email,
#                 role=user.role,
#                 phone=user.phone
#             )
#         )
#     db.session.commit()





