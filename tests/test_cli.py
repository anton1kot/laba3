import subprocess
import sys
from pathlib import Path


def test_cli_stderr():
    # ошибка пользователя должна вывести ошибку в stderr и завершиться с кодом 2
    result = subprocess.run(
        [sys.executable, '-m', 'books_catalog', 'get', '--id', 'BK-999'],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        check=False,
        text=True
    )
    assert result.returncode == 2


def test_cli_help_exits_with_0():
    # --help должен показывать справку и завершаться с кодом 0
    result = subprocess.run(
        [sys.executable, '-m', 'books_catalog', '--help'],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=True
    )
    assert result.returncode == 0
    # проверяем, что вывод не пустой (там должна быть справка)
    assert len(result.stdout.strip()) > 0
