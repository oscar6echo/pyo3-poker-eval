# Poker Eval

## Overview

Python [PyO3](https://pyo3.rs/) wrapper package over Rust crate [poker_eval](https://crates.io/crates/poker_eval).  
Cross compilation "linux2win" is done with [cross](https://github.com/cross-rs/cross).  

## Build

Commands:

```sh
# prerequisite
mm activate work
pip install -U build

# dev install
pip install -e .

# watch 
cargo watch --watch rust -- pip install -e .

# test
pytest

# install
pip install .

# build - native: linux
unset CARGO
unset CARGO_BUILD_TARGET
unset PYO3_CROSS_LIB_DIR
unset PYO3_CROSS_PYTHON_VERSION
unset DIST_EXTRA_CONFIG

python -m build

# build - cross to windows
cargo install cross

export CARGO=cross
export CARGO_BUILD_TARGET=x86_64-pc-windows-gnu
export DIST_EXTRA_CONFIG=/tmp/build-opts.cfg

# set wheel suffix
echo -e "[bdist_wheel]\nplat_name=pc_windows_gnu_x86_64" > $DIST_EXTRA_CONFIG

# image used by cross
docker build -t cross-pyo3:x86_64-pc-windows-gnu .

python -m build
```

This produced wheels for linux and windows:

```sh
ls -1  dist
pyo3_poker_eval-0.1.0-cp310-cp310-linux_x86_64.whl
pyo3_poker_eval-0.1.0-cp310-cp310-pc_windows_gnu_x86_64.whl
pyo3_poker_eval-0.1.0.tar.gz
```

## Publish

Commands:

```sh
# prerequisite
mm activate work
pip install -U twine

twine check dist/*

# assuming .pypirc configured
twine upload dist/*
```

## Install

Commands:

```sh
############ TBD - no ready yet
pip install pyo3_poker_eval
```

## Ref

Python packaging offical recommendation: [Is setup.py deprecated?](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/).
