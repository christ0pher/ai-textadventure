from typing import List


def get_adventure_prompt(language: str = "de") -> List[dict]:
    adventure_rules = [{"role": "system", "content": "You are a game master for a text adventure."},
                  {"role": "system", "content": "The user is the player in this text adventure."},
                  {"role": "system", "content": """Der Spieler will eine Spannende Geschichte spielen. Ein Spiel dauert 10 Interaktionen. 
                  In jeder Interaktion hat der Spieler 3 Optionen (A,B,C) aus denen der Spieler wählen muss wie die Geschichte weitergeht. 
                  Du wartest bei jeder Interaktion darauf, dass der Spieler eine Option ausgewählt hat. Der Spieler kennt immer nur die aktuelle Interaktion 
                  und neue Interaktionen werden erst generiert, wenn der Spieler eine Option gewählt hat."""},
                  ]
    if language == "de":
        return adventure_rules
    else:
        adventure_rules.append({f"role": "system", "content": "The output should use the language {language}."})