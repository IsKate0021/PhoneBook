import re
import os



class FileHandler():
    """Класс для работы с файлом для хранения данных"""
    def __init__(self, file_path) -> None:
        """
        Чтение данных из файла. Создание файла при его отсутствии
        
        Args:
        file_path (str): Путь к файлу для хранения данных Телефонной книги

        Returns:
            None
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'a') as file:
                pass

        with open(self.file_path, 'r', encoding="utf-8") as file:
            self.rows = file.readlines()


    def add_to_file(self, rows) -> None:
        """
        Запись данных (строки) в файл
        
        Args:
        rows (list): Список строк.

        Returns:
            None
        """
        with open(self.file_path, "a", encoding="utf-8") as file:
            for row in rows:
                file.write(row + '\n')


    def update_file(self, rows):  
        """
        Обновление данных в файле
        
        Args:
        rows (list): Список строк.

        Returns:
            None
        """  
        with open(self.file_path, "w", encoding="utf-8") as file:
            for row in rows:
                file.write(row + '\n')