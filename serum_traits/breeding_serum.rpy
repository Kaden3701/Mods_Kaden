# idea by quiboune
# original trait by Vavilon
# modified by Kaden
init -1 python:
    def impreg_on_day(person, the_serum, add_to_log):
        if (renpy.random.randint(0,100) < 50) and (person.fertility_percent < 100):
            person.fertility_percent += 1
            if add_to_log:
                mc.log_event((person.title or "???") + ": +1 Permanent Fertility", "float_text_red")
        if renpy.random.randint(0,100) < person.event_triggers_dict.get("serum_induced_lactation", 5):
            person.lactation_sources += 1
            person.event_triggers_dict["serum_induced_lactation"] = 0
        else:
            person.event_triggers_dict["serum_induced_lactation"] = person.event_triggers_dict.get("serum_induced_lactation", 5)+5
        return

    def add_quiboune_breeding_serum():
        impreg_serum_trait = SerumTraitMod(name = "Breeding Cow",
                desc = "Increases fertility and lactation of recepients as they sleep.",
                positive_slug = "50% chance of +1% Permanent Fertility overnight. Rare chance of increased lactation.",
                negative_slug = "+500 Serum Research",
                research_added = 500,
                base_side_effect_chance = 0,
                on_day = impreg_on_day,
                tier = 2,
                start_researched =  False,
                research_needed = 1600,
                clarity_cost = 1500,
                mental_aspect = 0, physical_aspect = 4, sexual_aspect = 2, medical_aspect = 2, flaws_aspect = 0, attention = 3,
                start_enabled = False
            )

# any label that starts with serum_mod is added to the serum mod list
label serum_mod_quiboune_breeding_trait(stack):
    python:
        add_quiboune_breeding_serum()
        execute_hijack_call(stack)
    return
