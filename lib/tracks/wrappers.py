# Tracks provides tools for analyzing large trajectory files.
# Copyright (C) 2007 - 2008 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Tracks.
#
# Tracks is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Tracks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


import os, shlex, sys
from subprocess import Popen, PIPE


__all__ = ["WrapperError", "Wrapper"]


class WrapperError(Exception):
    pass


class Wrapper(object):
    verbose = False

    def __init__(self, name):
        self.name = name

    def __call__(self, *arguments):
        args = []
        for argument in arguments:
            if isinstance(argument, list):
                args.extend(argument)
            else:
                args.append(argument)
        args = [str(arg) for arg in args]
        command = "%s %s" % (self.name, " ".join(args))
        if self.verbose:
            print command
        p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        retcode = p.returncode
        if retcode != 0 or self.verbose:
            print "Command output:"
            print output
            print "Command error:"
            print error
            if retcode != 0:
                raise WrapperError("An error occured while executing command (retcode=%i): \n%s" % (retcode, command))
        return output.split("\n")[:-1]

# when scripts are added, this list must be updated
names = [
    "tr-ac", "tr-ac-error", "tr-angular-momentum", "tr-blav", "tr-calc",
    "tr-corr", "tr-cwt", "tr-derive", "tr-fit-peaks", "tr-fluct",
    "tr-format-indexes", "tr-from-atrj", "tr-from-cp2k-cell",
    "tr-from-cp2k-ener", "tr-from-cp2k-stress", "tr-from-cpmd-ener",
    "tr-from-cpmd-traj", "tr-from-dlpoly-hist", "tr-from-dlpoly-output",
    "tr-from-txt", "tr-from-xyz", "tr-hist", "tr-ic-bend",  "tr-ic-dihed",
    "tr-ic-dist", "tr-ic-dtl", "tr-ic-oop", "tr-ic-psf", "tr-ic-puckering",
    "tr-integrate", "tr-irfft", "tr-length", "tr-mean-std", "tr-msd",
    "tr-msd-fit", "tr-norm", "tr-pca", "tr-plot", "tr-qh-entropy", "tr-rdf",
    "tr-reduce", "tr-rfft", "tr-select", "tr-select-rings",
    "tr-shortest-distance", "tr-slice", "tr-spectrum", "tr-split-com",
    "tr-to-txt", "tr-to-xyz",
]

for name in names:
    python_name = name.replace("-", "_")
    exec("%s = Wrapper(name)" % python_name)
    __all__.append(python_name)



