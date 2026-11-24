"""Automated offline tests for mongoDB-essential-training-3023263 docs, scripts, drivers, and configs."""

from __future__ import annotations

import importlib.util
import json
import os
import py_compile
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
QUADRANTS = ("01-tutorials", "02-how-to-guides", "03-reference", "04-explanation")

PURE_SHELL_SCRIPTS = (
    "1/1_2.sh",
    "1/1_3.sh",
    "1/1_4.sh",
    "2/2_5.sh",
    "7/7_2.sh",
    "7/7_3.sh",
    "7/7_4.sh",
)

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
MERMAID_HEAD_RE = re.compile(
    r"^\s*(?:flowchart(?:-elk)?(?:\s+(?:TD|TB|LR|RL|BT))?|graph\s+(?:TD|TB|LR|RL|BT)|"
    r"sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|gantt|pie|gitGraph|"
    r"mindmap|timeline|xychart-beta)\b"
)
BARE_ARROW_RE = re.compile(r"(?:(?<![<!])-->|(?<!<!)<--|(?<![=])==>|─+>|▼|▲)")
BOX_CHAR_RE = re.compile(r"[┌┐┘╔╗╚╝]|\+[-=]{2,}\+")
FORBIDDEN_HOWTO_MODAL_RE = re.compile(
    r"\b(?:should|would|may|might|shall|ought|can't|don't|won't|isn't|aren't|doesn't|didn't)\b",
    re.IGNORECASE,
)
FRENCH_LEAK_RE = re.compile(
    r"\b(?:tutoriels|guides\s+pratiques|explications|étapes|erreur|succès|fichiers)\b",
    re.IGNORECASE,
)


def _iter_repo_markdowns() -> list[Path]:
    skip = {".git", "node_modules", ".venv", "__pycache__"}
    out: list[Path] = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in skip)
        for name in sorted(names):
            if name.lower().endswith(".md"):
                out.append(Path(base) / name)
    return out


def _split_prose_and_code(text: str) -> tuple[list[tuple[str, bool]], list[tuple[str, str, int, str]]]:
    blocks: list[tuple[str, str, int, str]] = []
    prose: list[tuple[str, bool]] = []
    para_lines: list[str] = []
    in_fence = False
    fchar = ""
    flen = 0
    findent = ""
    flang = ""
    fline = 0
    fbody: list[str] = []

    def flush_para() -> None:
        if para_lines:
            joined = " ".join(para_lines).strip()
            if joined:
                prose.append((joined, joined.upper().startswith("NOTE:")))
            para_lines.clear()

    for idx, line in enumerate(text.splitlines(), start=1):
        if not in_fence:
            m = FENCE_RE.match(line)
            if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
                flush_para()
                in_fence = True
                findent = m.group(1)
                fchar = m.group(2)[0]
                flen = len(m.group(2))
                flang = m.group(3).strip().split()[0].lower() if m.group(3).strip() else ""
                fline = idx
                fbody = []
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("|") or re.match(r"^[-*_]{3,}$", stripped):
                flush_para()
                continue
            cleaned = re.sub(r"^(?:>\s*|[-*+]\s+|\d+\.\s+)", "", stripped)
            para_lines.append(cleaned)
        else:
            if re.match(rf"^[ \t]*{re.escape(fchar)}{{{flen},}}[ \t]*$", line):
                blocks.append((findent, flang, fline, "\n".join(fbody)))
                in_fence = False
            else:
                fbody.append(line)
    flush_para()
    return prose, blocks


def _find_mmdc() -> str | None:
    if found := shutil.which("mmdc"):
        return found
    candidate = Path("/home/jmren/node_modules/.bin/mmdc")
    return str(candidate) if candidate.is_file() else None


