# -*- coding: utf-8 -*-
# Description: nginx log netdata python.d module
# Author: Pawel Krupa (paulfantom)

from base import LogService
import re

priority = 60000
retries = 60
# update_every = 3

ORDER = ['codes']
CHARTS = {
    'codes': {
        'options': [None, 'nginx status codes', 'requests/s', 'requests', 'nginx_log.codes', 'stacked'],
        'lines': [
            ["20X", None, "incremental"],
            ["30X", None, "incremental"],
            ["40X", None, "incremental"],
            ["50X", None, "incremental"]
        ]}
}


class Service(LogService):
    def __init__(self, configuration=None, name=None):
        LogService.__init__(self, configuration=configuration, name=name)
        if len(self.log_path) == 0:
            self.log_path = "/var/log/nginx/access.log"
        self.order = ORDER
        self.definitions = CHARTS
        pattern = r'" ([0-9]{3}) ?'
        #pattern = r'(?:" )([0-9][0-9][0-9]) ?'
        self.regex = re.compile(pattern)

    def _get_data(self):
        """
        Parse new log lines
        :return: dict
        """
        data = {'20X': 0,
                '30X': 0,
                '40X': 0,
                '50X': 0}
        try:
            raw = self._get_raw_data()
            if raw is None:
                return None
            elif not raw:
                return data
        except (ValueError, AttributeError):
            return None

        regex = self.regex
        for line in raw:
            code = regex.search(line)
            beginning = code.group(1)[0]

            if beginning == '2':
                data["20X"] += 1
            elif beginning == '3':
                data["30X"] += 1
            elif beginning == '4':
                data["40X"] += 1
            elif beginning == '5':
                data["50X"] += 1

        return data

