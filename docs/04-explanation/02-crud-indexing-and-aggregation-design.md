# CRUD, Indexing, and Aggregation Design

Chapters `3` through `5` contrast ad-hoc queries, schema indexing, multi-document ACID transactions, and aggregation pipeline stages.

## Query and Pipeline Trade-Offs

- **Schema Flexibility vs Consistency (`3/` & `4/`):** `4_11.sh` embeds `items`, `user`, and `restaurant` subdocuments directly inside `order_app.orders`, avoiding joins during checkout reads while requiring explicit updates if embedded attributes change (`$mul`, `$set`, `$unset`). Multi-document transactions (`4_8.sh`) require replica set oplog support (`mongodb-essentials-rs`), which is why Chapter `2` sets up a 3-node replica set rather than keeping standalone `2_1.sh`.
- **Filtering Placement (`5_4.sh` & `5_8.sh`):** Placing `$match` before `$unwind` reduces the working set multiplied across array elements, whereas filtering only after `$unwind` scans unneeded elements first. `5_8.sh` uses `.explain("executionStats")` around `$lookup` to surface join scan costs between `movies` and `inventory`.
- **Materializing Output (`$out` vs `$merge` in `5_5.sh`):** `$out` atomically replaces the target collection (`purple`, `genres2000`), while `$merge` supports incremental updates (`whenMatched: "keepExisting"`, `whenNotMatched: "insert"`).
