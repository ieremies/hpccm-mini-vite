#!/usr/bin/env python3
"""
Container image for miniVite: a minimalistic version of Vite.
- OpenMPi with UCX as backend
- Clang 15 as compiler,
- compile miniVite for non-developers.

To test the container image:
docker run ieremies/minivite-hpccm mpiexec -n 2 minivite -n 1000
"""

Stage0 += baseimage(image="ubuntu:22.04")
Stage0 += packages(
    apt=[
        "make",
        "wget",
        "build-essential",
        "cmake",
        "pkg-config",
        "apt-utils",
        "git",
        "ca-certificates",
        "libtool",
        "autoconf",
        "automake",
        "make",
        "libnuma-dev",
    ]
)

compiler = llvm(version="15", eula=True)
Stage0 += compiler

Stage0 += gdrcopy(cuda=False, eula=True, toolchain=compiler.toolchain)
Stage0 += ucx(
    version="1.14.1",
    cuda=False,
    configure_opts=["--enable-optimizations"],
    gdrcopy=True,
)

Stage0 += openmpi(
    version="4.1.1",
    cuda=False,
    infiniband=False,
    ucx=True,
    toolchain=compiler.toolchain,
)


Stage0 += environment(
    variables={
        "CC": "mpicc",
        "CXX": "mpicxx",
        "OMPI_ALLOW_RUN_AS_ROOT": 1,
        "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM": 1,
        "OMPI_CXX": "clang++",
    }
)

Stage0 += shell(commands=["git clone https://github.com/ECP-ExaGraph/miniVite.git"])
Stage0 += copy(src="Makefile", dest="/miniVite")
Stage0 += shell(
    commands=[
        "cd /miniVite",
        "make",
        "mv ./miniVite /usr/local/bin/",
    ]
)
