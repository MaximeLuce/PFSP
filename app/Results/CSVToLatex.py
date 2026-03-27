import pandas as pd


def generate_latex_table(csv_path):
    # reading CSV file...
    df = pd.read_csv(csv_path, sep=';')
    
    # recuperation of uniques instances (preserving order)
    instances = df['Instance'].unique()
    num_instances = len(instances)
    
    # formating data: extracting interesting columns
    metrics = ['EA_Best', 'EA_Worst', 'EA_Avg', 'EA_Std', 'EA_Time(s)', 'EA_NFE_Avg']
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
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 1 ({instances[0]})}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 2 ({instances[1]})}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 3 ({instances[2]})}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & & & & & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('EA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('EA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('EA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('EA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('EA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('EA_NFE_Avg')} \\\\ \\hline
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
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 1 ({instances[0]})}}}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 2 ({instances[1]})}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('EA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('EA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('EA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('EA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('EA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('EA_NFE_Avg')} \\\\ \\hline
    \\end{{tabular}}
    }}
    \\caption{{\\textbf{{Results for 2 medium instances.}}}}
    \\label{{tab:ds_2}}
\\end{{table}}"""

    elif num_instances == 1:
        latex_code = f"""\\begin{{table}}[H]
    \\centering
    \\renewcommand{{\\arraystretch}}{{1.2}}
    \\resizebox{{0.7\\linewidth}}{{!}}{{
    \\begin{{tabular}}{{|c | c | c c c c |}}
        \\hline
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Evolutionary Alg. [10x]}}}} \\\\ \\cline{{3-6}}
        \\multicolumn{{2}}{{|c|}}{{}} & \\multicolumn{{4}}{{c|}}{{\\textbf{{Inst. 1 ({instances[0]})}}}} \\\\ \\hline
        \\multirow{{2}}{{*}}{{\\textbf{{Data}}}} & \\multirow{{2}}{{*}}{{\\diagbox[width=3.5cm, height=1.2cm]{{\\textbf{{Stat.}}}}{{\\textbf{{Case n°}}}}}} & \\multirow{{2}}{{*}}{{\\textbf{{1}}}} & \\multirow{{2}}{{*}}{{\\textbf{{2}}}} & \\multirow{{2}}{{*}}{{\\textbf{{3}}}} & \\multirow{{2}}{{*}}{{\\textbf{{4}}}} \\\\
        & & & & & \\\\ \\hline
        \\multirow{{4}}{{*}}{{\\textbf{{Score}}}} 
        & \\textbf{{best*}} & {get_row('EA_Best')} \\\\
        & \\textbf{{worst}} & {get_row('EA_Worst')} \\\\
        & \\textbf{{avg}}   & {get_row('EA_Avg')} \\\\
        & \\textbf{{std}}   & {get_row('EA_Std')} \\\\ \\hline
        \\textbf{{Time}} & \\textbf{{second (s)}} & {get_row('EA_Time(s)')} \\\\ \\hline
        \\textbf{{NFE}} & \\textbf{{number}} & {get_row('EA_NFE_Avg')} \\\\ \\hline
    \\end{{tabular}}
    }}
    \\caption{{\\textbf{{Results for 1 hard instance.}}}}
    \\label{{tab:ds_1}}
\\end{{table}}"""
    
    else:
        return "Erreur: Le nombre d'instances dans le CSV n'est pas géré (doit être 1, 2 ou 3)."

    return latex_code

# --- EXÉCUTION ---
# Remplace 'ton_fichier.csv' par le nom de ton fichier.
code_latex = generate_latex_table("app/Results/EAParameters_Table1.csv")
print(code_latex)