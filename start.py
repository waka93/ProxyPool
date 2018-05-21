from bin.api import app
from bin.schedule import Schedule
from multiprocessing import Process


class Start(object):
    @staticmethod
    def run_app():
        app.run()

    @staticmethod
    def run_schedule():
        s = Schedule()
        s.run()

    def run(self):
        process1 = Process(target=Start.run_app)
        process2 = Process(target=Start.run_schedule)
        process1.start()
        process2.start()


if __name__ == '__main__':
    s = Start()
    s.run()
