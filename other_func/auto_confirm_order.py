import requests
import threading
import time


class AutoConfirm:

    def __init__(self, gui):
        self.gui = gui
        self.t1 = threading.Thread(target=self.auto_confirm_order_cond)

        self.thread()

    def thread(self):
        self.t1.start()

    def stop_thread_auto_confirm(self):
        self.t1.join()

    def auto_confirm_order_cond(self):
        while self.gui.comboBox_auto_confirm_order.currentText() == 'Да':
            begin_time = str(int(time.time() * 1000) - 1200100100)
            end_time = str(int(time.time() * 1000))
            url = "https://kaspi.kz/shop/api/v2/orders?page[number]=0&page[size]=100&filter[orders][state]=NEW&" \
                  "filter[orders][creationDate][$ge]=" + begin_time + "&filter[orders][creationDate][$le]=" + end_time + "&filter[orders][status]=APPROVED_BY_BANK&" \
                                                                                                                         "filter[orders][deliveryType]=PICKUP&filter[orders][signatureRequired]=false&" \
                                                                                                                         "include[orders]=user"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                'Content-Type': 'application/vnd.api+json',
                'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}

            r = requests.get(url=url, headers=headers)

            data = r.json()
            id_order = [i['id'] for i in data['data']]
            attributes = [i['attributes'] for i in data['data']]
            print('id_order', id_order)

            count_order = 0
            for i in attributes:
                delay_t = int(end_time) - i['creationDate']

                if delay_t > 4800000:  # больше 80 мин.
                    print(id_order[count_order])
                    print('Confirmed')
                    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                    #             'HTTP': '/1.1',
                    #             'POST': '/api/v2/orders',
                    #             # 'Host': 'kaspi.kz/shop',
                    #             'Content-Type': 'application/vnd.api+json',
                    #             'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}
                    # data = {"data": {"type": "orders", "id": id_order[count_order]+"=", "attributes": {"code": "", "status": "ACCEPTED_BY_MERCHANT"}}}
                    # r = requests.post(url='https://kaspi.kz/shop/api/v2/orders', headers=headers, json=data)
                    # data = r.json()
                else:
                    print(id_order[count_order])
                    print(delay_t)
                    print('Wait')
                count_order += 1

            for _ in range(3):
                time.sleep(1)



