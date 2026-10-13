import enum
import logging

import cocotb
from cocotb.clock import Clock
from cocotb.queue import Queue, QueueEmpty
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles

from pyuvm import utility_classes

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def GoldenModel(reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy):
    if reset and DATA_VALID:
        if PAR_EN:
            parity_bit = int((bin(P_DATA).count('1') % 2) if PAR_TYP else not(bin(P_DATA).count('1') % 2))
            tx_out_combined_expected = [0] + [int(b) for b in format(int(P_DATA), '08b')] + [parity_bit, 1]
        else:
            tx_out_combined_expected = [0] + [int(b) for b in format(int(P_DATA), '08b')] + [1, None]
    elif reset == 0:
        tx_out_combined_expected = [1] * 5 + [0] * 6
    else:
        tx_out_combined_expected = [1] * 11

    return tx_out_combined_expected


class UartTxBfm(metaclass=utility_classes.Singleton):
    def __init__(self):
        self.dut = cocotb.top
        self.drv_queue = Queue(maxsize=1)
        self.mtr_queue = Queue(maxsize=0)
        self.cov_queue = Queue(maxsize=0)

    async def send_config(self, reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID):
        config_tuple = (reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID)
        await self.drv_queue.put(config_tuple)

    async def get_result(self):
        result = await self.mtr_queue.get()
        return result

    async def get_coverage_sample(self):
        result = await self.cov_queue.get()
        return result

    async def reset(self):
        await RisingEdge(self.dut.clk)
        self.dut.reset.value = 0
        self.dut.P_DATA.value = 0
        self.dut.PAR_EN.value = 0
        self.dut.PAR_TYP.value = 0
        self.dut.DATA_VALID.value = 0
        await RisingEdge(self.dut.clk)
        self.dut.reset.value = 1
        await RisingEdge(self.dut.clk)

    async def driver_bfm(self):
        self.dut.reset.value = 1
        self.dut.P_DATA.value = 0
        self.dut.PAR_EN.value = 0
        self.dut.PAR_TYP.value = 0
        self.dut.DATA_VALID.value = 0
        while True:
            await RisingEdge(self.dut.clk)
            try:
                (reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID) = self.drv_queue.get_nowait()
                self.dut.reset.value = reset
                self.dut.P_DATA.value = P_DATA
                self.dut.PAR_EN.value = PAR_EN
                self.dut.PAR_TYP.value = PAR_TYP
                self.dut.DATA_VALID.value = DATA_VALID
            except QueueEmpty:
                pass

    async def result_mtr_bfm(self):
        while True:
            await RisingEdge(self.dut.clk)
            if self.dut.reset.value == 1 and self.dut.DATA_VALID.value == 1:
                # Capture current configuration
                reset = self.dut.reset.value
                P_DATA = self.dut.P_DATA.value
                PAR_EN = self.dut.PAR_EN.value
                PAR_TYP = self.dut.PAR_TYP.value
                DATA_VALID = self.dut.DATA_VALID.value
                Busy = self.dut.Busy.value
                    
                tx_out_list = [None] * 11

                if PAR_EN:
                    # Wait for DUT to transition to START state, then capture start bit
                    await RisingEdge(self.dut.clk)
                    tx_out_list[0] = int(self.dut.TX_OUT.value)

                    # Data Bits
                    for i in range(8, 0, -1):
                        await RisingEdge(self.dut.clk)
                        tx_out_list[i] = int(self.dut.TX_OUT.value)

                    # Parity Bit
                    await RisingEdge(self.dut.clk)
                    tx_out_list[9] = int(self.dut.TX_OUT.value)

                    # Stop Bit
                    await RisingEdge(self.dut.clk)
                    tx_out_list[10] = int(self.dut.TX_OUT.value)
                else:
                    # Wait for DUT to transition to START state, then capture start bit
                    await RisingEdge(self.dut.clk)
                    tx_out_list[0] = int(self.dut.TX_OUT.value)

                    # Data Bits
                    for i in range(8, 0, -1):
                        await RisingEdge(self.dut.clk)
                        tx_out_list[i] = int(self.dut.TX_OUT.value)

                    # Stop Bit
                    await RisingEdge(self.dut.clk)
                    tx_out_list[9] = int(self.dut.TX_OUT.value)

            elif self.dut.reset.value == 0:
                await RisingEdge(self.dut.clk)

                # Capture current configuration
                reset = self.dut.reset.value
                P_DATA = self.dut.P_DATA.value
                PAR_EN = self.dut.PAR_EN.value
                PAR_TYP = self.dut.PAR_TYP.value
                DATA_VALID = self.dut.DATA_VALID.value
                Busy = self.dut.Busy.value
                TX_OUT = self.dut.TX_OUT.value

                tx_out_list = [int(TX_OUT)] * 5 + [int(Busy)] * 6

            else:
                # Capture current configuration
                reset = self.dut.reset.value
                P_DATA = self.dut.P_DATA.value
                PAR_EN = self.dut.PAR_EN.value
                PAR_TYP = self.dut.PAR_TYP.value
                DATA_VALID = self.dut.DATA_VALID.value
                Busy = self.dut.Busy.value
                TX_OUT = self.dut.TX_OUT.value

                tx_out_list = [int(TX_OUT)] * 11

            result = (reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy, tx_out_list)
            await self.mtr_queue.put(result)


    async def coverage_bfm(self):
        while True:
            await RisingEdge(self.dut.clk)
            # Capture current state every clock cycle for coverage
            reset = int(self.dut.reset.value)
            P_DATA = int(self.dut.P_DATA.value)
            PAR_EN = int(self.dut.PAR_EN.value)
            PAR_TYP = int(self.dut.PAR_TYP.value)
            DATA_VALID = int(self.dut.DATA_VALID.value)
            Busy = int(self.dut.Busy.value)
            TX_OUT = int(self.dut.TX_OUT.value)
            
            cov_sample = (reset, P_DATA, PAR_EN, PAR_TYP, DATA_VALID, Busy, TX_OUT)
            await self.cov_queue.put(cov_sample)

    def start_bfm(self):
        cocotb.start_soon(self.driver_bfm())
        cocotb.start_soon(self.result_mtr_bfm())
        cocotb.start_soon(self.coverage_bfm())