# Initialize Replica Set and Import Datasets

This guide tells how to launch the 3-node local replica set and import the course datasets.

**Prerequisites:**

- You must have `mongod`, `mongosh`, `mongoimport`, and `openssl` installed in `PATH`.
- You must confirm TCP ports `27017`, `27018`, and `27019` are free on `localhost`.

WARNING: NEVER COMMIT GENERATED `keyfile` SECRETS OR LAB DATA DIRECTORIES TO GIT. LEAKED KEYFILES ALLOW UNAUTHORIZED CLUSTER AUTHENTICATION.

CAUTION: KEEP `net.bindIp: localhost` INSIDE ALL `.conf` FILES DURING LABS. EXPOSED UNPROTECTED PORTS ALLOW REMOTE DATA ACCESS.

## Procedure

1. Open directory `2/` and create the shared `keyfile` with strict permissions (`0400`).

   ```bash
   cd 2 && openssl rand -base64 755 > keyfile && chmod 400 keyfile
   ```

2. Create the database directories for `m1`, `m2`, and `m3`.

   ```bash
   mkdir -p m1/db m2/db m3/db
   ```

3. Start all three `mongod` instances with `m1.conf`, `m2.conf`, and `m3.conf`.

   ```bash
   mongod -f m1.conf && mongod -f m2.conf && mongod -f m3.conf
   ```

4. Connect to `localhost:27017` and initiate `mongodb-essentials-rs` from `2_4.sh`.

5. Create the root `admin` user and authenticate before you import the datasets.

6. Open `datasets/` and import all three JSON files into `sample_data`.

   ```bash
   cd ../datasets && mongoimport --username="naomi" --authenticationDatabase="admin" --db=sample_data inventory.json
   mongoimport --username="naomi" --authenticationDatabase="admin" --db=sample_data movies.json
   mongoimport --username="naomi" --authenticationDatabase="admin" --db=sample_data orders.json
   ```

NOTE: Each `mongoimport` command prompts for the `naomi` user password configured during replica set setup.

## Verification

1. Check replica set status through `mongosh` on port `27017`.

   ```bash
   mongosh --port 27017 -u naomi --authenticationDatabase admin --eval "rs.status()"
   ```

2. Confirm `inventory`, `movies`, and `orders` collections contain `1000` records each.

   ```bash
   mongosh --port 27017 -u naomi --authenticationDatabase admin --eval "db.getSiblingDB('sample_data').getCollectionNames()"
   ```

## Rollback

Return to the repository root. Stop the three `mongod` instances and remove `keyfile`, `m*/db`, and log files:

```bash
cd ..
pkill -f "mongod -f m[123]\.conf" || true
rm -rf 2/keyfile 2/m1/db 2/m2/db 2/m3/db 2/m*/mongod.log
```

## References

- Config parameters and port table: [Replica Set Configs and Aggregation Reference](../03-reference/02-replica-set-and-aggregation-reference.md)
- Topology notes: [Replica Set and Driver Architecture](../04-explanation/01-replica-set-and-driver-architecture.md)
