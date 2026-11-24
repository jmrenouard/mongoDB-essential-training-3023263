# Replica Set Configs and Aggregation Reference

## Replica Set YAML Specifications (`2/m1.conf`–`2/m3.conf`)

| Config File | `net.bindIp` | `net.port` | `replication.replSetName` | `storage.dbPath` | `systemLog.path` | `security.authorization` |
| :--- | :--- | ---: | :--- | :--- | :--- | :--- |
| `2/m1.conf` | `localhost` | `27017` | `mongodb-essentials-rs` | `m1/db` | `m1/mongod.log` | `enabled` (`keyfile`) |
| `2/m2.conf` | `localhost` | `27018` | `mongodb-essentials-rs` | `m2/db` | `m2/mongod.log` | `enabled` (`keyfile`) |
| `2/m3.conf` | `localhost` | `27019` | `mongodb-essentials-rs` | `m3/db` | `m3/mongod.log` | `enabled` (`keyfile`) |

## Aggregation Pipeline Stages Covered in Chapter 5

| Stage | Scripts | Behavior / Option |
| :--- | :--- | :--- |
| `$match` | `5_4.sh`, `5_5.sh`, `5_10.sh` | Filters incoming documents early or after `$unwind` |
| `$project` | `5_6.sh`, `5_8.sh`, `5_10.sh` | Shapes projected fields and extracts `$year` or evaluates `$function` |
| `$unwind` | `5_4.sh`, `5_5.sh`, `5_10.sh` | Deconstructs `variations` and `genres` arrays |
| `$group` | `5_2.sh`, `5_10.sh` | Aggregates `$sum`, `$avg`, and `$push` by `$source` or `genres` |
| `$lookup` | `5_7.sh`, `5_8.sh` | Joins `orders.car_id` to `inventory._id` or `movies` year to `inventory.year` |
| `$out` / `$merge` | `5_5.sh`, `5_10.sh` | Writes full output (`genres2000`, `purple`) or merges incrementally (`whenMatched: "keepExisting"`, `whenNotMatched: "insert"`) |