class TestEssentialTrainingDocsAndLabs(unittest.TestCase):
    """Validate Diataxis docs, STE rules, Mermaid diagrams, JSON/YAML data, and multi-runtime syntax."""

    def test_diataxis_structure_links_and_english_isolation(self) -> None:
        """Check 4-quadrant tree, genre boundaries, valid README URLs, relative links, and English isolation."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[lil-course-url]: https://www.linkedin.com/learning/mongodb-essential-training", readme)
        self.assertNotIn("](/datasets/)", readme)
        self.assertIn("datasets/inventory.json", readme)

        self.assertTrue((DOCS_DIR / "index.md").is_file())
        for q in QUADRANTS:
            qdir = DOCS_DIR / q
            self.assertTrue((qdir / "index.md").is_file())
            self.assertGreaterEqual(len([p for p in qdir.glob("*.md") if p.name != "index.md"]), 2)

        for page in sorted((DOCS_DIR / "01-tutorials").glob("*.md")):
            if page.name != "index.md":
                txt = page.read_text(encoding="utf-8")
                self.assertIn("## Prerequisites", txt)
                self.assertIn("## Next Steps", txt)

        for page in sorted((DOCS_DIR / "03-reference").glob("*.md")):
            txt = page.read_text(encoding="utf-8")
            for banned in ("In this tutorial", "Let's ", "Step 1"):
                self.assertNotIn(banned, txt)

        for page in sorted((DOCS_DIR / "04-explanation").glob("*.md")):
            txt = page.read_text(encoding="utf-8")
            for banned in ("## Step 1", "## Rollback", "## Prerequisites"):
                self.assertNotIn(banned, txt)

        for md in [ROOT / "README.md", *sorted(DOCS_DIR.rglob("*.md"))]:
            txt = md.read_text(encoding="utf-8")
            self.assertIsNone(FRENCH_LEAK_RE.search(txt))
            _, blocks = _split_prose_and_code(txt)
            no_code = txt
            for _, _, _, body in blocks:
                if body:
                    no_code = no_code.replace(body, "")
            for raw in LINK_RE.findall(no_code):
                target = raw.strip().strip("<>").split()[0]
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path_part = target.split("#", 1)[0]
                if path_part:
                    self.assertTrue((md.parent / path_part).resolve().exists(), f"Broken link in {md.name}: {raw}")

    def test_ste_procedural_compliance(self) -> None:
        """Enforce ASD-STE100 procedural structure and length limits under docs/02-how-to-guides."""
        for page in sorted((DOCS_DIR / "02-how-to-guides").glob("*.md")):
            txt = page.read_text(encoding="utf-8")
            if page.name != "index.md":
                for sec in ("**Prerequisites:**", "## Procedure", "## Verification", "## Rollback"):
                    self.assertIn(sec, txt)
                self.assertTrue("WARNING:" in txt or "CAUTION:" in txt)
            prose, _ = _split_prose_and_code(txt)
            for para, is_note in prose:
                self.assertNotIn(";", para)
                self.assertFalse(FORBIDDEN_HOWTO_MODAL_RE.search(para))
                limit = 25 if is_note else 20
                for sent in [s.strip() for s in re.split(r"(?<=[.!?])\s+", para) if s.strip()]:
                    words = re.sub(r"`[^`]+`", "code", sent).split()
                    self.assertLessEqual(len(words), limit, f"Sentence > {limit}w in {page.name}: {sent}")

    def test_mermaid_diagrams_valid_and_zero_ascii_diagrams(self) -> None:
        """Confirm zero ASCII box-arrow diagrams and valid column-0 Mermaid diagrams via mmdc."""
        mmdc = _find_mmdc()
        mermaid_blocks: list[tuple[str, int, str]] = []
        for md in _iter_repo_markdowns():
            rel = md.relative_to(ROOT).as_posix()
            _, blocks = _split_prose_and_code(md.read_text(encoding="utf-8"))
            for indent, lang, line, body in blocks:
                if lang == "mermaid":
                    self.assertEqual(indent, "", f"Indented mermaid in {rel}:{line}")
                    mermaid_blocks.append((rel, line, body))
                else:
                    self.assertIsNone(MERMAID_HEAD_RE.match(body))
                    is_tree = bool(re.search(r"[├└]─", body)) and not BARE_ARROW_RE.search(body) and not BOX_CHAR_RE.search(body)
                    if not is_tree:
                        self.assertFalse(bool(BOX_CHAR_RE.search(body)) and bool(BARE_ARROW_RE.search(body)))

        self.assertGreaterEqual(len(mermaid_blocks), 2)
        if mmdc is not None:
            with tempfile.TemporaryDirectory() as tmpdir:
                for idx, (rel, line, code) in enumerate(mermaid_blocks):
                    in_f = Path(tmpdir) / f"d_{idx}.mmd"
                    out_f = Path(tmpdir) / f"d_{idx}.svg"
                    in_f.write_text(code + "\n", encoding="utf-8")
                    res = subprocess.run([mmdc, "-i", str(in_f), "-o", str(out_f)], capture_output=True, text=True, timeout=60)
                    self.assertEqual(res.returncode, 0, f"mmdc failed on {rel}:{line}: {res.stderr}")

    def test_datasets_configs_and_exercise_fixes(self) -> None:
        """Verify 3x1000 JSON datasets, replica set configs, and chapter snippet syntax fixes."""
        for ds in ("inventory.json", "movies.json", "orders.json"):
            lines = [ln for ln in (ROOT / "datasets" / ds).read_text(encoding="utf-8").splitlines() if ln.strip()]
            self.assertEqual(len(lines), 1000)
            json.loads(lines[0])
            json.loads(lines[-1])

        for idx, port in enumerate((27017, 27018, 27019), start=1):
            conf_txt = (ROOT / "2" / f"m{idx}.conf").read_text(encoding="utf-8")
            self.assertIn("bindIp: localhost", conf_txt)
            self.assertIn(f"port: {port}", conf_txt)
            self.assertIn("replSetName: mongodb-essentials-rs", conf_txt)

        s2_3 = (ROOT / "2" / "2_3.sh").read_text(encoding="utf-8")
        self.assertNotIn("\u201c", s2_3)
        self.assertIn('"mongodb://localhost:27017"', s2_3)

        s2_4 = (ROOT / "2" / "2_4.sh").read_text(encoding="utf-8")
        self.assertIn('"mongodb-essentials-rs"', s2_4)
        self.assertNotIn("rs.add", s2_4)

        self.assertIn("db.authors.createIndex", (ROOT / "3" / "3_4.sh").read_text(encoding="utf-8"))
        self.assertIn('{ "variations.variation": "Green" },', (ROOT / "4" / "4_4.sh").read_text(encoding="utf-8"))
        self.assertNotIn("db.oders", (ROOT / "4" / "4_11.sh").read_text(encoding="utf-8"))
        self.assertIn('whenMatched: "keepExisting",', (ROOT / "5" / "5_5.sh").read_text(encoding="utf-8"))

        pkg = json.loads((ROOT / "7" / "nodejs" / "package.json").read_text(encoding="utf-8"))
        self.assertIn("mongoose", pkg["dependencies"])
        node_src = (ROOT / "7" / "nodejs" / "index.js").read_text(encoding="utf-8")
        self.assertIn("mongodb://localhost:27017", node_src)
        self.assertNotIn("0.0.0.0:27017", node_src)

    def test_tutorial_01_commands_execute_with_stdlib_and_howto_rollback_matches(self) -> None:
        """Execute Tutorial 01 Step 1 and Step 2 stdlib commands and verify How-To 01 rollback paths."""
        tut_path = DOCS_DIR / "01-tutorials" / "01-datasets-and-configs-lab.md"
        _, tut_blocks = _split_prose_and_code(tut_path.read_text(encoding="utf-8"))
        bash_blocks = [body.strip() for _, lang, _, body in tut_blocks if lang == "bash"]
        text_blocks = [body.strip() for _, lang, _, body in tut_blocks if lang == "text"]
        self.assertGreaterEqual(len(bash_blocks), 2)
        self.assertGreaterEqual(len(text_blocks), 1)

        step_outputs: list[str] = []
        for cmd in bash_blocks[:2]:
            tokens = shlex.split(cmd)
            self.assertEqual(tokens[:3], ["python", "-B", "-c"])
            self.assertNotIn("yaml", tokens[3])
            res = subprocess.run(
                [sys.executable, *tokens[1:]],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
            self.assertEqual(res.returncode, 0, f"Tutorial 01 command failed: {res.stderr}")
            step_outputs.append(res.stdout.strip())

        for ds in ("inventory.json 1000", "movies.json 1000", "orders.json 1000"):
            self.assertIn(ds, step_outputs[0])
        self.assertEqual(step_outputs[1], text_blocks[0])

        howto = (DOCS_DIR / "02-how-to-guides" / "01-initialize-replica-set-and-import-datasets.md").read_text(
            encoding="utf-8"
        )
        rollback_section = howto.split("## Rollback", 1)[1]
        self.assertIn("cd ..", rollback_section)
        self.assertIn(r'pkill -f "mongod -f m[123]\.conf" || true', rollback_section)
        self.assertIn("rm -rf 2/keyfile 2/m1/db 2/m2/db 2/m3/db 2/m*/mongod.log", rollback_section)

    def test_multi_runtime_driver_syntax_and_mocked_python_execution(self) -> None:
        """Verify py_compile + mocked Python driver flow plus bash/node/php syntax checks when available."""
        with tempfile.TemporaryDirectory() as tmpdir:
            py_src = ROOT / "7" / "python" / "main.py"
            py_compile.compile(str(py_src), cfile=str(Path(tmpdir) / "main.pyc"), doraise=True)

        fake_coll = MagicMock()
        fake_coll.insert_one.return_value = types.SimpleNamespace(inserted_id="oid-123")
        fake_coll.find_one.return_value = {"author": "Naomi", "message": "hello world!"}
        fake_client_inst = {"sample_data": {"testpython": fake_coll}}
        pymongo_mod = types.ModuleType("pymongo")
        pymongo_mod.MongoClient = MagicMock(return_value=fake_client_inst)
        dotenv_mod = types.ModuleType("dotenv")
        dotenv_mod.load_dotenv = MagicMock()

        with patch.dict(sys.modules, {"pymongo": pymongo_mod, "dotenv": dotenv_mod}):
            spec = importlib.util.spec_from_file_location("ch7_python_main", ROOT / "7" / "python" / "main.py")
            assert spec and spec.loader
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # Importing does not auto-connect; calling run_sample exercises the mocked MongoClient.
            pymongo_mod.MongoClient.assert_not_called()
            doc_id, found = mod.run_sample()
            self.assertEqual(doc_id, "oid-123")
            self.assertEqual(found["author"], "Naomi")
            pymongo_mod.MongoClient.assert_called_once()

        if os.name == "posix" and shutil.which("bash"):
            for script in PURE_SHELL_SCRIPTS:
                res = subprocess.run(["bash", "-n", str(ROOT / script)], capture_output=True, text=True, timeout=15)
                self.assertEqual(res.returncode, 0, f"bash -n failed for {script}: {res.stderr}")
            if node := shutil.which("node"):
                n_res = subprocess.run([node, "--check", str(ROOT / "7" / "nodejs" / "index.js")], capture_output=True, text=True, timeout=15)
                self.assertEqual(n_res.returncode, 0, n_res.stderr)
            if php := shutil.which("php"):
                p_res = subprocess.run([php, "-l", str(ROOT / "7" / "php" / "index.php")], capture_output=True, text=True, timeout=15)
                self.assertEqual(p_res.returncode, 0, p_res.stderr)


if __name__ == "__main__":
    unittest.main()
