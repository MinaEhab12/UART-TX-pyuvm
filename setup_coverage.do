coverage save UART_TX_combined.ucdb -onexit

## Code Coverage Exclusions
coverage exclude -du * -code c
coverage exclude -du UART_TX_SVA -code c
coverage exclude -du UART_TX_SVA -code b
coverage exclude -du UART_TX_SVA -code e
coverage exclude -du UART_TX_SVA -code t
coverage exclude -du UART_TX_SVA -code f

coverage exclude -du FSM -line 94 -code s
coverage exclude -du FSM -line 93 -code b

coverage exclude -du FSM -ftrans current_state START->IDLE
coverage exclude -du FSM -ftrans current_state DATA->IDLE
coverage exclude -du FSM -ftrans current_state PARITY->IDLE

coverage exclude -du FSM -togglenode {next_state[2]}

coverage exclude -du MUX -togglenode {Start_Bit}
coverage exclude -du MUX -togglenode {Stop_Bit}


