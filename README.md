# Bot de surveillance de billets See Tickets

Ce bot surveille automatiquement la disponibilité des billets pour le Dream Nation 2026 (Vendredi) et ouvre la page dans le navigateur dès qu'un billet est disponible.

## 🚀 Fonctionnement
- **Cible** : Page de revente du Pass 1 jour Vendredi.
- **Méthode** : Utilise Playwright pour simuler un utilisateur réel et contourner les détections basiques.
- **Fréquence** : Rafraîchissement aléatoire toutes les 30 à 60 secondes pour éviter le bannissement.
- **Action** : Dès que le mot-clé "ajouter" (ou "achat", "disponible", "panier") est détecté sur un bouton ou un lien, le bot ouvre l'URL dans le navigateur par défaut de l'ordinateur.

## 🛠 Installation et Lancement

1. **Initialiser l'environnement** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install playwright playwright-stealth python-dotenv
   playwright install chromium
   ```

2. **Lancer le bot** :
   ```bash
   python3 monitor.py
   ```

## ⚠️ Notes
- Le bot doit être lancé sur une machine où un navigateur est installé pour que l'ouverture automatique fonctionne.
- Ne pas réduire l'intervalle de rafraîchissement en dessous de 30s pour limiter les risques de blocage d'IP.
