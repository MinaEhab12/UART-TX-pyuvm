import random
import cocotb_coverage.crv as crv
from pyuvm import uvm_sequence_item

class RandExample(crv.Randomized):
    def __init__(self):
        crv.Randomized.__init__(self)                   # initialize super-class
        # define class members and their default values
        self.reset = 1
        self.P_DATA = 0
        self.PAR_EN = 0
        self.PAR_TYP = 0
        self.DATA_VALID = 0

        self.reset_active_c = lambda reset: reset == 0     # Unused constraint by default

        self.add_rand("reset", list(range(2)))             # 1-bit space
        self.add_rand("P_DATA", list(range(256)))          # 8-bit space
        self.add_rand("PAR_EN", list(range(2)))            # 1-bit space
        self.add_rand("PAR_TYP", list(range(2)))           # 1-bit space
        self.add_rand("DATA_VALID", list(range(2)))        # 1-bit space

        
        # constraint reset_c: reset dist {1:= 97, 0:= 3}
        def reset_dist(reset):
            return 97 if reset == 1 else 3
        self.add_constraint(reset_dist)

        # constraint PAR_EN_c: PAR_EN dist {1:= 25, 0:= 75}
        def PAR_EN_dist(PAR_EN):
            return 25 if PAR_EN == 1 else 75
        self.add_constraint(PAR_EN_dist)

        # constraint DATA_VALID_c: DATA_VALID dist {1:= 90, 0:= 10}
        def DATA_VALID_dist(DATA_VALID):
            return 90 if DATA_VALID == 1 else 10
        self.add_constraint(DATA_VALID_dist)

        # constraint P_DATA_2_c: {P_DATA inside {8'hFF, 8'h00, 8'hAA}} dist {1:= 15, 0:= 85}
        def P_DATA_special_dist(P_DATA):
            return 15 if P_DATA in [0xFF, 0x00, 0xAA] else 85
        self.add_constraint(P_DATA_special_dist)


class UART_TX_sequence_item(uvm_sequence_item):
    def __init__(self, name, reset=1, P_DATA=0, PAR_EN=0, PAR_TYP=0, DATA_VALID=0):
        super().__init__(name)
        self.reset = reset
        self.P_DATA = P_DATA
        self.PAR_EN = PAR_EN
        self.PAR_TYP = PAR_TYP
        self.DATA_VALID = DATA_VALID
        self.rand_ = RandExample()

    def set_operands(self, name):
        if name == "rand_seq":
            self.rand_.randomize()
        elif name == "reset_seq":
            self.rand_.randomize_with(self.rand_.reset_active_c)
        
        # Copy randomized values from RandExample to this sequence item
        self.reset = int(self.rand_.reset)
        self.P_DATA = int(self.rand_.P_DATA)
        self.PAR_EN = int(self.rand_.PAR_EN)
        self.PAR_TYP = int(self.rand_.PAR_TYP)
        self.DATA_VALID = int(self.rand_.DATA_VALID)

        # Alternatively, without using cocotb_coverage.crv:
        #self.reset = 1 if random.random() < 0.98 else 0
        #self.P_DATA = random.randint(0, 0xFF)
        #self.PAR_EN = 1 if random.random() < 0.75 else 0
        #self.PAR_TYP = random.randint(0, 1)
        #self.DATA_VALID = 1 if random.random() < 0.90 else 0

    def __str__(self):
        return f"Stimulus in Driver: reset = 0x{self.reset} | P_DATA = 0b{self.P_DATA:08b} | PAR_EN = 0x{self.PAR_EN} | PAR_TYP = 0x{self.PAR_TYP} | DATA_VALID = 0x{self.DATA_VALID}"
