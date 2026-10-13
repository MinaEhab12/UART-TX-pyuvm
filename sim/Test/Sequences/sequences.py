import cocotb
from cocotb.triggers import Combine
from pyuvm import uvm_sequence, ConfigDB
from sim.Test.Sequences.Seq_items.sequence_item import UART_TX_sequence_item


class RandomSeq(uvm_sequence):
    async def body(self):
        for i in range(5000):
            rand_seq = UART_TX_sequence_item("rand_seq")
            await self.start_item(rand_seq)
            rand_seq.set_operands("rand_seq")
            await self.finish_item(rand_seq)


class ResetSeq(uvm_sequence):
    async def body(self):
        for i in range(100):
            reset_seq = UART_TX_sequence_item("reset_seq")
            await self.start_item(reset_seq)
            reset_seq.set_operands("reset_seq")
            await self.finish_item(reset_seq)

# Virtual Sequence to run all sequences
class TestAllSeq(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq("random")
        reset = ResetSeq("reset")
        await random.start(seqr)
        await reset.start(seqr)

# Virtual Sequence to run all sequences in parallel
class TestAllSeq_Parallel(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq("random")
        reset = ResetSeq("reset")
        random_task = cocotb.start_soon(random.start(seqr))
        reset_task = cocotb.start_soon(reset.start(seqr))
        await Combine(random_task, reset_task)
