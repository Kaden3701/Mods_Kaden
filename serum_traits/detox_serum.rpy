# idea and original design by electricat
# modified by Kaden
init -1 python:
    def detox_accelerator_trait_on_apply(person, the_serum, add_to_log):
        person.serum_tolerance += 1
        for serum in person.serum_effects:
            serum.duration -=2
        return

    def detox_accelerator_trait_on_remove(person, the_serum, add_to_log):
        person.serum_tolerance -= 1
        return

    def add_detox_accelerator_serum():
        detox_accelerator_trait = SerumTraitMod(name = "Pharmakokinetic Accelerator",
                desc = "Temporarily increases serum tolerance by speeding up the rate at which active serums are disposed of by the body.",
                positive_slug = "+1 serum tolerance",
                negative_slug = "-2 serum duration to all active serums",
                research_added = 20,
                base_side_effect_chance = 0,
                on_apply = detox_accelerator_trait_on_apply,
                on_remove = detox_accelerator_trait_on_remove,
                requires = [weight_loss],
                tier = 2,
                start_researched =  False,
                research_needed = 800,
                clarity_cost = 750,
                mental_aspect = 0, physical_aspect = 3, sexual_aspect = 0, medical_aspect = 5, flaws_aspect = -1, attention = 0,
                start_enabled = False
            )

# any label that starts with serum_mod is added to the serum mod list
label serum_mod_detox_accelerator_serum_trait(stack):
    python:
        add_detox_accelerator_serum()
        execute_hijack_call(stack)
    return
