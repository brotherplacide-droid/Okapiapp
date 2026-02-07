import streamlit as st
import json

st.title("📦 AGENCE OKAPI UVIRA")

# Charger les colis depuis le fichier JSON (sans fonction)
try:
    with open("registre_colis.json", "r", encoding="utf-8") as f:
        liste_colis = json.load(f)
except FileNotFoundError:
    liste_colis = []

# === Menu principal ===
menu = st.sidebar.radio("MENU PRINCIPAL", 
                        ["🏷️ Enregistrer un envoi", 
                         "📋 Afficher la liste des colis", 
                         "✅ Livrer un colis"])

# === ENREGISTRER UN ENVOI ===
if menu : 
    st.subheader("Enregistrement d’un nouvel envoi")

    expediteur_nom = st.text_input("Nom de l’expéditeur")
    expediteur_prenom = st.text_input("Prénom de l’expéditeur")
    expediteur_carte = st.text_input("Carte expéditeur (10 chiffres)")

    destinataire_nom = st.text_input("Nom du destinataire")
    destinataire_prenom = st.text_input("Prénom du destinataire")
    destinataire_carte = st.text_input("Carte destinataire (10 chiffres)")

    code = st.text_input("Code du colis (10 chiffres)")
    carte_electeur = st.text_input("Carte électeur (chiffres uniquement)")
    poids = st.number_input("Poids (kg)", min_value=0)
    valeur = st.number_input("Valeur déclarée", min_value=0)
    tarif = st.number_input("Tarif", min_value=0)
    ville_depart = st.text_input("Ville de départ")
    ville_arrivee = st.text_input("Ville d’arrivée")

    if st.button("📌 Enregistrer"):
        if not (expediteur_carte.isdigit() and len(expediteur_carte) == 10):
            st.error("Carte expéditeur invalide (10 chiffres).")
        elif not (destinataire_carte.isdigit() and len(destinataire_carte) == 10):
            st.error("Carte destinataire invalide (10 chiffres).")
        elif not (code.isdigit() and len(code) == 10):
            st.error("Code colis invalide (10 chiffres).")
        elif not carte_electeur.isdigit():
            st.error("Carte électeur invalide (chiffres uniquement).")
        else:
            colis = {
                "code": code,
                "carte_electeur": carte_electeur,
                "poids": poids,
                "valeur": valeur,
                "tarif": tarif,
                "depart": ville_depart,
                "arrivee": ville_arrivee,
                "expediteur": f"{expediteur_nom} {expediteur_prenom}",
                "destinataire": f"{destinataire_nom} {destinataire_prenom}"
            }
            liste_colis.append(colis)
            with open("registre_colis.json", "w", encoding="utf-8") as f:
                json.dump(liste_colis, f, ensure_ascii=False, indent=4)
            st.success(f"✅ Colis {code} enregistré avec succès !")

# === AFFICHER LA LISTE DES COLIS ===
elif menu.startswith("📋"):
    st.subheader("Liste des colis enregistrés")
    if not liste_colis:
        st.info("Aucun colis enregistré.")
    else:
        for i, colis in enumerate(liste_colis, start=1):
            st.markdown(f"""
            ### 📦 Colis {i}
            - **Code** : {colis['code']}
            - **Expéditeur** : {colis['expediteur']}
            - **Destinataire** : {colis['destinataire']}
            - **Carte électeur** : {colis['carte_electeur']}
            - **Poids** : {colis['poids']} kg
            - **Valeur déclarée** : {colis['valeur']}
            - **Ville départ** : {colis['depart']}
            - **Ville arrivée** : {colis['arrivee']}
            - **Tarif** : {colis['tarif']}
            """)

# === LIVRER UN COLIS ===
elif menu.startswith("✅"):
    st.subheader("Livraison d’un colis")

    code_livraison = st.text_input("Code du colis à livrer")
    collecteur_nom = st.text_input("Nom du collecteur")
    collecteur_prenom = st.text_input("Prénom du collecteur")
    collecteur_carte = st.text_input("Carte du collecteur")

    if st.button("🚚 Livrer"):
        colis_trouve = next((c for c in liste_colis if c["code"] == code_livraison), None)
        if not colis_trouve:
            st.error(f"Colis {code_livraison} introuvable.")
        elif not collecteur_nom or not collecteur_prenom or not collecteur_carte:
            st.error("Informations du collecteur incomplètes.")
        else:
            liste_colis.remove(colis_trouve)
            with open("registre_colis.json", "w", encoding="utf-8") as f:
                json.dump(liste_colis, f, ensure_ascii=False, indent=4)
            st.success(f"✅ Colis {code_livraison} livré et retiré de la liste.")
