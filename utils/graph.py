from decimal import *


#建立切分词图 基于十字邻接表实现图结构
def create(edges,text):
    vertex_num = len(text)+1
    graph = []
    for index in range(vertex_num):
        graph.append({"edge_head":[],"edge_tail":[],"probility":Decimal(0)})
    for edge in edges:
        graph[edge['start']]['edge_head'].append(edge)
        graph[edge['end']]['edge_tail'].append(edge)
    return graph