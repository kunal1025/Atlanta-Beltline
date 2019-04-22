import check_password_hash, generate_password_hash
import db

# from user password and username
# take each dictionary from each and update the password

def hashing():
    conn = db.get_connection()
    sql = "SELECT Username, Password FROM user"
    with conn.cursor() as cursor:
        cursor.execute(sql, email)
        users = cursor.fetchall()
        for user in users:
            hashedpass = generate_password_hash(user.Password)
            new = "UPDATE user set password = %s WHERE user = %s"
            cursor.execute(new, (hashedpass, user))
            conn.commit()

hashing()
