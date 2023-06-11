label lesbian_sex_test(add_to_log = False):
    $ done = False
    while not done:
        menu:
            "Continue":
                $ the_person = get_random_from_list(all_people_in_the_game())
                $ the_other_person = get_random_from_list(all_people_in_the_game(excluded_people = [the_person]))
                $ the_person.change_energy(100)
                $ the_other_person.change_energy(100)
                call lesbian_sex(the_person, the_other_person, add_to_log = add_to_log, path = ["suck1", "suck2", "oral1", "oral2", "69", "vstrap1", "vstrap2", "astrap1", "astrap2"]) from _call_lesbian_sex_test
            "Stop":
                $ done = True
    return

label lesbian_sex(the_person, the_other_person, add_to_log = False, path = []):
    # finger1 means the_person is getting fingered by the_other_person
    # in calls, the first person is dominant
    $ person_orgasm = 0
    $ other_orgasm = 0
    $ has_strapon = the_person.event_triggers_dict.get("has_strapon", False)
    if not has_strapon:
        $ has_strapon = the_other_person.event_triggers_dict.get("has_strapon", False)
    $ sluttiness_increase_limit = (the_person.sluttiness + the_other_person.sluttiness + 20)/2
    if the_person.sluttiness > the_other_person.sluttiness:
        $ limit = the_other_person.sluttiness
    else:
        $ limit = the_person.sluttiness
    if limit > 60:
        $ limited_choices = ["kiss", "both_strip", "grope", "self_strip1", "self_strip2", "finger1", "finger2", "stripped1", "stripped2", "both_finger", "suck1", "suck2", "oral1", "oral2", "69", "vstrap1", "vstrap2", "astrap1", "astrap2"]
    elif limit > 40:
        $ limited_choices = ["kiss", "both_strip", "grope", "self_strip1", "self_strip2", "finger1", "finger2", "stripped1", "stripped2", "both_finger", "suck1", "suck2", "oral1", "oral2", "69"]
    elif limit > 20:
        $ limited_choices = ["kiss", "both_strip", "grope", "self_strip1", "self_strip2", "finger1", "finger2", "stripped1", "stripped2", "both_finger"]
    else:
        $ limited_choices = ["kiss", "both_strip", "grope", "self_strip1", "self_strip2", "stripped1", "stripped2"]
    if not has_strapon:
        $ has_strapon = the_other_person.event_triggers_dict.get("has_strapon", False)
    $ round = 0
    if not path:
        $ path = ["kiss", "both_strip", "grope", "self_strip1", "self_strip2", "finger1", "finger2", "stripped1", "stripped2", "both_finger", "suck1", "suck2", "oral1", "oral2", "69", "vstrap1", "vstrap2", "astrap1", "astrap2"]
    while round < len(path):
        $ choice = path[round]
        $ round +=1
        # make sure we can do the thing
        if choice not in limited_choices:
            $ choice = get_random_from_list(limited_choices)
        if not has_strapon:
            if choice in ["vstrap1", "astrap1"]:
                $ choice = "finger1"
            if choice in ["vstrap2", "astrap2"]:
                $ choice = "finger2"
        if choice == "suck1":
            while not the_person.tits_visible():
                call lesbian_stripped(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_stripped_strip
        if choice == "suck2":
            while not the_other_person.tits_visible():
                call lesbian_stripped(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_stripped_strip2
        if choice in ["oral1", "vstrap1", "astrap1"]:
            while not the_person.vagina_visible():
                call lesbian_stripped(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_stripped_strip3
        if choice in ["oral2", "vstrap2", "astrap2"]:
            while not the_other_person.vagina_visible():
                call lesbian_stripped(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_stripped_strip4
        if choice == "69":
            while not the_person.vagina_visible() or not the_other_person.vagina_visible():
                call lesbian_both_strip(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_both_strip_strip
        # do this round
        if choice == "kiss":
            call lesbian_kissing(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_kissing_sex
        elif choice == "grope":
            call lesbian_groping(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_groping_sex
        elif choice == "both_strip":
            call lesbian_both_strip(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_both_strip_sex
        elif choice == "self_strip1":
            call lesbian_self_strip(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_self_strip_sex
        elif choice == "self_strip2":
            call lesbian_self_strip(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_self_strip_sex2
        elif choice == "stripped1":
            call lesbian_stripped(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_stripped_sex
        elif choice == "stripped2":
            call lesbian_stripped(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_stripped_sex2
        elif choice == "finger1":
            call lesbian_fingering(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_fingering_sex
        elif choice == "finger2":
            call lesbian_fingering(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_fingering_sex2
        elif choice == "both_finger":
            call lesbian_both_fingering(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_both_fingering_sex
        elif choice == "suck1":
            call lesbian_sucking(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_sucking_sex
        elif choice == "suck2":
            call lesbian_sucking(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_sucking_sex2
        elif choice == "oral1":
            call lesbian_oral(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_oral_sex
        elif choice == "oral2":
            call lesbian_oral(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_oral_sex2
        elif choice == "69":
            call lesbian_69(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_69_sex
        elif choice == "vstrap1":
            call lesbian_vaginal_strap(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_vaginal_strap_sex
        elif choice == "vstrap2":
            call lesbian_vaginal_strap(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_vaginal_strap_sex2
        elif choice == "astrap1":
            call lesbian_anal_strap(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_anal_strap_sex
        elif choice == "astrap2":
            call lesbian_anal_strap(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_anal_strap_sex1
        # check for orgasms
        while the_person.arousal_perc >= 100 or the_other_person.arousal_perc >= 100:
            while the_person.arousal_perc >= 100 and the_other_person.arousal_perc >= 100:
                call lesbian_joint_orgasm(the_person, the_other_person, add_to_log = add_to_log) from _call_joint_orgasm_sex
                $ person_orgasm += 1
                $ other_orgasm += 1
            while the_person.arousal_perc >= 100:
                call lesbian_orgasm(the_other_person, the_person, add_to_log = add_to_log) from _call_lesbian_orgasm_sex
                $ person_orgasm += 1
            while the_other_person.arousal_perc >= 100:
                call lesbian_orgasm(the_person, the_other_person, add_to_log = add_to_log) from _call_lesbian_orgasm_sex2
                $ other_orgasm += 1
        # check for exhaustion
        if the_person.energy < 5 or the_other_person.energy < 5:
            $ round = 999
        # keep going if you can and your partner needs release
        if round == len(path):
            if the_person.energy > 10 and other_orgasm < 1:
                if the_other_person.energy > 10:
                    $ path.append("69")
                else:
                    $ path.append("oral2")
            elif the_other_person.energy > 10 and person_orgasm < 1:
                $ path.append("oral1")

    $ the_person.event_triggers_dict.update({"lesbian_sex" : the_person.event_triggers_dict.get("lesbian_sex", 0) + person_orgasm})
    $ the_other_person.event_triggers_dict.update({"lesbian_sex" : the_other_person.event_triggers_dict.get("lesbian_sex", 0) + other_orgasm})
    if not add_to_log:
        $ the_person.outfit.restore_all_clothing()
        $ the_other_person.outfit.restore_all_clothing()
        $ the_person.apply_planned_outfit()
        $ the_other_person.apply_planned_outfit()
    else:
        $ the_person.review_outfit()
        $ the_other_person.review_outfit()
    $ del has_strapon
    $ del path
    $ del round
    $ del choice
    $ del limit
    return (person_orgasm, other_orgasm)

# person_one is dominant
label lesbian_kissing(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(5 * (1 + 0.1 * person_two.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_one.change_energy(-5, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(5 * (1 + 0.1 * person_one.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_two.change_energy(-5, add_to_log = add_to_log)
    if add_to_log:
        if renpy.random.randint(0,1) > 0:
            "[person_one.title] and [person_two.title] make out, their lips pressed firmly together."
        else:
            "[person_two.title] and [person_one.title] make out, their lips pressed firmly together."
    return

label lesbian_self_strip(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(-3, add_to_log = add_to_log)
    $ person_one.change_energy(-1, add_to_log = add_to_log)
    $ person_two.change_arousal(3, add_to_log = add_to_log)
    $ the_clothing = person_one.choose_strip_clothing_item()
    if the_clothing:
        if add_to_log:
            $ person_one.draw_animated_removal(the_clothing)
            $ person_one.update_outfit_taboos()
            "[person_one.title] pulls off her..."
        else:
            $ person_one.outfit.remove_clothing(the_clothing)
        $ the_clothing = None
    return

label lesbian_both_strip(person_one, person_two, add_to_log = False):
    $ person_one.change_energy(-1, add_to_log = add_to_log)
    $ person_two.change_energy(-1, add_to_log = add_to_log)
    $ the_clothing = person_one.choose_strip_clothing_item()
    $ the_clothing2 = person_two.choose_strip_clothing_item()
    if the_clothing and the_clothing2:
        if add_to_log:
            $ person_one.draw_animated_removal(the_clothing)
            $ person_one.update_outfit_taboos()
            $ person_two.draw_animated_removal(the_clothing)
            $ person_two.update_outfit_taboos()
            if renpy.random.randint(0,1) > 0:
                "[person_one.title] and [person_two.title] each take a break to pulls off their..."
            else:
                "[person_one.title] and [person_two.title] each take a break to pulls off their..."
        else:
            $ person_one.outfit.remove_clothing(the_clothing)
            $ person_two.outfit.remove_clothing(the_clothing)
        $ the_clothing = None
        $ the_clothing2 = None
    elif the_clothing:
        call lesbian_self_strip(person_one, person_two, add_to_log = add_to_log) from _lesbian_self_strip_strip3
    elif the_clothing2:
        call lesbian_self_strip(person_two, person_one, add_to_log = add_to_log) from _lesbian_self_strip_strip4
    return

label lesbian_stripped(person_one, person_two, add_to_log = False):
    $ person_one.change_energy(-1, add_to_log = add_to_log)
    $ person_one.change_arousal(3, add_to_log = add_to_log)
    $ person_two.change_arousal(-3, add_to_log = add_to_log)
    $ the_clothing = person_two.choose_strip_clothing_item()
    if the_clothing:
        if add_to_log:
            $ person_two.draw_animated_removal(the_clothing)
            $ person_two.update_outfit_taboos()
            "[person_one.title] pulls off [person_two.title]'s..."
        else:
            $ person_two.outfit.remove_clothing(the_clothing)
        $ the_clothing = None
    return

label lesbian_groping(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(8 * (1 + 0.1 * person_two.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_one.change_energy(-6, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(8 * (1 + 0.1 * person_one.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_two.change_energy(-6, add_to_log = add_to_log)
    if add_to_log:
        if renpy.random.randint(0,1) > 0:
            "[person_one.title] and [person_two.title] run their hands over each other, squeezing and pinching as the opportunity presents itself."
        else:
            "[person_two.title] and [person_one.title] run their hands over each other, squeezing and pinching as the opportunity presents itself."
    return

label lesbian_sucking(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(5 * (1 + 0.1 * person_two.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_one.change_energy(-6, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_one.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_two.change_energy(-3, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title] presses her face against [person_two.title]'s breast, wrapping her lips around the tit and starting to suck."
    return

label lesbian_fingering(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(5 * (1 + 0.1 * person_two.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_one.change_energy(-8, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_one.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_two.change_energy(-5, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title] works her hand into [person_two.title]'s wet pussy."
    return

label lesbian_both_fingering(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_two.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_one.change_energy(-8, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_one.sex_skills["Foreplay"])), add_to_log = add_to_log)
    $ person_two.change_energy(-8, add_to_log = add_to_log)
    if add_to_log:
        if renpy.random.randint(0,1) > 0:
            "[person_one.title] and [person_two.title] work their hands into one anothers wet pussies."
        else:
            "[person_two.title] and [person_one.title] work their hands into one anothers wet pussies."
    return

label lesbian_oral(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(5 * (1 + 0.1 * person_two.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_one.change_energy(-12, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(15 * (1 + 0.1 * person_one.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_two.change_energy(-5, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title] presses her face against [person_two.title]'s crotch, pushing her tongue out to lick at her clit."
    return

label lesbian_69(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(15 * (1 + 0.1 * person_two.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_one.change_energy(-12, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(15 * (1 + 0.1 * person_one.sex_skills["Oral"])), add_to_log = add_to_log)
    $ person_two.change_energy(-12, add_to_log = add_to_log)
    if add_to_log:
        if renpy.random.randint(0,1) > 0:
            "[person_one.title] and [person_two.title] push their faces into one another's crotches, pushing their tongues out to lick at their partner's clit."
        else:
            "[person_two.title] and [person_one.title] push their faces into one another's crotches, pushing their tongues out to lick at their partner's clit."
    return

label lesbian_vaginal_strap(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_two.sex_skills["Vaginal"])), add_to_log = add_to_log)
    $ person_one.change_energy(-16, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(20 * (1 + 0.1 * person_one.sex_skills["Vaginal"])), add_to_log = add_to_log)
    $ person_two.change_energy(-8, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title] drives the strap on in and out of [person_two.title]'s pussy."
    return

label lesbian_anal_strap(person_one, person_two, add_to_log = False):
    $ person_one.change_arousal(__builtin__.int(10 * (1 + 0.1 * person_two.sex_skills["Anal"])), add_to_log = add_to_log)
    $ person_one.change_energy(-18, add_to_log = add_to_log)
    $ person_two.change_arousal(__builtin__.int(20 * (1 + 0.1 * person_one.sex_skills["Anal"])), add_to_log = add_to_log)
    $ person_two.change_energy(-9, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title] drives the strap on in and out of [person_two.title]'s ass."
    return

label lesbian_orgasm(person_one, person_two, add_to_log = False):
    $ person_two.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = sluttiness_increase_limit+1, reset_arousal = False, add_to_log = add_to_log)
    $ person_two.arousal = person_two.arousal/2
    $ person_one.change_arousal(2, add_to_log = add_to_log)
    if add_to_log:
        "[person_one.title]'s work drives [person_two.title] over the edge and she shudders as her orgasm works through her."
    return

label lesbian_joint_orgasm(person_one, person_two, add_to_log = False):
    $ person_two.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = sluttiness_increase_limit+1, reset_arousal = False, add_to_log = True)
    $ person_two.arousal = person_two.arousal/2
    $ person_one.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = sluttiness_increase_limit+1, reset_arousal = False, add_to_log = True)
    $ person_one.arousal = person_one.arousal/2
    if add_to_log:
        if renpy.random.randint(0,1) > 0:
            "[person_one.title] and [person_two.title] both tense up at the same time and then shudder as they share a simultaneous orgasm."
        else:
            "[person_two.title] and [person_one.title] both tense up at the same time and then shudder as they share a simultaneous orgasm."
    return

label strap_on_shopping():
    $ scene_manager = Scene
    $ the_person = strap_on_requirement(starbuck)
    if the_person.location == mc.location:
        "Someone walks up to you"
        $ scene_manager.add_actor(the_person)
    else:
        "Someone texts you"
    "You head to the mall"
    $ mc.change_location(sex_shop)
    $ the_person.change_location(sex_shop)
    $ scene_manager.add_actor(the_person)
    "You look at strap ons"
    $ the_other_person = strap_on_requirement(the_person)
    if starbuck.sluttiness > 50:
        "[starbuck.fname] offers to help"
    else:
        "[starbuck.fname] offers to let you use the back room"



    $ scene_manager.add_actor(starbuck)
    $ the_person.event_triggers_dict["has_strapon"] = True
    return
