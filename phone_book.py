from file_handler import FileHandler
from typing import List, Dict 
from records_handler import RecordsHandler
import re
import tabulate



class PhoneBook:
    """Основной класс для управления телефонной книгой"""
    def __init__(self, file_path: str = 'data.txt') -> None: 
        """
        Создание экземпляра класса FileHandler,
        создание экземпляра класса RecordsHandler.
        Приветсвие пользователя.
        
        Args:
        file_path (str): Путь к файлу для хранения данных Телефонной книги

        Returns:
            None
        """
        self.file_handler = FileHandler(file_path)  
        self.records_handler = RecordsHandler(self.file_handler.rows)

        print("Добро пожаловать в Телефонный справочник!")


    def run(self) -> None:
        """
        Запуск основного цикла пользовательского интерфейса программы.

        Метод отображает меню с возможными действиями для пользователя и
        обрабатывает выбранные действия до тех пор, пока пользователь не выберет
        опцию для выхода из программы.

        Returns:
            None
        """
        while True:           
            action = int(input("\nВыберите номер действия: \n"
                           "1 - Вывод постранично записей из справочника на экран \n"
                           "2 - Добавление новой записи в справочник \n"
                           "3 - Возможность редактирования записей в справочнике \n"
                           "4 - Поиск записей по одной или нескольким характеристикам \n"
                           "5 - Выход \n"))
            match action:
                case 1:
                    self.print_pages()

                case 2:
                    self.add_row()

                case 3:
                    self.edit_record()

                case 4:
                    self.search_record()
                case 5:
                    break


    def pretty_print(self, rows: List[Dict[str, str]]) -> None:
        """
        Данный метод предназначен для удобного отображения данных.
        Args:
            rows (List[Dict[str, str]): Список словарей.

        Returns:
            None
        """
        if rows:
            header = ['Номер', 'Фамилия', 'Имя', 'Отчетсво', 'Организация', 'Рабочий номер телефона', 'Личный номер телефона']
            rows =  [x.values() for x in rows]
            print(tabulate.tabulate(rows, header, tablefmt='grid'))


    def print_pages(self) -> None:   
        """
        Выводит записи из справочника постранично на экран.

        Пользователю предлагается ввести номер страницы для просмотра. Каждая страница
        содержит фиксированное количество записей. Если выбранная страница превышает
        общее количество доступных страниц с записями, выводится сообщение о том,
        что страница пуста. 

        Returns:
            None
        """                
        lines_in_page = 10          # сколько строк в одной странице
        page_number = int(input("Введите номер страницы для просмотра: "))
         
        page_begin = (page_number - 1) * lines_in_page
        page_end = page_number * lines_in_page
        print(f"====={page_number} стр=====")
        if len(self.records_handler.records_list) > page_begin:

            self.pretty_print(self.records_handler.records_list[page_begin:page_end])
        else:
            print("Пустая страница \n")


    def add_row(self) -> None:
        """
        Добавляет новую запись в справочник на основе данных, введенных пользователем.

        Returns:
            None
        """
        last_name = input('Введите фамилию: ')
        name = input('Введите имя: ')
        patronymic = input('Введите отчество: ')
        organization = input('Введите организацию: ')
        work_phone = input('Введите рабочий номер телефона: ')
        personal_phone = input('Введите личный номер телефона: ')

        record = self.records_handler.add_to_records(
            len(self.records_handler.records_list), 
            last_name.strip().title(), 
            name.strip().title(), 
            patronymic.strip().title(), 
            organization.strip().title(), 
            work_phone.strip().title(), 
            personal_phone.strip().title()
        )
        rows = self.records_handler.record_to_row([record])
        self.file_handler.add_to_file(rows)


    def search_record(self) -> None:
        """
        Поиск записей в справочнике по заданным критериям (ФИО, наименование организации,
        рабочий или личный телефон).

        Если по указанному критерию записи не найдены, выводится соответствующее сообщение.

        Returns:
            None
        """
        value_for_search = int(input("Введите номер значения, по которому Вы хотите найти запись: \n" 
                                    "1 - фамилия, имя, отчество \n"
                                    "2 - наименование организации \n"
                                    "3 - телефон рабочий \n"
                                    "4 - телефон личный (сотовый) \n"))

        match value_for_search:
            case 1:
                last_name_for_search = input("Введите фамилию: ")
                name_for_search = input("Введите имя: ")
                patronymic_for_search = input("Введите отчество: ")
                list_for_output = []

                for record in self.records_handler.records_list:
                    if last_name_for_search.strip().title() == record['last_name'] \
                       and name_for_search.strip().title() == record['name'] \
                       and patronymic_for_search.strip().title() == record['patronymic']:
                        
                        list_for_output.append(record)
                        self.pretty_print(list_for_output)
                        break
                else:
                    print("Нет записей с такими ФИО")
            case 2:
                organization_for_search = input("Введите наименование организации: ")
                list_for_output = []

                for record in self.records_handler.records_list:
                    if organization_for_search.strip().title() == record['organization']:
                        list_for_output.append(record)
                        self.pretty_print(list_for_output)
                        break
                else:
                    print("Нет записей с такой организацией")
            case 3:
                work_phone_for_search = input("Введите телефон рабочий: ")
                list_for_output = []
                cleaned_work_phone_for_search = re.sub(r'\D', '', work_phone_for_search)

                for record in self.records_handler.records_list:
                    if cleaned_work_phone_for_search.strip() == record['work_phone']:
                        list_for_output.append(record)
                        self.pretty_print(list_for_output)
                        break
                else:
                    print("Нет записей с таким рабочим номером телефона")
            case 4:
                personal_phone_for_search = input("Введите телефон личный (сотовый): ")
                list_for_output = []
                cleaned_personal_phone_for_search = re.sub(r'\D', '', personal_phone_for_search)

                for record in self.records_handler.records_list:
                    if cleaned_personal_phone_for_search.strip() == record['personal_phone']:
                        list_for_output.append(record)
                        self.pretty_print(list_for_output)
                        break
                else:
                    print("Нет записей с таким личным номером телефона")


    def edit_record(self) -> None:
        """
        Предоставляет пользователю возможность изменения существующей записи в справочнике.

        Пользователю предлагается ввести фамилию для изменения записи в справочнике,
        при этом если записей несколько, пользователю предлагается выбрать номер нужной записи.

        Returns:
            None
        """
        while True:
            last_name_for_edit = input('Введите фамилию записи, которую хотите изменить: '
                                       '(Для выхода нажмите Enter) ')
            if not last_name_for_edit:
                break

            filtered_records = []

            for record in self.records_handler.records_list:      
                if last_name_for_edit.strip().title() == record['last_name']:
                    
                    filtered_records.append(record)

            self.pretty_print(filtered_records)
            index_list = [record['index'] for record in filtered_records]

            if index_list:  
                while True:
                    num_of_record = input('Введите номер из представленной таблицы для изменения,' 
                                          'нужной вам записи (Для выхода нажмите Enter) ')
                    if not num_of_record:
                        break
                    if num_of_record in index_list:
                        last_name = input('Введите фамилию: ')
                        name = input('Введите имя: ')
                        patronymic = input('Введите отчество: ')
                        organization = input('Введите организацию: ')
                        work_phone = input('Введите рабочий номер телефона: ')
                        personal_phone = input('Введите личный номер телефона: ')

                        self.records_handler.update_record(
                            num_of_record.strip().title(), 
                            last_name.strip().title(), 
                            name.strip().title(), 
                            patronymic.strip().title(), 
                            organization.strip().title(), 
                            work_phone.strip().title(), 
                            personal_phone.strip().title()
                        )
                        rows = self.records_handler.record_to_row(self.records_handler.records_list)
                        self.file_handler.update_file(rows)
                        return                 
                    else:
                            print("Нет фамилии с таким номером. Попробуйте еще раз")
            else:
                print("Нет записей с такой фамилией. Попробуйте еще раз")   


if __name__ == '__main__':
    phone_book_file = 'data.txt'
    phone_book = PhoneBook(phone_book_file)
    phone_book.run()