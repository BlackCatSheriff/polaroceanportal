#-*- coding: utf-8 -*-
import sqlite3
import hashlib
import board
import collections

def createuser(username,password,name,email,workplace):
    #检测是否有相同的username
    conn1 = sqlite3.connect(board.DatabasePath)
    conn1.row_factory = sqlite3.Row
    conn1.execute("pragma foreign_key=on")
    c1 = conn1.cursor()

    try:
        c1.execute("\
    select username as username \
    from \
    	register \
    where name=?;", \
                  (username,))
    except (sqlite3.DatabaseError) as e:
        print e
        return None
    else:
        user_row = c1.fetchone()
        if user_row == None:
            # 填充数据

            conn = sqlite3.connect(board.DatabasePath)
            conn.row_factory = sqlite3.Row
            conn.execute("pragma foreign_key=on")
            c = conn.cursor()

            md5 = hashlib.md5()
            md5.update(password)
            encrypted_passwd = md5.hexdigest()

            try:
                c.execute("\
                          insert into register (name,work,email,username,password) values (?,?,?,?,?);", \
                          (name, workplace, email, username, encrypted_passwd))
                c.execute("select last_insert_rowid() as user_id from register;")

            except (sqlite3.DatabaseError) as e:
                print e
                conn.rollback()
                return False
            else:
                conn.commit()
                return True
            finally:
                conn.close()


        else:
            return False
    finally:
        conn1.close()







