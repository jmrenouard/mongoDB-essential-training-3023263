# Tutorial 02: Validate Multi-Language Driver Clients Offline

In this tutorial, you check syntax for the Python, Node.js, and PHP client demos (`7/`) and run `7/python/main.py` offline against a mocked `MongoClient`.

## Prerequisites

- Python 3.10+ (`python --version`)
- Optional `node` (`node --version`) and `php` (`php --version`) binaries for syntax validation

## Step 1 — Compile and Run the Mocked Python Driver Script

Check `7/python/main.py` syntax and execute `run_sample()` with in-memory `pymongo` and `dotenv` mocks:

```bash
python -B -m py_compile 7/python/main.py
python -B -m unittest tests/test_docs_tutorials_howtos.py -v
```

Expected output reports all offline unit tests passing (`OK`).

## Step 2 — Check Node.js and PHP Syntax (When Runtimes Exist)

Run built-in parser checks on `7/nodejs/index.js` and `7/php/index.php` without executing database queries:

```bash
node --check 7/nodejs/index.js
php -l 7/php/index.php
```

Expected PHP output:

```text
No syntax errors detected in 7/php/index.php
```

## Next Steps

- Run live driver scripts against a local MongoDB instance via [Run Application Driver Clients](../02-how-to-guides/02-run-application-driver-clients.md).
- Compare driver env variables in [Replica Set Configs and Driver Specs](../03-reference/02-replica-set-and-aggregation-reference.md).
- Review CRUD and aggregation pipelines in [CRUD, Indexing, and Aggregation Design](../04-explanation/02-crud-indexing-and-aggregation-design.md).
