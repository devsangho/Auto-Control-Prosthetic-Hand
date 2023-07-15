import threading


class Worker(threading.Thread):
    def __init__(self, args=None, name="", model=None):
        threading.Thread.__init__(self)
        self.name = name
        self.args = args
        self.model = model

    def run(self):
        print("Starting " + self.name)
        self.model.run()
