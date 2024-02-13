# Poker Eval

Python/Rust poker eval package.

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

# build - native
unset CARGO
unset CARGO_BUILD_TARGET
unset PYO3_CROSS_LIB_DIR
unset PYO3_CROSS_PYTHON_VERSION
unset DIST_EXTRA_CONFIG

python -m build

# build - cross
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

## Ref

Packaging offical recommendation: [Is setup.py deprecated?](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/).
