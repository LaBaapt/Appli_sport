# S7 — Carnet SUPER7 : brief pour Claude Code

## Objectif
Transformer le prototype `super7-prototype.html` (fait dans claude.ai) en **web app installable (PWA)** que Baptiste ajoute à l’écran d’accueil de son iPhone. Ouverte depuis l’icône, elle doit s’afficher **en plein écran, sans la barre Safari**, et marcher **hors ligne** (salle de sport sans réseau).

Le prototype est la référence pour le design, les écrans et la logique. On ne refait pas l’app : on la porte, on la découpe proprement et on remplace ce qui dépend de claude.ai.

## Fichiers de ce dossier
- `super7-prototype.html` : le prototype complet (HTML + CSS + JS dans un seul fichier). Source de vérité.
- `programme-SUPER7-4-seances.pdf` : le programme d’origine (7 semaines, 4 séances/semaine). Les données sont déjà retranscrites dans la constante `PROGRAM` du prototype.
- `CLAUDE.md` : ce brief.
- `PROMPT-claude-code.md` : le message à coller dans Claude Code pour démarrer.

## Stack imposée
- Site **statique**, sans framework ni étape de build : `index.html`, `styles.css`, `app.js` (modules ES autorisés), `manifest.webmanifest`, `sw.js`, `icons/`, `fonts/`.
- Pas de dépendance npm à l’exécution. Garder le JS vanilla du prototype.
- Langue de l’interface : français. Apostrophes typographiques (’) dans les textes affichés.

## Ce qu’il faut remplacer (dépendances claude.ai)
1. **Stockage** : le prototype utilise `window.claude.use("db")` et `claude.use("user")` (n’existent pas hors claude.ai). Supprimer tout l’objet `store` lié à claude et le remplacer par :
   - `localStorage` pour l’état (clé `s7-carnet-v1`, même structure `S` : settings, custom, overrides, body, logs, live) ;
   - un bouton **Exporter mes données** (téléchargement d’un JSON) et **Importer** (lecture d’un JSON) dans l’onglet Calendrier > Réglages, pour les sauvegardes. Rappel : une web app installée sur l’écran d’accueil iOS a son propre stockage, distinct de Safari.
   - Garder l’indicateur en haut à droite, avec le texte « Enregistré sur cet appareil ».
2. **Polices** : le prototype charge Anton, Barlow Condensed et Barlow depuis Google Fonts. Les **auto-héberger** dans `fonts/` (licence OFL, fichiers woff2) pour que l’app marche hors ligne.
3. **Mode démo** : le garder tel quel (données générées en mémoire, jamais sauvegardées).

## Exigences PWA iPhone (le cœur de la demande)
Dans `index.html` :
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="S7">
<meta name="theme-color" content="#161514">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
```
`manifest.webmanifest` : `name` « S7 — Carnet SUPER7 », `short_name` « S7 », `display: "standalone"`, `start_url: "./"`, `scope: "./"`, `background_color` et `theme_color` `#161514`, `orientation: "portrait"`, icônes 192 et 512 px (dont une `maskable`).

Icônes : générer les PNG (180, 192, 512) avec un script (ex. Python + Pillow ou SVG converti) : fond `#161514`, texte « S7 » en Anton couleur `#FF5B4D`, centré, marge suffisante pour la version maskable.

Zones sûres : le prototype gère déjà `env(safe-area-inset-*)` (encoche, barre d’accueil). Vérifier qu’en mode standalone avec `black-translucent`, le contenu ne passe pas sous l’heure en haut ni sous la barre d’accueil en bas (barre d’onglets, bouton orange « Lancer la séance », écran de séance, bilan).

Service worker `sw.js` : précache de tous les fichiers (HTML, CSS, JS, polices, icônes), stratégie cache d’abord, versionnée (`const CACHE = "s7-v1"`), purge des anciens caches à l’activation. Incrémenter la version à chaque déploiement.

## Spécificités iOS à respecter
- Le minuteur se base sur des horodatages (`endsAt`) : il reste juste si l’écran se verrouille. Le garder ainsi.
- `navigator.vibrate` n’existe pas sur iOS : garder l’appel protégé (try/catch, test d’existence).
- Le son (bips de fin de repos) ne marche qu’après un geste utilisateur : garder `unlockAudio()` au clic.
- Wake Lock (`navigator.wakeLock`) : supporté sur iOS récent, garder l’appel protégé.
- Empêcher le zoom au double tap sur les boutons (`touch-action: manipulation`) et les champs (taille de police ≥ 16 px sur les inputs).

## Déploiement
Hébergement gratuit en HTTPS (obligatoire pour une PWA) sur **GitHub Pages** :
1. `git init`, premier commit.
2. Créer le dépôt public `s7-carnet` avec la CLI GitHub (`gh repo create s7-carnet --public --source . --push`).
3. Activer GitHub Pages sur la branche `main`, dossier racine (`gh api` ou paramètres du dépôt).
4. Donner à Baptiste l’URL finale (`https://<utilisateur>.github.io/s7-carnet/`).
Si `gh` n’est pas installé ou pas connecté, l’installer (winget sur Windows) et lancer `gh auth login`, puis attendre que Baptiste valide dans son navigateur.

## Critères d’acceptation
- [ ] Ouverte depuis l’icône de l’écran d’accueil : plein écran, aucune barre Safari.
- [ ] Mode avion : l’app s’ouvre et une séance complète se déroule (bloc, repos, saisie, finisher, bilan).
- [ ] Rien ne passe sous l’encoche ni sous la barre d’accueil.
- [ ] Les données persistent après fermeture complète de l’app.
- [ ] Export puis import JSON restaure tout.
- [ ] Aucun texte ne se chevauche (grands titres Anton : interlignes ≥ 1 sur plusieurs lignes).
- [ ] Toutes les fonctions du prototype marchent : blocs en superset, repos qui valide la série, validation de bloc avant la fin, finisher modifiable (marche inclinée : vitesse, pente, temps), calendrier, progrès, mesures, exercices perso, séance libre, mode démo.

## Ce qu’il ne faut pas changer
Le design (palette, typographies, mise en page), les textes, la logique de séance et les données du programme. Toute amélioration se propose d’abord à Baptiste.
