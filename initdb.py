import sqlite3

# 连接到 SQLite 数据库（如果不存在则创建）
conn = sqlite3.connect('gradio_app.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

# 提交更改并关闭连接
conn.commit()
conn.close()