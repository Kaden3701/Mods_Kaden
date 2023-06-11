init python:
    def add_side_effect_traits():
        temp_number = 1
        for trait in list_of_side_effects:
            temp_name = "side_effect_trait_"+str(temp_number)
            temp_name = SerumTraitMod(name = trait.name ,desc = trait.desc, positive_slug = trait.positive_slug, negative_slug = trait.negative_slug,
                research_added = 50, slots_added = trait.slots, production_added = 50, duration_added = trait.duration, base_side_effect_chance = 5, clarity_added = 50,
                on_apply = trait.on_apply, on_remove = trait.on_remove, on_turn = trait.on_turn, on_day = trait.on_day, on_move = trait.on_move,
                requires = trait.requires, tier = 1, start_researched = False, research_needed = 50, exclude_tags = trait.exclude_tags, is_side_effect = False,
                clarity_cost = 50, start_unlocked = False, start_enabled = False,
                mental_aspect = trait.mental_aspect, physical_aspect = trait.physical_aspect, sexual_aspect = trait.sexual_aspect, medical_aspect = trait.medical_aspect, flaws_aspect = trait.flaws_aspect, attention = trait.attention)
            temp_number +=1
        return
        
label serum_mod_side_effect_traits(stack):
    python:
        add_side_effect_traits()
        execute_hijack_call(stack)
    return
