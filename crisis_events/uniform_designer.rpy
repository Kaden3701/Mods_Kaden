init 2 python:
    def uniform_designer_requirement():
        if strict_uniform_policy.is_active():
            if mc.is_at_work():
                if not mc.business.event_triggers_dict.get("uniform_designer", None):
                    if mc.business.get_employee_count() > 3:
                        if mc.business.is_open_for_business():
                            return True
        return False

    def design_others_outfit(designer, model, temp_sluttiness_boost = 0, target = 0):
        if designer.effective_sluttiness() >= model.effective_sluttiness():
            outfit_slut_points = __builtin__.min(__builtin__.int((designer.effective_sluttiness() + temp_sluttiness_boost) / 8.0), 12.0)
            allow_skimpy = False
            model.change_stats(slut = 1, max_slut = (30 if designer.effective_sluttiness() >= 30 else designer.effective_sluttiness()))
        else:
            outfit_slut_points = __builtin__.min(__builtin__.int((model.effective_sluttiness() + temp_sluttiness_boost) / 8.0), 12.0)
            allow_skimpy = True
        builder = WardrobeBuilder(designer)
        thinks_appropriate = False
        if outfit_slut_points < target/12:
            outfit_slut_points = target/12
        while not thinks_appropriate or outfit_slut_points < 0:
            outfit = model.personalize_outfit(builder.build_outfit(None, outfit_slut_points), opinion_color = designer.favorite_colour(), coloured_underwear = True, swap_bottoms = True, allow_skimpy = allow_skimpy)
            thinks_appropriate = model.judge_outfit(outfit, temp_sluttiness_boost = __builtin__.int(temp_sluttiness_boost/4.0))
            outfit_slut_points -= 1
        if thinks_appropriate and outfit:
            return outfit
        return None

    def design_test(designer):
        temp_sluttiness_boost = 0
        target = 0
        if strict_uniform_policy.is_active():
            temp_sluttiness_boost +=4
            target = 10
            if reduced_coverage_uniform_policy.is_active():
                temp_sluttiness_boost +=4
                target = 20
                if casual_uniform_policy.is_active():
                    temp_sluttiness_boost +=4
                    target = 30
                    if minimal_coverage_uniform_policy.is_active():
                        temp_sluttiness_boost +=4
                        target = 40
                        if minimal_coverage_uniform_policy.is_active():
                            temp_sluttiness_boost +=4
                            target = 60
                            if corporate_enforced_nudity_policy.is_active():
                                temp_sluttiness_boost +=4
                                target = 80
                                if maximal_arousal_uniform_policy.is_active():
                                    temp_sluttiness_boost +=4
                                    target = 999
        for person in mc.business.get_employee_list():
            outfit = design_others_outfit(designer, person, temp_sluttiness_boost = temp_sluttiness_boost, target = target)
            if outfit:
                person.apply_outfit(outfit.get_copy())
        return

    def full_staff_design(designer):
        temp_sluttiness_boost = 0
        target = 0
        if strict_uniform_policy.is_active():
            temp_sluttiness_boost +=4
            target = 10
            if reduced_coverage_uniform_policy.is_active():
                temp_sluttiness_boost +=4
                target = 20
                if casual_uniform_policy.is_active():
                    temp_sluttiness_boost +=4
                    target = 30
                    if minimal_coverage_uniform_policy.is_active():
                        temp_sluttiness_boost +=4
                        target = 40
                        if minimal_coverage_uniform_policy.is_active():
                            temp_sluttiness_boost +=4
                            target = 60
                            if corporate_enforced_nudity_policy.is_active():
                                temp_sluttiness_boost +=4
                                target = 80
                                if maximal_arousal_uniform_policy.is_active():
                                    temp_sluttiness_boost +=4
                                    target = 999
        for person in mc.business.get_employee_list():
            outfit = design_others_outfit(designer, person, temp_sluttiness_boost = temp_sluttiness_boost, target = target)
            if outfit:
                person.event_triggers_dict["forced_uniform"] = outfit.get_copy()
        return

    def full_staff_clear():
        for person in mc.business.get_employee_list():
            person.event_triggers_dict["forced_uniform"] = None
        return

    def uniform_prep_requirement(): # monday morning
        if day%7 == 0:
            if time_of_day == 0:
                the_person = mc.business.event_triggers_dict.get("uniform_designer", None)
                if the_person:
                    if not the_person.is_employee():
                        the_person = None
                if the_person:
                    return True
        return False

    def uniform_followup_requirement():
        if mc.business.event_triggers_dict.get("uniform_designer", None):
            if day%7 == 2 or day%7 == 3:
                if mc.is_at_work():
                    if mc.business.event_triggers_dict.get("uniform_designer", None).is_at_office():
                        if len(build_forced_uniform_list(mc.business.event_triggers_dict.get("uniform_designer", None))) > 2:
                            return True
        return False

    uniform_designer_action = ActionMod("Uniform Designer", uniform_designer_requirement, "uniform_designer_action_label",
        menu_tooltip = "An employee wants to talk about the work uniforms.", category = "Business Crisis", is_crisis = True)

    def get_uniform_designer():
        temp_list = []
        opinion = -2
        slut = 0
        while not temp_list:
            for person in mc.business.get_employee_list():
                person.create_opinion("work uniforms", start_positive = False, start_known = False, add_to_log = False)
                if person.get_opinion_score("work uniforms") == opinion:
                    temp_list.append(person)
            opinion += 1
        person = get_random_from_list(temp_list)
        for x in temp_list:
            if x.sluttiness > person.sluttiness:
                person = x
        return person

    def build_forced_uniform_list(person):
        temp_list = mc.business.get_employee_list()
        temp_list.remove(person)
        for other_person in temp_list:
            if not person.event_triggers_dict.get("forced_uniform", None):
                temp_list.remove(other_person)
        return temp_list

    def uniform_followup_prep():
        temp_list = mc.business.get_employee_list()
        for person in temp_list:
            if person.event_triggers_dict.get("forced_uniform", None):
                person.apply_outfit(person.event_triggers_dict.get("forced_uniform", None).get_copy())
        return

