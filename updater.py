import re
import tempfile
import urllib.request
import urllib.error

REPO = "SXDIST/DayZ-LOD-Tools"
_RAW_URL = f"https://raw.githubusercontent.com/{REPO}/main/__init__.py"
_ZIP_URL = f"https://github.com/{REPO}/archive/refs/heads/main.zip"

status = 'UNKNOWN'         # 'UNKNOWN' | 'UP_TO_DATE' | 'AVAILABLE' | 'ERROR'
latest_version_str = ""
error_message = ""
_local_version = (0, 0, 0)


def set_local_version(version_tuple):
    global _local_version
    _local_version = version_tuple


def _parse_version(source):
    match = re.search(r'"version"\s*:\s*\((\d+),\s*(\d+),\s*(\d+)\)', source)
    if match:
        return tuple(int(x) for x in match.groups())
    return None


def check():
    global status, latest_version_str, error_message
    try:
        with urllib.request.urlopen(_RAW_URL, timeout=10) as response:
            source = response.read().decode('utf-8')
        remote_ver = _parse_version(source)
        if remote_ver is None:
            status = 'ERROR'
            error_message = "Could not parse remote version"
            return
        latest_version_str = ".".join(str(x) for x in remote_ver)
        status = 'AVAILABLE' if remote_ver > _local_version else 'UP_TO_DATE'
        error_message = ""
    except Exception as e:
        status = 'ERROR'
        error_message = str(e)[:64]


def download_and_install():
    """Download the main branch zip. Returns (success, path_or_error_str)."""
    try:
        tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        tmp.close()
        urllib.request.urlretrieve(_ZIP_URL, tmp.name)
        return True, tmp.name
    except Exception as e:
        return False, str(e)[:128]
