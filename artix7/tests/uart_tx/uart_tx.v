module UART_TX(
    input rst, clk, baud_edge, data_ready,
    input [7:0] data,
    output tx, data_accepted
);
    localparam START = 2'd1, DATA = 2'd2, END = 2'd3;

    reg [7:0] data_reg;
    reg [2:0] data_counter;
    reg [1:0] state = 0;
    reg tx_reg;
    reg data_accepted_reg;

    assign tx = tx_reg;
    assign data_accepted = data_accepted_reg;

    always @(posedge clk) begin
        if(rst) begin
            state <= END;
            tx_reg <= 1;
            data_accepted_reg <= 0;
        end else if(baud_edge) begin
            case(state)
                START: begin
                    tx_reg <= 0;
                    data_counter <= 0;
                    state <= DATA;
                    data_accepted_reg <= 0;
                end
                DATA: begin
                    tx_reg <= data_reg[data_counter];
                    if(data_counter != 7) begin
                        data_counter <= data_counter + 1;
                    end else begin
                        state <= END;
                    end
                    data_accepted_reg <= 0;
                end
                END: begin
                    tx_reg <= 1;
                    if(data_ready) begin
                        data_reg <= data;
                        data_accepted_reg <= 1;
                        state <= START;
                    end else begin
                        data_accepted_reg <= 0;
                    end
                end
                default: begin
                    tx_reg <= 1;
                    state <= END;
                end
            endcase
        end else begin
            data_accepted_reg <= 0;
        end
    end
endmodule
