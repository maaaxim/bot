from AutoHotPy import AutoHotPy
from destrotyer import Destroyer


def stop_bot(autohotpy, event):
    """
    exit the program when you press ESC
    """
    autohotpy.stop()


def start_bot(autohotpy, event):
    """
    This function simulates a left click
    """

    destr = Destroyer(autohotpy)
    destr.loop()
1

if __name__=="__main__":

    # destr = Destroyer(1)
    # destr.loop()

    print("Press \"S\" to start, press \"ESC\" to stop")

    auto = AutoHotPy()
    auto.registerExit(auto.ESC, stop_bot)
    auto.registerForKeyDown(auto.S, start_bot)
    auto.start()
