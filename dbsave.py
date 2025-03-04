import sqlite3
import pandas as pd
# 插入数据到 SQLite 数据库
def save_to_db(name, age):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()
    return f"Saved: {name}, {age}"

# 从 SQLite 数据库中查询数据
def query_db(name):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    if name:  # 如果输入不为空，按姓名查询
        cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    else:  # 如果输入为空，查询所有数据
        cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["ID", "姓名", "年龄"])
    return df

def delete_db(name):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()
