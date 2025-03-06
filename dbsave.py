import sqlite3
import pandas as pd
from datetime import date


# 插入数据到 SQLite 数据库
def zy_save_to_db(xs, jian_cha, shi_jian):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    out_str = ""
    if not shi_jian:
        shi_jian = date.today().strftime("%Y-%m-%d")
    for items in xs:
        item = items.split("|")
        count = cursor.execute('SELECT COUNT(*) FROM zuoye WHERE xue_hao = ? AND shi_jian = ? AND jian_cha= ? ',(item[0], shi_jian, jian_cha))
        if count.fetchone()[0] > 0:
            out_str += f"{item[1]} 于 {shi_jian} 已提交！\n"
            continue
        cursor.execute('INSERT INTO zuoye (jian_cha,xue_hao,shi_jian) VALUES (?, ?, ?)',
                   (jian_cha, item[0], shi_jian))
        out_str += f"{item[1]} 于 {shi_jian} 已提交！\n"
    conn.commit()
    conn.close()

    return out_str, tong_ji(shi_jian), zy_query_db("", shi_jian)

def tong_ji(shi_jian):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count(id) FROM zuoye WHERE shi_jian = ? AND jian_cha !=""', (shi_jian,))
    zy_count = cursor.fetchone()
    cursor.execute('SELECT count(id) FROM xuesheng')
    xs_count = cursor.fetchone()
    conn.commit()
    conn.close()
    res = f"{shi_jian}已提交{zy_count[0]},未提交{xs_count[0] - zy_count[0]}"
    return res

# 作业查询
def zy_query_db(xing_ming, shi_jian):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    if not shi_jian:
        shi_jian = date.today().strftime("%Y-%m-%d")
    sql = (
        'SELECT xuesheng.id,xuesheng.xing_ming,zy.jian_cha FROM xuesheng '
        'LEFT JOIN (SELECT shi_jian,xue_hao,jian_cha FROM zuoye '
        'WHERE zuoye.shi_jian = ? )zy ON xuesheng.id = zy.xue_hao'
    )
    if xing_ming:  # 如果输入不为空，按姓名查询
        sql += ' WHERE xing_ming = ?'
        cursor.execute(sql, (shi_jian, xing_ming))
    else:  # 如果输入为空，查询所有数据
        cursor.execute(sql, (shi_jian,))
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["ID", "姓名", "作业是否提交"])
    return df

# 未交作业查询
def wj_query_db(shi_jian):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    if not shi_jian:
        shi_jian = date.today().strftime("%Y-%m-%d")
    sql = (
        'SELECT id,xing_ming,"未交" FROM xuesheng '
        'WHERE id not in (SELECT xue_hao FROM zuoye WHERE shi_jian = ?)'
    )

    cursor.execute(sql, (shi_jian,))
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["ID", "姓名", "作业是否提交"])
    return df



def xs_save_to_db(xing_ming):
    if not xing_ming:
        return "请输入姓名！"
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO xuesheng (xing_ming) VALUES (?)', (xing_ming,))
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return f"{xing_ming} 已添加！学号为：{inserted_id}",xs_query_db("")


# 从 SQLite 数据库中查询数据
def xs_query_db(xing_ming):
    conn = sqlite3.connect('gradio_app.db')
    cursor = conn.cursor()
    if xing_ming:  # 如果输入不为空，按姓名查询
        cursor.execute('SELECT * FROM xuesheng WHERE xing_ming = ?', (xing_ming,))
    else:  # 如果输入为空，查询所有数据
        cursor.execute('SELECT * FROM xuesheng')
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["ID", "姓名"])
    return df

# def delete_db(name):
#     conn = sqlite3.connect('gradio_app.db')
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM users WHERE name = ?', (name,))
#     conn.commit()
#     conn.close()
