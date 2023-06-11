# idea by Starbuck
# design by Kaden
init python:
    def nocturnal_emission_actuator_serum_function_on_turn(person, the_serum, add_to_log):
        if time_of_day == 4:
            if the_serum.duration - the_serum.duration_counter == 1:
                if person.arousal_perc < 30:
                    person.change_arousal((30 - person.arousal),add_to_log = False)
            elif the_serum.duration - the_serum.duration_counter == 2:
                if person.arousal_perc < 60:
                    person.change_arousal((60 - person.arousal),add_to_log = False)
        return

    def nocturnal_emission_actuator_serum_function_on_day(person, the_serum, add_to_log):
        if person.arousal_perc < 90:
            person.change_arousal((90 - person.arousal),add_to_log = False)
        return

    def add_nocturnal_emission_actuator_serum():
        nocturnal_emission_actuator_serum_trait = SerumTraitMod(name = "Teasing Nightfall",
            desc = "No effect during the day. If a person is affected by it when going to bed, causes numerous lewd dreams.",
            positive_slug = "+90 Arousal over night",
            negative_slug = "+20 Serum Research",
            research_added = 20,
            base_side_effect_chance = 30,
            on_turn = nocturnal_emission_actuator_serum_function_on_turn,
            on_day = nocturnal_emission_actuator_serum_function_on_day,
            tier = 2,
            start_researched =  False,
            research_needed = 800,
            clarity_cost = 1000,
            mental_aspect = 2, sexual_aspect = 2, flaws_aspect = 1, attention = 1,
            start_enabled = False
            )

label serum_mod_nocturnal_emission_actuator_serum_trait(stack):
    python:
        add_nocturnal_emission_actuator_serum()
        execute_hijack_call(stack)
    return
