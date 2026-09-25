# Kob House, charte graphique

Kob House est une maison d'édition de livres d'énigmes à résoudre au stylo. La charte s'inspire du dossier d'enquête : papier crème, encre noire, un tampon rouge. Les livres apportent chacun leur propre couleur, la marque ne leur fait pas concurrence.

## Couleurs

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Fond de marque | Papier | `#EFE8D6` | Header, hero et sections « teintées » du hub, page légale, fonds Instagram de marque |
| Encre | Noir | `#111111` (site : `#000`) | Texte, cadres 3 px, ombres portées |
| Accent | Tampon | `#D8261C` | Logo, favicon, ombres des boutons, mot MAP du hero, numéros d'étapes, tampon « Case file » |
| Neutre | Blanc | `#FFFFFF` | Fond des sections de contenu, cartes |

Un seul accent par page. Le rouge n'est jamais utilisé comme fond de grande surface, seulement en trait, en ombre ou en tampon.

## Couleurs des livres (inchangées)

| Livre | Fond | Accent |
|---|---|---|
| Murder Map: Paris | `#1F6BED` | `#F4FF1E` |
| Murder Map: Tokyo | `#F26A4B` | `#D9F2E3` |
| Murder Map: New York | `#FBBA16` | `#F7F1E1` |

Chaque page livre du site, chaque couverture et chaque module A+ garde ce duo. Sur le hub, les cartes des livres portent leurs propres couleurs sur le fond de marque.

## Typographie

- Titres : Anton, capitales, interligne 0.95.
- Étiquettes, tags, navigation : Space Mono Bold, capitales, lettrage espacé (2 à 6 px).
- Texte courant : Nunito 400 et 700.

Les fichiers woff2 sont dans `assets/fonts/`.

## Formes

- Cadres noirs de 3 px, ombres portées pleines (6 à 14 px, noires ou dans l'accent), pas d'arrondi.
- Légères rotations (2 à 8 degrés) sur les stickers, tampons et couvertures.
- Tampon « Case file » : bordure 4 px rouge, texte rouge Space Mono, rotation -6 degrés.

## Logo

« K🐸B » en Anton avec la grenouille en place du O, « HOUSE » en Space Mono espacé dessous. Version monochrome noire sur fond papier ou blanc, blanche sur fond noir. Favicon : grenouille noire sur carré rouge `#D8261C`.

## Où c'est appliqué

- `build_site.py` : `BRAND_BG` et `BRAND_ACC` pilotent le hub et la page légale ; chaque entrée de `BOOKS` garde `bg` et `acc`.
- `data/_favicon.txt` : favicon.
