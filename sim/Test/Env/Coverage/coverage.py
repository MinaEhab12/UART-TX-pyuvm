import cocotb
from cocotb_coverage.coverage import *
from pyuvm import uvm_subscriber, uvm_tlm_analysis_fifo, uvm_get_port, uvm_component


# Define coverage section to combine all coverage items
# datum is expected to be a tuple with the following order:
# (Reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy, TX_OUT)
UART_TX_Coverage_Section = coverage_section(
    CoverPoint("cvr_gp.Reset_Coverage", xf=lambda datum: datum[0], bins=[0, 1], bins_labels=["reset", "no_reset"]),

    CoverPoint("cvr_gp.P_DATA_Coverage", xf=lambda datum: datum[1], bins=[0x00, 0xFF, 0xAA, *list(range(32, 256, 32))],
                bins_labels=["min_value", "max_value", "alt_pattern", *[f"value_{i}" for i in range(32, 256, 32)]]),

    CoverPoint("cvr_gp.PAR_EN_Coverage", xf=lambda datum: datum[2], bins=[0, 1], bins_labels=["parity_disabled", "parity_enabled"]),

    CoverPoint("cvr_gp.PAR_TYP_Coverage", xf=lambda datum: datum[3], bins=[0, 1], bins_labels=["even_parity", "odd_parity"]),

    CoverPoint("cvr_gp.DATA_VALID_Coverage", xf=lambda datum: datum[4], bins=[0, 1], bins_labels=["data_invalid", "data_valid"]),

    CoverPoint("cvr_gp.Busy_Coverage", xf=lambda datum: datum[5], bins=[0, 1], bins_labels=["busy_0", "busy_1"]),

    CoverPoint("cvr_gp.TX_OUT_Coverage", xf=lambda datum: datum[6], bins=[0, 1], bins_labels=["tx_out_0", "tx_out_1"]),

    CoverCross("cvr_gp.PAR_EN__PAR_TYP_CROSS", items=["cvr_gp.PAR_EN_Coverage", "cvr_gp.PAR_TYP_Coverage"]),

    CoverCross("cvr_gp.P_DATA__DATA_VALID_CROSS", items=["cvr_gp.P_DATA_Coverage", "cvr_gp.DATA_VALID_Coverage"]),

    CoverCross("cvr_gp.TX_OUT__Busy_CROSS", items=["cvr_gp.TX_OUT_Coverage", "cvr_gp.Busy_Coverage"], ign_bins=[("tx_out_0", "busy_0")]),

    # TX_OUT=0 and Busy=0 is illegal
    CoverCheck("cvr_gp.illegal_TX_OUT_Busy_Check",
               f_fail=lambda datum: datum[6] == 0 and datum[5] == 0)
)

@UART_TX_Coverage_Section
def sample_coverage(datum):
    pass


class UART_TX_coverage(uvm_component):
    def build_phase(self):
        self.cov_fifo = uvm_tlm_analysis_fifo("cov_fifo", self)
        self.cov_get_port = uvm_get_port("cov_get_port", self)
        self.cov_export = self.cov_fifo.analysis_export
        self.sample_coverage = sample_coverage

    def connect_phase(self):
        self.cov_get_port.connect(self.cov_fifo.get_export)

    def check_phase(self):
        try:
            while self.cov_get_port.can_get():
                _, cov_datum = self.cov_get_port.try_get()
                self.sample_coverage(cov_datum)
        except Exception as e:
            self.logger.error(f"Error during coverage collection: {e}")

        # Report coverage at the end
        coverage_db.report_coverage(cocotb.log.info, bins=True)
        coverage_db.export_to_xml(filename="func_coverage_report.xml")
        coverage_db.export_to_yaml(filename="func_coverage_report.yml")
