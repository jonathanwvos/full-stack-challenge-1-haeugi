from clickhouse_driver import Client
from dotenv import load_dotenv
from flask import Flask, request, jsonify

import logging
import os


load_dotenv()


CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
CLICKHOUSE_PORT = os.getenv('CLICKHOUSE_PORT')
REPORTER_HOST = os.getenv('REPORTER_HOST')
REPORTER_PORT = os.getenv('REPORTER_PORT')

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='reporter.log',
    level=logging.INFO,
    format='%(asctime)s: %(message)s'
)
app = Flask(__name__)
client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT)


@app.route('/top-products', methods=['GET'])
def top_products():
    logger.info('GET /top-products called.')

    count = request.args.get('count', default=10, type=int)
    try:
        result = client.execute('''
            SELECT title, quantity
            FROM products
            ORDER BY quantity DESC
            LIMIT %(count)s
            ''', {
                'count': count
            }
        )
        
        products = []
        for idx, (title, quantity) in enumerate(result):
            products.append({'title': title, 'rank': idx + 1, 'quantity': quantity})
            
        return jsonify(products)
    except Exception as e:
        return str(e), 503


if __name__ == '__main__':
    logger.info('Starting Reporter API.')    
    app.run(host=REPORTER_HOST, port=REPORTER_PORT)
