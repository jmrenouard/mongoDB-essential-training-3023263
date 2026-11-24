# Run Application Driver Clients

This guide tells how to configure environment credentials and run the Chapter 7 Python, Node.js, or PHP scripts.

**Prerequisites:**

- You must have an active MongoDB server on `localhost:27017` with `admin` authentication enabled.
- You must install the runtime dependencies for your chosen language (`pymongo`/`python-dotenv`, `mongoose`/`dotenv`, or Composer `mongodb/mongodb`).

WARNING: DO NOT STORE REAL PRODUCTION PASSWORDS INSIDE TRACKED `.env` FILES. USE DISPOSABLE LOCAL CREDENTIALS ONLY.

CAUTION: CONFIRM YOUR TARGET `sample_data` COLLECTION NAMES BEFORE EXECUTION. THE PYTHON, NODEJS, AND PHP SCRIPTS INSERT TEST DOCUMENTS DIRECTLY.

## Procedure

1. Open your chosen driver directory under `7/python`, `7/nodejs`, or `7/php`.

2. Create a local `.env` file (`0600`) with database credentials for your language.

   ```bash
   umask 077
   printf 'DB_USER=naomi\nDB_PASSWORD=change_me\n' > .env
   ```

3. For PHP inside `7/php`, export `MDB_USER` and `MDB_PASSWORD` inside `.env` instead.

   ```bash
   umask 077
   printf 'MDB_USER=naomi\nMDB_PASSWORD=change_me\n' > .env
   ```

4. Install dependencies inside an isolated virtual environment or package directory.

5. Execute `python3 main.py`, `node index.js`, or `php index.php` inside that folder.

NOTE: The Python script writes to `testpython`, Node.js writes to `testnodejs`, and PHP writes to `testphp` inside `sample_data`.

## Verification

1. Confirm the script prints the inserted document ID and queried document cleanly.

2. Verify clean `git status` after lab runs.

   ```bash
   git status --short
   ```

## Rollback

Remove temporary virtual environments, local `.env` files, and test documents:

```bash
rm -f 7/python/.env 7/nodejs/.env 7/php/.env
```

## References

- Driver env variable matrix: [Chapters, Drivers, and Datasets](../03-reference/01-chapters-drivers-and-datasets.md)
- Driver and architecture overview: [Replica Set and Driver Architecture](../04-explanation/01-replica-set-and-driver-architecture.md)
