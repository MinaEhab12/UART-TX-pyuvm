import cocotb
from cocotb.clock import Clock
import pyuvm
from pyuvm import *

from sim.Test.Sequences.sequences import RandomSeq, ResetSeq, TestAllSeq, TestAllSeq_Parallel
from sim.Test.Env.environment import UART_TX_env


# Tests
# Test all sequences sequentially
@pyuvm.test()
class Base_test(uvm_test):
    def build_phase(self):
        self.env = UART_TX_env("env", self)

    def end_of_elaboration_phase(self):
        self.seqr = ConfigDB().get(None, "", "SEQR")

    async def run_phase(self):
        cocotb.start_soon(Clock(cocotb.top.clk, 2, "ns").start())
        test_all_seq = TestAllSeq.create("test_all_seq")
        self.raise_objection()
        self.logger.info(f"Starting {type(test_all_seq).__name__} sequence")
        await test_all_seq.start(self.seqr)
        self.logger.info(f"{type(test_all_seq).__name__} sequence completed")
        self.drop_objection()


# Test all sequences in parallel
@pyuvm.test()
class ParallelTest(Base_test):
    def build_phase(self):
        uvm_factory().set_type_override_by_type(TestAllSeq, TestAllSeq_Parallel)
        super().build_phase()


# Test with reset sequence only
@pyuvm.test()
class ResetTest(Base_test):
    def build_phase(self):
        uvm_factory().set_type_override_by_type(TestAllSeq, ResetSeq)
        super().build_phase()


# Test with random sequence only
@pyuvm.test()
class RandomTest(Base_test):
    def build_phase(self):
        uvm_factory().set_type_override_by_type(TestAllSeq, RandomSeq)
        super().build_phase()
