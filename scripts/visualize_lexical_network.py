import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os

# --- SETUP ---

INPUT_FILE = './outputs/cooccurrence_pairs.csv'
OUTPUT_DIR = './outputs/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- LOAD DATA ---

df = pd.read_csv(INPUT_FILE)

# --- FILTER CO-OCCURRENCES ---

# Seuil de fréquence minimale pour garder les liaisons les plus significatives
THRESHOLD = 5
df_filtered = df[df['count'] >= THRESHOLD]

# --- BUILD GRAPH ---

G = nx.Graph()

for _, row in df_filtered.iterrows():
    word1, word2, count = row['word1'], row['word2'], row['count']
    G.add_edge(word1, word2, weight=count)

# --- DRAW GRAPH ---

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G, seed=42, k=0.4)  # Positionnement stable et lisible
edges = G.edges()

# Épaisseur des arêtes proportionnelle aux cooccurrences
weights = [G[u][v]['weight'] for u,v in edges]
nx.draw_networkx_edges(G, pos, edge_color='gray', width=[w*0.1 for w in weights])

# Noeuds
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)

# Étiquettes
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title('Lexical Co-occurrence Network (STS filtered)')
plt.axis('off')
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, 'lexical_network.png'))
plt.close()

# --- SAVE GRAPH STRUCTURE ---

nx.write_graphml(G, os.path.join(OUTPUT_DIR, 'lexical_network.graphml'))

print("Lexical network visualizations generated successfully.")
