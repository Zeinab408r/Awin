import logging
from time import sleep
from celery import shared_task

from .product_refresher import ProductRefresher
from .models import AwinProductLink, AwinProductLinkStateEnum

logger = logging.getLogger('network_app.worker')


@shared_task
def update_and_add_products():
    logger.info(">>>>>> STARTING: UPDATE PRODUCTS FROM AWIN LINKS. <<<<<<")
    # use this link to download a zip file containing products
    links = AwinProductLink.objects.filter(
        state=AwinProductLinkStateEnum.ACTIVE.value)
    print("I am here in side update_and_add_products function:)")
    for link in links:
        product_refresher = ProductRefresher(link=link)
        product_refresher.execute()
        sleep(20)
