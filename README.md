# poke.lootmath.com
Welcome! This is an in-development one-stop shop for the Pokemon data science you didn't know you wanted, with a concerted focus on specific combat matchups and optimizing parties.

### Current Scope
As of March 2024, the current scope of the project is all of Pokemon Generation 1, including:
* Pocket Monsters Red & Green
* Pocket Monsters Blue
* Pocket Monsters Stadium
* Pokemon Red & Blue Versions
* Pocket Monsters Stadium 2
* Pocket Monsters Pikachu
* Pokemon Yellow Version
* Pokemon Stadium

### General Roadmap
1. **Data Migration and Processing**
    * Collect all relevant data from Serebii, Bulbapedia, pkmn.help, The Cutting Room Floor, the JP Pokemon Wiki, and more.
    * Transform the data into SQL-friendly CSV tables and battle-sim-friendly JSON objects.
2. **Data Analysis Suite**
    * Leverage the transformed CSVs to build charts via Bokeh.
    * Expand upon findings in pseudo-academic data analysis articles.
    * Host this analysis on site, and organize 
3. **Battle Simulator**
    * Construct JSON objects of potential Pokemon parties and loadouts.
    * Build respectful battle simulator implemented for a specific game or game cluster.
    * Conduct extensive simulation to create more data about optimal combat matchups.
    * Implement specific trainer data to discover optimal strategies.
    * Add findings and more charts to Data Analysis Suite, and link pages to the corresponding games.
4. **Party Optimizer**
    * Leveraging matchup data, create tool to generate ideal parties based on opponent.
    * Implement modes such as "required mons" (such as a favorite or starter) to personalize the tool to the user.
5. **Attempt to disrupt the competitive metagame**
    * Use all available tools and data to simulate a developing Smogon competitive metagame, including Mon relegation and promotion over epochs.
    * Potentially discover something cool and/or useful for the competitive scene.
5. **Repeat steps for the next game**

