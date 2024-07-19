from clickhouse_driver import Client
from dotenv import load_dotenv

import logging
import os
import shopify
import time


class ScraperCommand:
    '''
    Command pattern for scraper.
    Used to initialize all required sessions and APIs and poll for orders.
    '''
     
    SHOPIFY_DATE = '2022-04'
    RETRY_ATTEMPTS = 5
    TIMEOUT_SECONDS = 5
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
        load_dotenv()

        shop_url = os.getenv('SHOPIFY_SHOP_URL')
        access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        clickhouse_host = os.getenv('CLICKHOUSE_HOST')
        clickhouse_port = os.getenv('CLICKHOUSE_PORT')
        
        self.client = self.init_db_client(clickhouse_host, clickhouse_port)
        self.session = self.init_shopify_session(access_token, shop_url)
    
    def init_db_client(self, host: str, port: int) -> Client:
        '''
        Initialize client session and products table.
        '''
        
        self.logger.info('Initializing DB client.')
        
        for _ in range(self.RETRY_ATTEMPTS):
            try:
                client = Client(host=host, port=port)
                client.execute('''
                    CREATE TABLE IF NOT EXISTS products
                    (
                        title String,
                        quantity UInt64
                    )
                    ENGINE = EmbeddedRocksDB
                    PRIMARY KEY title
                    '''
                )
                
                return client
            except Exception as e:
                self.logger.error('Unable to connect to Clickhouse instance: {e}')
                time.sleep(self.TIMEOUT_SECONDS)
                
        raise Exception(f'Clickhouse timeout ({self.RETRY_ATTEMPTS} attempts).')
        
    def init_shopify_session(self, access_token: str, shop_url: str) -> shopify.Session:
        '''
        Initialize shopify session.
        '''
        
        self.logger.info('Initializing Shopify session.')
        
        shopify.Session.setup(api_key=access_token)
        session = shopify.Session(shop_url, self.SHOPIFY_DATE, access_token)
        shopify.ShopifyResource.activate_session(session)
        
        return session
        
    def get_product_counts(self):
        '''
        Get orders from shopify and determine the total product
        quantity.
        '''
        
        self.logger.info('Fetching product counts.')
        
        orders = shopify.Order.find()
        product_counts = {}

        for order in orders:
            for line_item in order.line_items:
                title = line_item.title
                quantity = line_item.quantity
                
                if title not in product_counts:
                    product_counts[title] = 0
                
                product_counts[title] += quantity
            
        return product_counts
    
    def insert_product(self, title: str, quantity: int):
        return self.client.execute('''
            INSERT INTO products (title, quantity)
            VALUES (%(title)s, %(quantity)s)
            ''', {
                'title': title,
                'quantity': quantity
            }
        )
    
    def execute(self):
        '''
        Execute main event loop and periodically retrieve product
        counts from shopify store.
        '''
        
        self.logger.info('Executing Scraper main event loop.')
        
        while True:
            product_counts = self.get_product_counts()
            
            for title in product_counts:
                self.insert_product(title, product_counts[title])
            
            time.sleep(2)
            

if __name__ == '__main__':
    # Give clickhouse server time to startup
    time.sleep(5)
        
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename='scraper.log',
        level=logging.INFO,
        format='%(asctime)s: %(message)s'
    )
    
    command = ScraperCommand(logger)
    command.execute()
