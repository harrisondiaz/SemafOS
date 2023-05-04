import random
import time
import threading
from tkinter import *
from tkinter import ttk

CAPACITY = 5
buffer = [None] * CAPACITY
in_index = out_index = counter = 0
mutex = threading.Semaphore(1)
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)
buffer_used = 0

class Producer(threading.Thread):
    """A class representing a producer thread."""
    def __init__(self, name, output_label, gui_instance):
        super().__init__(name=name)
        self.output_label = output_label
        self.gui_instance = gui_instance

    def run(self):
        """The main function of the producer thread."""
        global CAPACITY, buffer, in_index, out_index, counter, buffer_used
        global mutex, empty, full

        items_produced = 0

        while items_produced < CAPACITY:
            empty.acquire()
            mutex.acquire()

            counter += 1
            buffer[in_index] = counter
            in_index = (in_index + 1) % CAPACITY
            buffer_used += 1
            self.output_label.config(text=f'Productor {self.name[-1]}: {counter}, {in_index}')
            self.gui_instance.update_buffer_used_label()

            mutex.release()
            full.release()

            time.sleep(random.randint(1, 3))

            items_produced += 1


class Consumer(threading.Thread):
    """A class representing a consumer thread."""
    def __init__(self, name, output_label, gui_instance):
        super().__init__(name=name)
        self.output_label = output_label
        self.gui_instance = gui_instance

    def run(self):
        """The main function of the consumer thread."""
        global CAPACITY, buffer, in_index, out_index, counter, buffer_used
        global mutex, empty, full

        items_consumed = 0

        while items_consumed < 20:
            full.acquire()
            mutex.acquire()

            item = buffer[out_index]
            buffer[out_index] = None
            out_index = (out_index + 1) % CAPACITY
            buffer_used -= 1
            self.output_label.config(text=f'Consumidor {self.name[-1]}: {item} , {out_index}')
            self.gui_instance.update_buffer_used_label()

            mutex.release()
            empty.release()

            time.sleep(random.randint(4, 6))

            items_consumed += 1


class ProducerConsumerGUI:
    """
        A GUI for visualizing the producer-consumer problem.

        """
    def __init__(self, buffer_size, num_producers, num_consumers):
        self.root = Tk()
        self.root.title("Productor-Consumidor")
        self.buffer_size = buffer_size
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.buffer_used = IntVar()
        self.producer_threads = []
        self.consumer_threads = []
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the GUI."""
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.producer_labels = []
        self.consumer_labels = []

        for i in range(self.num_producers):
            producer_label = ttk.Label(mainframe, text="")
            producer_label.grid(column=0, row=i + 1, sticky=(W, E))
            self.producer_labels.append(producer_label)

        for i in range(self.num_consumers):
            consumer_label = ttk.Label(mainframe, text="")
            consumer_label.grid(column=1, row=i + 1, sticky=(W, E))
            self.consumer_labels.append(consumer_label)

        ttk.Label(mainframe, text="Productores").grid(column=0, row=0, sticky=W)
        ttk.Label(mainframe, text="Consumidores").grid(column=1, row=0, sticky=W)

        buffer_used_label = ttk.Label(mainframe, text="Búfer utilizado:")
        buffer_used_label.grid(column=0, row=self.num_producers + 1, sticky=W)

        buffer_used_var = f"{buffer_used}/{self.buffer_size}"
        self.buffer_used_value_label = ttk.Label(mainframe, text=buffer_used_var)
        self.buffer_used_value_label.grid(column=1, row=self.num_producers + 1, sticky=(W, E))

        stop_button = ttk.Button(mainframe, text="Detener", command=self.stop_threads)
        stop_button.grid(column=1, row=self.num_producers + 2, sticky=E)

        self.start_threads()

    def start_threads(self):
        """Starts the producer and consumer threads."""
        for i in range(self.num_producers):
            producer_thread = Producer(f"Productor {i + 1}", self.producer_labels[i], self)
            producer_thread.start()
            self.producer_threads.append(producer_thread)

        for i in range(self.num_consumers):
            consumer_thread = Consumer(f"Consumidor {i + 1}", self.consumer_labels[i], self)
            consumer_thread.start()
            self.consumer_threads.append(consumer_thread)

    def stop_threads(self):
        """Stops the producer and consumer threads."""
        for producer_thread in self.producer_threads:
            producer_thread.join()

        for consumer_thread in self.consumer_threads:
            consumer_thread.join()

        self.root.destroy()

    def run(self):
        """Runs the GUI."""
        self.root.mainloop()

    def update_buffer_used_label(self):
        """Updates the buffer used label."""
        buffer_used_var = f"{buffer_used}/{self.buffer_size}"
        self.buffer_used_value_label.config(text=buffer_used_var)


class ConfigWindow:
    """ A window for configuring the producer-consumer problem."""
    def __init__(self):
        self.root = Tk()
        self.root.title("Configuración Productor-Consumidor")
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the configuration window."""
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Tamaño del búfer:").grid(column=0, row=0, sticky=W)
        self.buffer_size_var = StringVar()
        buffer_size_entry = ttk.Entry(mainframe, textvariable=self.buffer_size_var)
        buffer_size_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Número de productores:").grid(column=0, row=1, sticky=W)
        self.num_producers_var = StringVar()
        num_producers_entry = ttk.Entry(mainframe, textvariable=self.num_producers_var)
        num_producers_entry.grid(column=1, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Número de consumidores:").grid(column=0, row=2, sticky=W)
        self.num_consumers_var = StringVar()
        num_consumers_entry = ttk.Entry(mainframe, textvariable=self.num_consumers_var)
        num_consumers_entry.grid(column=1, row=2, sticky=(W, E))

        start_button = ttk.Button(mainframe, text="Iniciar", command=self.start_app)
        start_button.grid(column=1, row=3, sticky=W)

    def start_app(self):
        """Starts the producer-consumer GUI."""
        buffer_size = int(self.buffer_size_var.get())
        num_producers = int(self.num_producers_var.get())
        num_consumers = int(self.num_consumers_var.get())

        self.root.destroy()
        app = ProducerConsumerGUI(buffer_size, num_producers, num_consumers)
        app.run()

    def run(self):
        """Runs the configuration window."""
        self.root.mainloop()

def main():
    """Main function."""
    config_window = ConfigWindow()
    config_window.run()

if __name__ == "__main__":
    main()
