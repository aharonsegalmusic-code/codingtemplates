```markdown
# FOCUSED_TODO.md (Super Short Checklist + Where to Look)

## Global rules (read once)
- **Only edit service files** → `TASK_00_SETUP.md` (Section **1 WELCOME**, **Rule**) + `STRATEGY_MONGODB_TASKS.md` (Philosophy)
- **Before coding each domain** read in this order: **Model → Schema → Route** → `TASK_00_SETUP.md` (Section **The Three Layers You Need to Understand**)
- **Task order is strict** → `STRATEGY_MONGODB_TASKS.md` (Section **Strict Ordering**)

---

## 0) Run the project
### Do
1. Start infra:
```bash
docker compose up -d
docker compose ps
```
2. Open Swagger:
- `http://localhost:8000/docs`

### Reference
- `TASK_00_SETUP.md` → Section **3. PROJECT SETUP** + **3c Verify Everything Is Running** + **3d Verify the API**

---

## 1) TASK_01_USER — implement User CRUD (in `apps/mongo_backend/services/user.py`)
### Do (implement in this order)
- **5.1 create_user**: normalize email, uniqueness check, build embedded docs, insert, emit `USER_CREATED`
- **5.2 get_user**: `User.get(PydanticObjectId)`, reject soft-deleted, raise `NotFoundError`
- **5.3 list_users**: filter `deleted_at == None`, skip/limit, cap limit at 100
- **5.4 update_user**: fetch via get_user, update only fields that are not None, save, emit `USER_UPDATED`
- **5.5 delete_user**: soft delete (`deleted_at = utc_now()`), save, emit `USER_DELETED`

### Quick verify (paste)
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{ "email": "consumer@example.com", "password": "MySecure1Pass", "display_name": "Test Consumer" }'
```

### Reference
- `TASK_01_USER.md` → Exercises **5.1 → 5.5** (plus **Verification** blocks)

---

## 2) TASK_02_SUPPLIER — implement Supplier CRUD (still in `apps/mongo_backend/services/user.py`)
### Do
- **5.1 create_supplier(body)**: normalize email, uniqueness check, build nested embedded objects (inside → out), insert, emit `SUPPLIER_CREATED`
- **5.2 get_supplier**: `Supplier.get(PydanticObjectId)`, no soft delete logic
- **5.3 list_suppliers**: find all, skip/limit, cap at 100
- **5.4 update_supplier**: multi-level partial update across nested objects, save, emit `SUPPLIER_UPDATED`
- **5.5 delete_supplier**: **hard delete** (`await supplier.delete()`), emit `SUPPLIER_DELETED`

### Quick verify (paste)
```bash
curl -X POST http://localhost:8000/suppliers \
  -H "Content-Type: application/json" \
  -d '{ "password": "SecurePass1!", "contact_info": { "primary_email": "sales@acme-electronics.com", "primary_phone": "+1-555-0100", "contact_person_name": "John Doe", "contact_person_title": "Sales Director" }, "company_info": { "legal_name": "Acme Electronics Inc", "business_address": { "street_address_1": "100 Commerce Blvd", "city": "New York", "state": "NY", "zip_code": "10001", "country": "US" } } }'
```

### Reference
- `TASK_02_SUPPLIER.md` → Exercises **5.1 → 5.5**

---

## 3) TASK_04_PRODUCT — implement ProductService (`apps/mongo_backend/services/product.py`)
### Do (in this order)
- **5.1 helper methods**:
  - `_build_topic_descriptions(items)`
  - `_build_stock_locations(items)`
  - `_build_variants(variants_dict)` (dict/map field)
- **5.2 create_product(supplier_id, body)**:
  - validate supplier exists
  - build product (DRAFT) using helpers
  - insert product
  - update supplier back-reference (`supplier.product_ids.append(product.id)` then `supplier.save()`)
  - emit `PRODUCT_CREATED`
- **5.3 get_product**: exclude `status == DELETED`
- **5.4 list_products**: base filter excludes deleted (`$ne`), optional status via `$in`, skip/limit + sort
- **5.5 update_product**: partial update (only fields not None), save, emit `PRODUCT_UPDATED`
- **5.6 delete_product**: set `status = DELETED`, save, remove product_id from supplier.product_ids (try/except), emit `PRODUCT_DELETED`
- **5.7 lifecycle methods**: publish / discontinue / out_of_stock / restore with status guards + `ValidationError`

### Quick verify (paste)
```bash
curl -s -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -H "X-Supplier-ID: SUPPLIER_ID" \
  -d '{ "name": "Wireless Headphones", "short_description": "Premium noise-cancelling headphones", "topic_descriptions": [ {"topic": "Features", "description": "Active noise cancellation with 30hr battery", "display_order": 1} ], "category": "electronics", "unit_type": "piece", "base_sku": "HDPH-001", "brand": "AudioTech", "base_price_cents": 9999, "images": [{"url": "https://example.com/img.jpg", "alt_text": "Headphones", "order": 0, "is_primary": true}], "shipping": {"free_shipping": true, "ships_from_country": "US"}, "variants": { "Black": { "variant_id": "v1", "variant_name": "Black", "attributes": [{"attribute_name": "Color", "attribute_value": "Black"}], "sku": "HDPH-001-BLK", "price_cents": 9999, "quantity": 50, "package_dimensions": {"width_cm": 20, "height_cm": 15, "depth_cm": 10, "weight_grams": 350} } }, "stock_locations": [ { "location_id": "wh-1", "location_name": "Main Warehouse", "city": "Austin", "zip_code": "73301", "country": "US", "quantity": 100 } ] }' | python3 -m json.tool
