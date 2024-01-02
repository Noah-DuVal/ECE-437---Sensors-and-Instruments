`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: University of Illinois Urbana Champaign
// Engineer: Ryan Libiano
// 
// Create Date: 10/21/2023 07:33:08 PM
// Design Name: 
// Module Name: PWMDriver
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module PWMDriver 
                  (input wire CLK,
                  input wire RST,
                  input wire [11:0] DUTY_CYC,
                  output reg PWM_OUT);
     //define needed registers
     reg [11:0] counter;       
              
    initial begin
        counter = 12'd0;
        PWM_OUT = 1'd0;
    end
    always @(posedge CLK) begin
        if (RST) 
            counter <= 12'd0;
        else if (counter >= DUTY_CYC) begin
            counter <= counter + 12'd1;
            PWM_OUT <= 1'b0;
        end
        else if (counter < DUTY_CYC)begin
            counter <= counter + 12'd1;
            PWM_OUT <= 1'b1;
        end
    end

endmodule
