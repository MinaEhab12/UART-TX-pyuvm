
module UART_TX_top();
    parameter Data_Width = 8;

    logic clk;
    logic reset;
    logic [Data_Width-1:0] P_DATA;
    logic PAR_EN;
    logic PAR_TYP;
    logic DATA_VALID;
    logic TX_OUT;
    logic Busy;

    // Instantiate DUT with named parameter
    UART_TX #(.Data_Width(Data_Width)) DUT_inst (
        .clk(clk),
        .reset(reset),
        .P_DATA(P_DATA),
        .PAR_EN(PAR_EN),
        .PAR_TYP(PAR_TYP),
        .DATA_VALID(DATA_VALID),
        .TX_OUT(TX_OUT),
        .Busy(Busy)
    );

    // Bind SVA to DUT signals
    bind UART_TX UART_TX_SVA #(.Data_Width(Data_Width)) UART_TX_SVA_inst (
        .clk(clk),
        .reset(reset),
        .P_DATA(P_DATA),
        .PAR_EN(PAR_EN),
        .PAR_TYP(PAR_TYP),
        .DATA_VALID(DATA_VALID),
        .TX_OUT(TX_OUT),
        .Busy(Busy)
    );

endmodule
