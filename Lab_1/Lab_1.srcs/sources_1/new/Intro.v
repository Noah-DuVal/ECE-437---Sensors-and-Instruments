`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 08/22/2023 04:09:01 PM
// Design Name: 
// Module Name: Intro
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


module Intro(
    input [3:0] button,
    output [7:0] led,
    input sys_clkn,
    input sys_clkp  
    );
    
    reg [23:0] clkdiv;
    reg [7:0] counter;
    reg slow_clk;
    reg cnt_dir;
    
    // This section defines the main system clock from two
    //differential clock signals: sys_clkn and sys_clkp
    // Clk is a high speed clock signal running at ~200MHz
    wire clk;
    IBUFGDS osc_clk(
        .O(clk),
        .I(sys_clkp),
        .IB(sys_clkn)
    );
    
    initial begin
        clkdiv = 0;
        counter = 8'h00;
        cnt_dir = 1'b1;
    end
    
    assign led = ~counter;
            
    // This code creates a slow clock from the high speed Clk signal
    // You will use the slow clock to run your finite state machine
    // The slow clock is derived from the fast 20 MHz clock by dividing it 10,000,000 time
    // Hence, the slow clock will run at 2 Hz
    always @(posedge clk) begin
        clkdiv <= clkdiv + 1'b1;
        if (clkdiv == 10000000) begin
            slow_clk <= ~slow_clk;
            clkdiv <= 0;
        end
    end
     
    //The main code will run fr0m the slow clock.  The rest of the code will be in this section.  
    //The counter will decrement when button 0 is pressed and on the rising edge of the slow clk 
    //Otherwise the counter will increment
    
    ////// 1 a ///////
 always @ (posedge slow_clk) begin
   if (counter == 8'b01100100) begin
          counter <= counter;
      end
      else begin
         counter <= counter + 4'b1010;
     end
 end
////// 1 b /////////
    
 //always @ (posedge slow_clk) begin
 //    if (counter == 8'b01100100 - 4'b1010) begin
 //        cnt_dir <= 1'b0;
 //    end
 //    else if (counter == 8'b00000000 + 4'b1010) begin
 //       cnt_dir <= 1'b1;
 //   end
     
 //    if (cnt_dir) begin
 //       counter <= counter + 4'b1010;
 //   end
 //    else counter <= counter - 4'b1010;
// end
endmodule

