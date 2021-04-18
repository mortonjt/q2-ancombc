from qiime2.plugin import (
    Bool, Str, Int, Float, Choices, Citations, Plugin, Metadata
)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.feature_data import FeatureData, Differential, Taxonomy

import q2_ancombc
from q2_ancombc._method import ancombc


# TODO: will need to fix the version number
__version__ = '1.14.1'

plugin = Plugin(
    name='ancombc',
    version=__version__,
    website='https://github.com/mortonjt/q2-ancombc2',  # TODO: change this
    package='q2_ancombc',
    description=('Analysis Of Microbiomes with Bias Correction '),
    short_description='Plugin for differential abundance analysis.',
    citations=Citations.load('citations.bib', package='q2_ancombc')
)

plugin.methods.register_function(
    function=ancombc,  # TODO: may want a better name...
    name=('Analysis Of Microbiomes with Bias Correction'),
    description=('Performs log-ratio transformation and statistical testing'),
    inputs={'table': FeatureTable[Frequency],
            'taxonomy' : FeatureData[Taxonomy]},
    parameters={'metadata' : Metadata,
                'formula' : Str,
                'p_adj_method' : Str % Choices(['holm', 'hochberg', 'hommel', 
                                                'bonferroni', "BH", "BY", 
                                                "fdr", "none"]),
                'zero_cut' : Float,
                'lib_cut' : Int,
                'group' : Str,
                'struc_zero' : Bool,
                'neg_lb' : Bool,
                'tol' : Float,
                'max_iter' : Int,
                'conserve' : Bool,
                'alpha' : Float,
                # 'global_test' : Bool
                },
    outputs=[('differentials', FeatureData[Differential])],
    input_descriptions={
        'table': 'The feature table of abundances',
        'taxonomy': 'Taxonomy path.'
    },
    parameter_descriptions={
               'metadata': 'Sample Metadata path.',
               'formula':  ('One sided R-style regression formula to specify '
                            'experimental conditions'),
               'p_adj_method': 'The method for p-adjustment.',
               'zero_cut': ('A parameter for filtering zeros. Features with a'
                            ' proportion of zeros greater than 0 cut will be '
                            'excluded from the analysis.'),
               'min_sample_depth': ('the minimum sequencing depth to retain a'
                                    ' sample for testing'),
               'group': ('The grouping variable in the metadata. Required '
                         'for zero detection'),
               'struc_zero': ('Wether or not to detect structural zeros. '
                              'These are zeros that are biologically expected'
                              ' to be detected in one group but not another. '
                              'When detected, these taxa will be excluded '
                              'from further analysis. See Kual et al '
                              '(doi 10.3389/fmicb.2017.02114) for more '
                              'details.'),
               'neg_lb': ('Whether groups should be classified as structural'
                          ' zeros in the corresponding study group based on '
                          'an asymptotic lower bound.'),
               'tol': ('The convergence tolerance for the parameter '
                       'estimation algorithm'),
               'max_iter': ('The maximum number of iterations allowed '
                            'during parameter estimation optimizataion'),
               'conserve': ('When True, a conservative variance estimate will'
                            ' used for the test statitics. This should be '
                            'used when the sample size is small and/or the '
                            'number of differenitally abundant taxa is '
                            'believed to be large.'),
               'alpha': ('The level of significance in the multiple '
                         'hypothesis test'),
               # 'global_test': ''
    },
    output_descriptions={
        'differentials': 'The estimated per-feature differentials.'
    }
)
