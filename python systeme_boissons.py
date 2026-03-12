# ============================================================
# SYSTEME DE BOISSONS - POO Python
# TP MI-GUIDE | Licence Développement Web Avancé
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ============================================================
# PARTIE 1 : Classe abstraite Boisson
# ============================================================

class Boisson(ABC):
    """Classe abstraite représentant une boisson générique."""

    @abstractmethod
    def cout(self):
        """Retourne le prix de la boisson."""
        pass

    @abstractmethod
    def description(self):
        """Retourne la description de la boisson."""
        pass

    def afficher_commande(self):
        """Affiche les informations complètes de la boisson."""
        print(f"Commande : {self.description()}")
        print(f"Prix : {self.cout():.1f}€")

    # PARTIE 4 : Combinaison de boissons avec l'opérateur +
    def __add__(self, other):
        """Permet de combiner deux boissons avec l'opérateur +."""
        desc_combinee = self.description() + " + " + other.description()
        prix_total = self.cout() + other.cout()

        # On crée une boisson concrète combinée à la volée
        class BoissonCombinee(Boisson):
            def cout(self):
                return prix_total
            def description(self):
                return desc_combinee

        return BoissonCombinee()


# ============================================================
# PARTIE 2 : Boissons concrètes
# ============================================================

class Cafe(Boisson):
    """Représente un café simple."""

    def cout(self):
        return 2.0

    def description(self):
        return "Café simple"


class The(Boisson):
    """Représente un thé."""

    def cout(self):
        return 1.5

    def description(self):
        return "Thé"


class ChocolatChaud(Boisson):
    """Représente un chocolat chaud."""

    def cout(self):
        return 2.5

    def description(self):
        return "Chocolat chaud"


# ============================================================
# PARTIE 3 : Décorateurs d'ingrédients
# ============================================================

class DecorateurBoisson(Boisson):
    """Classe de base pour les décorateurs d'ingrédients."""

    def __init__(self, boisson):
        self._boisson = boisson


class Lait(DecorateurBoisson):
    """Ajoute du lait à une boisson (+0.5€)."""

    def cout(self):
        return self._boisson.cout() + 0.5

    def description(self):
        return self._boisson.description() + ", Lait"


class Sucre(DecorateurBoisson):
    """Ajoute du sucre à une boisson (+0.2€)."""

    def cout(self):
        return self._boisson.cout() + 0.2

    def description(self):
        return self._boisson.description() + ", Sucre"


class Caramel(DecorateurBoisson):
    """Ajoute du caramel à une boisson (+0.7€)."""

    def cout(self):
        return self._boisson.cout() + 0.7

    def description(self):
        return self._boisson.description() + ", Caramel"


# ============================================================
# PARTIE 5 : Représentation d'un client (dataclass)
# ============================================================

@dataclass
class Client:
    nom: str
    numero: int
    points_fidelite: int = 0


# ============================================================
# PARTIE 7 : Gestion des commandes
# ============================================================

class Commande:
    """Représente une commande passée par un client."""

    def __init__(self, client: Client):
        self.client = client
        self.boissons = []

    def ajouter_boisson(self, boisson: Boisson):
        """Ajoute une boisson à la commande."""
        self.boissons.append(boisson)

    def prix_total(self):
        """Calcule le prix total de la commande."""
        return sum(b.cout() for b in self.boissons)

    def afficher(self):
        """Affiche le contenu de la commande."""
        print(f"\n{'='*45}")
        print(f"  Commande de : {self.client.nom} (N°{self.client.numero})")
        print(f"{'='*45}")
        for b in self.boissons:
            print(f"  - {b.description()} : {b.cout():.1f}€")
        print(f"{'─'*45}")
        print(f"  TOTAL : {self.prix_total():.1f}€")
        print(f"{'='*45}")


class CommandeSurPlace(Commande):
    """Commande consommée sur place."""

    def afficher(self):
        print(f"\n{'='*45}")
        print(f"  [SUR PLACE] Commande de : {self.client.nom}")
        print(f"{'='*45}")
        for b in self.boissons:
            print(f"  - {b.description()} : {b.cout():.1f}€")
        print(f"{'─'*45}")
        print(f"  TOTAL : {self.prix_total():.1f}€")
        print(f"  Service en salle inclus.")
        print(f"{'='*45}")


