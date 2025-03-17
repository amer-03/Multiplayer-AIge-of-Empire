html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Condition avec HTML et CSS</title>
    # <style>
    #     /* Masque le contenu par défaut */
    #     .team-content {
    #         display: none;
    #     }

    #     /* Affiche le contenu associé à l'élément sélectionné */
    #     #team1:checked ~ #team1-content {
    #         display: block;
    #     }

    #     #team2:checked ~ #team2-content {
    #         display: block;
    #     }

    #     /* Style de base */
    #     body {
    #         font-family: Arial, sans-serif;
    #         margin: 20px;
    #     }

    #     h1 {
    #         text-align: center;
    #     }

    #     label {
    #         margin-right: 20px;
    #     }

    #     .content {
    #         margin-top: 20px;
    #     }

    #     .section {
    #         margin-bottom: 20px;
    #         padding: 10px;
    #         border: 1px solid #ccc;
    #         border-radius: 5px;
    #     }
    # </style>
</head>
<body>
    <h1>Sélection d'équipe</h1>

    <!-- Sélection d'équipe -->
    <div>
        <input type="radio" id="team1" name="team" checked>
        <label for="team1">Team 1</label>

        <input type="radio" id="team2" name="team">
        <label for="team2">Team 2</label>
    </div>

    <!-- Contenu conditionnel -->
    <div class="content">
        <div id="team1-content" class="team-content">
            <div class="section">
                <h2>Contenu de l'équipe 1</h2>
                <p>Ressources : Bois, Or, Nourriture.</p>
            </div>
        </div>

        <div id="team2-content" class="team-content">
            <div class="section">
                <h2>Contenu de l'équipe 2</h2>
                <p>Ressources : Pierres, Fer, Nourriture.</p>
            </div>
        </div>
    </div>
</body>
</html>

"""

with open("index1.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)