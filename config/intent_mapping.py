"""
Intent mapping configuration for data retrieval

"""

import pandas as pd

def get_intent_mapping(trees_df, patches_df):
    return {
        'tree_recommendations': {
            'lookup_column': trees_df['level_requirement'],
            'answer_column': trees_df['tree_name']
        },
        'tree_requirements': {
            'lookup_column': trees_df['tree_name'],
            'answer_column': trees_df['level_requirement']
        },
        'patch_requirements': {
            'lookup_column': patches_df['location_simple'],
            'answer_column': patches_df['patch_requirement']
        },
        'payment': {
            'lookup_column': trees_df['tree_name'],
            'answer_column': trees_df['payment_name']
        },
        'growth_time': {
            'lookup_column': trees_df['tree_name'],
            'answer_column': trees_df['growth_time_minutes']
        },
        'transportation': {
            'lookup_column': patches_df['location_simple'],
            'answer_column': patches_df['transportation_methods']
        },
        'list_regular_patches': {
            'filter_column': patches_df['is_fruit_patch'],
            'filter_value': False,
        },
        'list_fruit_patches': {
            'filter_column': patches_df['is_fruit_patch'],
            'filter_value': True,
        }
    }