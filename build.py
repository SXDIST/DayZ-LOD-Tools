import ast
import zipfile
from pathlib import Path

ADDON_DIR = Path(__file__).parent
MODULE_NAME = "dayz_lod_tools"


def get_version():
    src = (ADDON_DIR / "__init__.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "bl_info" for t in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for k, v in zip(node.value.keys, node.value.values):
            if isinstance(k, ast.Constant) and k.value == "version":
                if isinstance(v, ast.Tuple):
                    return ".".join(str(e.value) for e in v.elts)
    return "unknown"


def collect_files():
    this = Path(__file__)
    for path in sorted(ADDON_DIR.rglob("*.py")):
        if path == this:
            continue
        rel = path.relative_to(ADDON_DIR)
        if "__pycache__" in rel.parts:
            continue
        yield path, rel


def main():
    version = get_version()
    out_dir = ADDON_DIR / "dist"
    out_dir.mkdir(exist_ok=True)
    zip_path = out_dir / f"{MODULE_NAME}-{version}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in collect_files():
            zf.write(path, Path(MODULE_NAME) / rel)

    print(f"Built: {zip_path}")


if __name__ == "__main__":
    main()
