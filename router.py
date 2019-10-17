import json
import overpass
import math
from updatedGraph import DirectedGraph

def bBox(lst: list) -> list:
    ''' organizes bbox coords formated from boundingbox.klokantech.com '''
    boundingbox = list()
    boundingbox.append(lst[1])
    boundingbox.append(lst[0])
    boundingbox.append(lst[3])
    boundingbox.append(lst[2])
    return boundingbox

## Generate OpentStreetMaps API Call
api = overpass.API(timeout = 600)

## Helpers
def isOneWay(way) -> bool:
    ''' return true if way is one way, false otherwise '''
    try:
        return way['tags']['oneway'] == 'yes'
    except(KeyError):
        return False

def maxSpeed(way) -> int:
    ''' returns max speed (if available) for way from Json query '''
    try:
        speed = ''.join(x for x in way['tags']['maxspeed'] if x.isdigit())
        return int(speed)
    except(KeyError):
        try:
            return determine_speed(way['tags']['highway'])
        except(KeyError):
            return 0

def nodeInfo(nodeID: int) -> 'node':
    ''' retrieves node info, given id '''
    for node in nodes:
        if node['id'] == nodeID:
            return node

def determine_speed(roadType: str) -> int:
    ''' retrieves speed for way (if available) from Json query '''
    if roadType == 'residential':
        return 25
    elif roadType == 'primary':
        return 65
    elif roadType == 'secondary':
        return 45
    elif roadType == 'tertiary':
        return 35
    else:
        return 0

def fetch_name(way) -> str:
    ''' retrieves name of way (if available) from Json query '''
    try:
        return way['tags']['name']
    except(KeyError):
        return "No name"


## Assign information to the graph
    
def assign_map(nodes, ways, sampleMap) -> None:
    # Create/assign vertices
    for node in nodes:
        if sampleMap.vertex_exists(node['id']) == False:
            sampleMap.add_vertex(node['id'], node['lat'], node['lon'])
    print("vertices created")

    # Create/assign ways
    prevNode = 0
    for way in ways:
        for node in way['nodes']:
            if prevNode == 0:
                prevNode = node
            else:
                name = fetch_name(way)
                speed = maxSpeed(way)
                sampleMap.add_edge(prevNode, node, name, speed)
                # for two way streets
                if not isOneWay(way):
                    sampleMap.add_edge(node, prevNode, name, speed)
                prevNode = node



bbox = bBox([-118.268836,33.956458,-118.204527,33.992069])
mapquery = overpass.MapQuery(bbox[0], bbox[1], bbox[2], bbox[3])
jsoninfo = api.get(mapquery, responseformat = 'json')
ways = [feature for feature in jsoninfo['elements'] if feature['type'] == 'way']
nodes = [feature for feature in jsoninfo['elements'] if feature['type'] == 'node']
print("Ways and nodes created")
print(len(nodes))

## Create Graph
defaultMap = DirectedGraph(list())
assign_map(nodes, ways, defaultMap)
print("Graph has been created\n")


