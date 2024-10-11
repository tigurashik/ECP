import mysql.connector
from models import User, Login
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="rootpass",
            database="information"
        )
        self.create_users_table()
        self.create_logins_table()
        self.seed_data()

    def create_users_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                last_activity DATETIME NOT NULL,
                name VARCHAR(100) NOT NULL UNIQUE,
                role VARCHAR(50) NOT NULL,
                connections TEXT,
                password VARCHAR(255) NOT NULL
            );
        """)
        self.connection.commit()
        cursor.close()

    def create_logins_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                login_time DATETIME NOT NULL,
                ip_address VARCHAR(45) NOT NULL,
                status VARCHAR(20) NOT NULL
            );
        """)
        self.connection.commit()
        cursor.close()

    def add_user(self, user: User):
        cursor = self.connection.cursor()
        hashed_password = self.hash_password(user.password)
        cursor.execute("""
            INSERT INTO users (last_activity, name, role, connections, password)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            user.last_activity,
            user.name,
            user.role,
            ",".join(user.connections),
            hashed_password
        ))
        self.connection.commit()
        cursor.close()

    def get_all_users(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, last_activity, name, role, connections, password FROM users;")
        rows = cursor.fetchall()
        users = []
        for row in rows:
            user = User(
                id=row['id'],
                last_activity=row['last_activity'],
                name=row['name'],
                role=row['role'],
                connections=row['connections'].split(',') if row['connections'] else [],
                password=row['password']
            )
            users.append(user)
        cursor.close()
        return users

    def authenticate_user(self, name: str, password: str) -> bool:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE name = %s;", (name,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            stored_password = row['password']
            return self.verify_password(password, stored_password)
        return False

    def add_login(self, login: Login):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO logins (name, login_time, ip_address, status)
            VALUES (%s, %s, %s, %s);
        """, (
            login.name,
            login.login_time,
            login.ip_address,
            login.status  # Устанавливаем статус
        ))
        self.connection.commit()
        cursor.close()

    def get_all_logins(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logins;")
        rows = cursor.fetchall()
        logins = []
        for row in rows:
            login = Login(
                id=row['id'],
                name=row['name'],
                login_time=row['login_time'],
                ip_address=row['ip_address'],
                status=row['status']  # Получаем статус из базы данных
            )
            logins.append(login)
        cursor.close()
        return logins

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.hash_password(password) == hashed

    def seed_data(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
        cursor.close()
        if count == 0:
            test_users = [
                User(
                    id=0,
                    last_activity=datetime.now(),
                    name="Alice",
                    role="Admin",
                    connections=["Bob", "Charlie"],
                    password="alicepass"
                ),
                User(
                    id=0,
                    last_activity=datetime.now(),
                    name="Bob",
                    role="User",
                    connections=["Alice"],
                    password="bobpass"
                ),
                User(
                    id=0,
                    last_activity=datetime.now(),
                    name="Charlie",
                    role="Moderator",
                    connections=["Alice"],
                    password="charliepass"
                )
            ]
            for user in test_users:
                self.add_user(user)
