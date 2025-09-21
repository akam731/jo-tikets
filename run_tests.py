#!/usr/bin/env python
"""
Script pour lancer les tests de l'application JO Tickets.

Usage:
    python run_tests.py                    # Tous les tests
    python run_tests.py --unit             # Tests unitaires seulement
    python run_tests.py --functional       # Tests fonctionnels seulement
    python run_tests.py --selenium         # Tests Selenium seulement
    python run_tests.py --coverage         # Tests avec couverture de code
"""
import os
import sys
import subprocess
import argparse


def run_command(command):
    """Exécute une commande et retourne le code de sortie."""
    print(f"Exécution: {' '.join(command)}")
    result = subprocess.run(command, capture_output=False)
    return result.returncode


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Lancer les tests de JO Tickets")
    parser.add_argument(
        "--unit", action="store_true", help="Lancer les tests unitaires seulement"
    )
    parser.add_argument(
        "--functional",
        action="store_true",
        help="Lancer les tests fonctionnels seulement",
    )
    parser.add_argument(
        "--selenium", action="store_true", help="Lancer les tests Selenium seulement"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Générer un rapport de couverture"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")

    args = parser.parse_args()

    # Configuration Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jo_tickets.settings")

    # Commandes de base
    base_command = ["python", "manage.py", "test"]

    if args.verbose:
        base_command.extend(["-v", "2"])

    # Sélection des tests
    if args.unit:
        base_command.append("tests.unit")
        print("Lancement des tests unitaires...")
    elif args.functional:
        base_command.append(
            "tests.functional.test_user_registration.UserRegistrationFunctionalTest"
        )
        print("Lancement des tests fonctionnels...")
    elif args.selenium:
        base_command.append(
            "tests.functional.test_user_registration.UserRegistrationSeleniumTest"
        )
        print("Lancement des tests Selenium...")
    else:
        base_command.extend(
            [
                "tests.unit",
                "tests.functional.test_user_registration.UserRegistrationFunctionalTest",
            ]
        )
        print("Lancement de tous les tests...")

    # Exécution des tests
    exit_code = run_command(base_command)

    # Rapport de couverture si demandé
    if args.coverage:
        print("\nGénération du rapport de couverture...")
        coverage_command = [
            "coverage",
            "run",
            "--source=.",
            "manage.py",
            "test",
            "tests.unit",
            "tests.functional",
        ]
        run_command(coverage_command)

        print("Affichage du rapport de couverture...")
        run_command(["coverage", "report"])
        run_command(["coverage", "html"])
        print("Rapport HTML généré dans htmlcov/index.html")

    if exit_code == 0:
        print("Tous les tests sont passés avec succès!")
    else:
        print("Certains tests ont échoué.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
