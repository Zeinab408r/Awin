from datetime import datetime
from typing import Union

import requests
import gzip
import csv
import logging
from itertools import islice

from products.models import Product, ProductMerchant

logger = logging.getLogger('network_app.product_refresher')


class ProductRefresher:
    def __init__(self, link):
        self.link = link
        self.gz_file_address = 'downloads/products.gz'
        self.csv_file_address = 'downloads/products.csv'
        self.mapped_merchants = {}
        self.required_fields = [
            'aw_deep_link',
            'product_name',
            'aw_product_id',
            'merchant_name',
            'merchant_id',
            'aw_image_url',
            'description',
        ]

    def download(self):
        logger.info('Downloading new products csv.')
        r = requests.get(self.link.link_address, allow_redirects=True)
        logger.info('Download done with status:' + str(r.status_code))
        logger.info(r.request.body)
        open(self.gz_file_address, 'wb').write(r.content)
        logger.info('New products csv downloaded.')
        logger.info('============================')

    def extract(self):
        logger.info('Extracting products csv file.')
        gz_file = gzip.GzipFile(self.gz_file_address, 'rb')
        data = gz_file.read()
        gz_file.close()

        csv_file = open(self.csv_file_address, 'wb')
        csv_file.write(data)
        csv_file.close()
        logger.info('Extraction completed!')
        logger.info('=====================')

    def serialize(self):
        logger.info('Reading and serializing extracted data.')
        logger.info('=======================================')
        with open(self.csv_file_address, newline='') as csv_file:
            reader = csv.reader(csv_file)
            rows = []
            for item in reader:
                rows.append(item)
            headers = rows[0]
            items = rows[1:]
        return headers, items

    def map_products(self):
        logger.info('Mapping products.')
        headers, items = self.serialize()
        fields = {}
        for field in self.required_fields:
            field_index = headers.index(field)
            fields[field] = field_index
        logger.info('Mapping is completed!')
        logger.info('=================')
        return fields, items

    # TODO: merchants name might be updated!
    def update_merchants(self, merchants):
        pass

    def create_merchants(self, merchants):
        logger.info('Creating new merchants.')
        merchants_objs = []
        merchant_ids = []
        for index, merchant_name in merchants.items():
            merchants_objs.append(
                ProductMerchant(
                    awin_merchant_id=index, loader_link=self.link, name=merchant_name
                )
            )
            merchant_ids.append(index)
        inserted_objs = ProductMerchant.objects.bulk_create(merchants_objs)
        # batch_size = 100
        # while True:
        #     batch = list(islice(merchants_objs, batch_size))
        #     if not batch:
        #         break
        #     new_merchants =
        # inserted_objs.extend(new_merchants)
        inserted_data = ProductMerchant.objects.filter(
            awin_merchant_id__in=merchant_ids
        )
        logger.info('New merchants created!')
        logger.info('======================')
        return inserted_data

    def remap_merchants(self, merchant_instances):
        logger.info('Remapping merchants.')
        mapped_merchants = {}
        for merchant_instance in merchant_instances:
            mapped_merchants[merchant_instance.awin_merchant_id] = merchant_instance.id
        self.mapped_merchants = mapped_merchants
        logger.info('Remapping merchants completed.')
        logger.info('==============================')

    def extract_and_map_merchants(self, fields, items):
        logger.info('Extracting merchants from items.')
        merchant_ids = []
        merchants = {}
        for item in items:
            merchant_id = item[fields['merchant_id']]
            merchant_name = item[fields['merchant_name']]
            merchant_ids.append(merchant_id)
            merchants[merchant_id] = merchant_name
        existing_merchants = ProductMerchant.objects.filter(
            awin_merchant_id__in=merchant_ids
        )
        for existing in existing_merchants:
            merchants.pop(str(existing.awin_merchant_id))
        created_merchants = None
        if len(merchants) != 0:
            created_merchants = self.create_merchants(merchants)
        if created_merchants is not None and len(created_merchants) != 0:
            all_merchants = Union[existing_merchants, created_merchants]
            self.remap_merchants(all_merchants)
        else:
            self.remap_merchants(existing_merchants)
        logger.info('Extraction is completed!')
        logger.info('========================')

    def separate_and_prepare(self):
        logger.info('Separation and preparation started.')
        fields, items = self.map_products()
        self.extract_and_map_merchants(fields, items)
        aw_ids = []
        aw_indexed_items = {}
        for item in items:
            aw_id = item[fields['aw_product_id']]
            aw_ids.append(aw_id)
            aw_indexed_items[aw_id] = item

        existing_items = Product.objects.filter(awin_product_id__in=aw_ids).exclude(updated_by_admin=True)
        update_list = []
        for existing in existing_items:
            item = aw_indexed_items.pop(str(existing.awin_product_id))
            existing.name = item[fields['product_name']]
            existing.description = item[fields['description']]
            existing.price = item[fields['search_price']]
            existing.is_active = item[fields['in_stock']]
            existing.loader_link = self.link
            existing.awin_deep_link = item[fields['aw_deep_link']]
            update_list.append(existing)

        updated_by_admin_list = Product.objects.filter(awin_product_id__in=aw_ids, updated_by_admin=True)
        for updated in updated_by_admin_list:
            item = aw_indexed_items.pop(str(updated.awin_product_id))
            updated.name = item[fields['product_name']]
            updated.description = item[fields['description']]
            updated.price = item[fields['search_price']]
            if not item[fields['in_stock']]:
                updated.is_active = False
            updated.loader_link = self.link
            updated.awin_deep_link = item[fields['aw_deep_link']]
            update_list.append(updated)

        create_list = []
        for index, item in aw_indexed_items.items():
            image_url = item[fields['aw_image_url']]
            product = Product(
                awin_product_id=index,
                name=item[fields['product_name']],
                description=item[fields['description']],
                price=item[fields['search_price']],
                image_url=image_url,
                is_active=item[fields['in_stock']],
                awin_deep_link=item[fields['aw_deep_link']],
                merchant_id=self.mapped_merchants[int(item[fields['merchant_id']])],
                loader_link=self.link,
            )
            create_list.append(product)

        logger.info('Separation and preparation is completed!')
        logger.info('========================================')
        return create_list, update_list

    def update_database(self):
        create_list, update_list = self.separate_and_prepare()
        logger.info('Updating...')
        create_list_generator = (item for item in create_list)
        create_batch_size = 100
        create_res = []
        while True:
            batch = list(islice(create_list_generator, create_batch_size))
            if not batch:
                break
            create_res = Product.objects.bulk_create(batch, create_batch_size)

        logger.info(create_res)
        update_list_generator = (item for item in update_list)
        update_batch_size = 100
        update_res = []
        while True:
            batch = list(islice(update_list_generator, update_batch_size))
            if not batch:
                break
            update_res = Product.objects.bulk_update(
                batch,
                [
                    'name',
                    'description',
                    'price',
                    'image_url',
                    'is_active',
                    'loader_link',
                    'awin_deep_link',
                ],
                update_batch_size,
            )
        logger.info('Update is completed!')
        logger.info('====================')

    def execute(self):
        print(datetime.now())
        logger.info('Executing AWIN product refresher!')
        logger.info('=================================')
        self.download()
        self.extract()
        self.update_database()
        logger.info('Everything seems fine.')
        logger.info('======================')
        print(datetime.now())
