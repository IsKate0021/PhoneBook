import re

class RecordsHandler:
    """Класс для управления данными в удобном для обработки формате"""
    def __init__(self, rows) -> None:
        """
        Создание списка словарей по данным из файла
        
        Args:
            rows (list): Список строк

        Returns:
            None
        """
        self.records_list =[]
        keys = ['last_name', 'name', 'patronymic', 'organization', 'work_phone', 'personal_phone']
        for index, line in enumerate(rows):
            if line.strip():  
                values = line.strip().split(';') 
                if len(values) == len(keys): 
                    record = self.create_record(index, values[0], values[1], values[2], values[3], values[4], values[5])
                    self.records_list.append(record)


        
    def create_record(self, index, last_name, name, patronymic, organization, work_phone, personal_phone) -> dict:
        """
        Создание словаря
        
        Args:
            index (int): Уникальный индекс записи.
            last_name (str): Фамилия контакта.
            name (str): Имя контакта.
            patronymic (str): Отчество контакта.
            organization (str): Наименование организации контакта.
            work_phone (str): Рабочий номер телефона контакта (будет очищен от нецифровых символов).
            personal_phone (str): Личный (сотовый) номер телефона контакта (будет очищен от нецифровых символов).

        Returns:
            dict: Словарь, содержащий информацию о контакте с ключами 'index', 'last_name', 'name',
                'patronymic', 'organization', 'work_phone', 'personal_phone'.
        """
        cleaned_work_phone = re.sub(r'\D', '', work_phone)
        cleaned_personal_phone = re.sub(r'\D', '', personal_phone)

        record = {
            'index': str(index),
            'last_name': last_name,
            'name': name,
            'patronymic': patronymic,
            'organization': organization,
            'work_phone': cleaned_work_phone,
            'personal_phone': cleaned_personal_phone
        }

        return record
    
    def add_to_records(self, index, last_name, name, patronymic, organization, work_phone, personal_phone):
        """
        Добавление словаря в список
        
        Args:
            index (int): Уникальный индекс записи.
            last_name (str): Фамилия контакта.
            name (str): Имя контакта.
            patronymic (str): Отчество контакта.
            organization (str): Наименование организации контакта.
            work_phone (str): Рабочий номер телефона контакта (будет очищен от нецифровых символов).
            personal_phone (str): Личный (сотовый) номер телефона контакта (будет очищен от нецифровых символов).

        Returns:
            dict: Словарь, содержащий информацию о контакте с ключами 'index', 'last_name', 'name',
                'patronymic', 'organization', 'work_phone', 'personal_phone'.
        """
        record = self.create_record(index, last_name, name, patronymic, organization, work_phone, personal_phone)
        self.records_list.append(record)
        return record

    
    def update_record(self, index, last_name, name, patronymic, organization, work_phone, personal_phone) -> None: 
        """
        Обновление словаря с определенным индексом.
        
        Args:
            index (int): Уникальный индекс записи.
            last_name (str): Фамилия контакта.
            name (str): Имя контакта.
            patronymic (str): Отчество контакта.
            organization (str): Наименование организации контакта.
            work_phone (str): Рабочий номер телефона контакта (будет очищен от нецифровых символов).
            personal_phone (str): Личный (сотовый) номер телефона контакта (будет очищен от нецифровых символов).

        Returns:
            None
        """   
        record = self.create_record(index, last_name, name, patronymic, organization, work_phone, personal_phone)
        self.records_list[int(index)] = record


    def record_to_row(self, records_list) -> list:
        """
        Конвертирование списка словарей в список строк.
        
        Args:
            records_list (list): Список словарей

        Returns:
            list: Список строк
        """ 
        rows = []
        for record in records_list:
            row = ';'.join([record['last_name'], record['name'], record['patronymic'],
                                    record['organization'], record['work_phone'], record['personal_phone']])
            rows.append(row)
        return rows



