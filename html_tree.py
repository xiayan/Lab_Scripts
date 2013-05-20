import urllib2
import networkx as nx
from lxml import html
import matplotlib.pyplot as plt

raw = """
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link2">
    Tillie
   </a>
   ; and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
"""
raw = ''.join(urllib2.urlopen('http://www.recreation.ku.edu/~recserv/hours.shtml').readlines())

def traverse(parent, graph, labels):
    labels[parent] = parent.tag
    for node in parent.getchildren():
        graph.add_edge(parent, node)
        traverse(node, graph, labels)

G = nx.DiGraph()
labels = {}     # needed to map from node to tag
html_tag = html.document_fromstring(raw)
traverse(html_tag, G, labels)

pos = nx.graphviz_layout(G, prog='dot')

label_props = {'size': 3,
               'color': 'black',
               #'weight': 'bold',
               'horizontalalignment': 'center',
               'verticalalignment': 'center',
               'clip_on': True}
bbox_props = {'boxstyle': "round, pad=0.1",
              'fc': "grey",
              'ec': "b",
              'lw': 0.1}

nx.draw_networkx_edges(G, pos, arrows=False)
ax = plt.gca()

for node, label in labels.items():
        x, y = pos[node]
        ax.text(x, y, label,
                bbox=bbox_props,
                **label_props)

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.show()
