# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from scrapy_proxy_pool.policy import BanDetectionPolicy
from six.moves.urllib.parse import urlparse

MARKETPLACE_HOST_MAPPING = {
    'us': 'www.amazon.com',
    'ca': 'www.amazon.ca',
    'mx': 'www.amazon.com.mx',
    'uk': 'www.amazon.co.uk',
    'de': 'www.amazon.de',
    'fr': 'www.amazon.fr',
    'it': 'www.amazon.it',
    'es': 'www.amazon.es',
    'au': 'www.amazon.com.au',
    'jp': 'www.amazon.jp',
    'in': 'www.amazon.in',
    'cn': 'www.amazon.cn'
}

def is_robot_check(response):
    return response.xpath('//*[@id="captchacharacters"]').extract_first() is not None

def is_proxy_forbidden(response):
    o = urlparse(response.url)
    return o.netloc.find('amazon') == -1


class AmazonBanDetectionPolicy(BanDetectionPolicy):
    NOT_BAN_STATUSES = [200, 404, 500, 503]

    def response_is_ban(self, request, response):
        base_ban = super(AmazonBanDetectionPolicy, self).response_is_ban(request, response)
        amazon_ban = is_robot_check(response)
        proxy_ban = is_proxy_forbidden(response)

        return base_ban or amazon_ban or proxy_ban
