# Wrapper methods for working with github pull-requests.
# Written by Pavel Raiskup.
#
# Copyright (C) 2018 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


import os
from subprocess import check_output, call


def github_checkout_pr(pr_id, pr_remote="pull-requests"):
    null = open(os.devnull, 'w')
    cmd = ['git', 'config', '--get', 'remote.{0}.fetch'.format(pr_remote)]
    if not call(cmd, stderr=null, stdout=null) == 0:
        # We still need to add 'pr_remote' remote
        output = check_output(['git', 'remote', 'get-url', 'origin'])
        output = output.decode('ascii').strip()
        check_output(['git', 'remote', 'add', pr_remote, output])
        set_fetch = [
            'git', 'config', '--local',
            'remote.{0}.fetch'.format(pr_remote),
            '+refs/pull/*/merge:refs/remotes/{0}/pr/*/merge'.format(pr_remote)
        ]
        check_output(set_fetch)

    check_output(['git', 'fetch', pr_remote, '--prune'])

    branch = '{0}/pr/{1}/merge'.format(pr_remote, pr_id)

    check_output(['git', 'rev-parse', '--verify',
                  'remotes/{0}'.format(branch)])

    check_output(['git', 'checkout', branch])
