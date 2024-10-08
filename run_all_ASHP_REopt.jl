using Pkg
using JSON
using CSV
using DataFrames
#using Xpress
using GAMS
using JuMP
using REopt

dir = @__DIR__
results_path = joinpath(dir, "results","results_json")          # where to save results
posts_path = joinpath(dir, "data", "posts")

for file in readdir(posts_path) 
    print("\n",file)
    if file == ".DS_Store"
        continue
    else
        post = JSON.parsefile("$posts_path/$file")
    end
    #m1 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))
    #m2 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))
    
    m1 = Model(GAMS.Optimizer)
    m2 = Model(GAMS.Optimizer)
    set_optimizer_attribute(m1, "Solver", "CPLEX")
    set_optimizer_attribute(m2, "Solver", "CPLEX")

    r = run_reopt([m1,m2], REoptInputs(Scenario(post)))
    write(joinpath(results_path, file), JSON.json(r))
    #end
end