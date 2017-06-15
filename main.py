from pprint import pprint


def update(data, service, count):
    data = data.copy()
    host_load = [[k, sum(v.values())] for k, v in data.items()]
    while count:
        host_load.sort(key=lambda x: x[1])
        qty = min(host_load[1][1] - host_load[0][1] + 1, count)
        free_server = host_load[0][0]
        data[free_server][service] = data[free_server].get(service, 0) + qty
        host_load[0][1] += qty
        count -= qty

def update_with_predicted_config(data, service, count):
    # Изначально этот код был частью функции update, но так как я не
    # уверен что правильно понял дополнительное задание, и с
    # применением этого кода функция update перестает проходить
    # основной текст и вообще он мне ненравится, то я его лучше
    # вынесу в отдельную функцию.

    # Чтобы добиться "предсказуемой конфигурации" в не зависимости от
    # того в каком порядке добавляются сервисы мы при каждом добавлении
    # будем очищатся сервера и заново добавлять все сервисы
    # предварительно предсказуемо их отсортировав.
    services_to_add = {service: count}
    for server in data:
        for service, qnty in data[server].items():
            services_to_add[service] = services_to_add.get(service, 0) + qnty
        data[server] = {}

    # Отсортируем добавляемые сервисы в нашем случае по алфавиту но лкчше конечно
    #  по весу сервиса
    services_to_add = [(k, v) for k, v in services_to_add.items()]
    services_to_add.sort(key=lambda x: x[0])
    for service, count in services_to_add:
        update(data, service, count)


def main():
    example_data = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    print("Configuration before:")
    pprint(example_data)

    service = input('Service name [pylons]: ') or 'pylons'
    count = None
    while not count:
        try:
            count = int(input('Count [7]: ') or 7)
        except ValueError:
            print('Count should be a number.')
    # update(example_data, service, count)
    update_with_predicted_config(example_data, service, count)


    print("Configuration after:")
    pprint(example_data)

if __name__ == '__main__':
    main()
