"""Fail closed on changes to the frozen inputs, including the manifest itself."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError("validation must run with Python assertions enabled")
EXPECTED = {
    "vendor/Weaver_Os/triadic_controls/ledger.py": "a967376fd3b1c2170e5ee7b2659e15d851db884b",
    "vendor/Weaver_Os/tools/verify_triad_ledger.py": "e20322297af3c19e7ad3c5c1c32da3717cfea757",
    "vendor/Weaver_Os/schemas/triad_event.schema.json": "93ce0918131167cb492592d5696d3e9fa4faf49f",
    "vendor/Weaver_Os/tests/test_triad_multiblock.py": "17b5caff6187d6346c1cc8071fe2f796df5f62d4",
    "vendor/Weaver_Os/triadic_controls/schemas/triad_event.schema.json": "93ce0918131167cb492592d5696d3e9fa4faf49f",
    "vendor/Weaver_Os/triadic_controls/__init__.py": "d0af3513344d2e8c68262c08cf7b3f819a5957f8",
    "vendor/Weaver_Os/tools/__init__.py": "f5776b428586daaf9195921d19ca52b24ba911cb",
    "contracts/HISTORY_CONTRACT_v1.md": "2be9388acc0b4f66ba9d791fdbb4a66a63adc94e",
    "contracts/V0_6_FORWARD_SIMULATION_CONTRACT.md": "034a8742eb93a2cbf830ead2162af6f98dce071a",
    "AlphaOmega/History.lean": "ff88532b1315dbc76ab36f130e533a62e9ef9529",
}


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def check_pins():
    manifest = json.loads((ROOT / "source-pins.json").read_text())
    assert manifest == {
        "abstract_base": "8ac7478c92d95b891bdff4d1c002dbfed5d43b85",
        "contract_commit": "e7fb0be1713ce6cba94166e2234ebb8d16025081",
        "concrete_commit": "ee725f7cf923d86d915900fc93ef2e3f6e5eef1c",
        "git_blobs": EXPECTED,
    }, "source manifest drift"
    for path, expected in EXPECTED.items():
        assert git_blob((ROOT / path).read_bytes()) == expected, f"source pin mismatch: {path}"
    for path, expected in {
        "HISTORY_CONTRACT_v1.md": EXPECTED["contracts/HISTORY_CONTRACT_v1.md"],
        "V0_6_FORWARD_SIMULATION_CONTRACT.md": EXPECTED["contracts/V0_6_FORWARD_SIMULATION_CONTRACT.md"],
        "AlphaOmega/History.lean": EXPECTED["AlphaOmega/History.lean"],
    }.items():
        assert git_blob((ROOT.parent / path).read_bytes()) == expected, f"root contract drift: {path}"
    return manifest


if __name__ == "__main__":
    check_pins()
    print(f"frozen source pins PASS: {len(EXPECTED)} blobs")
