# Poker Eval

## Overview

Python [PyO3](https://pyo3.rs/) wrapper package over Rust crate [poker_eval](https://crates.io/crates/poker_eval).  

3 builds:

+ native i.e. current platform
+ to [manylinux](https://github.com/pypa/manylinux)
+ to Windows with [cross](https://github.com/cross-rs/cross).  

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

# ------- build native wheel
unset CARGO
unset CARGO_BUILD_TARGET
unset PYO3_CROSS_LIB_DIR
unset PYO3_CROSS_PYTHON_VERSION
unset DIST_EXTRA_CONFIG

python -m build


# ------- build manylinux wheel
# image used by build
docker build -t builder-manylinux:local -f ./Dockerfile.manylinux .

# build wheels for several python versions
docker run --rm -v $(pwd):/io builder-manylinux:local /bin/bash /io/build-manylinux-wheels.sh


# ------- build windows wheel - using cross
# prerequisite
cargo install cross

export CARGO=cross
export CARGO_BUILD_TARGET=x86_64-pc-windows-gnu
export DIST_EXTRA_CONFIG=/tmp/build-opts.cfg

# set wheel suffix
echo -e "[bdist_wheel]\nplat_name=win-amd64" > $DIST_EXTRA_CONFIG

# image used by cross
docker build -t cross-pyo3:x86_64-pc-windows-gnu -f ./Dockerfile.win .

# build windows wheel
python -m build
```

This produced wheels for linux and windows:

```sh
ls -1  dist
pyo3_poker_eval-0.1.0-cp310-cp310-linux_x86_64.whl
pyo3_poker_eval-0.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pyo3_poker_eval-0.1.0-cp310-cp310-win_amd64.whl
pyo3_poker_eval-0.1.0-cp311-cp311-linux_x86_64.whl
pyo3_poker_eval-0.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pyo3_poker_eval-0.1.0.tar.gz
```

## Publish

Commands:

```sh
# prerequisite
mm activate work
pip install -U twine auditwheel

twine check dist/*

# assuming .pypirc configured
# for linux only manylinux: the others will be refused
twine upload dist/*.tar.gz
twine upload dist/*manylinux*
twine upload dist/*win_amd64*
```

## Install

Commands:

```sh
pip install pyo3_poker_eval
```

## Ref

Python packaging offical recommendation: [Is setup.py deprecated?](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/).
