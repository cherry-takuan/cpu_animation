import time
RED_STROKE = "#b85450"
GREEN_STROKE = "#82b366"
BLUE_STROKE = "#6c8ebf"
ORANGE_STROKE = "#d79b00"
CLR_STROKE = "#000000"

RED_REG_FILL = "url(#mx-gradient-f8cecc-1-ea6b66-1-s-0)"
GREEN_REG_FILL = "url(#mx-gradient-d5e8d4-1-97d077-1-s-0)"
BLUE_REG_FILL = "url(#mx-gradient-dae8fc-1-7ea6e0-1-s-0)"
ORANGE_REG_FILL = "url(#mx-gradient-ffcd28-1-ffa500-1-s-0)"
CLR_REG_FILL = "#FFFFFF"

RED_PATH_FILL = "#f8cecc"
GREEN_PATH_FILL = "#d5e8d4"
BLUE_PATH_FILL = "#dae8fc"
ORANGE_PATH_FILL = "#ffe6cc"
CLR_PATH_FILL = "#FFFFFF"

Reg_table = {
    "IR1":0,
    "IR2":1,
    "IR3":2,
    "IV":3,
    "Flag":4,
    "RegA":5,
    "RegB":6,
    "RegC":7,
    "RegD":8,
    "RegE":9,
    "MEM":10,
    "Bank":11,
    "Address":12,
    "IP":13,
    "SP":14,
    "Zero":15
}

def Reg_Color(svg,ID,mode,step):
    select_s = "ID-"+str(ID).zfill(2)+"_STROKE"
    select_f = "ID-"+str(ID).zfill(2)+"_FILL"

    if mode == "a":
        svg = svg.replace(select_f,RED_REG_FILL)
        svg = svg.replace(select_s,RED_STROKE)
    elif mode == "b":
        svg = svg.replace(select_f,BLUE_REG_FILL)
        svg = svg.replace(select_s,BLUE_STROKE)
    elif mode == "r":
        if step%4 == 1:
            svg = svg.replace(select_f,GREEN_REG_FILL)
            svg = svg.replace(select_s,GREEN_STROKE)
        elif step%4 == 3:
            svg = svg.replace(select_f,ORANGE_REG_FILL)
            svg = svg.replace(select_s,ORANGE_STROKE)
    
    elif mode == "clr":
        svg = svg.replace(select_f,CLR_REG_FILL)
        svg = svg.replace(select_s,CLR_STROKE)
    return svg

def Reg_Color_CLR(svg):
    for num in range(16):
        svg = Reg_Color(svg,num,"clr",0)
    return svg

def path(svg,path_name,mode,step):
    select_s = path_name+"_PATH_STROKE"
    select_f = path_name+"_PATH_FILL"
    select_reg_s = path_name+"_STROKE"
    select_reg_f = path_name+"_FILL"

    if mode == "a":
        svg = svg.replace(select_f,RED_PATH_FILL)
        svg = svg.replace(select_s,RED_STROKE)
    elif mode == "b":
        svg = svg.replace(select_f,BLUE_PATH_FILL)
        svg = svg.replace(select_s,BLUE_STROKE)
    elif mode == "alu":
        if step%4 == 3 or step%4 == 0:
            svg = svg.replace(select_f,GREEN_PATH_FILL)
            svg = svg.replace(select_s,GREEN_STROKE)
        elif step%4 == 1 or step%4 == 2:
            svg = svg.replace(select_f,ORANGE_PATH_FILL)
            svg = svg.replace(select_s,ORANGE_STROKE)
    elif mode == "tmp":
        if step%4 == 0 or step%4 == 1:
            svg = svg.replace(select_f,GREEN_PATH_FILL)
            svg = svg.replace(select_s,GREEN_STROKE)
            svg = svg.replace(select_reg_f,GREEN_REG_FILL)
            svg = svg.replace(select_reg_s,GREEN_STROKE)
        elif step%4 == 2 or step%4 == 3:
            svg = svg.replace(select_f,ORANGE_PATH_FILL)
            svg = svg.replace(select_s,ORANGE_STROKE)
            svg = svg.replace(select_reg_f,ORANGE_REG_FILL)
            svg = svg.replace(select_reg_s,ORANGE_STROKE)
    elif mode == "clr":
        svg = svg.replace(select_f,CLR_PATH_FILL)
        svg = svg.replace(select_s,CLR_STROKE)

    return svg

