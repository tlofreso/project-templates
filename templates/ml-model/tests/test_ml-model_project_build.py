from pathlib import Path
from typing import Sequence

import copier
import pytest

TEMPLATE_ROOT = Path(__file__).parent.parent / "project"

@pytest.fixture
def test_answers():
    return {
        "model_name": "Detect Anomaly",
        "model_slug": "detect_anomaly",
        "model_class": "DetectAnomaly"
    }

def _check_file_contents(
    file_path: Path,
    expected_strs: Sequence[str] = (),
    unexpect_strs: Sequence[str] = (),
    ):

    assert file_path.exists()
    file_content = file_path.read_text()
    for content in expected_strs:
        assert content in file_content
    for content in unexpect_strs:
        assert content not in file_content

@pytest.mark.parametrize("file,expected", [
    ("README.md", ["# Detect Anomaly"]),
    ("f_deployment/detect_anomaly.py", ['class DetectAnomaly']),
    ("f_deployment/app.py", ["from detect_anomaly import DetectAnomaly"]),
    ("f_deployment/app.py", ["@app.route('/api/model/detect_anomaly', methods=['POST'])"]),
    ("f_deployment/main.py", ['    model = DetectAnomaly()'])
    ])
def test_defaults_values(
    tmp_path: Path,
    test_answers: dict[str, str | bool],
    file,
    expected
):
    dst_path = tmp_path / "detect-anomaly"
    worker = copier.run_copy(
        src_path=str(TEMPLATE_ROOT),
        dst_path=dst_path,
        data=test_answers,
        defaults=True,
        unsafe=True,
    )
    assert worker is not None
    assert tmp_path.exists()
    _check_file_contents(
        dst_path / file,
        expected
    )