# Kibana Setup Guide
# ──────────────────────────────────────────────────────────────
# After running `docker compose up`, open: http://localhost:5601
# ──────────────────────────────────────────────────────────────

## 1. Connect Kibana to the index

1. Go to: Stack Management → Index Management
   - You should see `pizza_orders` listed.

2. Go to: Stack Management → Data Views (formerly Index Patterns)
   - Click "Create data view"
   - Name: `pizza_orders`
   - Index pattern: `pizza_orders`
   - No time field (our data has no timestamp)
   - Click "Save data view to Kibana"

---

## 2. Explore data in Discover

1. Open the hamburger menu → Analytics → Discover
2. Select the `pizza_orders` data view
3. All 20 documents appear in the table
4. Try the search bar:
   - `special_instructions: allergy`   → full-text search
   - `is_delivery: true`               → boolean filter
   - `quantity >= 2`                   → range filter
   - `pizza_type: Pepperoni`           → exact match

---

## 3. Build a visualisation in Dashboard

1. Menu → Analytics → Dashboard → Create Dashboard
2. Click "Create visualization"

### Pie chart — orders by pizza type
- Chart type: Pie
- Slice by: pizza_type.keyword  (Terms aggregation)
- Size: count of records

### Bar chart — total quantity per type
- Chart type: Bar vertical
- X-axis: pizza_type.keyword (Terms aggregation)
- Y-axis: Sum of `quantity`

### Metric — delivery vs pickup
- Chart type: Metric
- Filter: is_delivery: true
- Count of records

3. Save dashboard as "Pizza Orders Overview"

---

## 4. Dev Tools (run raw ES queries)

1. Menu → Management → Dev Tools
2. This is a REST client built into Kibana.

Try these queries:

```
# Get all documents
GET pizza_orders/_search
{
  "query": { "match_all": {} }
}

# Search in special_instructions
GET pizza_orders/_search
{
  "query": {
    "match": { "special_instructions": "allergy" }
  }
}

# Count by pizza type (aggregation)
GET pizza_orders/_search
{
  "size": 0,
  "aggs": {
    "by_type": {
      "terms": { "field": "pizza_type.keyword" }
    }
  }
}

# Check the mapping
GET pizza_orders/_mapping

# Check index stats
GET pizza_orders/_stats
```

---

## 5. Useful Kibana URLs

| Page             | URL                                      |
|------------------|------------------------------------------|
| Discover         | http://localhost:5601/app/discover       |
| Dashboard        | http://localhost:5601/app/dashboards     |
| Dev Tools        | http://localhost:5601/app/dev_tools      |
| Index Management | http://localhost:5601/app/management/data/index_management |
