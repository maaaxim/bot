from functions import *
from bot import Bot


class Destroyer (Bot):

    def loop(self, stop_event):
        """
        main bot logic
        """

        while not stop_event.is_set():

            time.sleep(0.2)

            # Continue attacking if victim is alive
            targeted_hp = self.get_targeted_hp()
            if targeted_hp > 0:
                self.useless_steps = 0

                print("attack the target")
                self.autohot_py.N1.press()
                continue
            elif targeted_hp == 0:

                print("target is dead")
                continue
            else:
                print("no target yet")
                # Find and click on the victim
                if self.set_target():
                    self.useless_steps = 0
                    print("set_target - attack")
                    self.autohot_py.N1.press()
                    continue

            # Find and click on the victim
            if self.set_target():
                self.useless_steps = 0
                print("set_target - attack")
                self.autohot_py.N1.press()
                continue

            if self.useless_steps > 5:
                # We're stuck, go somewhere
                self.useless_steps = 0
                print("go_somewhere - we're stuck")
                self.go_somewhere()
            else:
                # Turn on 90 degrees
                self.turn()
                print("turn")

            print("next iteration")
            pass

        print("loop finished!")