label uniform_designer_action_label():
    $ the_person = get_uniform_designer()
    $ mc.business.event_triggers_dict["uniform_designer"] = the_person
    if the_person is None:
        return
    $ the_place = mc.business.get_employee_workstation(the_person)
    $ day_part = time_of_day_string(time_of_day)
    if (mc.location ==  the_place):
        "You're hard at work in the [day_part], when [the_person.possessive_title] asks you over to discuss something."
    else:
        "You're hard at work in the [day_part], when [the_person.possessive_title] calls you on your phone to discuss something."
    "You meet up in an empty office of the [the_place.name] department."
    $ mc.change_location(the_place)
    $ the_place = None
    $ done = False
    $ the_person.draw_person(position="sitting", emotion="happy")
    the_person "Hello [the_person.mc_title], thank you for meeting me on such short notice."
    the_person "I have been thinking about how to make work more enjoyable for the staff."
    $ the_person.discover_opinion("work uniforms")
    if the_person.get_opinion_score("work uniforms") < 0:
        the_person "I understand why you want us to wear uniforms, I just hate being so restricted."
    elif the_person.get_opinion_score("work uniforms") > 0:
        the_person "I love having uniforms planned out for my work week, but sometimes they can get a bit stale."
    else:
        the_person "I don't feel too strongly about uniforms, but I know some of our staff does."
    $ the_person.discover_opinion("skimpy uniforms")
    if the_person.get_opinion_score("skimpy uniforms") < 0:
        the_person "I also think that sometimes they can be too revealing."
    elif the_person.get_opinion_score("skimpy uniforms") > 0:
        the_person "I also think they can provide an excellent excuse for showing off my body."
    else:
        the_person "I've also heard some mixed reviews on how skimpy they can be."
    mc.name "I understand where you're coming from, but I still think it's important to maintain uniform standards."
    the_person "I figured you would say that, but I don't want to get rid of them entirely."
    the_person "I was hoping that maybe I could help the girls pick out an outfit for next week and see if you like any of them enough to replace what we are using now."
    mc.name "Hmm, that is an interesting idea. Do you think they would be willing to let you use them as dress up dolls?"
    if get_existing_rivals(town_relationships, the_person):
        $ rival = get_random_from_list(get_existing_rivals(town_relationships, the_person))
        the_person "I think so. Although [rival.fname] might give me a bit of trouble, she is such a bitch."
    elif get_existing_friends(town_relationships, the_person):
        $ friend = get_random_from_list(get_existing_friends(town_relationships, the_person))
        the_person "I think so. If I have any trouble I can always get [friend.fname] to help me out."
    else:
        the_person "I don't think I'll have any trouble with that."
    menu:
        "Design some uniforms":
            mc.name "Alright, lets give this a try. Go ahead and get with the girls this weekend so that they have something to wear on Monday."
            mc.name "We'll meet up later in the week and discuss how they look."
            the_person "Thanks [the_person.mc_title], you won't regret this!"
            $ the_person.change_stats(happiness = 5, obedience = 2)
            $ uniform_prep_action = Action("Uniform prep", uniform_prep_requirement, "uniform_prep_label")
            $ mc.business.add_mandatory_crisis(uniform_prep_action)
        "Not now":
            mc.name "I still don't think it is a good idea. Let's stick with what we have already."
            the_person "Yes sir."
            $ number = the_person.get_opinion_score("work uniforms")*4
            $ the_person.change_stats(happiness = number, obedience = 2)

    $ clear_scene()
    return

