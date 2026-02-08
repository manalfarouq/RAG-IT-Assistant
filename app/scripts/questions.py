"""
Questions IT Support basées sur le livre
Organisées par chapitres et catégories
"""

questions_data = [
    # Part I: IT Support Fundamentals
    
    # Chapter 1: Introduction to IT Support
    {"question": "Quels sont les fondamentaux du support IT ?", "category": "Fondamentaux IT"},
    {"question": "Quel est le rôle du support IT dans une entreprise ?", "category": "Fondamentaux IT"},
    {"question": "Comment éviter de faire des suppositions en support IT ?", "category": "Fondamentaux IT"},
    {"question": "Comment surmonter la barrière du langage technique ?", "category": "Fondamentaux IT"},
    {"question": "Pourquoi l'interconnexion des systèmes IT est-elle importante ?", "category": "Fondamentaux IT"},
    
    # Chapter 2: Understanding Your IT System Better
    {"question": "Quelle est la brève histoire de l'informatique ?", "category": "Systèmes IT"},
    {"question": "Quels sont les différents types de systèmes IT que l'on peut rencontrer ?", "category": "Systèmes IT"},
    {"question": "Quels sont les standards d'interface en informatique ?", "category": "Systèmes IT"},
    {"question": "Quels sont les différents types de périphériques ?", "category": "Systèmes IT"},
    {"question": "Quels sont les principaux systèmes d'exploitation ?", "category": "Systèmes IT"},
    {"question": "Comment les systèmes IT sont-ils interconnectés ?", "category": "Systèmes IT"},
    
    # Chapter 3: Understanding What Your Users Really Know
    {"question": "Comment communiquer efficacement avec les utilisateurs ?", "category": "Gestion Utilisateurs"},
    {"question": "Comment gérer la formation du personnel IT ?", "category": "Gestion Utilisateurs"},
    {"question": "Qu'est-ce que la théorie de l'apprentissage en IT ?", "category": "Gestion Utilisateurs"},
    {"question": "Comment structurer la formation et l'éducation IT ?", "category": "Gestion Utilisateurs"},
    {"question": "Comment placer les informations dans leur contexte ?", "category": "Gestion Utilisateurs"},
    {"question": "Comment définir les objectifs de formation ?", "category": "Gestion Utilisateurs"},
    {"question": "Comment évaluer les connaissances des apprenants ?", "category": "Gestion Utilisateurs"},
    
    # Part II: IT Support Methodology
    
    # Chapter 4: Flow Logic and Troubleshooting
    {"question": "Comment fonctionne la logique de flux en dépannage ?", "category": "Dépannage & Méthodologie"},
    {"question": "Qu'est-ce que le processus d'élimination en troubleshooting ?", "category": "Dépannage & Méthodologie"},
    {"question": "Pourquoi l'information est-elle essentielle en dépannage ?", "category": "Dépannage & Méthodologie"},
    {"question": "Comment commencer par la fin sans travailler à l'envers ?", "category": "Dépannage & Méthodologie"},
    {"question": "Comment rendre l'impossible possible en dépannage ?", "category": "Dépannage & Méthodologie"},
    {"question": "Comment travailler efficacement en équipe pour résoudre les problèmes ?", "category": "Dépannage & Méthodologie"},
    
    # Chapter 5: Querying Users Effectively
    {"question": "Comment interroger les utilisateurs efficacement pour diagnostiquer les problèmes ?", "category": "Diagnostic & Communication"},
    {"question": "Pourquoi ne jamais faire de suppositions lors du diagnostic ?", "category": "Diagnostic & Communication"},
    {"question": "Comment poser des questions oui/non efficacement ?", "category": "Diagnostic & Communication"},
    {"question": "Comment accompagner l'utilisateur dans le processus de dépannage ?", "category": "Diagnostic & Communication"},
    {"question": "Comment utiliser un dictionnaire non-technique avec les utilisateurs ?", "category": "Diagnostic & Communication"},
    {"question": "Comment gérer le chat en ligne pour le support ?", "category": "Diagnostic & Communication"},
    
    # Chapter 6: Finding the Root Cause
    {"question": "Comment trouver la cause racine d'un problème IT ?", "category": "Analyse de Problèmes"},
    {"question": "Qu'est-ce que la méthode 'beginning of the end' en troubleshooting ?", "category": "Analyse de Problèmes"},
    {"question": "Comment travailler en arrière pour trouver la source du problème ?", "category": "Analyse de Problèmes"},
    {"question": "Quels sont les points de connexion dont il faut tenir compte ?", "category": "Analyse de Problèmes"},
    {"question": "Comment garder l'esprit ouvert lors du diagnostic ?", "category": "Analyse de Problèmes"},
    
    # Part III: Understanding IT System Problems
    
    # Chapter 7: How IT Systems Are Structured
    {"question": "Comment les systèmes IT sont-ils structurés ?", "category": "Architecture Systèmes"},
    {"question": "Qu'est-ce que l'univers Unix et son importance ?", "category": "Architecture Systèmes"},
    {"question": "Comment fonctionne le protocole IP ?", "category": "Architecture Systèmes"},
    {"question": "Qu'est-ce que les technologies vieillissantes en IT ?", "category": "Architecture Systèmes"},
    {"question": "Quelle est l'évolution de Windows NT à Windows 11 ?", "category": "Architecture Systèmes"},
    {"question": "Comment créer une nouvelle version Android ?", "category": "Architecture Systèmes"},
    {"question": "Comment vivre à l'ère d'Internet ?", "category": "Architecture Systèmes"},
    {"question": "Quel est le rôle de YouTube dans l'écosystème IT ?", "category": "Architecture Systèmes"},
    
    # Chapter 8: The Human Factor
    {"question": "Comment le facteur humain affecte-t-il les systèmes IT ?", "category": "Facteur Humain"},
    {"question": "Pourquoi les utilisateurs causent-ils des problèmes aux systèmes IT ?", "category": "Facteur Humain"},
    {"question": "Quels sont les problèmes matériels causés par les utilisateurs ?", "category": "Facteur Humain"},
    {"question": "Quels sont les problèmes logiciels causés par les utilisateurs ?", "category": "Facteur Humain"},
    {"question": "Comment les paramètres mal configurés causent-ils des problèmes ?", "category": "Facteur Humain"},
    {"question": "Comment l'IT et l'accessibilité sont-ils liés ?", "category": "Facteur Humain"},
    {"question": "Pourquoi les utilisateurs ne sont-ils pas des professionnels IT ?", "category": "Facteur Humain"},
    {"question": "Qu'est-ce que le 'monkey mind' en IT support ?", "category": "Facteur Humain"},
    {"question": "Pourquoi les gens sont-ils complexes en support IT ?", "category": "Facteur Humain"},
    
    # Chapter 9: The Peripheral Problem
    {"question": "Qu'est-ce que le problème des périphériques ?", "category": "Matériel & Périphériques"},
    {"question": "Comment ajouter des périphériques legacy à Windows ?", "category": "Matériel & Périphériques"},
    {"question": "Comment configurer et dépanner les périphériques legacy ?", "category": "Matériel & Périphériques"},
    {"question": "Comment résoudre les problèmes de pilotes de périphériques ?", "category": "Matériel & Périphériques"},
    {"question": "Quels autres problèmes peuvent survenir avec les périphériques ?", "category": "Matériel & Périphériques"},
    
    # Chapter 10: Building and Environmental Factors
    {"question": "Comment les facteurs environnementaux affectent-ils les systèmes IT ?", "category": "Infrastructure & Environnement"},
    {"question": "Quel est l'impact de la météo sur les équipements IT ?", "category": "Infrastructure & Environnement"},
    {"question": "Comment le sable, la poussière, l'eau et l'humidité affectent-ils le matériel ?", "category": "Infrastructure & Environnement"},
    {"question": "Quel est l'impact de l'environnement du bâtiment sur l'IT ?", "category": "Infrastructure & Environnement"},
    {"question": "Où placer les équipements Wi-Fi de manière optimale ?", "category": "Infrastructure & Environnement"},
    {"question": "Quel est le rôle du Bluetooth et du réseau cellulaire ?", "category": "Infrastructure & Environnement"},
    {"question": "Quelle est la différence entre la ville et la campagne pour l'IT ?", "category": "Infrastructure & Environnement"},
    
    # Part IV: Documentation
    
    # Chapter 11: Why Good Documentation Matters
    {"question": "Pourquoi une bonne documentation est-elle importante ?", "category": "Documentation"},
    {"question": "Comment la documentation fait-elle gagner du temps et de l'argent ?", "category": "Documentation"},
    {"question": "Comment utiliser la documentation pour la formation ?", "category": "Documentation"},
    {"question": "Comment simplifier les choses dans la documentation ?", "category": "Documentation"},
    {"question": "Comment documenter pour le dépannage ?", "category": "Documentation"},
    {"question": "Quel est le rôle du personnel et des SLA dans la documentation ?", "category": "Documentation"},
    {"question": "Comment se conformer aux exigences de documentation ?", "category": "Documentation"},
    {"question": "Comment créer des solutions d'ingénierie documentées ?", "category": "Documentation"},
    {"question": "Comment garder la documentation claire et concise ?", "category": "Documentation"},
    
    # Chapter 12: Creating Troubleshooting Guides
    {"question": "Comment créer des guides de dépannage efficaces ?", "category": "Guides & Procédures"},
    {"question": "Comment rendre les guides clairs, concis et faciles à comprendre ?", "category": "Guides & Procédures"},
    {"question": "Comment utiliser la logique de flux dans les guides ?", "category": "Guides & Procédures"},
    {"question": "Qu'est-ce que le problème Dev en documentation ?", "category": "Guides & Procédures"},
    {"question": "Comment raconter une histoire dans un guide de dépannage ?", "category": "Guides & Procédures"},
    
    # Chapter 13: Creating and Managing Paperwork
    {"question": "Comment créer et gérer la paperasse du support IT ?", "category": "Gestion Administrative"},
    {"question": "Qu'est-ce que le paperwork de première ligne ?", "category": "Gestion Administrative"},
    {"question": "Qu'est-ce que le paperwork de deuxième et troisième ligne ?", "category": "Gestion Administrative"},
    {"question": "Comment gérer le paperwork des ingénieurs ?", "category": "Gestion Administrative"},
    {"question": "Quels formulaires et rapports additionnels sont nécessaires ?", "category": "Gestion Administrative"},
    
    # Chapter 14: Harnessing System Tools in Windows
    {"question": "Comment exploiter les outils système de Windows ?", "category": "Outils Windows"},
    {"question": "Comment consulter l'historique de fiabilité Windows ?", "category": "Outils Windows"},
    {"question": "Comment utiliser les outils administratifs de Windows ?", "category": "Outils Windows"},
    {"question": "Comment utiliser l'outil Information Système ?", "category": "Outils Windows"},
    {"question": "Comment utiliser le Moniteur de Performance ?", "category": "Outils Windows"},
    {"question": "Comment utiliser l'Observateur d'événements ?", "category": "Outils Windows"},
    {"question": "Quel est le rôle du Gestionnaire des tâches ?", "category": "Outils Windows"},
    
    # Chapter 15: Advanced Error and Status Information
    {"question": "Comment obtenir des informations avancées sur les erreurs et le statut ?", "category": "Diagnostics Avancés"},
    {"question": "Comment obtenir des informations détaillées sur les erreurs ?", "category": "Diagnostics Avancés"},
    {"question": "Comment copier et sauvegarder les détails d'événements ?", "category": "Diagnostics Avancés"},
    {"question": "Comment se connecter au journal d'événements sur un autre PC ?", "category": "Diagnostics Avancés"},
    {"question": "Comment trouver d'autres journaux d'erreurs Windows ?", "category": "Diagnostics Avancés"},
    {"question": "Comment utiliser les fichiers journaux texte ?", "category": "Diagnostics Avancés"},
    {"question": "Comment utiliser les fichiers journaux XML et ETL ?", "category": "Diagnostics Avancés"},
    {"question": "Comment analyser les fichiers Dmp ?", "category": "Diagnostics Avancés"},
    
    # Chapter 17: Gathering Information Remotely
    {"question": "Comment collecter des informations à distance ?", "category": "Administration Distante"},
    {"question": "Comment commencer avec l'Asset Tag ?", "category": "Administration Distante"},
    {"question": "Comment permettre l'administration distante des PC ?", "category": "Administration Distante"},
    {"question": "Comment se connecter au registre en tant qu'autre utilisateur ?", "category": "Administration Distante"},
    {"question": "Comment utiliser la Console de Gestion Microsoft à distance ?", "category": "Administration Distante"},
    
    # Chapter 18: Helping Users to Help You
    {"question": "Comment aider les utilisateurs à vous aider ?", "category": "Assistance Utilisateurs"},
    {"question": "Comment utiliser l'enregistreur d'étapes de problèmes ?", "category": "Assistance Utilisateurs"},
    {"question": "Comment sauvegarder des captures d'écran ?", "category": "Assistance Utilisateurs"},
    {"question": "Comment utiliser le screencasting ?", "category": "Assistance Utilisateurs"},
    {"question": "Comment utiliser la barre de jeu Xbox pour capturer des problèmes ?", "category": "Assistance Utilisateurs"},
]

# Pour compatibilité avec le clustering
questions = [q["question"] for q in questions_data]