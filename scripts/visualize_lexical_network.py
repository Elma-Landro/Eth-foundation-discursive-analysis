
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Charger le fichier de cooccurrence produit par le Module 3
df = pd.read_csv('./outputs/cooccurrence_pairs.csv')

# On filtre pour éviter les liaisons trop faibles (seuil paramétrable)
threshold = 5
df_filtered = df[df['count'] >= threshold]

# Création du graphe
G = nx.Graph()

for index, row in df_filtered.iterrows():
    G.add_edge(row['word1'], row['word2'], weight=row['count'])

# Mise en page du graphe
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G, k=0.15, iterations=50)
edges = G.edges(data=True)
weights = [edata['weight'] for _,_,edata in edges]

# Dessin du réseau avec taille de trait selon poids
nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue')
nx.draw_networkx_edges(G, pos, width=[w/2 for w in weights], alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

plt.title("Network of lexical co-occurrences")
plt.axis('off')
plt.tight_layout()
plt.savefig('./outputs/lexical_network.png')
plt.close()

# Export du graphe en format .graphml pour Gephi ou autre analyse réseau
nx.write_graphml(G, "./outputs/lexical_network.graphml")

print("Réseau généré : voir outputs/lexical_network.png et lexical_network.graphml")
