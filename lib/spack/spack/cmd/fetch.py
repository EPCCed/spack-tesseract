##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.repo
import spack.cmd.common.arguments as arguments

description = "fetch archives for packages"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-m', '--missing', action='store_true',
        help="fetch only missing (not yet installed) dependencies")
    subparser.add_argument(
        '-D', '--dependencies', action='store_true',
        help="also fetch all dependencies")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to fetch")


def fetch(parser, args):
    if not args.packages:
        tty.die("fetch requires at least one package argument")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    specs = spack.cmd.parse_specs(args.packages, concretize=True)
    for spec in specs:
        if args.missing or args.dependencies:
            for s in spec.traverse():
                package = spack.repo.path().get(s)

                # Skip already-installed packages with --missing
                if args.missing and package.installed:
                    continue

                # Do not attempt to fetch externals (they're local)
                if package.spec.external:
                    continue

                package.do_fetch()

        package = spack.repo.path().get(spec)
        package.do_fetch()
