
import os

def count_txt_files(directory):
    count = 0
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            count += 1
    return count

if __name__ == "__main__":
    # Specify the relative path from the root of your GitHub repo
    directory = "./data/corpus_txt"
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found. Please check the path.")
    else:
        total_files = count_txt_files(directory)
        print(f"Total .txt files found in '{directory}': {total_files}")
