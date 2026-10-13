// verilog_lint: waive-start explicit-parameter-storage-type
// verilog_lint: waive-start unpacked-dimensions-range-ordering
// verilog_lint: waive-start line-length
// verilog_lint: waive-start enum-name-style
// verilog_lint: waive-start typedef-enums

module UART_TX_SVA # (parameter Data_Width = 8) (
    input wire clk,
    input wire reset,
    input wire [Data_Width-1:0] P_DATA,
    input wire DATA_VALID,
    input wire PAR_EN,
    input wire PAR_TYP,
    input wire TX_OUT,
    input wire Busy
);

always_comb begin
    if (!reset) begin
        Reset_a: assert final (TX_OUT && ~Busy) else $error("Reset Violation detected!");
        Reset_c: cover  final (TX_OUT && ~Busy);
    end
end

property start_bit_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && DATA_VALID) |=> (~TX_OUT);
endproperty

property Data_Bits_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && DATA_VALID)
    |=> ##1 (TX_OUT == P_DATA[0])
    ##1 (TX_OUT == P_DATA[1])
    ##1 (TX_OUT == P_DATA[2])
    ##1 (TX_OUT == P_DATA[3])
    ##1 (TX_OUT == P_DATA[4])
    ##1 (TX_OUT == P_DATA[5])
    ##1 (TX_OUT == P_DATA[6])
    ##1 (TX_OUT == P_DATA[7]);
endproperty

property odd_parity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && PAR_EN && PAR_TYP && DATA_VALID) |=> ##9 (TX_OUT == ^P_DATA);
endproperty

property even_parity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && PAR_EN && ~PAR_TYP && DATA_VALID) |=> ##9 (TX_OUT == ~^P_DATA);
endproperty

property stop_bit_WithParity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && PAR_EN && DATA_VALID) |=> ##10 (TX_OUT);
endproperty

property stop_bit_WithoutParity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && ~PAR_EN && DATA_VALID) |=> ##9 (TX_OUT);
endproperty

property busy_WithParity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && PAR_EN && DATA_VALID) |=> (Busy[*10]);
endproperty

property busy_WithoutParity_p;
    @(posedge clk) disable iff (!reset)
    ((P_DATA != $past(P_DATA)) && ~PAR_EN && DATA_VALID) |=> (Busy[*9]);
endproperty

property idle_when_not_busy_p;
  @(posedge clk) disable iff (!reset)
  (!Busy) |-> (TX_OUT);
endproperty


Odd_Parity_a: assert property (odd_parity_p) else $error("Odd Parity Violation detected!");
Odd_Parity_c: cover property (odd_parity_p);

Even_Parity_a: assert property (even_parity_p) else $error("Even Parity Violation detected!");
Even_Parity_c: cover property (even_parity_p);

Start_Bit_a: assert property (start_bit_p) else $error("Start Bit Violation detected!");
Start_Bit_c: cover property (start_bit_p);

Stop_Bit_With_Parity_a: assert property (stop_bit_WithParity_p) else $error("Stop Bit With Parity Violation detected!");
Stop_Bit_With_Parity_c: cover property (stop_bit_WithParity_p);

Stop_Bit_Without_Parity_a: assert property (stop_bit_WithoutParity_p) else $error("Stop Bit Without Parity Violation detected!");
Stop_Bit_Without_Parity_c: cover property (stop_bit_WithoutParity_p);

Busy_WithParity_a: assert property (busy_WithParity_p) else $error("Busy With Parity Violation detected!");
Busy_WithParity_c: cover property (busy_WithParity_p);

Busy_WithoutParity_a: assert property (busy_WithoutParity_p) else $error("Busy Without Parity Violation detected!");
Busy_WithoutParity_c: cover property (busy_WithoutParity_p);

Data_Bits_a: assert property (Data_Bits_p) else $error("Data Bits Violation detected!");
Data_Bits_c: cover property (Data_Bits_p);

Idle_When_Not_Busy_a: assert property (idle_when_not_busy_p) else $error("Idle When Not Busy Violation detected!");
Idle_When_Not_Busy_c: cover property (idle_when_not_busy_p);

endmodule
