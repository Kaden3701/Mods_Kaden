init -1 python:
    def personality_change_on_turn(goal_personality, the_person, the_serum, add_to_log):
        if the_person.personality in list_of_personalities:
            if renpy.random.randint(0,200) < the_person.suggestibility:
                if not goal_personality in list_of_personalities and the_person.personality == wild_personality:
                    goal_personality = wild_personality
                else:
                    the_person.personality = goal_personality
                if goal_personality == introvert_personality:
                    if the_person.personality == reserved_personality:
                        the_person.personality = introvert_personality
                    elif the_person.personality == relaxed_personality:
                        the_person.personality = reserved_personality
                    elif the_person.personality == wild_personality:
                        the_person.personality = relaxed_personality
                elif goal_personality == reserved_personality:
                    if the_person.personality == introvert_personality:
                        the_person.personality = reserved_personality
                    elif the_person.personality == relaxed_personality:
                        the_person.personality = reserved_personality
                    elif the_person.personality == wild_personality:
                        the_person.personality = relaxed_personality
                elif goal_personality == relaxed_personality:
                    if the_person.personality == introvert_personality:
                        the_person.personality = reserved_personality
                    elif the_person.personality == reserved_personality:
                        the_person.personality = relaxed_personality
                    elif the_person.personality == wild_personality:
                        the_person.personality = relaxed_personality
                elif goal_personality == wild_personality:
                    if the_person.personality == introvert_personality:
                        the_person.personality = reserved_personality
                    elif the_person.personality == reserved_personality:
                        the_person.personality = relaxed_personality
                    elif the_person.personality == relaxed_personality:
                        the_person.personality = wild_personality
        else:
            mc.log_event(the_person.name + " can not change personalities", "float_text_grey")
        return

init 1 python:
    personality_change_trait = SerumTraitBlueprint(
        unlock_label = "personality_change_unlock_label",
        name = "Personality Alterations",
        desc = "Modifies the core of the subject's personality. Suggestion based chance of changing each turn.",
        positive_slug = "Shifts Personality Towards Set Target",
        negative_slug = "",
        research_added = 400,
        base_side_effect_chance = 80,
        tier = 3,
        research_needed = 2000,
        clarity_cost = 2200,
        mental_aspect = 8, physical_aspect = 0, sexual_aspect = 0, medical_aspect = 0, flaws_aspect = 0, attention = 3)

init 5 python:
    add_label_hijack("instantiate_serum_trait_blueprints", "instantiate_personality_blueprint")
    add_label_hijack("after_load", "instantiate_personality_blueprint")

label instantiate_personality_blueprint(stack): # Called from instantiate_serum_traits.
    python:
        if not personality_change_trait in list_of_traits:
            list_of_traits.append(personality_change_trait)
        execute_hijack_call(stack)
    return

label personality_change_unlock_label(new_trait):
    menu:
        "Introvert":
            $ return_personality = introvert_personality
            $ temp_text = "Introvert"
        "Reserved":
            $ return_personality = reserved_personality
            $ temp_text = "Reserved"
        "Relaxed":
            $ return_personality = relaxed_personality
            $ temp_text = "Relaxed"
        "Wild":
            $ return_personality = wild_personality
            $ temp_text = "Wild"
        "Alpha":
            $ return_personality = alpha_personality
            $ temp_text = "Alpha"
        "Cougar":
            $ return_personality = cougar_personality
            $ temp_text = "Cougar"
        # "Breeding Stock":
        #     $ return_personality = breeding_stock
        #     $ temp_text = "Breeding Stock"
        # "Daddy's Girl":
        #     $ return_personality = daddy_girl
        #     $ temp_text = "Daddy's Girl"
    python:
        new_trait.on_turn = partial(personality_change_on_turn, return_personality) #Generates a partially filled function
        new_trait.desc += " "+temp_text+" is the target personality."
        new_trait.name += ": "+temp_text
        del return_personality
        del temp_text
    return
