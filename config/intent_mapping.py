"""
Intent mapping configuration for data retrieval

"""

import pandas as pd

def get_intent_mapping(trees_df, patches_df):
    return {
        'tree_recommendations': {
            'column_to_extract': trees_df['level_requirement'],
            'column_to_return': trees_df['tree_name']
        },
        'level_requirements': {
            'column_to_extract': trees_df['tree_name'],
            'column_to_return': trees_df['level_requirement']
        },
        'quest_requirements': {
            'column_to_extract': patches_df['location_simple'],
            'column_to_return': patches_df['patch_requirement']
        },
        'payment': {
            'column_to_extract': trees_df['tree_name'],
            'column_to_return': trees_df['payment_name']
        },
        'growth_time': {
            'column_to_extract': trees_df['tree_name'],
            'column_to_return': trees_df['growth_time_minutes']
        },
        'transportation': {
            'column_to_extract': patches_df['location_simple'],
            'column_to_return': patches_df['transportation_methods']
        }
    }