label uniform_prep_label():
    $ the_person = mc.business.event_triggers_dict.get("uniform_designer", None)
    $ full_staff_design(the_person)
    $ uniform_followup_action = Action("Uniform followup", uniform_followup_requirement, "uniform_followup_label")
    $ mc.business.add_mandatory_crisis(uniform_followup_action)
    return

label uniform_followup_label():
    $ outfit = None
    $ stripped = True
    $ scene_manager = Scene()
    $ new_uniforms = 0
    $ all_uniforms = 0
    $ the_person = mc.business.event_triggers_dict.get("uniform_designer", None)
    $ forced_uniform_list = build_forced_uniform_list(the_person)
    $ uniform_followup_prep()
    "It has been a few days and you have to admit at least the girl's uniforms do have a bit more variety."
    "You take a moment out of your work day and track down [the_person.title] and talk to her about them."
    $ mc.location = the_person.location
    $ scene_manager.add_actor(the_person, position = "sitting", display_transform = character_left_flipped)
    the_person "Hello, [the_person.mc_title]! How can I help you?"
    mc.name "I wanted to talk to you about the uniforms you picked out for the girls this week."
    the_person "Of course, I've been expecting this. We should probably get someone to come model their outfit so you can give me specific feedback."
    the_person "Was there a specific outfit that you like more than the rest?"
    $ done = False
    while not done:
        call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(forced_uniform_list, "Uniform review", ["Back"])]))
        $ person_choice = _return
        if person_choice != "Back":
            $ outfit = person_choice.event_triggers_dict.get("forced_uniform", None)
            $ forced_uniform_list.remove("Uniform review")
            $ forced_uniform_list.remove("Back")
            $ forced_uniform_list.remove(person_choice)
            $ over = outfit.get_copy()
            $ under = outfit.get_copy()
            python:
                for clothing in over.get_full_strip_list(strip_feet = True):
                    if clothing.layer < 2:
                        over.remove_clothing(clothing)
                for clothing in under.get_full_strip_list(strip_feet = True):
                    if clothing.layer > 1:
                        under.remove_clothing(clothing)
                over.update_name()
                under.update_name()
            mc.name "I think the clothes [person_choice.fname] has been wearing look great."
            "You send a message to [person_choice.title] and ask her to come meet with you and [the_person.title]."
            "After some time you get a response..."
            person_choice "Be right there [person_choice.mc_title]!"
            $ person_choice.apply_outfit(outfit.get_copy())
            $ scene_manager.update_actor(the_person, display_transform = character_left_flipped)
            $ scene_manager.add_actor(person_choice)
            "After a short time, [person_choice.title] makes her appearance, wearing the outfit that [the_person.title] helped design."
            mc.name "What do you think of the outfit that [the_person.fname] helped you pick out to wear this week?"
            if person_choice.judge_outfit(outfit, as_underwear = False, as_overwear = False):
                person_choice "I really like it."
                mc.name "That's good to hear, how would you feel about adding it to your normal uniform rotation?"
                person_choice "That would be great."
            else:
                person_choice "It is a bit revealing."
                mc.name "I'm sorry you feel that way. Do you think you might wear it if it was included in your normal uniform rotation?"
                person_choice "I don't know... I guess it would depend on what my other options were."
                if person_choice.judge_outfit(outfit, 20, as_underwear = False, as_overwear = False):
                    the_person "It isn't the worst outfit ever, so I might wear it occasionally."
                else:
                    the_person "It really makes me uncomfortable, but if there isn't anything better I won't have a choice."
            "Ultimately the decision is yours, what do you want to do?"
            menu:
                "Add to uniforms":
                    mc.name "Let's keep this, I think having it as an option will be a good thing."
                    the_person "Great, I'm so happy I could contribute to the company uniforms."
                    $ new_uniforms +=1
                    $ mc.business.business_uniforms.append(UniformOutfit(outfit))
                    $ mc.business.listener_system.fire_event("add_uniform", the_outfit = outfit)
                    $ mc.designed_wardrobe.add_outfit(outfit)
                "Discard design":
                    mc.name "It's just not what I picture when I think about our company."
                    the_person "Okay, I understand."
            if reduced_coverage_uniform_policy.is_active():
                $ stripped = True
                $ slut_continue_requirement = 0
                mc.name "Now, strip down to your underwear."
                if new_uniforms > 0:
                    mc.name "Let's see if the parts of the uniform are worth using as well."
                else:
                    mc.name "Maybe we can salvage something from this experiment."
                if not (person_choice.outfit.wearing_bra() and person_choice.outfit.wearing_panties()):
                    $ slut_continue_requirement = 40
                    person_choice "I... I can't do that [person_choice.mc_title]."
                    mc.name "What do you mean you can't? These are the rules you agreed with to work here, if you..."
                    "She shakes her head and interrupts you."
                    if not (person_choice.outfit.wearing_bra() or person_choice.outfit.wearing_panties()):
                        person_choice "No, I mean I can't strip down to my underwear because... I'm not wearing any."
                        $ slut_continue_requirement = 60
                        $ slut_continue_requirement += -(5*person_choice.get_opinion_score("not wearing anything"))
                    elif not person_choice.outfit.wearing_bra():
                        person_choice "No, I mean I can't strip down to my underwear because... I'm not wearing a bra."
                        person_choice "My... breasts would be out."
                        $ slut_continue_requirement += -(5*person_choice.get_opinion_score("showing her tits"))
                    else: #not wearing panties
                        person_choice "No, I mean I can't strip down to my underwear because... I'm not wearing any panties."
                        $ slut_continue_requirement += -(5*person_choice.get_opinion_score("showing her ass"))
                    "You consider this for a moment, then shrug."
                    if new_uniforms > 0:
                        mc.name "That's unfortunate, I didn't realize she had designed an outfit without some items."
                    else:
                        mc.name "That's surprising, maybe I judged this outfit too soon."
                    mc.name "We better take a look."
                    person_choice "So you still want me to..."
                    mc.name "Strip. Now."
                    if person_choice.effective_sluttiness() < slut_continue_requirement:
                        "[person_choice.possessive_title] shuffles nervously."
                        person_choice "I don't think I can do it. I'm sorry [person_choice.mc_title]."
                        if office_punishment.is_active():
                            mc.name "If you're refusing the only choice I have is to write you up for disobedience, which will carry a penalty."
                            person_choice "I'm sorry, but I just can't do it. I'll accept a punishment if I have to."
                            $ person_choice.add_infraction(Infraction.disobedience_factory())
                            $ stripped = False
                        $ person_choice.change_happiness(-5)
                        $ person_choice.change_obedience(-1)
                        mc.name "Fine, we'll do it your way."
                    else:
                        $ person_choice.change_happiness(-5)
                        $ person_choice.change_obedience(2 + person_choice.get_opinion_score("being submissive"))
                        "Your words seem to shock her into action."
                elif person_choice.obedience < (130 - (10*person_choice.get_opinion_score("being submissive"))):
                    if person_choice.effective_sluttiness("underwear_nudity") < 40:
                        $ person_choice.draw_person(emotion = "angry")
                        person_choice "You... You can't make me do that!"
                        mc.name "Of course I can, it's company policy."
                        person_choice "But... It's not..."
                        mc.name "Strip. Now."
                        "[person_choice.possessive_title] glares at you, and for a moment you think she is going to refuse."
                        person_choice "Fine."
                        $ person_choice.change_obedience(1 + person_choice.get_opinion_score("being submissive"))
                    else:
                        person_choice "Okay."
                else:
                    if person_choice.effective_sluttiness("underwear_nudity") < 40:
                        "She blushes and looks away."
                        person_choice "Are you sure [person_choice.mc_title]? I'm not used to... being undressed in front of people."
                        mc.name "Of course I'm sure. Now strip."
                        "She nods meekly."
                        person_choice "Okay, if you say I have to..."
                    else:
                        "[person_choice.title] nods obediently."
                        person_choice "Yes [person_choice.mc_title], I'll go change."
                        mc.name "You'll change right here. Now strip."
                        person_choice "Of course. Right away."
                if person_choice.effective_sluttiness() > slut_continue_requirement:
                    $ generalised_strip_description(person_choice, person_choice.outfit.get_underwear_strip_list(visible_enough = False, avoid_nudity = False, strip_shoes = True))
                    $ scene_manager.update_actor(person_choice)
                    $ mc.change_locked_clarity(20)
                    if person_choice.update_outfit_taboos() or person_choice.effective_sluttiness() < 40:
                        "[person_choice.possessive_title] blushes and tries to cover her body."
                        person_choice "This is so embarrassing..."
                    $ slut_change = 0
                    if person_choice.tits_visible():
                        $ slut_change += person_choice.get_opinion_score("showing her tits")
                    if person_choice.vagina_visible():
                        $ slut_change += person_choice.get_opinion_score("showing her ass")
                    if person_choice.tits_visible() and person_choice.vagina_visible():
                        $ slut_change += person_choice.get_opinion_score("not wearing anything")
                    $ person_choice.change_slut(slut_change, 40)
                    mc.name "What do you think of the underwear that [the_person.title] helped you pick out to wear this week?"
                    if person_choice.judge_outfit(under, as_underwear = True, as_overwear = False):
                        person_choice "I really like it."
                        mc.name "That's good to hear, how would you feel about adding it to your normal uniform rotation?"
                        person_choice "That would be great."
                    else:
                        person_choice "It is a bit revealing."
                        mc.name "I'm sorry you feel that way. Do you think you might wear it if it was included in your normal uniform rotation?"
                        person_choice "I don't know... I guess it would depend on what my other options were."
                        if person_choice.judge_outfit(under, 20, as_underwear = True, as_overwear = False):
                            person_choice "It isn't the worst underwear ever, so I might wear it occasionally."
                        else:
                            person_choice "It really makes me uncomfortable, but if there isn't anything else better I won't have a choice."
                    "Ultimately the decision is yours, what do you want to do?"
                    menu:
                        "Add to uniforms":
                            mc.name "Let's keep this, I think having it as an option will be a good thing."
                            the_person "Great, I'm so happy I could contribute to the company uniforms."
                            $ new_uniforms +=1
                            $ mc.business.business_uniforms.append(UniformOutfit(under))
                            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = under)
                            $ mc.designed_wardrobe.add_underwear_set(under)
                        "Discard design":
                            mc.name "It's just not what I picture when I think about our company."
                            the_person "Okay, I understand."
                    if minimal_coverage_uniform_policy.is_active():
                        mc.name "Great! Now to make sure we've covered all our bases lets see the overwear without underwear."
                        if not (person_choice.tits_visible() and person_choice.vagina_visible() and person_choice.tits_visible() and person_choice.vagina_visible()): #Something to strip
                            mc.name "Let's start by having you strip down."
                            $ generalised_strip_description(person_choice, person_choice.outfit.get_full_strip_list(strip_feet = True))
                            $ mc.change_locked_clarity(15)
                            if person_choice.update_outfit_taboos(): # Broke a taboo
                                "[person_choice.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
                        else:
                            mc.name "You're already un-dressed for the occasion."
                        mc.name "Go ahead and put on the overwear."
                        $ person_choice.apply_outfit(over.get_copy())
                        $ scene_manager.update_actor(person_choice)
                        mc.name "What do you think of the overwear that [person_choice.title] helped you pick out to wear this week?"
                        if person_choice.judge_outfit(under, as_underwear = False, as_overwear = True):
                            person_choice "I really like it."
                            mc.name "That's good to hear, how would you feel about adding it to your normal uniform rotation?"
                            person_choice "That would be great."
                        else:
                            person_choice "It is a bit revealing, I guess I can try and find underwear that works with it."
                            mc.name "I'm sorry you feel that way. Do you think you might wear it if it was included in your normal uniform rotation?"
                            person_choice "I don't know... I guess it would depend on what my other options were."
                            if person_choice.judge_outfit(under, 20, as_underwear = True, as_overwear = False):
                                person_choice "It isn't the worst clothing ever, so I might wear it occasionally."
                            else:
                                person_choice "It really makes me uncomfortable, but if there isn't anything else better I won't have a choice."
                        "Ultimately the decision is yours, what do you want to do?"
                        menu:
                            "Add to uniforms":
                                mc.name "Let's keep this, I think having it as an option will be a good thing."
                                the_person "Great, I'm so happy I could contribute to the company uniforms."
                                $ new_uniforms +=1
                                $ mc.business.business_uniforms.append(UniformOutfit(over))
                                $ mc.business.listener_system.fire_event("add_uniform", the_outfit = over)
                                $ mc.designed_wardrobe.add_overwear_set(over)
                            "Discard design":
                                mc.name "It's just not what I picture when I think about our company."
                                the_person "Okay, I understand."
            $ all_uniforms += new_uniforms
            $ new_uniforms = 0
            menu:
                "Check another" if len(forced_uniform_list) > 2:
                    call uniform_dismissal_label(the_person, person_choice, stripped) from _call_uniform_dismissal_label_1
                "Finish up":
                    $ done = True
        else:
            $ done = True
            mc.name "Actually I don't think I like any of the outfits."
            the_person "Oh... okay. I guess we'll just go back to the uniforms you pick out."
    if all_uniforms > 1:
        the_person "Great, I'm so happy that you found something new worth using for our uniforms."
        the_person "As soon as you get a chance be sure to let us know which departments are going to be able to wear the new outfits."
        $ the_person.change_stats(happiness = all_uniforms, obedience = all_uniforms)
    elif all_uniforms > 0:
        the_person "Great, I'm so happy that you found something new worth using for our uniforms."
        the_person "As soon as you get a chance be sure to let us know which departments are going to be able to wear the new outfit."
    else:
        the_person "I'm sorry I couldn't find anything to your liking."
        $ the_person.change_stats(happiness = -5, obedience = 5)
    if renpy.random.randint(0,2) < all_uniforms:
        $ the_person.strengthen_opinion("work uniforms")
    the_person "Would you like the girls to go back to wearing their normal uniforms for the rest of the week?"
    menu:
        "Back to normal":
            mc.name "Yes, I really prefer what I picked out for them."
            $ full_staff_clear()
        "Keep wearing new uniforms" if all_uniforms > 0:
            mc.name "No, it has been a great change of pace seeing them in something differnt."
    the_person "What about for next week? Can I design some new uniforms for the girls?"
    menu:
        "Design more uniforms":
            mc.name "That would be great."
            $ uniform_prep_action = Action("Uniform prep", uniform_prep_requirement, "uniform_prep_label")
            $ mc.business.add_mandatory_crisis(uniform_prep_action)
        "Back to normal":
            mc.name "I'd rather that you didn't."
            $ mc.business.event_triggers_dict["uniform_designer"] = None
    if person_choice != "Back":
        call uniform_dismissal_label(the_person, person_choice, stripped) from _call_uniform_dismissal_label_2
    $ clear_scene()
    return

