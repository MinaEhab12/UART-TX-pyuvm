from pyuvm import uvm_component, uvm_tlm_analysis_fifo, uvm_get_port
from sim.UART_TX_utils import GoldenModel


class UART_TX_scoreboard(uvm_component):
    def build_phase(self):
        self.sc_fifo = uvm_tlm_analysis_fifo("sc_fifo", self)
        self.sc_get_port = uvm_get_port("sc_get_port", self)
        self.sc_export = self.sc_fifo.analysis_export

    def connect_phase(self):
        self.sc_get_port.connect(self.sc_fifo.get_export)

    def check_phase(self):
        succeeded_tests = 0
        failed_tests = 0
        passed = True
        try:
            while self.sc_get_port.can_get():
                _, actual_result = self.sc_get_port.try_get()
                (reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy, tx_out_list) = actual_result
                
                # Get expected result from golden model
                expected = GoldenModel(reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy)
                
                # Compare actual vs expected
                match = True
                if expected != tx_out_list:
                    match = False
                
                if match:
                    succeeded_tests += 1
                else:
                    self.logger.error(f"FAILED: P_DATA=0b{int(P_DATA):08b}, Reset={reset}, DATA_VALID={DATA_VALID}, Expected={expected}, Actual={tx_out_list}")
                    failed_tests += 1
                    passed = False
        except Exception as e:
            self.logger.error(f"Error during checking: {e}")
            passed = False

        self.logger.info(f"========== Test Summary ==========")
        self.logger.info(f"Total Tests: {succeeded_tests + failed_tests}")
        self.logger.info(f"Passed: {succeeded_tests}")
        self.logger.info(f"Failed: {failed_tests}")
        self.logger.info(f"==================================")
        
        assert passed, "Some tests failed in scoreboard"
