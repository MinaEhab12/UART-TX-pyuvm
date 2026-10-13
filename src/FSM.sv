module FSM (
	input wire CLK,
	input wire RST,
	input wire Data_Valid,
	input wire PAR_EN,
	input wire Ser_Done,
	output reg Ser_En,
	output reg [1:0] MUX_Sel,
	output reg Busy
);

localparam [1:0] START_Mux  = 2'b00,
				 DATA_Mux   = 2'b01,
				 PARITY_Mux = 2'b11,
				 STOP_Mux   = 2'b10;

typedef enum bit [2:0] {
		IDLE   = 3'b000,
		START  = 3'b001,
		DATA   = 3'b011,
		PARITY = 3'b010,
		STOP   = 3'b110
} state;
			

state current_state,next_state;

reg busy_comb;

always @(posedge CLK or negedge RST) begin
	if(~RST) begin
		current_state <= IDLE;
		Busy <= 1'b0;
	end 
	else begin
		current_state <= next_state;
		Busy <= busy_comb;
	end
end

always @(*) begin
	Ser_En = 1'b0;
	MUX_Sel = STOP_Mux;
	busy_comb = 1'b0;
	case (current_state)
		IDLE     : begin
					if (Data_Valid) begin
						next_state = START;
						MUX_Sel = START_Mux;
						busy_comb = 1'b1;
					end
					else begin
						next_state = IDLE;
					end
			       end

		START    : begin
					next_state = DATA;
					Ser_En = 1'b1;
					MUX_Sel = DATA_Mux;
					busy_comb = 1'b1;
			       end

		DATA     : begin
					if (Ser_Done && PAR_EN) begin
						next_state = PARITY;
						MUX_Sel = PARITY_Mux;
						busy_comb = 1'b1;
					end
					else if (Ser_Done && ~PAR_EN) begin
						next_state = STOP;
						MUX_Sel = STOP_Mux;
						busy_comb = 1'b1;
					end
					else begin
						next_state = DATA;
						Ser_En = 1'b1;
						MUX_Sel = DATA_Mux;
						busy_comb = 1'b1;
					end
			      end

		PARITY  : begin
					next_state = STOP;
					MUX_Sel = STOP_Mux;
					busy_comb = 1'b1;
			      end

		STOP    : begin
					next_state = IDLE;
			      end
			      
		default : begin
					next_state = IDLE;
			   	  end
	endcase
end


property illegal_transitions_p;
  @(posedge CLK) disable iff (!RST)
  1 |-> (
    ($past(current_state) == IDLE)   -> !(current_state inside {DATA, PARITY, STOP}) &&
    ($past(current_state) == START)  -> !(current_state inside {IDLE, PARITY, STOP}) &&
    ($past(current_state) == DATA)   -> !(current_state inside {IDLE, START})        &&
    ($past(current_state) == PARITY) -> !(current_state inside {IDLE, START, DATA})  &&
    ($past(current_state) == STOP)   -> !(current_state inside {START, DATA, PARITY})
  );
endproperty

illegal_transitions_a: assert property (illegal_transitions_p) else $error("Illegal Transitions Violation detected!");
illegal_transitions_c: cover property (illegal_transitions_p);

endmodule
