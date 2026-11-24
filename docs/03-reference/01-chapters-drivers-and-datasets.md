# Chapters, Drivers, and Datasets

## Chapter Exercise Files

| Folder | Lesson Topics | Script Type | Key Targets / Notes |
| :--- | :--- | :--- | :--- |
| `1/` | macOS (`1_2.sh`) and Linux (`1_3.sh`, `1_4.sh`) installation of `m`, `mongod`, `mongosh`, `mongodb-database-tools` | Shell | Installs CLI tools and `mongoimport` |
| `2/` | Standalone `mongod` (`2_1.sh`), CLI replica set (`2_3.sh`), YAML config replica set (`2_4.sh`, `m1..m3.conf`), dataset import (`2_5.sh`) | Shell + `mongosh` | Ports `27017–27019`, replica set `mongodb-essentials-rs` |
| `3/` | Collections (`3_2.sh`), CRUD (`3_3.sh`), indexes (`3_4.sh`, `3_6.sh`) | `mongosh` | `blog.authors`, `lookup.records` |
| `4/` | Dot notation (`4_2.sh`), comparisons (`4_3.sh`), logical (`4_4.sh`), sort/skip/limit (`4_5.sh`), updates (`4_6.sh`), arrays (`4_7.sh`), transactions (`4_8.sh`), projections (`4_9.sh`), order workflow (`4_11.sh`) | `mongosh` | `sample_data`, `blog`, `order_app.orders` |
| `5/` | `$group` (`5_2.sh`), empty placeholder (`5_3.sh`), `$unwind` (`5_4.sh`), `$out`/`$merge` (`5_5.sh`), `$function` (`5_6.sh`), `$lookup` (`5_7.sh`), `explain` (`5_8.sh`), `$project` + `$out` (`5_10.sh`) | `mongosh` | `sample_data.inventory`, `movies`, `orders`, `purple`, `genres2000` |
| `6/` | Additional `blog.authors` insert (`6_3.sh`) | `mongosh` | `blog.authors` |
| `7/` | Python, Node.js, and PHP MongoDB driver quickstarts (`7_2.sh`–`7_4.sh`) | Shell + App code | Inserts into `sample_data.testpython`, `testnodejs`, `testphp` |

## Chapter 7 Driver Matrix

| Language | Entrypoint | Env Variables Read | Target Namespace |
| :--- | :--- | :--- | :--- |
| Python | `7/python/main.py` (`run_sample()`) | `DB_USER`, `DB_PASSWORD` | `sample_data.testpython` |
| Node.js | `7/nodejs/index.js` (`mongoose ^6.2.7`, `dotenv ^16.0.0`) | `DB_USER`, `DB_PASSWORD` | `sample_data.testnodejs` |
| PHP | `7/php/index.php` (`mongodb/mongodb`, `vlucas/phpdotenv`) | `MDB_USER`, `MDB_PASSWORD` | `sample_data.testphp` |

## Datasets

| File | Records | Target Collection (`sample_data`) | Sample Fields |
| :--- | ---: | :--- | :--- |
| `datasets/inventory.json` | `1000` | `inventory` | `_id`, `name`, `model`, `year`, `price`, `source`, `sale_frequency`, `variations` |
| `datasets/movies.json` | `1000` | `movies` | `title`, `director`, `actors`, `release_year`, `genres`, `gross`, `runtime_min`, `ratings` |
| `datasets/orders.json` | `1000` | `orders` | `_id`, `car_id`, `name_id`, `price`, `credit_card`, `credit_card_type` |
