# POS Default Customer — SOPROMER fork

Module Odoo 18 permettant de configurer un **client par défaut par point de vente**. Le client défini est automatiquement pré-sélectionné à la création d'une nouvelle commande POS.

## Origine

Module d'origine **iPredict IT Solutions Pvt. Ltd.** publié sur Odoo Apps Store.
- Site : http://ipredictitsolutions.com
- Licence : **OPL-1** (propriétaire — voir note ci-dessous)

Ce dépôt est un **fork interne SOPROMER** pour suivre les adaptations et améliorations appliquées en production.

> ⚠️ **Note licence OPL-1** : le code original reste propriété d'iPredict. Ce fork est privé à l'usage interne SOPROMER. Ne pas redistribuer hors contexte.

## Contexte SOPROMER

- Distribution produits de la mer, Madagascar
- 40 points de vente actifs (entrepôts CFMP23, CFPF23, CFC, MG04, E01..E55)
- Besoin : pré-affecter un client "comptoir" par PdV pour éviter la saisie manuelle à chaque commande

## Fonctionnalités

- Champ `default_partner_id` sur `pos.config` (Many2one vers `res.partner`)
- Configuration via **Point de Vente > Configuration > Paramètres** → bloc "Default Customer in POS Order"
- À l'ouverture d'une commande POS : si aucun client saisi et commande non verrouillée → client par défaut appliqué

## Installation

```bash
# Déploiement via script SOPROMER
./scripts/deploy.sh pos_set_default_customer 45

# Puis upgrade
docker exec odoo-dev /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf \
    -d SOPROMER-REST220426 -u pos_set_default_customer --stop-after-init
```

## Modifications SOPROMER vs version originale

| Version | Date | Change | Auteur |
|---------|------|--------|--------|
| 18.0.0.1.1 | 2026-04-24 | Import initial depuis Apps Store | SOPROMER |
| 18.0.0.1.2 | 2026-04-24 | Retrait `console.log` debug dans `pos_order.js` | Claude (opus-4.7) |
| 18.0.0.1.2 | 2026-04-24 | `application: True` → `False` (pas une app) | Claude (opus-4.7) |
| 18.0.0.1.3 | 2026-04-24 | Ajout `views/res_config_views.xml` manquant dans manifest `data` | Claude (opus-4.7) |
| 18.0.0.1.4 | 2026-04-24 | Durcissement ACL : domain customer_rank+active+multi-co, groups `group_pos_manager` | Claude (opus-4.7) |
| 18.0.0.1.7 | 2026-04-30 | Override `res.partner._load_pos_data_domain` pour charger le partner par défaut dans le pool POS frontend (fix auto-set silencieux) | Claude (opus-4.7) |
| 18.0.0.1.9 | 2026-04-30 | Bloc settings `default_partner_id` masqué entièrement aux non-managers (groups sur outer div) | Claude (opus-4.7) |
| 18.0.0.2.0 | 2026-04-30 | Patch `PosStore.selectPartner` — bouton client POS bloqué pour caissiers (notification "Changement non autorisé"), managers gardent contrôle total | Claude (opus-4.7) |

## Sécurité (v18.0.0.2.0)

Architecture multi-niveaux :

- **Backend** :
  - Domain restrictif sur `default_partner_id` : `customer_rank > 0`, `active = True`, multi-compagnie
  - Bloc settings entièrement masqué aux non-managers via `groups="point_of_sale.group_pos_manager"` sur outer div
  - Wrapper `pos_default_partner_id` sur `res.config.settings` réservé managers
- **POS frontend** :
  - Patch `PosStore.selectPartner` → bloque ouverture sélecteur client pour caissiers, notification rouge
  - Auto-set partner_id à création commande via `PosOrder.setup` patch
  - `res.partner._load_pos_data_domain` étendu pour inclure le partner par défaut dans pool POS
- Pas de `sudo()` ni bypass ACL
- Pas de `groups=` sur définition Python `default_partner_id` (sinon POS frontend ne peut pas le lire)

Voir `models/pos_config.py` + `static/src/overrides/store/pos_store.js`.

## Améliorations prévues (TODO)

- [ ] Traduction française des labels (`pos.config` + `res.config.settings`)
- [ ] Tests unitaires (`tests/test_default_customer.py`)
- [ ] Icône module conforme charte SOPROMER

## Déploiement

| Environnement | Serveur | DB cible | Statut |
|---------------|---------|----------|--------|
| TEST | `192.73.0.45` | `SOPROMER-REST2904` | ✅ installé v18.0.0.2.0 |
| PROD | `192.73.0.43` | `SOPROMER` | ✅ installé v18.0.0.2.0 (2026-04-30) |

## Structure module

```
pos_set_default_customer/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── pos_config.py          # champ default_partner_id + relation settings
├── views/
│   ├── pos_config_view.xml    # héritage form pos.config
│   └── res_config_views.xml   # héritage res.config.settings (onglet PdV)
├── static/src/overrides/models/
│   └── pos_order.js           # patch PosOrder.setup (pré-affectation client)
├── README.md
└── .gitignore
```

## Comparaison avec alternative écartée

Deux modules candidats analysés :
- ❌ `bi_pos_default_customer` (BrowseInfo) — JS legacy (`set_partner(id)` incompatible Odoo 18), nom de champ confondant (`res_partner_id`)
- ✅ `pos_set_default_customer` (iPredict) — JS moderne (`update({partner_id})`), respect de `uiState.locked`, nommage conforme

## Licence

OPL-1 (propriété iPredict IT Solutions). Usage interne SOPROMER uniquement.
