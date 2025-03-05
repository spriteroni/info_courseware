import sqlite3

# 连接到 SQLite 数据库（如果不存在则创建）
conn = sqlite3.connect('gradio_app.db')
cursor = conn.cursor()

# 作业表
cursor.execute('''
CREATE TABLE IF NOT EXISTS zuoye (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jian_cha TEXT NOT NULL,
    xue_hao INTEGER NOT NULL,
    shi_jian TEXT NOT NULL
)
''')
# 学生信息
cursor.execute('''
CREATE TABLE IF NOT EXISTS xuesheng (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    xing_ming TEXT NOT NULL
)
''')

# 提交更改并关闭连接
conn.commit()
conn.close()