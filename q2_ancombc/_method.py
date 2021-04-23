import os
import warnings
import qiime2
import pandas as pd
import tempfile
import subprocess
import numpy as np


def run_commands(cmds, verbose=True):
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        proc = subprocess.run(cmd, check=True)
        # TODO: need to get global test at some point
        # for line in iter(proc.stdout.readline,''):
        #     if 'global_test' in line:
        #         return float(line.split(' ')[1])


# TODO: may want a better name ...
def ancombc(table: pd.DataFrame,
            metadata : qiime2.Metadata,
            formula : str,
            p_adj_method : str = "holm",
            zero_cut : float = 0.90,
            lib_cut : int = 1000,
            group : str = None,
            struc_zero : bool = True,
            neg_lb : bool = True,
            tol : float = 1e-5,
            max_iter : int = 100,
            conserve : bool = True,
            alpha : float = 0.05,
            # global_test : bool = True
            ) -> pd.DataFrame:

    # create series from the metadata column
    meta = metadata.to_dataframe()

    # checks for variable lengths and warns if there's only one value per
    # group. ANCOM will fail silently lateer because of it and thats harder
    # to debug 
    variables = np.unique(np.hstack([x.split("*") 
                                     for x in formula.split("+")]))
    variables = np.array([x.strip() for x in variables])
    var_counts = pd.DataFrame.from_dict(orient='index', data={
        var: {'n_groups': len(meta[var].dropna().unique())}
        for var in variables
        })
    if (var_counts['n_groups'] < 2).all():
        raise ValueError("None of the columns in the metadata satisfy "
                         "ANCOM-BC's requirements. All columns in the "
                         "formula should have more than one value.")


    # filter the metadata so only the samples present in the table are used
    # this also reorders it for the correct condition selection
    # it has to be re ordered for ancombc to correctly input the conditions
    meta = meta.loc[list(table.index)]

    # force reorder based on the data to ensure conds are selected correctly
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_name = '.' # debug
        biom_fp = os.path.join(temp_dir_name, 'input.biom.tsv')
        meta_fp = os.path.join(temp_dir_name, 'input.map.txt')
        summary_fp = os.path.join(temp_dir_name, 'output.summary.txt')
        # Need to manually specify header=True for Series (i.e. "meta"). It's
        # already the default for DataFrames (i.e. "table"), but we manually
        # specify it here anyway to alleviate any potential confusion.
        table.to_csv(biom_fp, sep='\t', header=True)
        meta.to_csv(meta_fp, sep='\t', header=True)

        if group is None:
            group = formula

        cmd = ['run_ancombc.R',
               biom_fp,                    # inp.abundances.path
               meta_fp,                    # inp.metadata.path
               formula,                    # formula
               p_adj_method,               # p_adj_method
               zero_cut,                   # zero_cut
               lib_cut,                    # lib_cut
               group,                      # group
               str(struc_zero).upper(),    # struc_zero
               str(neg_lb).upper(),        # neg_lb
               tol,                        # tol
               max_iter,                   # max_iter
               str(conserve).upper(),      # conserve
               alpha,                      # alpha
               'FALSE',                    # global -- temporary until better understood
               # str(global_test).upper(),   # global
               summary_fp                  # output
        ]
        cmd = list(map(str, cmd))

        try:
            global_test = run_commands([cmd])
            # TODO: not sure what to do about the `global_test` statistic
            # may need another custom q2 type for this...
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered while running ANCOMBC"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)

        summary = pd.read_csv(summary_fp, index_col=0)
        
        # del summary['diff_abn']  # remove this field for now ...
        # summary.index.name = "featureid"
        return summary
