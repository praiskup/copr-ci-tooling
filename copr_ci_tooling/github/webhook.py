# Parse GitHub webhook content.
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

import sys
import json

class Webhook(object):
    kind = 'unknown'

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "..."


class WebhookPR(Webhook):
    kind = 'pull_request'

    def __init__(self, data):
        super(WebhookPR, self).__init__(data)
        self.id = data['pull_request']['number']

    def __str__(self):
        return "PR {0} {1}".format(self.id, self.data['action'])


def WebhookFactory(data):
    if 'pull_request' in data:
        return WebhookPR(data)

    raise Exception("unknown webhook type" + str(data))


def github_hook_from_file(hook_file):
    return WebhookFactory(json.load(hook_file))


def github_hook_from_file_name(hook_file_name='-'):
    if hook_file_name == '-':
        return github_hook_from_file(sys.stdin)
    else:
        with open(hook_file_name, 'r') as hook_file:
            return github_hook_from_file(hook_file)