class CommandeEmporter(Commande):
    """Commande à emporter."""

    def afficher(self):
        print(f"\n{'='*45}")
        print(f"  [A EMPORTER] Commande de : {self.client.nom}")
        print(f"{'='*45}")
        for b in self.boissons:
            print(f"  - {b.description()} : {b.cout():.1f}€")
        print(f"{'─'*45}")
        print(f"  TOTAL : {self.prix_total():.1f}€")
        print(f"  Emballage eco-friendly fourni.")
        print(f"{'='*45}")


# ============================================================
# PARTIE 7.3 : Programme de fidélité
# ============================================================

class Fidelite:
    """Gestion du programme de fidélité."""

    POINTS_PAR_EURO = 10  # 10 points par euro dépensé

    def ajouter_points(self, client: Client, montant: float):
        """Ajoute des points de fidélité au client selon le montant."""
        points_gagnes = int(montant * self.POINTS_PAR_EURO)
        client.points_fidelite += points_gagnes
        print(f"\n  ★ {points_gagnes} points ajoutés à {client.nom}.")
        print(f"  ★ Total points : {client.points_fidelite} pts")


class CommandeFidele(Commande, Fidelite):
    """Commande avec programme de fidélité (héritage multiple)."""

    def valider(self):
        """Valide la commande et attribue les points de fidélité."""
        self.afficher()
        self.ajouter_points(self.client, self.prix_total())


# ============================================================
# PROGRAMME PRINCIPAL - Tests
# ============================================================

if __name__ == "__main__":

    print("\n" + "="*45)
    print("  PARTIE 2 & 3 : Boissons et ingrédients")
    print("="*45)

    # Café simple avec lait et sucre
    boisson = Cafe()
    boisson = Lait(boisson)
    boisson = Sucre(boisson)
    boisson.afficher_commande()

    print()

    # Thé avec caramel
    the_caramel = The()
    the_caramel = Caramel(the_caramel)
    the_caramel.afficher_commande()

    print("\n" + "="*45)
    print("  PARTIE 4 : Combinaison de boissons (+)")
    print("="*45)

    cafe = Cafe()
    the = The()
    menu = cafe + the
    menu.afficher_commande()

    print("\n" + "="*45)
    print("  PARTIE 7 : Gestion des commandes")
    print("="*45)

    # Création d'un client
    client1 = Client(nom="Ali Benali", numero=101, points_fidelite=0)
    print(f"\nClient créé : {client1}")

    # Commande sur place
    commande1 = CommandeSurPlace(client1)
    commande1.ajouter_boisson(Sucre(Lait(Cafe())))
    commande1.ajouter_boisson(The())
    commande1.afficher()

    # Commande à emporter
    client2 = Client(nom="Sara Ahsain", numero=202)
    commande2 = CommandeEmporter(client2)
    commande2.ajouter_boisson(Caramel(Cafe()))
    commande2.ajouter_boisson(ChocolatChaud())
    commande2.afficher()

    print("\n" + "="*45)
    print("  PARTIE 7.4 : Héritage multiple - CommandeFidele")
    print("="*45)

    client3 = Client(nom="Youssef El Fassi", numero=303)
    cmd_fidele = CommandeFidele(client3)
    cmd_fidele.ajouter_boisson(Sucre(Lait(Cafe())))
    cmd_fidele.ajouter_boisson(Caramel(The()))
    cmd_fidele.valider()

    print("\n" + "="*45)
    print("  PARTIE 8 : Questions de réflexion")
    print("="*45)
    print("""
  Q1 : Le patron Décorateur (DecorateurBoisson) permet d'ajouter
       facilement de nouveaux ingrédients sans modifier les classes
       existantes. Il suffit de créer une nouvelle classe héritant
       de DecorateurBoisson.

  Q2 : Pour ajouter le chocolat chaud, il suffit de créer une nouvelle
       classe ChocolatChaud(Boisson) avec son cout() et description().
       Aucune autre classe n'a besoin d'être modifiée.

  Q3 : Séparer les responsabilités (principe SRP) rend le code plus
       facile à maintenir car chaque classe a un rôle précis. Un
       changement dans une classe n'affecte pas les autres, ce qui
       réduit les bugs et facilite les tests.
    """)
