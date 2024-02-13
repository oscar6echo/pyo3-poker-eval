
FROM quay.io/pypa/manylinux_2_28_x86_64 AS manylinux
# FROM quay.io/pypa/manylinux2014_x86_64 AS manylinux
# FROM quay.io/pypa/manylinux2014_aarch64 AS manylinux

FROM ghcr.io/cross-rs/x86_64-pc-windows-gnu:edge
# FROM ghcr.io/cross-rs/x86_64-pc-windows-gnu:0.2.5

RUN apt install zstd -y 

# download linux python - https://github.com/indygreg/python-build-standalone/releases
# make it system python
ENV DATE=20240107
ENV VERSION=cpython-3.10.13
ENV URL_ASSET=https://github.com/indygreg/python-build-standalone/releases/download/$DATE/$VERSION+$DATE-x86_64-unknown-linux-gnu-install_only.tar.gz

RUN curl -L $URL_ASSET | tar -xz -C /usr/local

# RUN ls -al /usr/local

# download mingw64 python - https://repo.msys2.org/mingw/mingw64/
# keep only dll
ENV URL_ASSET=https://repo.msys2.org/mingw/mingw64/mingw-w64-x86_64-python-3.10.12-1-any.pkg.tar.zst

RUN curl $URL_ASSET > /tmp/pkg.tar.zst && \
    tar -axvf /tmp/pkg.tar.zst -C /tmp && \
    cp /tmp/mingw64/lib/libpython3.10.dll.a /usr/x86_64-w64-mingw32/lib/libpython310.dll.a && \
    rm /tmp/pkg.tar.zst && \
    rm -rf /tmp/mingw64


ENV PATH=/usr/local/python/bin:$PATH
