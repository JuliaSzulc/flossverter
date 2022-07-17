from setuptools import setup


base_pkgs = [
    "dash~=2.6",
    "dash-bootstrap-components~=1.2",
    "numpy~=1.23",
    "pandas~=1.4",
]

formatter_pkgs = [
    "black==22.6",
]

linter_pkgs = [
    "darglint~=1.8",
    "flake8~=4.0",
    "flake8-annotations~=2.9",
    "flake8-bandit~=3.0",
    "flake8-broken-line~=0.4",
    "flake8-bugbear~=22.7",
    "flake8-comprehensions~=3.10",
    "flake8-debugger~=4.1",
    "flake8-docstrings~=1.6",
    "flake8-eradicate~=1.2",
    "flake8-functions~=0.0",
    "flake8-print~=5.0",
    "flake8-quotes~=3.3",
    "flake8-string-format~=0.3",
]

notebook_pkgs = base_pkgs + [
    "jupyter",
    "jupyter-dash",
    "jupyter-packaging",
    "jupyter-server",
    "matplotlib",
    "seaborn",
]

test_pkgs = base_pkgs + [
    "pytest",
    "pytest-cov",
    "pytest-mock",
]

dev_pkgs = (
    test_pkgs
    + linter_pkgs
    + formatter_pkgs
    + notebook_pkgs
    + [
        "pre-commit",
    ]
)


user_pkgs = base_pkgs + notebook_pkgs

setup(
    name="flossverter",
    python_requires="~=3.9",
    extras_require={
        "base": base_pkgs,
        "dev": dev_pkgs,
        "formatter": formatter_pkgs,
        "linter": linter_pkgs,
        "notebook": notebook_pkgs,
        "test": test_pkgs,
        "user": user_pkgs,
    },
)
