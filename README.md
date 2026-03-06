
**代码风格格式化命令**
# 仅检查（不改代码）
ruff check .
black --check .

# 自动修复 + 格式化（会改代码）
ruff check . --fix
black .