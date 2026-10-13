from pyuvm import uvm_env
from sim.Test.Env.Agent.agent import UART_TX_agent
from sim.Test.Env.Scoreboard.scoreboard import UART_TX_scoreboard
from sim.Test.Env.Coverage.coverage import UART_TX_coverage


class UART_TX_env(uvm_env):
    def build_phase(self):
        self.agt = UART_TX_agent("agt", self)
        self.scb = UART_TX_scoreboard("scb", self)
        self.cov = UART_TX_coverage("cov", self)

    def connect_phase(self):
        self.agt.agt_ap_scoreboard.connect(self.scb.sc_export)
        self.agt.agt_ap_coverage.connect(self.cov.cov_export)
