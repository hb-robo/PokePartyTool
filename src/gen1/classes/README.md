Separation of Class Information
(for my sanity)


Contained in Pokemon Class:
    Input:
        Pokemon name
        Generation
        Game
        Ability
        Item
        Gender
        Tera Type
        IV spread
        EV spread
        Moves
        Level
    Derived from Data JSON:
        Type 1 and 2
        Height
        Weight
        Base stats
        Derived stats
        Learndex / possible moves
        Egg group
        Catch rate
        Hatch time
        EX curve
        EXP yield
        EV yield
        shape
        footprint
        color
        base friendship


Contained in BattlePokemon Class:
    Current HP
    EVasion and accuracy
    Movepool 
    Stat stages
    Status Conditions
    In air / underground
    In play or not
    Generation constants such as stat stage multipliers
    Transformation status / stats 



Contained in Battle Class:
    Move effect handling
    damage calculations
    critical hit chance calculations
    move accuracy / hits and misses
    Move picking
    Who moves first
    Text logging
