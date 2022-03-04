import logging
from time import sleep
from celery import shared_task

from .product_refresher import ProductRefresher
from .models import AwinProductLink, AwinProductLinkStateEnum

logger = logging.getLogger('network_app.worker')


@shared_task
def mask_all_products():
    logger.info(">>>>>> STARTING: UPDATE PRODUCTS FROM AWIN LINKS. <<<<<<")
    # use this link to download a zip file containing products
    links = ["https://ui2.awin.com/affiliates/shopwindow/datafeed_metadata.php?user=712705&password=cb06eaeb32ac6e7fd42f72a4e1675a38&format=CSV&filter=SUBSCRIBED&compression=zip"]
    for link in links:
        product_refresher = ProductRefresher(link=link)
        product_refresher.execute()
        sleep(20)
