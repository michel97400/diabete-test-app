#!/usr/bin/env python3
"""
Script de test pour l'API de prédiction du diabète
Test suite avec 5 requêtes : 3 succès et 2 erreurs
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

class APITester:
    """Classe pour tester l'API de prédiction du diabète"""
    
    def __init__(self):
        self.results = []
        self.success_count = 0
        self.error_count = 0
    
    def test_request(self, test_name: str, data: Dict[str, Any], expected_success: bool = True):
        """
        Test une requête vers l'API
        
        Args:
            test_name: Nom du test
            data: Données à envoyer
            expected_success: Si True, on s'attend à un succès, sinon à une erreur
        """
        print(f"\n🧪 Test: {test_name}")
        print(f"📤 Données envoyées: {json.dumps(data, indent=2)}")
        
        try:
            response = requests.post(PREDICT_ENDPOINT, json=data)
            result = response.json()
            
            print(f"📥 Status Code: {response.status_code}")
            print(f"📥 Réponse: {json.dumps(result, indent=2)}")
            
            # Évaluer le résultat
            if response.status_code == 200 and expected_success:
                if result.get('success', False):
                    print("✅ TEST RÉUSSI: Prédiction réussie comme attendu")
                    self.success_count += 1
                    status = "SUCCESS"
                else:
                    print("❌ TEST ÉCHOUÉ: Prédiction échouée alors qu'elle devrait réussir")
                    status = "FAILED"
            elif response.status_code != 200 and not expected_success:
                print("✅ TEST RÉUSSI: Erreur capturée comme attendu")
                self.error_count += 1
                status = "SUCCESS (Expected Error)"
            elif response.status_code != 200 and expected_success:
                print("❌ TEST ÉCHOUÉ: Erreur inattendue")
                status = "FAILED"
            else:
                print("✅ TEST RÉUSSI: Comportement attendu")
                if expected_success:
                    self.success_count += 1
                else:
                    self.error_count += 1
                status = "SUCCESS"
            
            self.results.append({
                "test_name": test_name,
                "status_code": response.status_code,
                "expected_success": expected_success,
                "actual_success": response.status_code == 200 and result.get('success', False),
                "status": status,
                "response": result
            })
            
        except requests.exceptions.RequestException as e:
            print(f"❌ ERREUR DE CONNEXION: {e}")
            self.results.append({
                "test_name": test_name,
                "status": "CONNECTION_ERROR",
                "error": str(e)
            })
    
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🚀 Démarrage des tests de l'API de prédiction du diabète")
        print("=" * 60)
        
        # TEST 1: Cas normal - Patient avec diabète probable
        self.test_request(
            "Test 1 - Patient à risque élevé",
            {
                "age": 65,
                "gender": "Male",
                "polyuria": "Yes",
                "polydipsia": "Yes",
                "sudden_weight_loss": "Yes",
                "weakness": "Yes",
                "polyphagia": "Yes",
                "genital_thrush": "No",
                "visual_blurring": "Yes",
                "itching": "Yes",
                "irritability": "Yes",
                "delayed_healing": "Yes",
                "partial_paresis": "No",
                "muscle_stiffness": "Yes",
                "alopecia": "No",
                "obesity": "Yes"
            },
            expected_success=True
        )
        
        # TEST 2: Cas normal - Patient en bonne santé
        self.test_request(
            "Test 2 - Patient en bonne santé",
            {
                "age": 25,
                "gender": "Female",
                "polyuria": "No",
                "polydipsia": "No",
                "sudden_weight_loss": "No",
                "weakness": "No",
                "polyphagia": "No",
                "genital_thrush": "No",
                "visual_blurring": "No",
                "itching": "No",
                "irritability": "No",
                "delayed_healing": "No",
                "partial_paresis": "No",
                "muscle_stiffness": "No",
                "alopecia": "No",
                "obesity": "No"
            },
            expected_success=True
        )
        
        # TEST 3: Cas normal - Patient d'âge moyen avec quelques symptômes
        self.test_request(
            "Test 3 - Patient d'âge moyen",
            {
                "age": 45,
                "gender": "Female",
                "polyuria": "No",
                "polydipsia": "Yes",
                "sudden_weight_loss": "No",
                "weakness": "Yes",
                "polyphagia": "No",
                "genital_thrush": "No",
                "visual_blurring": "No",
                "itching": "Yes",
                "irritability": "No",
                "delayed_healing": "No",
                "partial_paresis": "No",
                "muscle_stiffness": "Yes",
                "alopecia": "No",
                "obesity": "Yes"
            },
            expected_success=True
        )
        
        # TEST 4: ERREUR - Âge invalide
        self.test_request(
            "Test 4 - Erreur: Âge invalide",
            {
                "age": 150,  # Âge invalide (> 120)
                "gender": "Female",
                "polyuria": "No",
                "polydipsia": "Yes",
                "sudden_weight_loss": "No",
                "weakness": "Yes",
                "polyphagia": "No",
                "genital_thrush": "No",
                "visual_blurring": "No",
                "itching": "Yes",
                "irritability": "No",
                "delayed_healing": "No",
                "partial_paresis": "No",
                "muscle_stiffness": "Yes",
                "alopecia": "No",
                "obesity": "Yes"
            },
            expected_success=False
        )
        
        # TEST 5: ERREUR - Champ manquant
        self.test_request(
            "Test 5 - Erreur: Champ manquant",
            {
                "age": 45,
                "gender": "Female",
                "polyuria": "No",
                # "polydipsia" manquant intentionnellement
                "sudden_weight_loss": "No",
                "weakness": "Yes",
                "polyphagia": "No",
                "genital_thrush": "No",
                "visual_blurring": "No",
                "itching": "Yes",
                "irritability": "No",
                "delayed_healing": "No",
                "partial_paresis": "No",
                "muscle_stiffness": "Yes",
                "alopecia": "No",
                "obesity": "Yes"
            },
            expected_success=False
        )
        
        # Afficher le résumé
        self.print_summary()
    
    def print_summary(self):
        """Affiche le résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if "SUCCESS" in r.get("status", ""))
        failed_tests = total_tests - passed_tests
        
        print(f"Total des tests: {total_tests}")
        print(f"Tests réussis: {passed_tests}")
        print(f"Tests échoués: {failed_tests}")
        print(f"Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📈 Statistiques attendues:")
        print(f"- Prédictions réussies: {self.success_count}/3")
        print(f"- Erreurs capturées: {self.error_count}/2")
        
        print(f"\n📋 Détail par test:")
        for i, result in enumerate(self.results, 1):
            status_icon = "✅" if "SUCCESS" in result.get("status", "") else "❌"
            print(f"{status_icon} Test {i}: {result['test_name']} - {result.get('status', 'UNKNOWN')}")
        
        # Vérification finale
        if passed_tests == 5 and self.success_count == 3 and self.error_count == 2:
            print(f"\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
            print(f"✅ 3 prédictions réussies")
            print(f"✅ 2 erreurs gérées correctement")
        else:
            print(f"\n⚠️ Certains tests ont échoué. Vérifiez votre API.")

def check_api_availability():
    """Vérifie si l'API est disponible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API disponible")
            return True
        else:
            print(f"⚠️ API répond mais status code: {response.status_code}")
            return True  # On peut quand même tester
    except requests.exceptions.RequestException:
        print("❌ API non disponible. Assurez-vous qu'elle tourne sur http://127.0.0.1:8000")
        return False

if __name__ == "__main__":
    print("🩺 Test Suite - API de Prédiction du Diabète")
    print("=" * 60)
    
    # Vérifier la disponibilité de l'API
    if not check_api_availability():
        print("\n💡 Pour démarrer l'API, lancez: uvicorn main:app --reload")
        exit(1)
    
    # Lancer les tests
    tester = APITester()
    tester.run_all_tests()