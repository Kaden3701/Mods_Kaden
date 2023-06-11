init -1 python:
    def pubes_change_on_day(goal_pubes, the_person, the_serum, add_to_log):
        if the_person.pubes_style != goal_pubes:
            if renpy.random.randint(0,100) < the_person.suggestibility:
                if goal_pubes == default_pubes:
                    if the_person.pubes_style == trimmed_pubes:
                        the_person.pubes_style = default_pubes
                    else:
                        goal_pubes = trimmed_pubes
                if goal_pubes == trimmed_pubes:
                    if the_person.pubes_style == diamond_pubes or default_pubes:
                        the_person.pubes_style = trimmed_pubes
                    else:
                        goal_pubes = diamond_pubes
                if goal_pubes == diamond_pubes:
                    if the_person.pubes_style == trimmed_pubes or landing_strip_pubes:
                        the_person.pubes_style = diamond_pubes
                    elif the_person.pubes_style == default_pubes:
                        the_person.pubes_style = trimmed_pubes
                    else:
                        goal_pubes = landing_strip_pubes
                if goal_pubes == landing_strip_pubes:
                    if the_person.pubes_style == diamond_pubes or shaved_pubes:
                        the_person.pubes_style = landing_strip_pubes
                    elif the_person.pubes_style == trimmed_pubes:
                        the_person.pubes_style = diamond_pubes
                    else:
                        the_person.pubes_style = trimmed_pubes
                if goal_pubes == shaved_pubes:
                    if the_person.pubes_style == landing_strip_pubes:
                        the_person.pubes_style = shaved_pubes
                    elif the_person.pubes_style == diamond_pubes:
                        the_person.pubes_style = landing_strip_pubes
                    elif the_person.pubes_style == trimmed_pubes:
                        the_person.pubes_style = diamond_pubes
                    elif the_person.pubes_style == default_pubes:
                        the_person.pubes_style = trimmed_pubes
        return

init 1 python:
    pubes_change_trait = SerumTraitBlueprint(
        unlock_label = "pubes_change_unlock_label",
        name = "Pube Alterations",
        desc = "Modifies the desire for body hair. Suggestion based chance of changing each night. ",
        positive_slug = "Shifts Pubes Towards Set Target",
        negative_slug = "",
        research_added = 80,
        base_side_effect_chance = 20,
        tier = 2,
        research_needed = 400,
        clarity_cost = 300,
        mental_aspect = 2, physical_aspect = 2, sexual_aspect = 0, medical_aspect = 1, flaws_aspect = 0, attention = 3)

init 5 python:
    add_label_hijack("instantiate_serum_trait_blueprints", "instantiate_pubes_blueprint")
    add_label_hijack("after_load", "instantiate_pubes_blueprint")

label instantiate_pubes_blueprint(stack): # Called from instantiate_serum_traits.
    python:
        if not pubes_change_trait in list_of_traits:
            list_of_traits.append(pubes_change_trait)
        execute_hijack_call(stack)
    return

label pubes_change_unlock_label(new_trait):
    menu:
        "Shaved":
            $ return_pubes = shaved_pubes
            $ temp_text = "Shaved"
        "Landing Strip":
            $ return_pubes = landing_strip_pubes
            $ temp_text = "Landing Strip"
        "Diamond":
            $ return_pubes = diamond_pubes
            $ temp_text = "Diamond"
        "Trimmed":
            $ return_pubes = trimmed_pubes
            $ temp_text = "Trimmed"
        "Natural":
            $ return_pubes = default_pubes
            $ temp_text = "Natural"
    python:
        new_trait.on_day = partial(pubes_change_on_day, return_pubes) #Generates a partially filled function
        new_trait.desc += " "+temp_text+ " is the target style."
        new_trait.name += ": "+temp_text
        del return_pubes
        del temp_text
    return
