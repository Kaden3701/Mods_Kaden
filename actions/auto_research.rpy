init 1 python:
    def auto_research_requirement():
        if mc.business.is_open_for_business():
            if mc.business.head_researcher:
                if mc.business.active_research_design is None or (isinstance(mc.business.active_research_design, SerumTrait) and mc.business.active_research_design.get_effective_side_effect_chance() < 10):
                    if not mc.business.event_triggers_dict.get("auto_research_intro", False) or mc.business.event_triggers_dict.get("auto_research_active", False):
                        if auto_research_trait():
                            return True
        return False

    def auto_research_discuss_requirement(person):
        if person != mc.business.head_researcher:
            return False
        if not mc.business.event_triggers_dict.get("auto_research_intro", False):
            return False
        if not mc.is_at_work() or not mc.business.is_open_for_business():
            return "Talk at work"
        return True

    def auto_research_trait():
        temp_list = []
        temp_number = 99999
        for trait in list_of_traits:
            if trait.unlocked and not trait.researched:
                if not isinstance(trait, SerumTraitBlueprint):
                    temp_list.append(trait)
        if temp_list:
            for trait in temp_list:
                if (trait.research_needed-trait.current_research) < temp_number:
                    temp_number = (trait.research_needed-trait.current_research)
                    temp_trait = trait
            return temp_trait

        for trait in list_of_traits:
            if trait.has_required() and not trait.researched:
                if not isinstance(trait, SerumTraitBlueprint):
                    temp_list.append(trait)
        if temp_list:
            for trait in temp_list:
                if trait.clarity_cost < temp_number:
                    temp_number = trait.clarity_cost
                    temp_trait = trait
            if temp_trait.clarity_cost < mc.free_clarity:
                return temp_trait
            else:
                return False

        for trait in list_of_traits:
            if trait.has_required() and trait.get_effective_side_effect_chance() > 0:
                if not isinstance(trait, SerumTraitBlueprint):
                    temp_list.append(trait)
        if temp_list:
            temp_number = 0
            for trait in temp_list:
                if trait.get_effective_side_effect_chance() > temp_number:
                    temp_number = trait.get_effective_side_effect_chance()
                    temp_trait = trait
            if mc.business.active_research_design != temp_trait:
                return temp_trait
        return False

init 5 python:
    add_label_hijack("normal_start", "activate_auto_research_mod_core")
    add_label_hijack("after_load", "update_auto_research_mod_core")

    def auto_research_mod_initialization():
        auto_research = Action("Auto Research", auto_research_requirement, "auto_research_label")
        auto_research_discuss = Action("Discuss Automatic Research", auto_research_discuss_requirement, "auto_research_discuss_label", menu_tooltip = "Discuss your Head Researcher picking research topics.", priority = 2)
        if auto_research_discuss not in head_researcher.actions:
            mc.business.mandatory_crises_list.append(auto_research)
            head_researcher.add_action(auto_research_discuss)
        return

label activate_auto_research_mod_core(stack):
    python:
        auto_research_mod_initialization()
        execute_hijack_call(stack)
    return

label update_auto_research_mod_core(stack):
    python:
        auto_research_mod_initialization()
        execute_hijack_call(stack)
    return

label auto_research_label():
    $ the_person = mc.business.head_researcher
    "You receive a text from your head researcher [the_person.title]. It reads:"
    if not mc.business.event_triggers_dict.get("auto_research_intro", False):
        $ mc.business.event_triggers_dict["auto_research_intro"] = True
        $ mc.start_text_convo(the_person)
        the_person "[the_person.mc_title], I appreciate all the free time you're giving me in the lab, but I think my talents would be better used if you put me to work."
        the_person "I've got some promising leads, would you like me to pick one to pursue?"
        "How would you like to reply?"
        menu:
            "Let her pick research":
                mc.name "Yeah, that's fine. Go ahead."
                the_person "Really? That's great. You won't regret this."
                $ mc.business.event_triggers_dict["auto_research_active"] = True
                the_person "If you ever decide you want to take over again just let me know. I'll look the traits over and let you know what I pick to do next."
                $ mc.end_text_convo()
                "A short time later you get another text from [the_person.title] which reads:"
            "Pick your own research":
                mc.name "No, I've got an idea already, just wait for me to decide."
                the_person "Okay."
                $ mc.end_text_convo()
                return
            "Not now":
                mc.name "I don't have time for this right now. I'll get back to you."
                the_person "Okay."
                $ mc.end_text_convo()
                return
    $ temp_trait = auto_research_trait()
    if not temp_trait.unlocked:
        $ temp_trait.unlock_trait()
    if temp_trait.unlocked:
        $ mc.business.set_serum_research(temp_trait)
    $ mc.start_text_convo(the_person)
    the_person "The research department has refocused to take a look at [temp_trait.name]."
    $ mc.end_text_convo()
    python:
        auto_research = Action("Auto Research", auto_research_requirement, "auto_research_label")
        mc.business.mandatory_crises_list.append(auto_research)
    $ del temp_trait
    return

label auto_research_discuss_label(the_person):
    if mc.business.event_triggers_dict.get("auto_research_active", False):
        the_person "I'm currently unlocking and researching traits without input from you. Would you like me to continue?"
        menu:
            "Continue researching":
                mc.name "Yes, this has been great."
            "Stop researching":
                mc.name "No, I want to assign research projects myself."
                $ mc.business.event_triggers_dict["auto_research_active"] = False
                while auto_research in mc.business.mandatory_crises_list:
                    python:
                        mc.business.mandatory_crises_list.remove(auto_research)
    else:
        the_person "I'm not researching anything unless you tell me too. Would you like me start?"
        menu:
            "Start researching":
                mc.name "Yes, I don't have time so you should take care of that."
                $ mc.business.event_triggers_dict["auto_research_active"] = True
                python:
                    auto_research = Action("Auto Research", auto_research_requirement, "auto_research_label")
                    mc.business.mandatory_crises_list.append(auto_research)
            "Not now":
                mc.name "No, I'll continue to assign research projects myself."
    return
