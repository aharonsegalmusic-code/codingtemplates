API->
    """
gets orders from json
    adds status field
    set ot to "PREPARING"
    inserts to mogno
    sends to kafka
    to topic-pizza-orders
"""

text-processor (Preprocessor) ->
    """
listens to pizza-orders topic
    labels allergies
    cleans text (remove punctuation, UPPERCASE)
    sends cleaned data to cleaned-instructions topic
"""

enricher ->
    """
listens to cleaned-instructions topic
    analyzes pizza_type against closed lists
    checks redis cache (TTL 5s) for pizza metadata
    determines is_kosher, is_meat, is_dairy
    if not kosher -> BURNT
    adds insertion_time
    updates mongo
"""

kitchen ->
    """
listens to pizza-orders topic
    waits 15s
    updates status to DELIVERED
    deletes redis cache key
"""

risk_evaluator (Part 3 - NEW) ->
    """
pulls orders from mongo into pandas DataFrame
    matches clean_special_instructions vs common_allergens (substring)
    case-normalized matching (UPPERCASE)
    CANCELLED overrides all statuses
    adds update_time, allergens_matched
    logs to stdout
    caches dashboard metrics in redis (TTL 30s)
    runs every 10 seconds
"""

streamlit_dashboard (Part 3 - NEW) ->
    """
reads from mongo directly
    pie chart: status distribution + total orders
    bar chart: top 10 allergens (from CANCELLED)
    table: last 10 orders by update_time desc
    optional: redis cache for fast loads
"""
