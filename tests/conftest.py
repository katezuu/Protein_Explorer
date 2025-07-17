import os
import sys

# Подкладываем корень репозитория в sys.path,
# чтобы тесты могли делать `import app` без ошибок.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)