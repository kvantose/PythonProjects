import sqlite3


def writing_to_a_file(message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS title '
                   '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   ' message TEXT)')

    cursor.execute('SELECT COUNT(*) FROM title')

    row_count = cursor.fetchone()[0]
    if row_count > 10:
        cursor.execute('DELETE FROM title WHERE id = (SELECT id FROM title ORDER BY id ASC LIMIT 1)')
        conn.commit()

    cursor.execute('INSERT INTO title (message) VALUES (?)', (message,))

    conn.commit()
    cursor.close()
    conn.close()








# def writing_to_a_file(message):
#     with open('title.log', 'a', encoding='utf-8') as file:
#         file.write(f'--- {message}\n')
#     with open('title.log', 'r', encoding='utf-8') as fi:
#         lines = fi.readlines()
#         if len(lines) > 10:
#             with open('title.log', 'w', encoding='utf-8') as f:
#                 f.writelines(lines[1:])
