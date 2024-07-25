from multiprocessing import Lock, Pool
from time import sleep

lock = Lock()


class WarehouseManager:
    data = {}

    def process_request(self, request):
        if request[0] in self.data:
            if request[1] == "receipt":
                self.data[request[0]] += request[2]
            elif request[1] == "shipment" and self.data[request[0]] > 0:
                self.data[request[0]] -= request[2]
        elif request[0] not in self.data and request[1] == "receipt":
            self.data[request[0]] = request[2]
        return self.data

    def run(self, requests):
        with Pool(processes=4) as pool:
            pool.map(self.process_request, requests)



if __name__ == '__main__':
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)
