class Person:
    def __init__(self, name, device_type, browser, sex, age, bill, region):
        self.name = name
        self.device_type = device_type
        self.browser = browser
        self.sex = sex
        self.age = age
        self.bill = bill
        self.region = region

    def write_to_file(self, file): # запись атрибутов в файл в необходимом формате
        gender = "женского" if self.sex == "female" else "мужского"
        device = "мобильного" if self.device_type == "mobile" else "настольного"
        output = f"Пользователь {self.name} {gender} пола, {self.age} лет "\
                 f"совершил(а) покупку на {self.bill} у.е. с {device} "\
                 f"браузера {self.browser}. Регион, из которого совершалась покупка: {self.region}.\n"
        file.write(output)


with open("web_clients_correct.csv", 'r') as f_in, open("output.txt", 'w') as f_out:
    f_in.readline() # пропуск первой строки с названиями столбцов
    data = f_in.readlines() # список всех строк входного файла, можно было и в цикле по одной строке считывать и с каждой работать, но мне так больше нравится
    for el in data: # перебираем каждый элемент списка - строку
        line = el.strip().split(',') # убираем символ переноса строки и создаем список, разделяя строку по запятым
        current_person = Person(*line) # создаем экземпляр класса и распаковываем список, чтобы заполнить поля
        current_person.write_to_file(f_out) # вызываем метод класса для записи в файл