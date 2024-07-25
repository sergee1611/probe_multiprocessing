from multiprocessing import Manager, Pool


class WarehouseManager:
    def __init__(self):
        managers = Manager()
        self.data = managers.dict()

    def process_request(self, request):
        if request[1] == "receipt":
            if request[0] in self.data:
                self.data[request[0]] += request[2]
            else:
                self.data[request[0]] = request[2]
        elif request[1] == "shipment":
            if request[0] in self.data and self.data[request[0]] >= request[2]:
                self.data[request[0]] -= request[2]
        # for i in request:
        #     product, action, quantity = i
        #     if action == "receipt":
        #         if product in self.data:
        #             self.data[product] += quantity
        #         else:
        #             self.data[product] = quantity
        #     elif action == "shipment":
        #         if product in self.data and self.data[product] > quantity:
        #             self.data[product] -= quantity

    def run(self, requests):
        with Pool(processes=2) as pool:
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
