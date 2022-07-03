import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Sale, Shop
DSN = "postgresql://postgres:Natalikud@localhost:5432/orm_test_db"
engine = sqlalchemy.create_engine(DSN)

#вызвали движок из моделс, таблицы успешно созданы
create_tables(engine)

#открыли сессию
Session = sessionmaker(bind=engine)
session = Session()

#записали данные из файла jsone, шаблон из ДЗ,
# изменила текст файла (столбцы не соответствовали названиям колонок (#shop и id_shop)
with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

#insert(вручную)
# pub1 = Publisher (name = 'O\u2019Reilly')
# pub2 = Publisher (name = 'Pearson')
# pub3 = Publisher (name = 'Microsoft Press')
# pub4 = Publisher (name = 'No starch press')

# b1 = Book(title='Programming Python, 4th Edition','1')


#создание запросов
#запрос выборки магазинов, продающих целевого издателя, например 'Pearson'
input1 = input(f'Введите имя издательства:')
query = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name.ilike(f"%{input1}%"))
for shop in query.all():
    print(f'Издательство {input1}... продается в магазине:{shop.name}, id магазина: {shop.id}')

# session.close()