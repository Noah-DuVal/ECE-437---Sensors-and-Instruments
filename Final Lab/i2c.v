 `timescale 1ns / 1ps

module I2C_Transmit(    
    input  sys_clkn,
    input  sys_clkp,
    output ADT7420_A0,
    output ADT7420_A1,
    output I2C_SCL_1,
    inout  I2C_SDA_1,        
    output reg FSM_Clk_reg,    
    output reg ILA_Clk_reg,
    output reg ACK_bit,
    output reg SCL,
    output reg SDA,
    output reg [9:0] State,
    output wire [31:0] PC_control,
    input  wire    [4:0] okUH,
    output wire    [2:0] okHU,
    inout  wire    [31:0] okUHU,
    output    wire [31:0] DeviceAd,
    output wire [31:0] SubAd,   
    output wire [31:0] DataW,   
    output wire [31:0] DutyCyc, 
    output wire [31:0] MotorD, 
    output wire [31:0] Pulses, 
    output PMOD_A1,     
    output PMOD_A2,
    output wire Direction,
    output wire Step,
    output wire [3:0] MState,
    output wire slow_clk,
    output wire [31:0] Data_Counter,
    inout wire okAA,
    output wire topclk, okClk,
    output wire FIFO_read_enable, 
    input wire FIFO_BT_BlockSize_Full,
    output wire [31:0] variable_1, variable_2, variable_3, python_start, Reset_Counter,
    input wire [31:0] result_wire, variable_4, FIFO_data    

    
    );
       
    wire [23:0] ClkDivThreshold = 10;   
    wire FSM_Clk, ILA_Clk; 
    wire clk1, BT_Strobe;
    assign topclk = clk1;
    ClockGenerator ClockGenerator1 (  .sys_clkn(sys_clkn),
                                      .sys_clkp(sys_clkp),                                      
                                      .ClkDivThreshold(ClkDivThreshold),
                                      .FSM_Clk(FSM_Clk),         
                                      .clk1(clk1),                             
                                      .ILA_Clk(ILA_Clk) );
                                      
   MotorControl MotorCont ( .clkp(clk1),
                            .MotorD(MotorD),
                            .Pulses(Pulses), 
                            .DutyCyc(DutyCyc),
                            .PMOD_A1(PMOD_A1),
                            .PMOD_A2(PMOD_A2),
                            .Direction(Direction),
                            .Step(Step),
                            .counter(Data_Counter),
                            .State(MState),
                            .slow_clk(slow_clk)
                              );

    ////////////////// Creating Variables /////////////////                

    reg [7:0] Data_Counter;
    reg [7:0] Next_State;
    reg error_bit = 1'b1;   
    reg [7:0] Data_In;
    reg RWflag;
    reg [7:0] Data_1, Data_2, Data_3, Data_4, Data_5, Data_6;
    reg [7:0] Data_Out;
    wire [15:0] Data_Out_1, Data_Out_2, Data_Out_3;
    wire clkp;

    //////////////// Assigning Data Read to Data Out ///////////////

    assign Data_Out_1 = {Data_1, Data_2};
    assign Data_Out_2 = {Data_3, Data_4};
    assign Data_Out_3 = {Data_5, Data_6};     


    ////////////// Creating Variables for I2C Sequences //////////////   
       
    localparam STATE_INIT       = 10'd0;    
    parameter start = 8'd1;
    parameter stop = 8'd8;
    parameter end_i2c = 8'd88;
    parameter Restart = 8'd3;
    parameter S_ACK = 8'd12;
    parameter M_ACK = 8'd16;
    parameter N_ACK = 8'd20;
    parameter Send_Data = 8'd24;
    parameter Get_Data = 8'd56;


    assign ADT7420_A0 = 1'b0;
    assign ADT7420_A1 = 1'b0;
    assign I2C_SCL_1 = SCL;
    assign I2C_SDA_1 = SDA; 
    assign clkp = sys_clkp;

    always @(*) begin          
        FSM_Clk_reg = FSM_Clk;
        ILA_Clk_reg = ILA_Clk;   

    end   

    initial  begin
        SCL = 1'b1;
        SDA = 1'b1;
        ACK_bit = 1'b1;  
        State = 10'd0; 
        RWflag = 1'b0;
        Data_In = 8'd0;
        
    end
    
    //////////// I2C State Machine ///////////////////


    always @(posedge FSM_Clk) begin                       
        case (State)
            // Press Button[3] to start the state machine. Otherwise, stay in the STATE_INIT state        
            STATE_INIT : begin
                 if (PC_control[0] == 1'b1) State <= 10'd1;                   
                 else begin                 
                      SCL <= 1'b1;
                      SDA <= 1'b1;
                      State <= 10'd0;
                  end
            end            
            
            ///////// Start Sequence ///////////////

            10'd1 : begin                                    
                Data_Counter <= 8'd0;
                SCL <= 1'b1; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd2 : begin        
                SCL <= 1'b0; 
                SDA <= 1'b0;
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State; 
            end

            ////// Start Sequence ////////

            10'd3 : begin                                   
                SCL <= 1'b0; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd4 : begin        
                SCL <= 1'b0; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd5 : begin       
                SCL <= 1'b1; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd6 : begin        
                SCL <= 1'b1; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd7 : begin        
                SCL <= 1'b0; 
                SDA <= 1'b0;
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State;  
            end

            /////// Stop Sequence //////////


            10'd8 : begin        
                SCL <= 1'b0; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd9 : begin        
                SCL <= 1'b1; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd10 : begin        
                SCL <= 1'b1; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd11 : begin        
                SCL <= 1'b1; 
                SDA <= 1'b1;
                State <= end_i2c;  
            end

            /////// Slave Ack //////////

            10'd12 : begin      
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd13 : begin     
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd14 : begin       
                SCL <= 1'b1; 
                ACK_bit <= SDA;
                State <= State + 1'b1; 
            end

            10'd15 : begin       
                SCL <= 1'b0; 
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State;  
            end

            /////////   Master ACK  .//////////

            10'd16 : begin       
                SCL <= 1'b0; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd17 : begin      
                SCL <= 1'b1; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd18 : begin       
                SCL <= 1'b1; 
                SDA <= 1'b0;
                State <= State + 1'b1; 
            end

            10'd19 : begin       
                SCL <= 1'b0; 
                SDA <= 1'b0;
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State; 
            end

            ////////    Master No ACK   ///////////


            10'd20 : begin       
                SCL <= 1'b0; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd21 : begin       
                SCL <= 1'b1; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd22 : begin       
                SCL <= 1'b1; 
                SDA <= 1'b1;
                State <= State + 1'b1; 
            end

            10'd23 : begin       
                SCL <= 1'b0; 
                SDA <= 1'b1;
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State; 
            end

            //////// Transmit Data In ///////////


            10'd24 : begin       
                SCL <= 1'b0; 
                SDA <= Data_In[7];
                State <= State + 1'b1; 
            end

            10'd25 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd26 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd27 : begin       
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd28 : begin       
                SCL <= 1'b0; 
                SDA <= Data_In[6];
                State <= State + 1'b1; 
            end

            10'd29 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd30 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd31 : begin        
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd32 : begin      
                SCL <= 1'b0; 
                SDA <= Data_In[5];
                State <= State + 1'b1; 
            end

            10'd33 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd34 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd35 : begin     
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd36 : begin       
                SCL <= 1'b0; 
                SDA <= Data_In[4];
                State <= State + 1'b1; 
            end

            10'd37 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd38 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd39 : begin    
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd40 : begin      
                SCL <= 1'b0; 
                SDA <= Data_In[3];
                State <= State + 1'b1; 
            end

            10'd41 : begin     
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd42 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd43 : begin     
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd44 : begin    
                SCL <= 1'b0; 
                SDA <= Data_In[2];
                State <= State + 1'b1; 
            end

            10'd45 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd46 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd47 : begin    
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd48 : begin       
                SCL <= 1'b0; 
                SDA <= Data_In[1];
                State <= State + 1'b1; 
            end

            10'd49 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd50 : begin    
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd51 : begin      
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd52 : begin       
                SCL <= 1'b0; 
                SDA <= Data_In[0];
                State <= State + 1'b1; 
            end

            10'd53 : begin    
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd54 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd55 : begin       
                SCL <= 1'b0; 
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State;  
            end

            //////  Reading DATA In  ////////////

            10'd56 : begin       
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd57 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd58 : begin       
                SCL <= 1'b1; 
                Data_Out[7] <= SDA;
                State <= State + 1'b1; 
            end

            10'd59 : begin      
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd60 : begin       
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd61 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd62 : begin     
                SCL <= 1'b1; 
                Data_Out[6] <= SDA;
                State <= State + 1'b1; 
            end

            10'd63 : begin       
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd64 : begin       
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd65 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd66 : begin        
                SCL <= 1'b1; 
                Data_Out[5] <= SDA;
                State <= State + 1'b1; 
            end

            10'd67 : begin       
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd68 : begin      
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd69 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd70 : begin      
                SCL <= 1'b1; 
                Data_Out[4] <= SDA;
                State <= State + 1'b1; 
            end

            10'd71 : begin      
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd72 : begin      
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd73 : begin       
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd74 : begin      
                SCL <= 1'b1; 
                Data_Out[3] <= SDA;
                State <= State + 1'b1; 
            end

            10'd75 : begin       
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd76 : begin      
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd77 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd78 : begin       
                SCL <= 1'b1; 
                Data_Out[2] <= SDA;
                State <= State + 1'b1; 
            end

            10'd79 : begin      
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd80 : begin     
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd81 : begin      
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd82 : begin       
                SCL <= 1'b1; 
                Data_Out[1] <= SDA;
                State <= State + 1'b1; 
            end

            10'd83 : begin     
                SCL <= 1'b0; 
                State <= State + 1'b1; 
            end

            10'd84 : begin       
                SCL <= 1'b0; 
                SDA <= 1'bz;
                State <= State + 1'b1; 
            end

            10'd85 : begin     
                SCL <= 1'b1; 
                State <= State + 1'b1; 
            end

            10'd86 : begin      
                SCL <= 1'b1; 
                Data_Out[0] <= SDA;
                
                State <= State + 1'b1; 
            end

            ///// Adjust for Incremental Reading  ///////////

            10'd87 : begin      
                SCL <= 1'b0; 
                case(Data_Counter) 
                    8'd8 : Data_1 <= Data_Out;
                    8'd10 :  Data_2 <= Data_Out;
                    8'd12 :  Data_3 <= Data_Out;
                    8'd14 :  Data_4 <= Data_Out;
                    8'd16 :  Data_5 <= Data_Out;
                    8'd18 :  Data_6 <= Data_Out;
                    default : Data_6 <= Data_Out;
                endcase
                Data_Counter <= Data_Counter + 1'b1;
                State <= Next_State; 
            end
            
            10'd88 : begin 
                if(PC_control[0] == 1'b0) begin
                    State <= STATE_INIT; 
                end
            end

            default : begin
              error_bit <= 0;
            end
            
        endcase                           
    end      
    
    ///////// Case Statement to decide on which I2C sequence to run //////////

    always @(*) begin
                
        Data_In = 1'bz;
        case (Data_Counter) 
            8'd0 : begin
                Next_State = Send_Data;
                Data_In = {DeviceAd[7:1], 1'b0};
            end
            
            8'd1 : begin
                Next_State = S_ACK;
                Data_In = {DeviceAd[7:1], 1'b0}; 
            end
            
            8'd2 : begin
                Next_State = Send_Data;
                Data_In = SubAd;
            end
            
            8'd3 : begin
                Next_State = S_ACK;
                Data_In = SubAd;
            end
            
            8'd4 : begin
                if (SubAd[7] == 1'b0) begin 
                    Next_State = Send_Data;
                end 
                else begin
                    Next_State = Restart;
                    Data_In = DataW;
                end
            end
            
            8'd5 : begin
                if (SubAd[7] == 1'b0) begin 
                    Next_State = S_ACK;
                    Data_In = DataW;
                end 
                else begin
                    Next_State = Send_Data;
                    Data_In = {DeviceAd[7:1], 1'b1};
                end
            end
            
            8'd6 : begin
                if (SubAd[7] == 1'b0) begin 
                    Next_State = stop;
                end 
                else begin
                    Next_State = S_ACK;
                    Data_In = {DeviceAd[7:1], 1'b1};
                end
            end
            
            8'd7 : begin
                Next_State = Get_Data;
            end
            
            8'd8 : begin
                Next_State = M_ACK;
            end
            
            8'd9 : begin
                Next_State = Get_Data;
            end
            
            8'd10 : begin
                Next_State = M_ACK;
            end
            
            8'd11 : begin
                Next_State = Get_Data;
            end
            
            8'd12 : begin
                Next_State = M_ACK;
            end
            
            8'd13 : begin
                Next_State = Get_Data;    
            end
            
            8'd14 : begin
                Next_State = M_ACK;
            end
            
            8'd15 : begin
                Next_State = Get_Data;
            end
            
            8'd16 : begin
                Next_State = M_ACK;
            end
            
            8'd17 : begin
                Next_State = Get_Data;
            end
            
            8'd18 : begin
                Next_State = N_ACK;
                
            end
            
            8'd19 : begin
                Next_State = stop;
            end
            
            default : begin 
                Next_State = stop;
                Data_In = 8'b11111111;
            end
            
        endcase
    end


    ///////// OK Wires  //////////

    wire [112:0]    okHE;     
    wire [64:0]     okEH; 
     
    okHost hostIF (
        .okUH(okUH),
        .okHU(okHU),
        .okUHU(okUHU),
        .okClk(okClk),
        .okAA(okAA),
        .okHE(okHE),
        .okEH(okEH)
    );

    localparam  endPt_count = 6;
    wire [endPt_count*65-1:0] okEHx;  
    okWireOR # (.N(endPt_count)) wireOR (okEH, okEHx);
   
    okWireIn wire10 (   .okHE(okHE), 
                        .ep_addr(8'h00), 
                        .ep_dataout(PC_control));            
    okWireIn wire11 (   .okHE(okHE), 
                        .ep_addr(8'h01), 
                        .ep_dataout(DeviceAd));      
    okWireIn wire12 (   .okHE(okHE), 
                        .ep_addr(8'h02), 
                        .ep_dataout(SubAd));               
    okWireIn wire13 (   .okHE(okHE), 
                        .ep_addr(8'h03), 
                        .ep_dataout(DataW));      
    okWireIn wire14 (   .okHE(okHE), 
                        .ep_addr(8'h04), 
                        .ep_dataout(variable_1));
    okWireIn wire15 (   .okHE(okHE), 
                        .ep_addr(8'h05), 
                        .ep_dataout(variable_2));
    okWireIn wire16 (   .okHE(okHE), 
                        .ep_addr(8'h06), 
                        .ep_dataout(variable_3));
    okWireIn wire17 (   .okHE(okHE), 
                        .ep_addr(8'h07), 
                        .ep_dataout(python_start));
    okWireIn wire18 (   .okHE(okHE), 
                        .ep_addr(8'h08), 
                        .ep_dataout(Reset_Counter));         
    okWireIn wire20 (   .okHE(okHE), 
                        .ep_addr(8'h09), 
                        .ep_dataout(MotorD));            
    okWireIn wire21 (   .okHE(okHE), 
                        .ep_addr(8'h10), 
                        .ep_dataout(Pulses));
    okWireIn wire22 (   .okHE(okHE), 
                        .ep_addr(8'h11), 
                        .ep_dataout(DutyCyc));                               
    okWireOut wire23 (  .okHE(okHE), 
                        .okEH(okEHx[ 0*65 +: 65 ]), 
                        .ep_addr(8'h20), 
                        .ep_datain(Data_Out_1));                        
    okWireOut wire24 (  .okHE(okHE), 
                        .okEH(okEHx[ 1*65 +: 65 ]),
                        .ep_addr(8'h21), 
                        .ep_datain(Data_Out_2));                           
    okWireOut wire25 (  .okHE(okHE), 
                        .okEH(okEHx[ 2*65 +: 65 ]),
                        .ep_addr(8'h22), 
                        .ep_datain(Data_Out_3));                   
    okWireOut wire26 (  .okHE(okHE), 
                        .okEH(okEHx[ 3*65 +: 65 ]),
                        .ep_addr(8'h23), 
                        .ep_datain(result_wire));  
    okWireOut wire27 (  .okHE(okHE), 
                        .okEH(okEHx[ 4*65 +: 65 ]),
                        .ep_addr(8'h24), 
                        .ep_datain(variable_4));  
                        
    wire fiforeaden, fifobtblockfull, btstrobe;
    assign FIFO_read_enable = fiforeaden;
    assign fifobtblockfull = FIFO_BT_BlockSize_Full;  
    okBTPipeOut CounterToPC (
        .okHE(okHE), 
        .okEH(okEHx[ 5*65 +: 65 ]),
        .ep_addr(8'ha0), 
        .ep_datain(FIFO_data),  //input 32
        .ep_read(fiforeaden), //output 1
        .ep_blockstrobe(btstrobe), //input 1
        .ep_ready(fifobtblockfull) //output 1
    );                        
                                     
endmodule