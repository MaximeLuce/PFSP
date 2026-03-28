import pandas as pd

def generate_latex_table(csv_path):
    # reading CSV file...
    df = pd.read_csv(csv_path, sep=';')
    
    # recuperation of uniques instances (preserving order)
    instances = df['Instance'].unique()
    num_instances = len(instances)
    
    # formating data: extracting interesting columns
    metrics = ['SA_Best', 'SA_Worst', 'SA_Avg', 'SA_Std', 'SA_Time(s)', 'SA_NFE_Avg', 'Best_Known_Value']
    data = {m: [] for m in metrics}
    
    for inst in instances:
        # filter by instance and Case_ID
        df_inst = df[df['Instance'] == inst].sort_values('Case_ID')
        for m in metrics:
            # adding data to the dico
            data[m].extend(df_inst[m].tolist())
            
    # formating function (& between value)
    def get_row(metric):
        return " & ".join(map(str, data[metric]))

    # different template for each number of instances
    
    if num_instances == 3:
        latex_code = f"""\\begin{{table}}[H]
    \\centering
    \\renewcommand{{\\arraystretch}}{{1.2}}
    \\resizebox{{\\linewidth}}{{!}}{{
    \\begin{{tabular}}{{|c | c | c c c c | c c c c | c c c c|}}
        \\hline
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{12}}{{c|}}{{\\textbf{{Evolutionary Alg. [10x]}}}} \\\\ \\cline{{3-14}}
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 1 (20x5)}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 2 (20x10)}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 3 (20x20)}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & & & & & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('SA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('SA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('SA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('SA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('SA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('SA_NFE_Avg')} \\\\ \\hline
        \\multicolumn{{2}}{{|c|}}{{\\textbf{{Best Known Value}}}} & {get_row('Best_Known_Value')} \\\\ \\hline
    \\end{{tabular}}
    }}
    \\caption{{\\textbf{{Results for 3 basic instances.}}}}
    \\label{{tab:ds_3}}
\\end{{table}}"""

    elif num_instances == 2:
        latex_code = f"""\\begin{{table}}[H]
    \\centering
    \\renewcommand{{\\arraystretch}}{{1.2}}
    \\resizebox{{\\linewidth}}{{!}}{{
    \\begin{{tabular}}{{|c | c | c c c c | c c c c |}}
        \\hline
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{8}}{{c|}}{{\\textbf{{Evolutionary Alg. [10x]}}}} \\\\ \\cline{{3-10}}
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Instance 4 (100x10)}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Instance 5 (100x20)}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('SA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('SA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('SA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('SA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('SA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('SA_NFE_Avg')} \\\\ \\hline
        \\multicolumn{{2}}{{|c|}}{{\\textbf{{Best Known Value}}}} & {get_row('Best_Known_Value')} \\\\ \\hline
    \\end{{tabular}}
    }}
    \\caption{{\\textbf{{Results for 2 medium instances.}}}}
    \\label{{tab:ds_2}}
\\end{{table}}"""

    elif num_instances == 1:
        latex_code = f"""\\begin{{table}}[H]
    \\centering
    \\renewcommand{{\\arraystretch}}{{1.2}}
    \\begin{{tabular}}{{|c | c | c c c c |}}
        \\hline
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Evolutionary Alg. [10x]}}}} \\\\ \\cline{{3-6}}
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Instance 6 (500x20)}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('SA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('SA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('SA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('SA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('SA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('SA_NFE_Avg')} \\\\ \\hline
        \\multicolumn{{2}}{{|c|}}{{\\textbf{{Best Known Value}}}} & {get_row('Best_Known_Value')} \\\\ \\hline
    \\end{{tabular}}
    \\caption{{\\textbf{{Results for 1 hard instance.}}}}
    \\label{{tab:ds_1}}
\\end{{table}}"""
    
    else:
        return "Error! Nb of instances must be 1, 2 or 3"

    return latex_code

code_latex = generate_latex_table("app/Results/SAParameters_Best_Cooling_Rate_Hard_Instance.csv")
print(code_latex)