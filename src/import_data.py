#!/usr/bin/env python3

import mysql.connector
import ast

""" 取得连接对象 """
conn = mysql.connector.connect(user='', password='', database='', host="", port=1111,
                               charset="utf8")
cu = conn.cursor()

with open(r'v1.txt', mode="r", encoding="utf-8") as f:
    for line in f.readlines():
        data = ast.literal_eval(line)
        try:
            for x in data:
                print(x['content'])
                print(x['createtime'])
                cu.execute("insert into playoff(vs, title, play, comm, create_time) values(%s, %s, %s, %s, %s);",
                           ("warrior_rocket", "western_final", "1", x['content'], x['createtime']))
                conn.commit()
        except Exception as e:
            print("操作异常: %s" % e)
            continue
        finally:
            pass

""" 游标关闭 """
cu.close()
""" 连接关闭 """
conn.close()
