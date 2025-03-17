# liste de toute les entités présentes sur la map
#Entity_list=[x for x in map.cell_matrix.linked_entity if x!='-']


html_content="""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age of Empires - Vue d'ensemble</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
        }
        .team {
            margin-bottom: 40px;
        }
        .team h2 {
            text-align: center;
            color: #34495e;
            border-bottom: 2px solid #ddd;
            padding-bottom: 5px;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
        }
        .section {
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 15px;
            flex: 1 1 calc(30% - 20px);
            min-width: 280px;
        }
        .section h3 {
            margin-top: 0;
            color: #2c3e50;
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            margin: 10px 0;
            padding: 10px;
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        ul li span {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Age of Empires - Vue d'ensemble</h1>

    <!-- 	&Eacutequipe 1 -->
    <div class="team">
        <h2>Team 1</h2>
        <div class="container">
            <!-- Ressources Section -->
            <div class="section" id="ressources-team1">
                <h3>Ressources</h3>
                <ul>
"""
html_content+="""   
                    <li><span>Wood</span> : 500</li>
                    <li><span>Gold</span> : 300</li>
                    <li><span>Food</span> : 700</li>
"""  #mettre une boucle sur les ressources de la team 1

for x in Entity_list:
    if isinstance(x,Ressources):
        html_content+="""<li><span>"""
        html_content+=type(x)
        html_content+="""</span> : """
        html_content+=x.quantity()
        html_content+="""</li>"""


html_content+=""""
                </ul>
            </div>

            <!-- Units Section -->
            <div class="section" id="unites-team1">
                <h3>Units</h3>
                <ul>
                    <li>
                        <span>Villager</span> :
                        <ul>
                            <li>Villager 1 : HP = 25, Position = (5, 10)</li>
                            <li>Villager 2 : HP = 22, Position = (6, 12)</li>
                        </ul>
                    </li>
                    <li>
                        <span>Archer</span> :
                        <ul>
                            <li>Archer 1 : HP = 40, Position = (8, 15)</li>
                        </ul>
                    </li>
                </ul>
            </div>

            <!-- Buildings Section -->
            <div class="section" id="batiments-team1">
                <h3>Buildings</h3>
                <ul>
                    <li>
                        <span>Finished</span> :
                        <ul>
                            <li>Towncenter 1 : Position = (3, 6)</li>
                        </ul>
                    </li>
                    <li>
                        <span>Under construction</span> :
                        <ul>
                            <li>Farm : Progression = 60%, Position = (10, 12)</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 	&#201quipe 2 -->
    <div class="team">
        <h2>Team 2</h2>
        <div class="container">
            <!-- Ressources Section -->
            <div class="section" id="ressources-team2">
                <h3>Ressources</h3>
                <ul>
                    <li><span>Wood</span> : 400</li>
                    <li><span>Gold</span> : 200</li>
                    <li><span>Food</span> : 600</li>
                </ul>
            </div>

            <!-- Units Section -->
            <div class="section" id="unites-team2">
                <h3>Units</h3>
                <ul>
                    <li>
                        <span>Villager</span> :
                        <ul>
                            <li>Villager 1 : HP = 20, Position = (4, 8)</li>
                            <li>Villager 2 : HP = 25, Position = (7, 14)</li>
                        </ul>
                    </li>
                    <li>
                        <span>Swordsman</span> :
                        <ul>
                            <li>Swordsman 1 : HP = 60, Position = (10, 10)</li>
                        </ul>
                    </li>
                </ul>
            </div>

            <!-- Building Section -->
            <div class="section" id="batiments-team2">
                <h3>Buildings</h3>
                <ul>
                    <li>
                        <span>Finished</span> :
                        <ul>
                            <li>Towncenter 1 : Position = (2, 5)</li>
                        </ul>
                    </li>
                    <li>
                        <span>Under construction</span> :
                        <ul>
                            <li>Farm : Progression = 50%, Position = (9, 15)</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>

"""


file_name="fichier_3.html"

with open(file_name,"w",) as file:
    file.write(html_content)

print(f"Fichier HTML crée : {file_name}")