def CLK(svg,step):
    select1 = "CLK_1"
    select2 = "CLK_2"
    if step%2 == 0:
        svg = svg.replace(select1,"rgb(51, 255, 51)")
        svg = svg.replace(select2,"rgb(s55, 255, s55)")
    elif step%2 == 1:
        svg = svg.replace(select1,"rgb(255, 255, 255)")
        svg = svg.replace(select2,"rgb(51, 255, 51)")
    
    return svg

def svg_make(a_bus,b_bus,y_bus,mode,sel,step):
    with open("./base.svg") as f:
        svg = f.read()
        
        svg = Reg_Color(svg,Reg_table[a_bus],"a",step)
        if b_bus != None:
            svg = Reg_Color(svg,Reg_table[b_bus],"b",step)
        svg = Reg_Color(svg,Reg_table[y_bus],"r",step)

        svg = path(svg,"A","a",step)
        svg = path(svg,"B","b",step)
        svg = path(svg,"ALU","alu",step)
        svg = path(svg,"TMP","tmp",step)

        svg = text_set(svg,"ALU_MODE",mode)
        svg = text_set(svg,"ALU_SEL",sel)

        svg = text_set(svg,"STEP_COUNT",str(step))
        svg = text_set(svg,"INSTRUCTION_N","CALL")
        if b_bus != None:
            svg = text_set(svg,"MICRO_INSTRUCTION",mode+" : "+a_bus+", "+b_bus+"  -&gt; "+y_bus)
        else:
            svg = text_set(svg,"MICRO_INSTRUCTION",mode+" : "+a_bus+" -&gt; "+y_bus)

        if a_bus == "MEM":
            svg = path(svg,"EXT","a",step)
        elif b_bus == "MEM":
            svg = path(svg,"EXT","b",step)
        elif y_bus == "MEM":
            svg = path(svg,"EXT","r",step)
        else:
            svg = path(svg,"EXT","clr",step)
        
        
        if y_bus == "IP":
            svg = Reg_Color(svg,Reg_table["Address"],"r",step)
        
        if y_bus == "SP":
            svg = Reg_Color(svg,Reg_table["Address"],"r",step)

        svg = Reg_Color_CLR(svg)
        svg = CLK(svg,step)

        with open("./test/"+str(step)+".svg", mode='w') as f:
            f.write(svg)
        with open("./test.svg", mode='w') as f:
            f.write(svg)

def main():
    with open("./pattern.txt") as f:
        inst_list = f.readlines()
    now_inst = inst_list[0]
    inst_list = inst_list[1:]
    step = 0
    for next_inst in inst_list:
        inst_token = now_inst[0:-1].split(" ")

        now_a_bus = None
        now_b_bus = None
        now_y_bus = None
        now_mode = "MOV"
        now_sel = "Y"

        if len(inst_token) == 3:
            print("Mode:",inst_token[0],",\tto:",inst_token[1],",\tfrom:",inst_token[2])
            
            now_mode = inst_token[0]
            now_y_bus = inst_token[1]
            now_a_bus = inst_token[2]

        elif len(inst_token) == 4:
            print("Mode:",inst_token[0],",\tto:",inst_token[1],",\tfrom:",inst_token[2],",\t",inst_token[3])
        
            now_mode = inst_token[0]
            now_y_bus = inst_token[1]
            now_a_bus = inst_token[2]
            now_b_bus = inst_token[3]
        
        next_a_bus = None
        next_b_bus = None
        next_y_bus = None
        next_mode = "MOV"
        next_sel = "Y"

        if len(inst_token) == 3:
            
            next_mode = inst_token[0]
            next_y_bus = inst_token[1]
            next_a_bus = inst_token[2]

        elif len(inst_token) == 4:
        
            next_mode = inst_token[0]
            next_y_bus = inst_token[1]
            next_a_bus = inst_token[2]
            next_b_bus = inst_token[3]
        
        svg_make(now_a_bus,now_b_bus,now_y_bus,now_mode,now_sel,step)
        step += 1
        time.sleep(1)
        svg_make(next_a_bus,next_b_bus,now_y_bus,next_mode,next_sel,step)
        step += 1
        now_inst = next_inst
        time.sleep(1)

def text_set(svg,name,txt):
    select = name
    svg = svg.replace(select,txt)
    return svg


if __name__ == "__main__":
    main()