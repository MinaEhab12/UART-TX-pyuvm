# defaults
COCOTB_REDUCED_LOG_FMT = True
SIM ?= questa-compat
TOPLEVEL_LANG ?= verilog

# Add questa installation path to PATH
export PATH := C:\questasim64_2021.1\win64:$(PATH)

# Enable code coverage
VLOG_ARGS += +cover -covercells
VSIM_ARGS += -classdebug -cover -coverage
VSIM_ARGS += -do setup_coverage.do

# Adding Verilog sources
VERILOG_SOURCES += $(PWD)/src/FSM.sv
VERILOG_SOURCES += $(PWD)/src/MUX.v
VERILOG_SOURCES += $(PWD)/src/Parity_Calc.v
VERILOG_SOURCES += $(PWD)/src/Serializer.v
VERILOG_SOURCES += $(PWD)/src/UART_TX.v
VERILOG_SOURCES += $(PWD)/sim/Assertions/UART_TX_SVA.sv
VERILOG_SOURCES += $(PWD)/sim/UART_TX_top.sv

# TOPLEVEL is the name of the toplevel module in your Verilog file
TOPLEVEL = UART_TX_top

# MODULE is the basename of the Python test file
MODULE = sim.Test.testbench

# set the HDL time unit and precision
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ns

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

report_code_coverage:
	vcover report UART_TX_combined.ucdb -details -all -codeAll -output code_coverage_report.txt

report_assertion_coverage:
	vcover report UART_TX_combined.ucdb -details -all -byfile -assert -directive -output assertion_coverage_report.txt

cleanall:
	@rm -rf __pycache__
	@rm -rf sim_build
	@rm -rf modelsim.ini
	@rm -rf transcript
	@rm -rf *.txt
	@rm -rf *.ucdb
	@rm -rf *.xml
	@rm -rf *.yml
	@rm -rf *.vstf
	@rm -rf *.vcd
	@echo "Cleanup completed successfully!"
