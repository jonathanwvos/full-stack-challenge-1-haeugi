### Klar! Full stack challenge #1

The task is to fetch data from the Shopify API, extract 
relevant information, persist this data in a Clickhouse database 
table, and then provide a REST interface where a list 
of "Top products" can be retrieved from.
The solution needs to be containerized using Docker and docker-compose.

Read this file carefully and make sure that you understand the requirements. 

In this repository you will find two python files. app/scraper.py and 
app/web.py. 

#### app/scraper.py
Here you should write the code to fetch the data from the Shopify 
API and insert it into clickhouse. The script should fetch the data,
load it into a table, and then exit. 

You will find the data you need by fetching Shopify "Order" objects. 
Only persist the data you need in order to satisfy the requirements 
of the "reporter" below.


#### app/reporter.py 
Here you should build your REST API interface. The API should 
provide a single REST GET endpoint that returns a list 
of the "Top 10 products" for the shop. The #1 top product is 
the product that was purchased the most times. The #2 top product
is the product that was purchased the second most times and so on. 

You may consider each "Product Title" to uniquely identify a product.

The result format should be JSON and match the shape: 
```
[
{
"title":"Product title #1",
"rank": 1,
"cnt_bought":100
},
{
"title":"Product title #2",
"rank": 2,
"cnt_bought":50
},
... 
]
```

You should produce this data by selecting data from the clickhouse table you
populated in the "scraper" above.

If the data is not yet available at the time the REST endpoint is 
called, the endpoint should return an HTTP service not available 
status code.

You should provide the option to pass in a query string parameter 
such as this: 

```
GET /top-products?count=10
```

Which will return the top 10 products. 

```
GET /top-products?count=5
```

Which will return the top 5, and so on. 

To access the Shopify API you will be provided with Shopify credentials: 
A Shopify "Shop URL" and an access token. 



### Docker 
Finally, your solution should be containerized so that it can run 
on any system with a docker stack. For this you will need 
to update the docker-compose.yml and Dockerfile as required. 

It is a requirement that your solution can be evaluated by performing 
the following four simple steps.

1) Pull the repository
2) Update the .env file with appropriate configuration variables
3) Run ```docker-compose build``` to build the docker container
4) Run ```docker-compose up``` to run the stack

When running ```docker-compose up``` the stack should start up,
the scraper should extract the data and the REST endpoint 
should come up. The REST endpoint must be accessible with a browser
on the local machine running the docker stack.

A .env.example file is provided where you can add hints to the 
user of your service as to what environment variables are required for configuration. 


### Coding Challenge Guidelines

1) Only extract the data you need from the Shopify Orders. The Order
objects are quite detailed and complex and you don't need to create a complex 
table structure to store all of the information. Only extract 
and persist the data you need to satisfy the requirements.    
   
2) Do not commit any secrets to this repository

3) Write succinct, idiomatic Python 3, but don't overdo it. 
Your code should still be easily understandable and extensible. 

### Evaluation Criteria

1) Fulfillment of requirements, particularly that the solution 
can be brought up using the 4 steps in the Docker section.
   
2) Clean and idiomatic use of Python

3) Sensible engineering practices



### Useful information

#### Hints

1) There exists a Python Shopify API Client
https://github.com/Shopify/shopify_python_api
   
2) You will find all the data you need to complete this
task in the Shopify Order(s) object(s)

3) Clickhouse driver is a nice client for Clickhouse:
https://clickhouse-driver.readthedocs.io/en/latest/
   
4) You can access a web console for clickhouse by 
starting up the docker stack and visiting: 
http://localhost:8123/play

5) By default, clickhouse can be accessed with username: default and a blank password

6) Clickhouse provides a multitude of different 
storage mechanisms. For your implementation, keep it
simple and just make use of the EmbeddedRocksDB storage
engine. You create a table like so: 
   
```
CREATE TABLE mytable
(
    `id` UInt64,
    `some_string` String,
    `some_number` UInt64
)
ENGINE = EmbeddedRocksDB
PRIMARY KEY id

```
Read more about that here: 

https://clickhouse.com/docs/en/sql-reference/statements/create/table/

7) Flask is a nice, easy to use and fairly lean REST framework 
for Python 

  
8) Above all, keep things simple and focus on satisfying 
the task requirements. 


#### Bonus 

* What happens if the extraction process breaks half way through ? 
* Clickhouse has some other interesting storage engines. Would any be relevant 
for further exploration for this use case ? 


   

### Klar!

Have fun and do your best ! 
