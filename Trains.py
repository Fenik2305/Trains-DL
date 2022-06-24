import csv

def toInt(string):   #приймає на вхід рядок та видяляє з нього нечислові символи
    res = ''
    for char in string:
        res += char * char.isdigit()
    return int(res)

def toTime(string):    #перевіряє рядок на часовий формат
    res = ''
    for char in string:
        if char.isdigit() or char == ':':
            res += char
    return res

def finPrice(route):   #функція підраховує скільки часу в хвилинах пройшло з моменту t1 до моменту t2
    return round(sum(map(lambda x: x[3], route)), 2)

def finTime(route):   #функція підраховує скільки часу в хвилинах пройшло з моменту t1 до моменту t2
    total = calcTime(route[0][4], route[0][5])
    for i in range(1, len(route)):
        total += calcTime(route[i - 1][5], route[i][5])
    return total

def calcTime(t1, t2):   #функція підраховує скільки часу в хвилинах пройшло з моменту t1 до моменту t2
    t1, t2 = list(map(int, t1.split(":"))), list(map(int, t2.split(":")))
    return (t2[0] * 60 + t2[1] - t1[0] * 60 - t1[1] + 1440) % 1440

def timetableInput(path):   #імпорт даних з таблиці
    with open(path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        datum = []
        for row in csvreader:
            row = ''.join(row).split(';')
            datum.append([toInt(row[0]), int(row[1]), int(row[2]), round(float(row[3]), 2), toTime(row[4]), toTime(row[5])])
    return datum

def calcForPrice(data):
    stations = list(set(map(lambda x: x[1], data))) #отримуємо список всіх станцій
    minCostStarts = [min(filter(lambda x: x[1] == station, data), key=lambda x: x[3]) for station in stations] #знаходимо найдешевший потяг з кожної станції
    routes = []
    for start in minCostStarts: #для кожного початкового маршруту методом найближчого сусіда шукаємо найдешевший гамільтонів шлях
        route = [start] #вписуємо до загального маршруту початковий потяг
        visited = [start[1], start[2]] #додаємо до списку вже відвіданих станцій перші дві з початкового маршруту
        frame = data.copy()
        frame.remove(start) #видаляємо початковий маршрут з множини всіх подільших можливих, щоб уникнути циклів
        currStation = start[2] #задаємо поточну станцію (куди приїхав перший потяг)
        while set(visited) != set(stations):
            roads = list(filter(lambda x: x[1] == currStation and x[2] not in visited, frame)) #переглядаємо з поточної станції куди ми можемо потрапити ще
            if roads: #якщо з поточної станції є якийсь маршрут до не відвіданої, то шукаємо найдешевший з них
                bestChoice = min(roads, key=lambda x: x[3])
                route.append(bestChoice)
                currStation = bestChoice[2]
                visited.append(currStation)
                frame.remove(bestChoice)
            else: #якщо маршрутів немає, або всі вони йдуть у вже відвідані станції, то починаємо прокладати новий з іншої початкової станції
                break
        routes.append(route)
    routes = list(filter(lambda x: len(x) == len(stations) - 1, routes)) #фільтруємо лише повні маршрути, такі, що виконують умову задачі
    minPrice = min(list(map(lambda x: finPrice(x), routes))) #знаходимо мінімальну ціну такого маршруту
    result = filter(lambda x: finPrice(x) == minPrice, routes) #шукаємо всі найдешевші маршрути
    counter = 1
    for el in result: #виводимо отримані результати
        print(f"Cheap Route №{counter}:")
        for i in range(len(el)):
            print(f"{i + 1}) {el[i]}")
        counter += 1
    print(f"Total price: {minPrice}.\n")

'''
Пошук найшвидшого маршруту відбувається за такою ж логікою, але для кожного наступного
потяга мінімізуємо "час очікування потяга" + "час який потяг буде їхати"
'''

def calcForTime(data):
    stations = list(set(map(lambda x: x[1], data)))
    minTimeStarts = [min(filter(lambda x: x[1] == station, data), key=lambda x: calcTime(x[4], x[5])) for station in stations]
    routes = []
    for start in minTimeStarts:
        visited = [start[1], start[2]]
        route = [start]
        frame = data.copy()
        currStation = start[2]
        frame.remove(start)
        while set(visited) != set(stations):
            roads = list(filter(lambda x: x[1] == currStation and x[2] not in visited, frame))
            if roads:
                bestChoice = min(roads, key=lambda x: calcTime(route[-1][5], x[4]) + calcTime(x[4], x[5]))
                route.append(bestChoice)
                currStation = bestChoice[2]
                visited.append(currStation)
                frame.remove(bestChoice)
            else:
                break
        routes.append(route)
    routes = list(filter(lambda x: len(x) == len(stations) - 1, routes))
    minTime = min(list(map(lambda x: finTime(x), routes)))
    result = filter(lambda x: finTime(x) == minTime, routes)
    counter = 1
    for el in result:
        print(f"Fast Route №{counter}:")
        for i in range(len(el)):
            print(f"{i + 1}) {el[i]}")
        counter += 1
    print(f"Total travel time: {minTime // 60} hours and {minTime % 60} minutes.\n")

if __name__ == "__main__":
    inputPath = "C:/Users/mykola/Desktop/test_task_data.csv" #Вказуємо шлях до файла з розкладом
    data = timetableInput(inputPath)
    calcForPrice(data)
    calcForTime(data)
