from langflow.custom import Component
from langflow.io import Output, MessageTextInput
from langflow.schema import Data
import requests

class EnvoyerDonneesVerreTableComponent(Component):
    display_name = "Envoyer Données Verre à la Table"
    description = "Envoyer la composition détaillée du verre et les informations de référence du document au serveur Flask."
    icon = "table"

    inputs = [
        MessageTextInput(
            name="texte_extrait",
            display_name="Texte Extrait",
            info=(
                "Texte extrait contenant la référence du document et les informations sur la composition du verre."
            ),
            value=(
                "1. Type du document : Article scientifique\n"
                "2. Titre du document : Can a simple topological-constraints-based model predict the initial dissolution rate of borosilicate and aluminosilicate glasses?\n"
                "3. Référence : npj Materials Degradation (2020) 4:6 ; https://doi.org/10.1038/s41529-020-0111-4\n"
                "4. Premier Auteur : Stéphane Gin\n"
                "5. Nombre de types de verres : 3\n"
                "6. Verre_type1 : [Type1]\n"
                "7. SiO₂(Verre_type1) : [Valeur]\n"
                "8. B₂O₃(Verre_type1) : [Valeur]\n"
                "9. Na₂O(Verre_type1) : [Valeur]\n"
                "10. Al₂O₃(Verre_type1) : [Valeur]\n"
                "11. CaO(Verre_type1) : [Valeur]\n"
                "12. ZrO₂(Verre_type1) : [Valeur]\n"
                "13. Ce₂O₃(Verre_type1) : [Valeur]\n"
                "14. Li₂O(Verre_type1) : [Valeur]\n"
                "15. Fe₂O₃(Verre_type1) : [Valeur]\n"
                "16. ZnO(Verre_type1) : [Valeur]\n"
                "17. P₂O₅(Verre_type1) : [Valeur]\n"
                "18. MoO₃(Verre_type1) : [Valeur]\n"
                "19. TiO₂(Verre_type1) : [Valeur]\n"
                "20. MgO(Verre_type1) : [Valeur]\n"
                "21. Fines(Verre_type1) : [Valeur]\n"
                "22. Autres(Verre_type1) : [Valeur]\n"
                "23. Somme(Verre_type1) : [Valeur]\n"
                "24. Densité(Verre_type1) : [Valeur]\n"
                "25. Homogénéité(Verre_type1) : [Commentaire]\n"
                "26. % B(IV)(Verre_type1) : [Valeur]\n"
                "27. Irradié(Verre_type1) : [O/N]\n"
                "28. Caractéristiques si irradié(Verre_type1) : [Commentaire]\n"
                "29. Température(Verre_type1) : [Valeur]\n"
                "30. Statique/dynamique(Verre_type1) : [Commentaire]\n"
                "31. Plage granulométrique (si poudre)(Verre_type1) : [Valeur]\n"
                "32. Surface spécifique géométrique (si poudre)(Verre_type1) : [Valeur]\n"
                "33. Surface spécifique BET (si poudre)(Verre_type1) : [Valeur]\n"
                "34. Qualité de polissage (si monolithe)(Verre_type1) : [Commentaire]\n"
                "35. Masse du verre(Verre_type1) : [Valeur]\n"
                "36. Surface du verre (S)(Verre_type1) : [Valeur]\n"
                "37. Volume de la solution (V)(Verre_type1) : [Valeur]\n"
                "38. Débit de la solution(Verre_type1) : [Valeur]\n"
                "39. pH initial (T amb)(Verre_type1) : [Valeur]\n"
                "40. pH initial (T essai)(Verre_type1) : [Valeur]\n"
                "41. Composition de la solution(Verre_type1) : [Commentaire]\n"
                "42. Durée de l'expérience(Verre_type1) : [Valeur]\n"
                "43. pH final (T amb)(Verre_type1) : [Valeur]\n"
                "44. pH final (T essai)(Verre_type1) : [Valeur]\n"
                "45. Normalisation de la vitesse (Sgeo ou SBET)(Verre_type1) : [Valeur]\n"
                "46. V₀(Si) ou r₀(Si)(Verre_type1) : [Valeur]\n"
                "47. r²(Si)(Verre_type1) : [Valeur]\n"
                "48. Ordonnée à l'origine (Si)(Verre_type1) : [Valeur]\n"
                "49. V₀(B) ou r₀(B)(Verre_type1) : [Valeur]\n"
                "50. Ordonnée à l'origine (B)(Verre_type1) : [Valeur]\n"
                "51. V₀(Na) ou r₀(Na)(Verre_type1) : [Valeur]\n"
                "52. r²(Na)(Verre_type1) : [Valeur]\n"
                "53. Ordonnée à l'origine (Na)(Verre_type1) : [Valeur]\n"
                "54. V₀(ΔM) ou r₀(ΔM)(Verre_type1) : [Valeur]\n"
                "55. Congruence(Verre_type1) : [Commentaire ou valeur numérique]\n"
                "..."
            ),
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Réponse", name="sortie", method="construire_sortie"),
    ]

    def construire_sortie(self) -> Data:
        texte_extrait = self.texte_extrait
        print(f"Texte Extrait: {texte_extrait}")

        try:
            # Nettoyer et analyser le texte
            lignes = [ligne.strip() for ligne in texte_extrait.split("\n") if ligne.strip()]

            # Extraction des données générales
            type_doc = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("1. Type du document :")), None)
            titre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("2. Titre du document :")), None)
            reference = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("3. Référence :")), None)
            premier_auteur = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("4. Premier Auteur :")), None)
            nombre_types_verres = int(next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("5. Nombre de types de verres :")), None))

            # Initialisation des données pour chaque type de verre
            donnees_verres = []

            for i in range(nombre_types_verres):
                verre_data = {}
                verre_type_key = f"Verre_type{i+1}"
                verre_data["type"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{6 + i * 50}. {verre_type_key} :")), None)

                # Extraction des caractéristiques pour chaque type de verre
                verre_data["sio2"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{7 + i * 50}. SiO₂({verre_type_key}) :")), None)
                verre_data["b2o3"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{8 + i * 50}. B₂O₃({verre_type_key}) :")), None)
                verre_data["na2o"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{9 + i * 50}. Na₂O({verre_type_key}) :")), None)
                verre_data["al2o3"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{10 + i * 50}. Al₂O₃({verre_type_key}) :")), None)
                verre_data["cao"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{11 + i * 50}. CaO({verre_type_key}) :")), None)
                verre_data["zro2"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{12 + i * 50}. ZrO₂({verre_type_key}) :")), None)
                verre_data["ce2o3"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{13 + i * 50}. Ce₂O₃({verre_type_key}) :")), None)
                verre_data["lio2"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{14 + i * 50}. Li₂O({verre_type_key}) :")), None)
                verre_data["fe2o3"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{15 + i * 50}. Fe₂O₃({verre_type_key}) :")), None)
                verre_data["zno"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{16 + i * 50}. ZnO({verre_type_key}) :")), None)
                verre_data["p2o5"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{17 + i * 50}. P₂O₅({verre_type_key}) :")), None)
                verre_data["mo3"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{18 + i * 50}. MoO₃({verre_type_key}) :")), None)
                verre_data["tio2"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{19 + i * 50}. TiO₂({verre_type_key}) :")), None)
                verre_data["mgo"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{20 + i * 50}. MgO({verre_type_key}) :")), None)
                verre_data["fines"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{21 + i * 50}. Fines({verre_type_key}) :")), None)
                verre_data["autres"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{22 + i * 50}. Autres({verre_type_key}) :")), None)
                verre_data["somme"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{23 + i * 50}. Somme({verre_type_key}) :")), None)
                verre_data["densite"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{24 + i * 50}. Densité({verre_type_key}) :")), None)
                verre_data["homogeneite"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{25 + i * 50}. Homogénéité({verre_type_key}) :")), None)
                verre_data["b_iv_pourcent"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{26 + i * 50}. % B(IV)({verre_type_key}) :")), None)
                verre_data["irradie"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{27 + i * 50}. Irradié({verre_type_key}) :")), None)
                verre_data["caracteristiques_irradie"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{28 + i * 50}. Caractéristiques si irradié({verre_type_key}) :")), None)
                verre_data["temperature"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{29 + i * 50}. Température({verre_type_key}) :")), None)
                verre_data["statique_dynamique"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{30 + i * 50}. Statique/dynamique({verre_type_key}) :")), None)
                verre_data["plage_granulo"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{31 + i * 50}. Plage granulométrique (si poudre)({verre_type_key}) :")), None)
                verre_data["surface_specifique_geometrique"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{32 + i * 50}. Surface spécifique géométrique (si poudre)({verre_type_key}) :")), None)
                verre_data["surface_specifique_bet"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{33 + i * 50}. Surface spécifique BET (si poudre)({verre_type_key}) :")), None)
                verre_data["qualite_polissage"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{34 + i * 50}. Qualité de polissage (si monolithe)({verre_type_key}) :")), None)
                verre_data["masse_verre"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{35 + i * 50}. Masse du verre({verre_type_key}) :")), None)
                verre_data["s_verre"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{36 + i * 50}. Surface du verre (S)({verre_type_key}) :")), None)
                verre_data["v_solution"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{37 + i * 50}. Volume de la solution (V)({verre_type_key}) :")), None)
                verre_data["debit_solution"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{38 + i * 50}. Débit de la solution({verre_type_key}) :")), None)
                verre_data["ph_initial"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{39 + i * 50}. pH initial (T amb)({verre_type_key}) :")), None)
                verre_data["ph_initial_test"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{40 + i * 50}. pH initial (T essai)({verre_type_key}) :")), None)
                verre_data["composition_solution"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{41 + i * 50}. Composition de la solution({verre_type_key}) :")), None)
                verre_data["duree_experience"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{42 + i * 50}. Durée de l'expérience({verre_type_key}) :")), None)
                verre_data["ph_final_amb"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{43 + i * 50}. pH final (T amb)({verre_type_key}) :")), None)
                verre_data["ph_final_test"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{44 + i * 50}. pH final (T essai)({verre_type_key}) :")), None)
                verre_data["normalisation_vitesse"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{45 + i * 50}. Normalisation de la vitesse (Sgeo ou SBET)({verre_type_key}) :")), None)
                verre_data["v0_si"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{46 + i * 50}. V₀(Si) ou r₀(Si)({verre_type_key}) :")), None)
                verre_data["r_carre_si"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{47 + i * 50}. r²(Si)({verre_type_key}) :")), None)
                verre_data["ordonnee_origine_si"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{48 + i * 50}. Ordonnée à l'origine (Si)({verre_type_key}) :")), None)
                verre_data["v0_b"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{49 + i * 50}. V₀(B) ou r₀(B)({verre_type_key}) :")), None)
                verre_data["ordonnee_origine_b"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{50 + i * 50}. Ordonnée à l'origine (B)({verre_type_key}) :")), None)
                verre_data["v0_na"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{51 + i * 50}. V₀(Na) ou r₀(Na)({verre_type_key}) :")), None)
                verre_data["r_carre_na"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{52 + i * 50}. r²(Na)({verre_type_key}) :")), None)
                verre_data["ordonnee_origine_na"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{53 + i * 50}. Ordonnée à l'origine (Na)({verre_type_key}) :")), None)
                verre_data["v0_dm"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{54 + i * 50}. V₀(ΔM) ou r₀(ΔM)({verre_type_key}) :")), None)
                verre_data["congruence"] = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{55 + i * 50}. Congruence({verre_type_key}) :")), None)

                donnees_verres.append(verre_data)

            # Préparer les données
            url = 'http://127.0.0.1:5001/add_glass_data'
            donnees = {
                "type": type_doc,
                "titre": titre,
                "reference": reference,
                "premier_auteur": premier_auteur,
                "nombre_types_verres": nombre_types_verres,
                "verres": donnees_verres
            }
            print(f"Envoi des données: {donnees}")

            reponse = requests.post(url, json=donnees)

            if reponse.status_code == 200:
                return Data(value="Données du verre ajoutées avec succès!")
            else:
                return Data(value=f"Erreur lors de l'ajout des données du verre. Code d'état: {reponse.status_code} - {reponse.text}")

        except Exception as e:
            return Data(value=f"Exception survenue: {str(e)}")
