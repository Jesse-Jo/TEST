"""
@author:Jesse

这是一个模拟注册登录的程序
1. 注册：输入账号和密码，登记到数据库中
2. 登录：将账号与数据库中的密码进行比对，正确则登陆成功

"""

import pymysql


# 登录交互界面
def GUI():
    while True:
        print("""
        +============+
        |   注册(R)   |
        |   登陆(L)   |
        +============+
        """)
        action = input("请选择操作：(R/L)")
        if action == 'R':
            if register():
                response = input("注册成功，是否直接登录(Y/N)")
                if response == 'Y':
                    print("登录成功！")
                    break
                else:
                    continue
            else:
                print("注册失败！")
                continue
        elif action == 'L':
            if login():
                print("登陆成功！")
                break
            else:
                print("登录失败！")
                continue
        else:
            print("请重新选择...")
            continue


def register():
    # 获取并检查用户名
    while True:
        user_name = input("用户名：")
        # 检查用户名是否重合(读数据库)
        sql = "select * from register where user_name='{}';".format(user_name)
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            print("用户名已存在！请重新输入...")
            continue
        break
    # 检查密码
    while True:
        password = input("密码：")
        if len(password) < 8:
            print("密码不能少于8位！")
            continue
        break
    # 将审核通过的账号和密码写入数据库
    sql = "insert into register (user_name, password) value (%s, %s);"
    try:
        cur.execute(sql, [user_name, password])
        db.commit()
        return True
    except Exception as e:
        # 写入失败时，退回上一步
        db.rollback()
        print(e)
        return False


def login():
    # 获取用户名，检查是否存在
    while True:
        user_name = input("请输入用户名：")
        sql = "select * from register where user_name='{}';".format(user_name)
        result = cur.execute(sql)
        if not result:
            print("用户名不存在！")
            continue
        break
    # 获取登录密码，最多输入三次
    t = 3
    while t > 0:
        password = input("请输入密码：")
        sql = "select password from register where user_name=%s;"
        cur.execute(sql, [user_name])
        if password == cur.fetchone()[0]:
            return True
        else:
            t -= 1
            print("密码错误，请重新输入...(还剩{}次机会)".format(t))
    return False


if __name__ == '__main__':
    # 连接数据库
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='debian-sys-maint',
                         password='S73ItwyEQUk90n7S',
                         database='User',
                         charset='utf8')
    # 获取游标
    cur = db.cursor()
    # 启动GUI
    GUI()
    # 断开数据库的连接
    cur.close()
    db.close()
