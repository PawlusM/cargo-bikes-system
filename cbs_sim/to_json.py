import json

nodes = []

f = open('rynek_nodes.txt', 'r')
for data_line in f:
    data = data_line.split('\t')
    nodes.append({'lng': float(data[4]),
                  'lat': float(data[3]),
                  'description': str(data[1])})
f.close()
print(nodes)

json = json.dumps(nodes)
f = open("nodes.json", "w")
f.write(json)
f.close()
