import cocotb
from pyuvm import uvm_component, uvm_analysis_port
from sim.UART_TX_utils import UartTxBfm


class UART_TX_monitor(uvm_component):
    def build_phase(self):
        self.mtr_ap_scoreboard = uvm_analysis_port("mtr_ap_scoreboard", self)
        self.mtr_ap_coverage = uvm_analysis_port("mtr_ap_coverage", self)
        self.bfm = UartTxBfm()

    async def run_phase(self):
        # Start coverage sampling task in parallel
        cocotb.start_soon(self.sample_coverage())

        # Main loop for scoreboard - sends data at end of UART transmission
        while True:
            datum = await self.bfm.get_result()
            self.mtr_ap_scoreboard.write(datum)

    async def sample_coverage(self):
        while True:
            cov_datum = await self.bfm.get_coverage_sample()
            self.mtr_ap_coverage.write(cov_datum)
