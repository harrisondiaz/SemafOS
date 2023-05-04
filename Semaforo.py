class Producer(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        global CAPACITY, buffer, in_index, out_index, counter
        global mutex, empty, full	

        items_produced = 0

        while items_produced < CAPACITY:
            empty.acquire()
            mutex.acquire()

            print("semphores acquire")
            print("Semaforo produtor vazio: ", empty._value)
            print("Semaforo produtor mutex: ", mutex._value)
            counter += 1
            buffer[in_index] = counter
            in_index = (in_index + 1) % CAPACITY
            print("Buffer productor")
            print(f'Producer {self.name} produced item {counter}')
            print(buffer)

            mutex.release()
            full.release()

            print("semphores release")
            print("Semaforo produtor full: ", full._value)
            print("Semaforo produtor mutex: ", mutex._value)

            time.sleep(random.randint(1,3))

            items_produced += 1

    

        self.start()

class Consumer(threading.Thread):

    def __init__(self, name):
        super().__init__(name=name)

    def run(self):

        global CAPACITY, buffer, in_index, out_index, counter
        global mutex, empty, full

        items_consumed = 0

        while items_consumed < 20:
            full.acquire()
            mutex.acquire()

            print("Semapforo release productor")
            print ("Semaforo productor full", full._value)
            print ("Semaforo productor mutex", mutex._value)

            item = buffer[out_index]
            buffer[out_index] = None
            out_index = (out_index + 1) % CAPACITY
            print("Buffer consumidor")
            print(f'Consumer {self.name} consumed item {item} at index {out_index}')
            print(buffer)

            mutex.release()
            empty.release()

            print("Semapforo release consumidor")
            print ("Semaforo consumidor empty", empty._value)
            print ("Semaforo consumidor mutex", mutex._value)

            time.sleep(random.random(4,6))

            items_consumed += 1