label uniform_dismissal_label(the_person, person_choice, stripped):
    mc.name "Thank you for coming to model for us [person_choice.title], you can head back to work."
    person_choice "Okay, thanks."
    if reduced_coverage_uniform_policy.is_active() and stripped:
        "Since she has been dismissed, [person_choice.title] reaches for her discared clothing, and you get a sudden idea."
        if minimal_coverage_uniform_policy.is_active():
            menu:
                "Keep her underwear":
                    mc.name "Actually, I think I like your outfit best the way it is now. You can stay like that for the rest of the week."
                    "She hesitates for a moment, but it isn't like that is an unreasonable request."
                    if person_choice.judge_outfit(over, as_underwear = False, as_overwear = False):
                        person_choice "Sure, I kinda like it better this way too."
                    else:
                        person_choice "...okay."
                        "It seems like she wants to argue but there is really no way for her to justify refusing to comply with this uniform."
                    $ person_choice.event_triggers_dict["forced_uniform"] = over.get_copy()
                "Take her overwear":
                    $ generalised_strip_description(person_choice, person_choice.outfit.get_underwear_strip_list())
                    $ person_choice.apply_outfit(under.get_copy())
                    $ person_choice.event_triggers_dict["forced_uniform"] = under.get_copy()
                    "Once she has her underwear back on you stop her."
                    mc.name "Actually, leave those. I want to make sure that we get them listed in the uniform system properly, you can head back to work like you are."
                    if person_choice.judge_outfit(under, as_underwear = False, as_overwear = False):
                        person_choice "Sure, I kinda like it better this way too."
                    else:
                        if not under.wearing_bra() and not under.wearing_panties():
                            person_choice "Like this? But I'm not really wearing anything."
                            mc.name "Exactly, I think I like you best this way."
                        elif not under.wearing_panties():
                            person_choice "Like this? But everyone is going to be able to see my pussy."
                            if not person_choice.has_taboo("vaginal_sex"):
                                mc.name "Exactly, and it will give me easier access if I get bored at work."
                            else:
                                mc.name "Exactly, and we all appreciate the show."
                        elif not under.wearing_bra():
                            person_choice "Like this? But everyone is going to be able to see my tits."
                            mc.name "Exactly, and we all appreciate the show."
                        else:
                            person_choice "...okay."
                            "It seems like she wants to argue but there is really no way for her to justify refusing to comply with this uniform."
                "Let her get dressed":
                    $ generalised_strip_description(person_choice, person_choice.outfit.get_underwear_strip_list())
                    $ person_choice.apply_outfit(outfit.get_copy())
                    $ person_choice.outfit.restore_all_clothing()
        else:
            menu:
                "Keep her overwear":
                    mc.name "Actually, leave those. I want to make sure that we get them listed in the uniform system properly, you can head back to work like you are."
                    $ person_choice.event_triggers_dict["forced_uniform"] = under.get_copy()
                    if person_choice.judge_outfit(under, as_underwear = False, as_overwear = False):
                        person_choice "Sure, I kinda like it better this way too."
                    else:
                        if not under.wearing_bra() and not under.wearing_panties():
                            person_choice "Like this? But I'm not really wearing anything."
                            mc.name "Exactly, I think I like you best this way."
                        elif not under.wearing_panties():
                            person_choice "Like this? But everyone is going to be able to see my pussy."
                            if not person_choice.has_taboo("vaginal_sex"):
                                mc.name "Exactly, and it will give me easier access if I get bored at work."
                            else:
                                mc.name "Exactly, and we all appreciate the show."
                        elif not under.wearing_bra():
                            person_choice "Like this? But everyone is going to be able to see my tits."
                            mc.name "Exactly, and we all appreciate the show."
                        else:
                            person_choice "...okay."
                            "It seems like she wants to argue but there is really no way for her to justify refusing to comply with this uniform."
                "Let her get dressed":
                    $ person_choice.apply_outfit(outfit.get_copy())
                    $ person_choice.outfit.restore_all_clothing()
    $ person_choice.wear_uniform()
    $ scene_manager.remove_actor(person_choice)
    return