```

### Reference
- `TASK_04_PRODUCT.md` → Exercises **5.1 → 5.7** (method list is in **4. THE SERVICE CONTRACT**)

---

## 4) TASK_05_POST — implement PostService (`apps/mongo_backend/services/post.py`)
### Do
- **5.1 helpers**:
  - `_build_media(media_list)`
  - `_build_link_preview(lp)`
- **5.2 create_post(user_id, body)**:
  - call `author = await build_post_author(user_id)` (utility)
  - set `published_at = None` if draft else `utc_now()`
  - insert + emit `POST_CREATED`
- **5.3 get_post**: `Post.get()` + soft delete check (`deleted_at`)
- **5.4 list_posts** (feed):
  - filter: `deleted_at: None` AND `published_at != None`
  - optional filter: `author.user_id`
  - sort `-published_at`, skip/limit
- **5.5 update_post**: partial update, save, emit `POST_UPDATED`
- **5.6 delete_post**: soft delete (`deleted_at = utc_now()`), emit `POST_DELETED`
- **5.7 publish_post**: only if `published_at is None`, then set it, emit `POST_PUBLISHED`

### Quick verify (paste)
```bash
curl -s -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -H "X-User-ID: USER_ID" \
  -d '{ "community_id": "test-community", "post_type": "text", "text_content": "Hello world! My first post on this platform.", "is_draft": false }' | python3 -m json.tool
```

### Reference
- `TASK_05_POST.md` → Exercises **5.1 → 5.7**
- `TASK_05_POST.md` → Section **Important: build_post_author() Utility** (tells you to call it, not re-implement it)

---

## 5) TASK_07_ORDER — implement OrderService (`apps/mongo_backend/services/order.py`)
### Do
- **5.1**: first read utilities in `utils/order_utils.py` (understand what’s already done)
- **5.2 create_order(user_id, body)**:
  - `customer = await build_order_customer(user_id)` (utility)
  - for each item: fetch Product by id, require `status == ACTIVE`
  - use `build_order_item(i, product, variant_name, quantity)` (utility)
  - build `ShippingAddress` from request
  - set `order_number = generate_order_number()`
  - insert + emit `ORDER_CREATED`
- **5.3 get_order(order_id)**: `Order.get(PydanticObjectId)`
- **5.4 list_orders(user_id, skip, limit, status_filter)**:
  - query nested `customer.user_id`
  - optional status `$in` from comma-separated list
  - sort `-created_at`, skip/limit
- **5.5 cancel_order(order_id, reason)**:
  - only allow if status in (PENDING, CONFIRMED)
  - set status CANCELLED, save
  - emit `ORDER_CANCELLED` with minimal payload

### Reference
- `TASK_07_ORDER.md` → Exercises **5.1 → 5.5**
- `TASK_07_ORDER.md` → Section **Utility Functions (in utils/order_utils.py)** (use them, don’t rewrite them)

---

## 6) TASK_08_ANALYTICS — create new file + implement 8 pipelines (`apps/mongo_backend/services/analytics.py`)
### Do
1. Create the file with this starter (paste):
```python
""" Analytics Service - Aggregation pipeline exercises """
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from beanie import PydanticObjectId

from shared.models.order import Order
from shared.models.product import Product
from shared.models.user import User
from shared.models.post import Post
from shared.models.supplier import Supplier
from utils.datetime_utils import utc_now


class AnalyticsService:
    """ Analytics service using MongoDB aggregation pipelines.

    Each method implements a different aggregation pattern
    that answers a real business question.
    """

    # Exercise 1-8 methods go here
    pass
```
2. Implement the **8 methods** (pipelines are TODOs in the doc):
- revenue_by_supplier
- top_products_by_order_count
- orders_with_product_details (uses raw motor `$lookup`)
- post_engagement_report
- product_price_distribution
- daily_revenue
- top_product_categories
- platform_dashboard

### Reference
- `TASK_08_ANALYTICS.md` → Section **Create Your Service File** + **4. SERVICE CONTRACT** + **5. EXERCISES (1–8)**

---

## 7) TASK_09_KAFKA (Bonus) — infra + producer + consumer
### Do (only what the doc says you must implement)
- **Exercise 1**: docker-compose Kafka env (KRaft) + wire env vars into app + mysql-service
- **Exercise 2**: `shared/kafka/config.py` implement:
  - `from_env`
  - `to_producer_config` (returns dict shown in doc)
  - `to_consumer_config` (returns dict shown in doc)
- **Exercise 3**: `shared/kafka/topics.py` define Topic constants + EventType constants list
- **Exercise 4**: `apps/mongo_backend/kafka/producer.py` implement `send/emit/flush` + singleton
- **Exercise 5**: `apps/mysql_server/src/kafka/consumer.py` implement poll loop + handler routing

### Reference
- `TASK_09_KAFKA.md` → Exercises **1 → 5** (it lists exact files + exact expected behavior)

---
```

If you tell me **which task you are on right now** (example: “TASK_04, Exercise 5.2 create_product”), I can make an even smaller checklist for *only that task* (just the methods + exact reference lines you’ll keep open). Would you like me to do that for the specific exercise you’re currently implementing?