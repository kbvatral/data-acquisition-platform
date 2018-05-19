from influxdb import InfluxDBClient

host = '10.128.189.163'
port = 8086
ssl = True
user = 'root'
password = 'ENCLions'
dbname = 'mydb'
query = 'SELECT * FROM test_values;'
json_body = [
    {
        "measurement": "test_values",
        "tags": {
            "host": "Caleb-Laptop",
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64,
        }
    }
]

points = []
data = 'test_values,host=Caleb-Laptop value=0.12 1465839830100400200'
points.append(data)

client = InfluxDBClient(host, port, user, password, dbname, ssl)

# print("Write points: {0}".format(json_body))
client.write_points(points, protocol='line')

print("Queying data: " + query)
result = client.query(query)

print("Result: {0}".format(result))
