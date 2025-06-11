
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Chargement du fichier de fréquences
df = pd.read_csv('./outputs/word_frequencies.csv')

# Top N mots les plus fréquents
N = 30
top_words = df.head(N)

plt.figure(figsize=(12, 6))
plt.bar(top_words['word'], top_words['frequency'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title(f'Top {N} mots les plus fréquents')
plt.tight_layout()
plt.savefig('./outputs/top_words_bar_chart.png')
plt.close()

# Génération du wordcloud complet
word_freq = dict(zip(df['word'], df['frequency']))
wordcloud = WordCloud(width=1600, height=800, background_color='white').generate_from_frequencies(word_freq)

plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nuage de mots complet')
plt.savefig('./outputs/wordcloud.png')
plt.close()

print("Visualisations générées : voir outputs/")
