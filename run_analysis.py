
#!/usr/bin/env python3
"""
Script de lancement complet - Analyse Discursive v1.1
Ethereum Foundation Blog Analysis

Exécute l'ensemble du pipeline d'analyse discursive :
1. Extraction des fréquences lexicales
2. Calcul des cooccurrences
3. Visualisations (fréquences + réseau lexical)
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_path, description):
    """Exécute un script et gère les erreurs"""
    print(f"\n{'='*60}")
    print(f"📊 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              text=True, 
                              check=True)
        print(f"✅ {description} - TERMINÉ")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de {script_path}")
        print(f"Code d'erreur: {e.returncode}")
        return False

def main():
    """Pipeline principal d'analyse discursive"""
    print("🚀 LANCEMENT DE L'ANALYSE DISCURSIVE COMPLÈTE v1.1")
    print(f"⏰ Heure de début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Corpus: 567 articles Ethereum Foundation (2013-2025)")
    
    # Vérification de l'existence du corpus
    if not os.path.exists("./data/corpus_txt"):
        print("❌ ERREUR: Dossier corpus_txt non trouvé!")
        print("Vérifiez que le corpus est bien extrait dans ./data/corpus_txt/")
        return
    
    # Comptage des fichiers
    txt_files = [f for f in os.listdir("./data/corpus_txt") if f.endswith('.txt')]
    print(f"📊 Fichiers détectés: {len(txt_files)} articles")
    
    if len(txt_files) == 0:
        print("❌ ERREUR: Aucun fichier .txt trouvé dans le corpus!")
        return
    
    # Pipeline d'exécution
    scripts = [
        ("scripts/extract_word_frequencies.py", "Extraction des fréquences lexicales"),
        ("scripts/compute_cooccurrences.py", "Calcul des cooccurrences"),
        ("scripts/visualize_frequencies.py", "Génération des visualisations de fréquences"),
        ("scripts/visualize_lexical_network.py", "Génération du réseau lexical")
    ]
    
    success_count = 0
    total_scripts = len(scripts)
    
    # Exécution séquentielle
    for script_path, description in scripts:
        if run_script(script_path, description):
            success_count += 1
        else:
            print(f"⚠️  Arrêt du pipeline suite à l'erreur dans {script_path}")
            break
    
    # Rapport final
    print(f"\n{'='*60}")
    print("📋 RAPPORT FINAL D'EXÉCUTION")
    print(f"{'='*60}")
    print(f"⏰ Heure de fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Scripts exécutés avec succès: {success_count}/{total_scripts}")
    
    if success_count == total_scripts:
        print("🎉 ANALYSE COMPLÈTE TERMINÉE AVEC SUCCÈS!")
        print("\n📁 Résultats disponibles dans le dossier './outputs/':")
        print("   - word_frequencies.csv (fréquences lexicales)")
        print("   - cooccurrence_pairs.csv (cooccurrences)")
        print("   - top_words_bar_chart.png (graphique fréquences)")
        print("   - wordcloud.png (nuage de mots)")
        print("   - lexical_network.png (réseau de cooccurrences)")
        print("   - lexical_network.graphml (export Gephi)")
    else:
        print("⚠️  Analyse incomplète - Vérifiez les erreurs ci-dessus")
    
    print(f"\n🔬 Méthodologie: Approche STS + Théorie ancrée")
    print(f"📚 Documentation: README.md et Methodological_Appendix_v1_clean.md")

if __name__ == "__main__":
    main()
