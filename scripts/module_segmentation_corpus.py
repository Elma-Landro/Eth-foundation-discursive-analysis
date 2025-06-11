
import os
import pandas as pd
import shutil

# Path to metadata CSV
CSV_FILE = './data/corpus_raw/ethereum_blog_articles.csv'
# Directory where the flat txt corpus is stored
SOURCE_DIR = './data/corpus_txt/'
# Output directory where segmented corpus will be organized
OUTPUT_DIR = './data/segmented_corpus/'

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load metadata CSV
df = pd.read_csv(CSV_FILE)

# Ensure required columns exist
if 'category' not in df.columns or 'filename' not in df.columns:
    raise ValueError("CSV file must contain 'filename' and 'category' columns.")

# Process each row in metadata
for index, row in df.iterrows():
    filename = row['filename']
    category = row['category']

    # Sanitize category name for folders
    category_dir = category.replace(" ", "_").replace("/", "-")
    target_dir = os.path.join(OUTPUT_DIR, category_dir)
    os.makedirs(target_dir, exist_ok=True)

    # Build full paths
    source_path = os.path.join(SOURCE_DIR, filename)
    target_path = os.path.join(target_dir, filename)

    # Copy file if exists
    if os.path.exists(source_path):
        shutil.copy2(source_path, target_path)
    else:
        print(f"WARNING: File not found in corpus_txt: {filename}")

print("✅ Segmentation complete. Segmented corpus located in:", OUTPUT_DIR)
