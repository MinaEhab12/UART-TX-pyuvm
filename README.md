# UART TX Verification Project

## Overview
- This project verifies a UART transmitter designed in SystemVerilog using a Python-based UVM testbench.
- The main objective is to check correct UART transmission behavior, including reset, data serialization, parity handling, and output timing.
- The verification flow uses:
  - PyUVM for the testbench and sequences
  - Cocotb for simulation integration
  - Questa/ModelSim for RTL simulation
  - Assertions and coverage reports to validate the design

## Project Purpose
- Validate the UART transmitter module under different input conditions.
- Run multiple test scenarios such as reset, random transmissions, and parallel execution.
- Check functional correctness with assertions and coverage collection.
- Generate coverage reports for code and assertion coverage.

## Main Components
- RTL design files in the `src/` folder
- Verification environment and sequences in the `sim/` folder
- Assertions in the `sim/Assertions/` folder
- Coverage setup in the project root

## Project Structure
- `src/`
  - `UART_TX.v` — UART transmitter design
  - `FSM.sv` — finite state machine
  - `Serializer.v` — serial data output logic
  - `Parity_Calc.v` — parity generation
  - `MUX.v` — output selection logic
- `sim/`
  - `UART_TX_top.sv` — top-level simulation wrapper
  - `UART_TX_utils.py` — helper utilities
  - `Assertions/UART_TX_SVA.sv` — SystemVerilog assertions
  - `Test/`
    - `testbench.py` — PyUVM tests
    - `Env/` — environment, agent, monitor, driver, scoreboard
    - `Sequences/` — verification sequences
- `Makefile` — simulation and coverage commands
- `code_coverage_report.txt` — code coverage output
- `assertion_coverage_report.txt` — assertion coverage output

## Requirements
- Python
- Cocotb
- PyUVM
- Questa/ModelSim simulator
- A valid simulator path configured in the `Makefile`

> The project currently points to `C:\questasim64_2021.1\win64` in the Makefile. If your installation path is different, update it before running the tests.

## How to Run the Project
1. Open a terminal in the project folder.
2. Make sure the simulator is installed and accessible.
3. Run the simulation:
   - `make`
4. If you want to clean generated files:
   - `make cleanall`

## Available Verification Tests
- Base test runs the complete UART TX sequence flow.
- Parallel test executes sequence sets in parallel.
- Reset test validates reset behavior.
- Random test runs randomized stimulus scenarios.

## Coverage Reports
- Generate code coverage:
  - `make report_code_coverage`
- Generate assertion coverage:
  - `make report_assertion_coverage`


