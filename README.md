dub.snap
========

This project defines a snap package for DUB, a package and build manager
for the D programming language.  It is an 'external' snap, meaning that
it downloads and builds the source from the official DUB git repo.  For
more information on DUB, see: https://github.com/dlang/dub

The D programming language is a systems programming language with C-like
syntax and static typing.  It combines efficiency, control and modelling
power with safety and programmer productivity.  For more information on
the D language, see: https://dlang.org/

Snap packages are designed to provide secure, containerized applications
that are appropriately sandboxed away from the rest of the system they
are running on.  For more information on snap packages, see:
http://snapcraft.io/


Building
--------

On Ubuntu 16.04 with snapcraft installed (`sudo apt install snapcraft`):

    git clone https://github.com/WebDrake/dub.snap.git
    cd dub.snap
    snapcraft

To ensure a clean build, install lxd (`sudo apt install lxd`), configure
its network settings, and then:

    snapcraft cleanbuild


Installing
----------

Self-built snaps are unsigned, so installing them requires the use of
the `--force-dangerous` flag:

    sudo snap install --force-dangerous dub_1.0.0_amd64.snap
