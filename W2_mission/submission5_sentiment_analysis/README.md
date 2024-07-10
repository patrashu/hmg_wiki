### Install Library

```bash
pyenv local 3.10.14

poetry init
poetry config virtualenvs.in-project true --local
poetry env use python3.10
poetry run python --version
poetry install
```

### Add new library

```bash
poetry add <library_name> #  = pip install <library_name>
```

### koNLPy 활용 방법

- Okt

    ```bash
    poetry add konlpy
    brew install --cask oracle-java
    brew install --cask oracle-jdk
    ```

- Mecab

    ```bash
    brew install mecab mecab-ipadic
    poetry add mecab-python3
    ```