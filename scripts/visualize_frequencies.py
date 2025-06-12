import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# --- SETUP ---

INPUT_FILE = './outputs/word_frequencies.csv'
OUTPUT_DIR = './outputs/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- LOAD DATA ---

df = pd.read_csv(INPUT_FILE)

# --- BAR CHART ---

N = 30  # Nombre de mots à visualiser

top_words = df.head(N)

plt.figure(figsize=(12, 6))
plt.bar(top_words['word'], top_words['frequency'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title(f'Top {N} most frequent words (STS filtered)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'top_words_bar_chart.png'))
plt.close()

# --- WORD CLOUD ---

word_freq = dict(zip(df['word'], df['frequency']))

wordcloud = WordCloud(width=1600, height=800, background_color='white').generate_from_frequencies(word_freq)

plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud (STS filtered)')
plt.savefig(os.path.join(OUTPUT_DIR, 'wordcloud.png'))
plt.close()

print("Visualizations generated successfully.")
