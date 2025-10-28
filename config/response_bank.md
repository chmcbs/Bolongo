# Tree Recommendations
dataframe = trees_df
lookup_value = level_requirement
answer_value = tree_name

    - The best tree at level {lookup_value} Farming is {answer_value}.
    - The best trees at level {lookup_value} Farming are {answer_value} trees.
    - At level {lookup_value} Farming, you should grow {answer_value} trees.
    - At level {lookup_value} Farming, you should plant {answer_value} trees.
    - The best tree to grow at level {lookup_value} Farming is {answer_value}.
    - The best trees to grow at level {lookup_value} Farming are {answer_value} trees.

# Level Requirements
dataframe = trees_df
lookup_value = tree_name
answer_value = level_requirement

    - To grow {lookup_value} trees, you need level {answer_value} Farming.
    - To plant {lookup_value} trees, you need level {answer_value} Farming.  
    - Growing {lookup_value} trees requires level {answer_value} Farming.
    - Planting {lookup_value} trees requires level {answer_value} Farming.
    - {lookup_value} trees require level {answer_value} Farming to plant.
    - {lookup_value} trees require level {answer_value} Farming to grow.
    - {lookup_value} trees require level {answer_value} Farming.
    - Level {answer_value} Farming is required to grow {lookup_value} trees.
    - Level {answer_value} Farming is required to plant {lookup_value} trees.
    - You can grow {lookup_value} trees at level {answer_value} Farming.
    - You can plant {lookup_value} trees at level {answer_value} Farming.
    - You need level {answer_value} Farming to plant {lookup_value} trees.
    - You need level {answer_value} Farming to grow {lookup_value} trees.

# Payment
dataframe = trees_df
lookup_value = tree_name
answer_value = payment_name

    - {lookup_value} trees require {answer_value} as a protection payment.
    - To protect {lookup_value} trees, pay the farmer with {answer_value}.
    - The protection payment for {lookup_value} trees is {answer_value}.
    - Farmers require {answer_value} to protect {lookup_value} trees.
    - {lookup_value} trees can be protected by giving the farmer {answer_value}.
    - {lookup_value} trees can be protected with {answer_value}.

# Growth Time
dataframe = trees_df
lookup_value = tree_name
answer_value = growth_time_minutes

    - {lookup_value} trees take {answer_value} to grow.
    - {lookup_value} trees will be fully grown after {answer_value}.
    - {lookup_value} trees take {answer_value} until they are fully grown.
    - {lookup_value} trees will be fully grown {answer_value} after planting.
    - {lookup_value} trees will be ready {answer_value} after planting.