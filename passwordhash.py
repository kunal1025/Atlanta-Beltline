from werkzeug.security import check_password_hash, generate_password_hash
import db

# from user password and username
# take each dictionary from each and update the password

def hashing():
    conn = db.get_connection()
    sql = "SELECT username, password FROM user"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        users = cursor.fetchall()
        for user in users:
            hashedpass = generate_password_hash(user['password'])
            new = "UPDATE user set password = %s WHERE username = %s"
            cursor.execute(new, (hashedpass, user['username']))
            conn.commit()

hashing()
print('done')
