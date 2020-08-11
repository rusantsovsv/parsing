# этими скриптами будем создавать базы данных
import sqlite3 as sl

# создадим соединение (оно создаст базу, если база не существует)
con = sl.connect('db/parse_habr.db')

# создаем таблицу для хранения данных по запросу
def create_table(name, connector=None):
    with connector:
        connector.execute(f"""
            CREATE TABLE {name} (
                user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                date TEXT,
                title TEXT,
                likes TEXT,
                tags TEXT,
                post_link TEXT,
                post_text TEXT        
            );    
        """)

# создаем таблицу DATA_SCIENCE
create_table('DATA_SCIENCE', con)

