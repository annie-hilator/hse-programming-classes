import csv
import random

def read_and_write(input_file, output_file):
    categories = ["Продукты", "Электроника", "Бытовая техника", "Одежда", "Книги"]

    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8', newline='') as f_out:

        csv_reader = csv.reader(f_in, delimiter='\t')
        csv_writer = csv.writer(f_out)

        csv_writer.writerow(['user_id', 'source', 'category'])
        next(csv_reader)

        for row in csv_reader:
            user_id, source = row[0].split(",")
            if user_id == "0":
                continue
            category = random.choice(categories)
            csv_writer.writerow([user_id, source, category])

read_and_write('visit_log.csv', 'funnel.csv')

with open('funnel.csv', 'r', encoding='utf-8') as result:
    for _ in range(5):
        print(result.readline().strip())
