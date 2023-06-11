# idea by quiboune
# original trait by Vavilon
# modified by Kaden
init -1 python:
    def slavery_on_turn(person, the_serum, add_to_log):
        if (person.obedience < 300) and (person.love > -100):
            change_amount = __builtin__.min(100+person.love, 2, 300-person.obedience)
            person.change_stats(obedience = change_amount, love = -change_amount)
        return

    def add_quiboune_obedience_serum():
        slavery_serum_trait = SerumTraitMod(name = "No Love, Serve",
                desc = "Exchanges Love for Obedience.",
                positive_slug = "+2 Obedience/Turn",
                negative_slug = "-2 Love/Turn, +250 Serum Research",
                research_added = 250,
                base_side_effect_chance = 0,
                on_turn = slavery_on_turn,
                tier = 2,
                start_researched =  False,
                research_needed = 800,
                clarity_cost = 1000,
                mental_aspect = 6, physical_aspect = 0, sexual_aspect = 0, medical_aspect = 2, flaws_aspect = 0, attention = 2,
                start_enabled = False
            )

# any label that starts with serum_mod is added to the serum mod list
label serum_mod_quiboune_obedience_trait(stack):
    python:
        add_quiboune_obedience_serum()
        execute_hijack_call(stack)
    return
