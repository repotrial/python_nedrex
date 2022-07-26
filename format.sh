black -l 120 nedrex
isort --profile black nedrex
flake8 --max-line-length=120 nedrex
pylint --max-line-length=120 nedrex
bandit -r nedrex
mypy --strict nedrex
