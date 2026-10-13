module UART_TX # (parameter Data_Width = 8)
(
	input wire clk,
	input wire reset,
	input wire [Data_Width-1:0] P_DATA,
	input wire DATA_VALID,
	input wire PAR_EN,
	input wire PAR_TYP,
	output wire TX_OUT,
	output wire Busy
);

// Internal connections
wire ser_done,ser_en,ser_data,par_bit;
wire [1:0] mux_sel;


Serializer U_Serializer (
.CLK       (clk),
.RST       (reset),
.Busy      (Busy),
.P_DATA    (P_DATA),
.Data_Valid(DATA_VALID),
.Ser_En    (ser_en),
.Ser_Data  (ser_data),
.Ser_Done  (ser_done)
);

FSM U_FSM (
.CLK       (clk),
.RST       (reset),
.Ser_En    (ser_en),
.Ser_Done  (ser_done),
.Data_Valid(DATA_VALID),
.PAR_EN    (PAR_EN),
.MUX_Sel   (mux_sel),
.Busy      (Busy)
);

Parity_Calc U_Parity_Calc (
.CLK       (clk),
.RST       (reset),
.Data_Valid(DATA_VALID),
.Busy      (Busy),
.P_DATA    (P_DATA),
.PAR_TYP   (PAR_TYP),
.Par_Bit   (par_bit)
);

MUX U_MUX (
.CLK      (clk),
.RST      (reset),
.MUX_Sel  (mux_sel),
.Par_Bit  (par_bit),
.Ser_Data (ser_data),
.Start_Bit(1'b0),
.Stop_Bit (1'b1),
.TX_OUT   (TX_OUT)
);

initial begin
    $dumpfile("UART_TX.vcd");
    $dumpvars(0, UART_TX);
end

endmodule
