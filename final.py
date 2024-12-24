from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from requests import get, post

def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    #print("Я работаю")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

def write_to_file(tasks):
    with open('tasks.txt', 'w') as file:
        tasks_json = [task.to_json() for task in tasks]
        file.write("\n".join(tasks_json))

def read_from_file():
    tasks = []
    try:
        with open('tasks.txt', 'r') as file:
            for line in file:
                task_data = json.loads(line.strip())
                task = Task(task_data['title'], task_data['priority'], task_data['id'], task_data['isDone'])
                tasks.append(task)
    except FileNotFoundError:
        pass
    return tasks

class Task:
    def __init__(self, title, priority, id, isDone=False):
        self.title = title
        self.priority = priority
        self.isDone = isDone
        self.id = id

    def to_json(self):
        return json.dumps(self.__dict__)


class TaskServer(BaseHTTPRequestHandler):
    tasks = read_from_file() # список задач из файла
    next_id = next_id = 1 if not tasks else max(task.id for task in tasks) + 1 # номер который будет присваиваться задаче

    def do_GET(self): # получаем список задач
        if self.path == '/tasks':
            self.send_response(200) # успещно
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            tasks_json = [task.to_json() for task in TaskServer.tasks]
            self.wfile.write("[{}]".format(', '.join(tasks_json)).encode())
            # отправляем задачи в json

    def do_POST(self): # создаем новую задачу
        if self.path == '/tasks':
            content_len = int(self.headers['Content-Length']) # длина тела запроса
            post_data = self.rfile.read(content_len) # считываем столько же байтов

            try:
                data = json.loads(post_data) # json ответ преобразовывается в словарь
                title = data.get('title') # поле title
                priority = data.get('priority') # поле priority

                if not title or not priority: # проверка наличия обязательных полей
                    raise ValueError("нет поля 'title' и/или 'priority'")

                task = Task(title, priority, TaskServer.next_id) # создается экземпляр задачи
                TaskServer.tasks.append(task) # добавляется в список
                TaskServer.next_id += 1 # уникальный номер для следующей задачи +1

                write_to_file(TaskServer.tasks)

                self.send_response(201) # создано
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(task.to_json().encode())

            except (json.JSONDecodeError, ValueError):
                self.send_response(400) # некорректный запрос

        # отмечаем задачу как выполненную
        elif self.path.startswith('/tasks/') and self.path.endswith('/complete'):
            path_parts = self.path.split('/') # разбиваем путь
            #print(path_parts)

            try:
                task_id = int(path_parts[2]) # определяем номер задачи
            except ValueError:
                self.send_response(400)
                return

            # ищем задачу с таким номером
            task = next((t for t in TaskServer.tasks if t.id == task_id), None)

            # задачи с таким номером нет
            if task is None:
                self.send_response(404) # не найдено
            else: # задача найдена, отмечаем выполнение
                task.isDone = True
                write_to_file(TaskServer.tasks)
                self.send_response(200) # успешно
            self.end_headers()

run(handler_class=TaskServer)