from pyuvm import uvm_agent, uvm_sequencer, uvm_analysis_port, ConfigDB
from sim.Test.Env.Agent.Driver.driver import UART_TX_driver
from sim.Test.Env.Agent.Monitor.monitor import UART_TX_monitor


class UART_TX_agent(uvm_agent):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.drv = UART_TX_driver.create("drv", self)
        self.mtr = UART_TX_monitor.create("mtr", self)
        self.agt_ap_scoreboard = uvm_analysis_port("agt_ap_scoreboard", self)
        self.agt_ap_coverage = uvm_analysis_port("agt_ap_coverage", self)

    def connect_phase(self):
        self.drv.seq_item_port.connect(self.seqr.seq_item_export)
        self.mtr.mtr_ap_scoreboard.connect(self.agt_ap_scoreboard)
        self.mtr.mtr_ap_coverage.connect(self.agt_ap_coverage)
