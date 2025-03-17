from unit.Buildings import Building 
from unit.Buildings import Position

def get_unit_count():
    # Exemple : cette fonction retourne le nombre d'unités (logique simulée)
    return 42

def get_buildings_count():
    # Exemple : cette fonction retourne le nombre de bâtiments (logique simulée)
    return 30

# Données pour les unités et bâtiments
resources = {
    "unit": {
        "Villager": "Basic game entity with building capacity.",
        "Archer": "Effective ranged unit against infantry.",
        "Horseman": "A fast, powerful cavalry unit.",
        "Swordsman": "A powerful and strong infantry.",
    },
    "building": {
        "Town Center" : "Main building of the village.",
        "House" : "Homes of the villagers.",
        "Camp": "Drop pint for ressources",
        "Farm":"Contains food.",
        "Barracks": "Building used to train swordsmen.",
        "Archery Range": "Building to train archers.",
        "Stable": "Building for training horsemen.",
        "Keep": "Protect the village.",
    },
}

# Génération du contenu HTML
unit_count = get_unit_count()
building_count = get_buildings_count()

html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ressources</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Current Resources</h1>
    <p>Number of Units: {unit_count}</p>
    <p>Number of Buildings: {building_count}</p>

    <h1>Select a Team</h1>

    <!-- Menu pour sélectionner une équipe -->
    <form>
        <label>
            <input type="radio" name="team" id="team1"> Team 1
        </label>
        <label>
            <input type="radio" name="team" id="team2"> Team 2
        </label>
    </form>

    <form id="resource-form">
        <label for="type">Choose a category :</label>
        <select id="type" name="type">
            <option value="">-- Choose a category --</option>
            <option value="unit">Unit</option>
            <option value="building">Building</option>
        </select>

        <button type="button">Valider</button>
    </form>

    <h2>Units</h2>
    <div>
        {"".join([f"<p>{unit}: {description}</p>" for unit, description in resources['unit'].items()])}
    </div>

    <h2>Buildings</h2>
    <div>
        {"".join([f"<p>{building}: {description}</p>" for building, description in resources['building'].items()])}
    </div>
</body>
</html>
"""

# Écriture du fichier HTML
with open("index.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

# Contenu CSS
css_content = """
body {
    font-family: 'Cloister Black', serif;
    font-size: 14px;
    text-align: center;
    margin: 0;
    padding: 20px;
    background-image: url("agoe_1.png");
    background-color: #f9f9f9;
    background-repeat: no-repeat;
    color: #333;
}
h1 {
    font-size: 24px;
    color: #222;
    margin-bottom: 20px;
}
form {
    margin: 20px auto;
    max-width: 400px;
}
label {
    display: block;
    margin: 10px 0 5px;
    font-size: 16px;
}
select, button {
    font-size: 14px;
    padding: 5px;
    margin: 5px 0;
    width: 100%;
    max-width: 400px;
}
#result {
    margin-top: 20px;
    font-size: 16px;
    color: #555;
}
"""

# Écriture du fichier CSS
with open("style.css", "w", encoding="utf-8") as css_file:
    css_file.write(css_content)
