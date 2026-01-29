"""
Ma'lumotlar bazasi moduli - SQLite yordamida vazifalar va foydalanuvchilarni boshqarish
OOP tamoyiliga asoslangan
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
from config import Config


class Database:
    def __init__(self, db_name: str = None):
        """Database obyektini yaratish"""
        self.db_name = db_name or Config.DATABASE_NAME
        self.init_db()
    
    def get_connection(self):
        """Database ga ulanish"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Ma'lumotlar bazasini yaratish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Foydalanuvchilar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Vazifalar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                priority TEXT DEFAULT 'o''rta',
                deadline DATE,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str):
        """Yangi foydalanuvchi qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
        finally:
            conn.close()
    
    def add_task(self, user_id: int, task_name: str, priority: str = 'o\'rta', 
                 deadline: Optional[datetime] = None):
        """Yangi vazifa qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tasks (user_id, task_name, priority, deadline)
                VALUES (?, ?, ?, ?)
            ''', (user_id, task_name, priority, deadline))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return None
        finally:
            conn.close()
    
    def get_tasks(self, user_id: int, completed: bool = False) -> List[Tuple]:
        """Foydalanuvchi vazifalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, task_name, priority, deadline, created_at, completed_at
                FROM tasks
                WHERE user_id = ? AND completed = ?
                ORDER BY 
                    CASE priority
                        WHEN 'yuqori' THEN 1
                        WHEN 'o''rta' THEN 2
                        WHEN 'past' THEN 3
                    END,
                    deadline ASC,
                    created_at ASC
            ''', (user_id, 1 if completed else 0))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return []
        finally:
            conn.close()
    
    def complete_task(self, task_id: int):
        """Vazifani bajarilgan deb belgilash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE tasks
                SET completed = 1, completed_at = ?
                WHERE id = ?
            ''', (datetime.now(), task_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return False
        finally:
            conn.close()
    
    def delete_task(self, task_id: int):
        """Vazifani o'chirish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return False
        finally:
            conn.close()
    
    def get_task_count(self, user_id: int, completed: Optional[bool] = None) -> int:
        """Vazifalar sonini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if completed is None:
                cursor.execute('''
                    SELECT COUNT(*) FROM tasks WHERE user_id = ?
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = ?
                ''', (user_id, 1 if completed else 0))
            
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return 0
        finally:
            conn.close()
    
    def get_today_tasks(self, user_id: int) -> List[Tuple]:
        """Bugungi vazifalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().date()
        
        try:
            cursor.execute('''
                SELECT id, task_name, priority, deadline, created_at, completed_at
                FROM tasks
                WHERE user_id = ? AND completed = 0 AND deadline <= ?
                ORDER BY priority DESC, deadline ASC
            ''', (user_id, today))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return []
        finally:
            conn.close()
    
    def get_overdue_tasks(self, user_id: int) -> List[Tuple]:
        """Muddati o'tgan vazifalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().date()
        
        try:
            cursor.execute('''
                SELECT id, task_name, priority, deadline, created_at, completed_at
                FROM tasks
                WHERE user_id = ? AND completed = 0 AND deadline < ?
                ORDER BY deadline ASC
            ''', (user_id, today))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")
            return []
        finally:
            conn.close()
