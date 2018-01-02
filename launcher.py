import threading
from AutoHotPy import AutoHotPy
from destrotyer import Destroyer


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        kind of constructor = get instance
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Launcher:

    __metaclass__ = Singleton

    def __init__(self):
        """
        constructor
        """

        # create AutoHotPy instance and set stop event handler
        auto_py = AutoHotPy()
        auto_py.registerExit(auto_py.ESC, self.stop_bot_event_handler)

        # init bot stop event
        self.bot_thread_stop_event = threading.Event()

        # init threads
        self.auto_py_thread = threading.Thread(target=self.start_auto_py, args=(auto_py,))
        self.bot_thread = threading.Thread(target=self.start_destroyer, args=(auto_py, self.bot_thread_stop_event))

        # start threads
        self.auto_py_thread.start()
        self.bot_thread.start()

    def stop_bot(self):
        """
        send stop signal to bot thread
        """
        self.bot_thread_stop_event.set()

    @staticmethod
    def start_destroyer(auto, stop_event):
        """
        start bot loop
        """
        destroyer = Destroyer(auto)
        destroyer.loop(stop_event)

    @staticmethod
    def start_auto_py(auto):
        """
        start AutoHotPy
        """
        auto.start()

    @staticmethod
    def stop_bot_event_handler(auto, event):
        """
        exit the program when you press ESC
        """
        auto.stop()
        launcher = Launcher()
        launcher.stop_bot()
