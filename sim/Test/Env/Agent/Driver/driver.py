import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from pyuvm import uvm_driver
from sim.UART_TX_utils import UartTxBfm


class UART_TX_driver(uvm_driver):
    def start_of_simulation_phase(self):
        self.bfm = UartTxBfm()

    async def launch_tb(self):
        await self.bfm.reset()
        self.bfm.start_bfm()

    async def run_phase(self):
        await self.launch_tb()
        while True:
            seq_item = await self.seq_item_port.get_next_item()

            #print(f"[DRIVER] Sending sequence item: {seq_item}")

            # Wait until UART is idle (Busy == 0)
            while cocotb.top.Busy.value == 1:
                await RisingEdge(cocotb.top.clk)

            await self.bfm.send_config(seq_item.reset, seq_item.P_DATA, seq_item.PAR_EN, seq_item.PAR_TYP, seq_item.DATA_VALID)

            if seq_item.reset == 0 or seq_item.DATA_VALID == 0:
                await ClockCycles(cocotb.top.clk, 2, rising=True)
            else:
                if seq_item.PAR_EN == 1:
                    await RisingEdge(cocotb.top.clk)
                    # Set DATA_VALID to 0
                    await self.bfm.send_config(seq_item.reset, seq_item.P_DATA, seq_item.PAR_EN, seq_item.PAR_TYP, 0)
                    await ClockCycles(cocotb.top.clk, 11, rising=True)
                else:
                    await RisingEdge(cocotb.top.clk)
                    # Set DATA_VALID to 0
                    await self.bfm.send_config(seq_item.reset, seq_item.P_DATA, seq_item.PAR_EN, seq_item.PAR_TYP, 0)
                    await ClockCycles(cocotb.top.clk, 10, rising=True)

            self.seq_item_port.item_done()
