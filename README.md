# S7 — Carnet SUPER7

Web app installable (PWA) du programme SUPER7 : 7 semaines, 4 séances par semaine. Plein écran depuis l’écran d’accueil de l’iPhone, fonctionne hors ligne.

## Fichiers
- `index.html`, `styles.css`, `app.js` : l’app (portée de `super7-prototype.html`, qui reste la référence).
- `manifest.webmanifest`, `sw.js` : installation et hors ligne (précache, cache d’abord).
- `fonts/` : Anton, Barlow Condensed, Barlow en woff2 (SIL OFL 1.1, licences jointes).
- `icons/` : générées par `python3 tools/make-icons.py` (Pillow).

## Déployer une nouvelle version
1. Modifier les fichiers.
2. Incrémenter `CACHE` dans `sw.js` (`s7-v1` → `s7-v2`…). Si un fichier est ajouté, l’ajouter aussi à `ASSETS`.
3. Pousser sur `main` (GitHub Pages, dossier racine). Sur l’iPhone, ouvrir l’app deux fois pour charger la nouvelle version.

## Tester en local
```
python3 -m http.server 8000
```
puis ouvrir http://localhost:8000/.

## Données
Tout est stocké dans `localStorage` (clé `s7-carnet-v1`). L’app installée sur l’écran d’accueil a son propre stockage, distinct de Safari : utiliser **Calendrier > Sauvegarde > Exporter mes données** pour garder une copie, et **Importer** pour restaurer.
