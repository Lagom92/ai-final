import sqlite3
conn = sqlite3.connect('app.db')

c = conn.cursor()

c.execute('''CREATE TABLE thinkB
             (created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              question text,
              answer text)''')

c.execute('''Select * FROM thinkB;''')

data = c.fetchone()# one line
data = c.fetchall()#list

conn.commit()
conn.close()