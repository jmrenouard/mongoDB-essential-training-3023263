# Tutorial 01: Explore Datasets and Replica Set Configs

In this tutorial, you inspect the three JSON datasets in `datasets/` and verify the `2/m1.conf`–`2/m3.conf` replica set YAML files without starting `mongod`.

## Prerequisites

- Python 3.10+ (`python --version`)
- Repository files under `datasets/` and `2/`

## Step 1 — Inspect Dataset Line Counts and First Documents

Count records and parse sample documents from `inventory.json`, `movies.json`, and `orders.json`:

```bash
python -B -c "import json, pathlib; [print(p.name, len(p.read_text(encoding='utf-8').splitlines()), list(json.loads(p.read_text(encoding='utf-8').splitlines()[0]).keys())) for p in sorted(pathlib.Path('datasets').glob('*.json'))]"
```

Expected output prints `1000` records for each of the 3 datasets (`inventory.json`, `movies.json`, `orders.json`).

## Step 2 — Verify Replica Set YAML Configurations

Parse `2/m1.conf`, `2/m2.conf`, and `2/m3.conf` with Python stdlib and confirm matching `mongodb-essentials-rs` names and `localhost` ports (`27017`–`27019`):

```bash
python -B -c "import pathlib, re; [print(p.name, dict(re.findall(r'^\s+(bindIp|port|replSetName):\s*(\S+)', p.read_text(encoding='utf-8'), re.M))) for p in sorted(pathlib.Path('2').glob('m*.conf'))]"
```

Expected output:

```text
m1.conf {'bindIp': 'localhost', 'port': '27017', 'replSetName': 'mongodb-essentials-rs'}
m2.conf {'bindIp': 'localhost', 'port': '27018', 'replSetName': 'mongodb-essentials-rs'}
m3.conf {'bindIp': 'localhost', 'port': '27019', 'replSetName': 'mongodb-essentials-rs'}
```

## Step 3 — Verify Shell Setup Scripts Syntax

Check POSIX syntax on the installation and import shell scripts:

```bash
for s in 1/1_2.sh 1/1_3.sh 1/1_4.sh 2/2_5.sh 7/7_2.sh 7/7_3.sh 7/7_4.sh; do bash -n "$s"; done
```

## Next Steps

- Test Python, Node.js, and PHP client code offline in [Tutorial 02](02-driver-clients-offline-lab.md).
- Configure live replica sets cleanly via [Initialize Replica Set and Import Datasets](../02-how-to-guides/01-initialize-replica-set-and-import-datasets.md).
- Inspect all chapter files in [Chapters, Drivers, and Datasets](../03-reference/01-chapters-drivers-and-datasets.md).
- Read design rationale in [Replica Set and Driver Architecture](../04-explanation/01-replica-set-and-driver-architecture.md).
