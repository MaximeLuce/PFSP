import pandas as pd
import re

def extract_size(inst_name):
    match = re.search(r'tai(\d+)_(\d+)', str(inst_name))
    if match:
        return f"{match.group(1)}x{match.group(2)}"
    return inst_name.replace('_', '\\_') # Fallback si le nom est différent

def generate_latex_table_algos(csv_path):
    df = pd.read_csv(csv_path, sep=';')
    
    instances = df['Instance'].unique()
    num_instances = len(instances)
    
    latex_code = """\\begin{table}[H]
    \\centering
    \\renewcommand{\\arraystretch}{1.2}
    \\resizebox{\\linewidth}{!}{
    \\begin{tabular}{|c | c | c | c c c c | c | c c c c | c c c c|}
        \\hline
        & & & \\multicolumn{4}{c|}{\\textbf{Random Alg. [10k]}} & \\textbf{Greedy Alg.} & \\multicolumn{4}{c|}{\\textbf{Evolutionary Alg. [10x]}} & \\multicolumn{4}{c|}{\\textbf{Simulated Annealing [10x]}} \\\\
        
        \\textbf{Instance} & \\textbf{BKV} & \\textbf{Data} & \\textbf{best*} & \\textbf{worst} & \\textbf{avg} & \\textbf{std} & \\textbf{best*} & \\textbf{best*} & \\textbf{worst} & \\textbf{avg} & \\textbf{std} & \\textbf{best*} & \\textbf{worst} & \\textbf{avg} & \\textbf{std} \\\\ \\hline
"""

    for idx, inst in enumerate(instances):
        df_inst = df[df['Instance'] == inst]
        
        for i, (_, row) in enumerate(df_inst.iterrows()):
            
            inst_num = idx + 1
            size_str = extract_size(inst)
            bkv = row['Best_Known_Value']
            
            rs_best, rs_worst, rs_avg, rs_std = row['RS_Best'], row['RS_Worst'], row['RS_Avg'], row['RS_Std']
            gr_best = row['GR_Best']
            ea_best, ea_worst, ea_avg, ea_std = row['EA_Best'], row['EA_Worst'], row['EA_Avg'], row['EA_Std']
            sa_best, sa_worst, sa_avg, sa_std = row['SA_Best'], row['SA_Worst'], row['SA_Avg'], row['SA_Std']
            
            rs_time, gr_time, ea_time, sa_time = row['RS_Time(s)'], row['GR_Time(s)'], row['EA_Time(s)'], row['SA_Time(s)']
            rs_nfe, gr_nfe, ea_nfe, sa_nfe = row['RS_NFE'], row['GR_NFE'], row['EA_NFE_Avg'], row['SA_NFE_Avg']
            
            latex_code += f"        \\multirow{{3}}{{*}}{{\\makecell{{\\textbf{{{inst_num}}}\\\\ {size_str}}}}} & \\multirow{{3}}{{*}}{{{bkv}}} & \\textbf{{Score}} & {rs_best} & {rs_worst} & {rs_avg} & {rs_std} & {gr_best} & {ea_best} & {ea_worst} & {ea_avg} & {ea_std} & {sa_best} & {sa_worst} & {sa_avg} & {sa_std} \\\\ \\cdashline{{3-16}}\n"
            
            latex_code += f"        & & \\textbf{{Time}} & \\multicolumn{{4}}{{c|}}{{{rs_time} s}} & {gr_time} s & \\multicolumn{{4}}{{c|}}{{{ea_time} s}} & \\multicolumn{{4}}{{c|}}{{{sa_time} s}} \\\\ \\cdashline{{3-16}}\n"
            
            latex_code += f"        & & \\textbf{{NFE}} & \\multicolumn{{4}}{{c|}}{{{rs_nfe}}} & {gr_nfe} & \\multicolumn{{4}}{{c|}}{{{ea_nfe}}} & \\multicolumn{{4}}{{c|}}{{{sa_nfe}}} \\\\\n"
            
            latex_code += "        \\hline\n"

    latex_code += f"""    \\end{{tabular}}
    }}
    \\caption{{Determine the best population size for basic instances ({num_instances} instances analysed).}}
    \\label{{tab:ds_algos}}
\\end{{table}}"""

    return latex_code


code_latex = generate_latex_table_algos("app/Results/Final_Comparison_Final_Parameters_Hard_Instance.csv")
print(code_latex)