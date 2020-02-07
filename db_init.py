import sqlite3
conn = sqlite3.connect('app.db')

c = conn.cursor()

c.execute('''CREATE TABLE search_history
             (created_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              query text)''')

c.execute('''Select * FROM search_history;''')

data = c.fetchone()# one line
data = c.fetchall()#list

conn.commit()
conn.close()