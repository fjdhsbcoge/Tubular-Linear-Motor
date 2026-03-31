local filename = "Config1_force_ripple_PhaseC_2A.txt"
local pole_pitch = 15.0
local steps = 60
local total_travel = 60
local move_group = 1

local file = openfile(filename, "w")
if file == nil then
    messageBox("Cannot open file")
    return
end

write(file, "Position_mm\tFx_N\tFy_N\n")

local i, pos, fx, fy
for i = 0, steps do
    pos = i * (total_travel / steps)
    
    mi_analyze()
    mi_loadsolution()
    
    mo_groupselectblock(move_group)
    fx = mo_blockintegral(18)
    fy = mo_blockintegral(19)
    
    write(file, pos .. "\t" .. fx .. "\t" .. fy .. "\n")
    print("Step " .. i .. " Pos: " .. pos .. " Fx: " .. fx)
    
    if i < steps then
        mi_selectgroup(move_group)
        mi_movetranslate(total_travel/steps, 0)
        mi_clearselected()
    end
end

closefile(file)
print("Ripple analysis complete")