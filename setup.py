from setuptools import setup


base_pkgs = [
    "dash~=2.0",
    "dash-bootstrap-components~=1.0",
    "numpy~=1.21",
    "pandas~=1.2",
    "plotly~=5.4",
]

formatter_pkgs = [
    "black==21.11b1",
]

linter_pkgs = [
    "darglint~=1.8",
    "flake8~=3.9",
    "flake8-annotations~=2.7",
    "flake8-bandit~=2.1",
    "flake8-broken-line~=0.4",
    "flake8-bugbear~=19.8",
    "flake8-comprehensions~=3.7",
    "flake8-debugger~=3.2",
    "flake8-docstrings~=1.6",
    "flake8-eradicate~=0.4",
    "flake8-functions~=0.0",
    "flake8-polyfill~=1.0",
    "flake8-print~=4.0",
    "flake8_quotes~=2.1",
    "flake8-string-format~=0.3",
    "flake8-type-annotations~=0.1",
    "pydocstyle~=5.0",
]

notebook_pkgs = base_pkgs + [
    "ipykernel~=5.5",
    "ipython~=7.21",
    "ipywidgets~=7.6",
    "jupyter~=1.0",
    "jupyter-core~=4.6",
    "jupyter-dash~=0.4",
    "jupyter-packaging~=0.9",
    "jupyter-server~=1.6",
    "matplotlib~=3.3",
    "seaborn~=0.11",
]

test_pkgs = base_pkgs + [
    "pytest~=6.2",
    "pytest-cov~=3.0",
    "pytest-mock~=3.6",
]

dev_pkgs = (
    test_pkgs
    + linter_pkgs
    + formatter_pkgs
    + notebook_pkgs
    + [
        "pre-commit~=2.15",
    ]
)


user_pkgs = (
    base_pkgs
    + notebook_pkgs
)

setup(
    name="mouline_converter",
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
