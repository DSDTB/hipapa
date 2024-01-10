import pandas as pd
import streamlit as st
from sqlalchemy import text

###################用户表#################################
def create_usertable(c):
    c.execute(text("CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)"))


def login_user(username, password, c):
    r = c.execute(
        text(f'SELECT * FROM userstable WHERE username ="{username}" AND password = "{password}"'
    ))
    data = r.fetchall()
    return data


####################################################
def add_card(bm,cname,pname,phone,room,cs,sdate,edate,c):

    sql = f"""
INSERT INTO tb_card(bm,cname,pname,phone,room,cs,sdate,edate,flag)
VALUES ('{bm}','{cname}','{pname}','{phone}','{room}','{cs}','{sdate}','{edate}','0')
"""

    c.execute(text(sql))
    c.commit()
    
def batch_card_df(c):

    sql = """
    INSERT INTO tb_card 
SELECT * FROM tb_card_df
"""

    c.execute(text(sql))
    c.commit()
def update_card_df(c):
    sql1 = """
    DELETE FROM tb_card  
    WHERE bm IN (SELECT bm FROM tb_card_df) 
    """
    sql2 = """
    INSERT INTO tb_card 
SELECT * FROM tb_card_df
"""
    c.execute(text(sql1))
    c.execute(text(sql2))
    c.commit()

#@st.cache_data()
def focus_card_df(c,s):
#     df = _c.execute("select * from tb_card")
#     return df
    sql=f"select * from tb_card where cname||pname||phone like '%{s}%' order by bm desc "

    cur = c.execute(text(sql))
    df=cur.fetchall()
    return pd.DataFrame(df)

# @st.cache_data()
def all_card_df(c):
#     df = _c.execute("select * from tb_card")
#     return df

    cur = c.execute(text("select * from tb_card order by bm desc"))
    df=cur.fetchall()
    return pd.DataFrame(df)


def create_card(c):
    c.excute(text(
        """CREATE TABLE IF NOT EXISTS tb_card(

    bm      TEXT (20)   PRIMARY KEY
                        NOT NULL,
    cname   TEXT (20),
    pname   TEXT (20),
    phone   TEXT (11),
    room    TEXT (20),
    cs      INTEGER (8),
    sdate   TEXT (50),
    edate   TEXT (50),
    delay   TEXT (50),
    detimes INTEGER (3),
    flag    TEXT (10),
    url     TEXT (100) 
)"""
    ))


###################教室表#################################
def op_room_df(c):
    cur = c.execute(text("select bm,mc from tb_room"))
    df=cur.fetchall()
    return pd.DataFrame(df)


def create_room(c):
    c.execute(text(
        """CREATE TABLE IF NOT EXISTS tb_room (
    bm TEXT    PRIMARY KEY
               NOT NULL,
    mc TEXT    NOT NULL,
    qy TEXT,
    rs INTEGER,
    bz TEXT
    )"""
    ))


def add_room(bm, mc, qy, rs, bz, c):
    c.execute(text(
        f"INSERT INTO tb_room(bm,mc,qy,rs,bz) VALUES ('{bm}','{mc}','{qy}','{rs}','{bz}')"
    ))
    c.commit()


def all_room(c):
    r = c.execute(text("SELECT bm FROM tb_room"))
    data = r.fetchall()
    return data


def qry_room(bm, c):
    r = c.execute(text(f'SELECT * FROM tb_room WHERE bm ="{bm}" '))
    data = r.fetchall()
    return data


def delete_room(bm, c):
    c.execute(text(f'DELETE FROM tb_room WHERE bm="{bm}"'))
    c.commit()


def change_room(bm, mc, qy, rs, bz, c):
    c.execute( text(
        f'update tb_room SET mc ="{mc}",qy="{qy}",rs="{rs}",bz="{bz}"  WHERE bm="{bm}"'
    ))
    c.commit()


######################################################
def create_table(s):
    s.execute(
        "CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate,DATE)"
    )


def add_data(author, title, article, postdate, s):
    s.execute(
        f"INSERT INTO blogtable(author,title,article,postdate) VALUES ('{author}','{title}','{article}','{postdate}')"
    )
    s.commit()


def view_all_notes(s):
    e = s.execute("SELECT * FROM blogtable")
    data = e.fetchall()
    # for row in data:
    # 	print(row)
    return data


def view_all_titles(s):
    e = s.execute("SELECT DISTINCT title FROM blogtable")
    data = e.fetchall()
    # for row in data:
    # 	print(row)
    return data


def get_single_blog(title, s):
    e = s.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = e.fetchall()
    return data


def get_blog_by_title(title, s):
    e = s.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = e.fetchall()
    return data


def get_blog_by_author(author, s):
    e = s.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
    data = e.fetchall()
    return data


def get_blog_by_msg(article, s):
    e = s.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
    data = e.fetchall()
    return data


def edit_blog_author(author, new_author, s):
    e = s.execute(
        'UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author, author)
    )
    s.commit()
    data = e.fetchall()
    return data


def edit_blog_title(title, new_title, s):
    e = s.execute(
        'UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_title, title)
    )
    s.commit()
    data = e.fetchall()
    return data


def edit_blog_article(article, new_article, s):
    e = s.execute(
        'UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_article, article)
    )
    s.commit()
    data = e.fetchall()
    return data


def delete_data(title, s):
    s.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
    s.commit()
