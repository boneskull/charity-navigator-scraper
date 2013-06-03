# Scrapy settings for charitynav project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'charitynav'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['charitynav.spiders']
NEWSPIDER_MODULE = 'charitynav.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)


ITEM_PIPELINES = ['charitynav.pipelines.JsonWriterPipeline']

