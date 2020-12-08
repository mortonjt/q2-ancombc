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
                'p_adj_method' : Str % Choices(['holm']),
                'zero_cut' : Float,
                'lib_cut' : Int,
                'group' : Str % Choices(['nation']),
                'struc_zero' : Bool,
                'neg_lb' : Bool,
                'tol' : Float,
                'max_iter' : Int,
                'conserve' : Bool,
                'alpha' : Float,
                'global_test' : Bool},
    outputs=[('differentials', FeatureData[Differential])],
    input_descriptions={
        'table': 'The feature table of abundances',
        'taxonomy': 'Taxonomy path.'
    },
    parameter_descriptions={
               'metadata': 'Sample Metadata path.',
               'formula':  'Regression formula to specify experimental conditions',
               'p_adj_method': '?',
               'zero_cut': '?',
               'lib_cut': '?',
               'group': '?',
               'struc_zero': '?',
               'neg_lb': '?',
               'tol': '?',
               'max_iter': '?',
               'conserve': '?',
               'alpha': '?',
               'global_test': '?'
    },
    output_descriptions={
        'differentials': 'The estimated per-feature differentials'
    }
)
