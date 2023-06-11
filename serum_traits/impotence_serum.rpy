init python:
    def get_impotence_person():
        potential_people = []
        for a_person in mc.location.people:
            if not a_person.title is None:
                if a_person.event_triggers_dict.get("impotence_tracker", 0) >= 10:
                    if not a_person.has_role(girlfriend_role) and not a_person.has_role(harem_role):
                        potential_people.append(a_person)
        return get_random_from_list(potential_people)

    def impotence_requirement():
        if time_of_day > 0 and time_of_day < 4:
            return not get_impotence_person() is None
        return False

    def impotence_serum_function_on_day(person, the_serum, add_to_log):
        if not person.has_role(girlfriend_role) and not person.has_role(harem_role):
            if person.energy > 60:
                temp_number = person.effective_sluttiness() + person.get_opinion_score("bareback_sex")*10
                if person.relationship == "Girlfriend":
                    temp_number +=10
                elif person.relationship == "Fiancée":
                    temp_number +=20
                elif person.relationship == "Married":
                    temp_number -=10
                if person.personality in [wild_personality, alpha_personality, cougar_personality]:
                    temp_number +=10
                if renpy.random.randint(0,200) < temp_number:
                    person.change_stats(arousal = 30, happiness = -5)
                    person.event_triggers_dict.update({"impotence_tracker" : person.event_triggers_dict.get("impotence_tracker", 0) + temp_number/10})
                    impotence_crisis = Action("Friend SO relationship worsen", impotence_requirement, "impotence_label")
                    crisis_list.append([impotence_crisis, 10])
        return

    def add_impotence_serum():
        impotence_serum_trait = SerumTraitMod(name = "Impotence Secretions",
            desc = "Forces a person to secrete chemicals that cause impotence in potential mates (after innoculating yourself).",
            positive_slug = "Potential for unsatisfying overnight exertions. Impact on relationships and arousal.",
            negative_slug = "",
            research_added = 20,
            base_side_effect_chance = 30,
            on_day = impotence_serum_function_on_day,
            tier = 2,
            start_researched =  False,
            research_needed = 800,
            clarity_cost = 1000,
            mental_aspect = 0, sexual_aspect = 2, physical_aspect = 1, flaws_aspect = 1, attention = 1,
            start_enabled = False
            )

label serum_mod_impotence_serum_trait(stack):
    python:
        add_impotence_serum()
        execute_hijack_call(stack)
    return

label impotence_label():
    $ the_person = get_impotence_person()
    if the_person is None or not the_person.title or the_person.mc_title == "Stranger":
        return #Something's changed and there is no longer a valid person
    $ so_title = SO_relationship_to_title(the_person.relationship)
    $ the_person.draw_person()
    if not the_person.event_triggers_dict.get("impotence_chat", False):
        if renpy.random.randint(0,(100-the_person.love)/2) > the_person.event_triggers_dict.get("impotence_tracker", 0):
            "[the_person.title] walks towards you as if she's going to say something, but turns away at the last moment."
            $ the_person.draw_person(position = "walking_away")
            "She looked flushed at first and maybe embarassed as she walked away. She must not feel comfortable talking to you yet."
            "You wonder if the serum you gave her is having an effect."
        else:
            $ the_person.event_triggers_dict["impotence_chat"] = True
            the_person "Hey [the_person.mc_title], it's good to see you. I have a delicate question I was hoping you could answer."
            mc.name "Of course, how can I help?"
            if len(mc.location.people) > 1:
                "[the_person.title] takes a look around and then steps a bit closer to you, lowering her voice to nearly a whisper."
            the_person "This is a bit embarrassing, can you keep it to yourself?"
            mc.name "Of course."
            the_person "You know [the_person.SO_name], my [so_title]? The last time we were together he had a bit of trouble performing."
            if not the_person.has_taboo("vaginal_sex") or not the_person.has_taboo("anal_sex"):
                the_person "You've never had that problem with me, but you know... does it ever happen to you?"
            else:
                the_person "I know this is super personal, but... does that ever happen for you?"
            menu:
                "Reassure her":
                    mc.name "I've never run into that myself, but it does happen to people."
                    mc.name "Sometimes if a guy drinks too much he can have trouble getting it up."
                    $ the_person.change_love(2)
                    $ the_person.event_triggers_dict["impotence_tracker"] -= 5
                    the_person "Well, that's the thing. He got it up but then once we started getting busy he... went soft."
                    mc.name "Two pump chump?"
                    if the_person.wants_creampie():
                        the_person "No, worse than that. He didn't cum, his condom was empty."
                    else:
                        the_person "No, worse than that. When he pulled out there wasn't any cum."
                    mc.name "Maybe it was just an off night, the next time might be better."
                    the_person "Yeah... I guess. Well, thanks for listening [the_person.mc_title]."
                "Add to her doubts":
                    mc.name "Sorry, that is a problem I've never had."
                    mc.name "If we're being honest, I'm a little surprised that anyone could fail to get it up with someone as hot as you."
                    $ the_person.change_slut(2)
                    $ the_person.event_triggers_dict["impotence_tracker"] += 5
                    the_person "Well, that's the thing. He got it up but then once we started getting busy he... went soft."
                    mc.name "Two pump chump?"
                    if the_person.wants_creampie():
                        the_person "No, worse than that. He didn't cum, his condom was empty."
                    else:
                        the_person "No, worse than that. When he pulled out there wasn't any cum."
                    mc.name "Wow, I understand why you're concerned. Could he be seeing someone else?"
                    the_person "I don't think so... I guess maybe I need to watch him more. Well, thanks for listening [the_person.mc_title]."
            if the_person.love > 40:
                mc.name "No problem. You know, if he left you unsatisfied I could help out..."
                if not the_person.has_taboo("vaginal_sex") or not the_person.has_taboo("anal_sex") or not the_person.has_taboo("licking_pussy") or not the_person.has_taboo("touching_vagina"):
                    if the_person.get_opinion_score("cheating on men") < 0:
                        the_person "Seriously? I'm still with my [so_title]... but I really do need some help."
                    else:
                        the_person "I was hoping you would suggest something like that."
                    if len(mc.location.people) > 1:
                        the_person "Let's go somewhere a bit more private."
                if the_person.outfit.can_half_off_to_vagina():
                    $ generalised_strip_description(the_person, the_person.outfit.get_half_off_to_vagina_list(), position = "stand3", half_off_instead = True)
                else:
                    $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list(), position = "stand3")
                if not the_person.has_taboo("vaginal_sex") and the_person.arousal_perc > 30:
                    call fuck_person(the_person, start_position = SB_doggy_standing, private = True, start_object = make_wall(), skip_intro = False, skip_condom = False) from _call_fuck_person_i1
                elif not the_person.has_taboo("anal_sex") and the_person.arousal_perc > 20:
                    call fuck_person(the_person, start_position = SB_anal_standing, private = True, start_object = make_floor(), skip_intro = False, skip_condom = False) from _call_fuck_person_i2
                elif not the_person.has_taboo("licking_pussy") and the_person.arousal_perc > 10:
                    call fuck_person(the_person, start_position = standing_cunnilingus, private = True, start_object = make_floor(), skip_intro = False, skip_condom = False) from _call_fuck_person_i3
                elif not the_person.has_taboo("touching_vagina"):
                    call fuck_person(the_person, start_position = standing_finger, private = True, start_object = make_floor(), skip_intro = False, skip_condom = False) from _call_fuck_person_i4
                else:
                    "[the_person.possessive_title] starts and gives you a searching look as if trying to decide how serious you are."
                    if the_person.get_opinion_score("cheating on men") < 0:
                        the_person "Seriously? I'm still with my [so_title], I can't believe you would even suggest that."
                    else:
                        the_person "That's sort of sweet but also sort of weird. I'll keep you in mind if things don't improve."
            else:
                mc.name "No problem, I hope things get better for you and I'm here if you need to talk."
            the_person "I guess I'll see you around."
            $ the_person.draw_person(position = "walking_away")
            "As she walks away you take a moment to appreciate the view."
            "It seems like your serum is having an effect, but it hasn't pushed her hard enough to make any life altering decisions yet."
    # add a loop because different relationships should take more to end
    else:
        $ the_person.change_happiness(-20)
        the_person "Hey [the_person.mc_title], it's good to see you."
        if len(mc.location.people) > 1:
            "[the_person.title] takes a look around and then steps a bit closer to you, lowering her voice to nearly a whisper."
        the_person "Do you remember when I told you about [the_person.SO_name]'s little problem?"
        mc.name "I do, have things gotten any better?"
        the_person "No, unfortunately he wasn't even able to get it up the last time tried."
        the_person "I've been so frustrated, and he keeps swearing that there isn't another woman, but..."
        the_person "We fought and things got pretty ugly. We decided to split up."
        $ the_person.relationship = "Single"
        $ the_person.SO_name = None
        $ the_person.change_stats(happiness = -10)
        mc.name "I'm sorry to hear that, [the_person.title], just take it easy and take your time to process it."
        the_person "Thanks, it's appreciated."
        if the_person.has_role(affair_role):
            the_person "I know it's kind of sudden, but... since I'm single now we don't need to keep hiding what we have."
            $ the_person.remove_role(affair_role)
            menu:
                "Start dating her":
                    mc.name "I'm so happy to hear that! I would love to start dating you for real."
                    the_person "Thank god, I was a bit worried about being totally alone."
                    $ the_person.draw_person(position = "kissing", emotion = "happy")
                    "She wraps you in her arms and plants a firm kiss on your lips. It looks like you have a new girlfriend."
                    $ the_person.add_role(girlfriend_role)
                    $ the_person.change_stats(love = 5, happiness = 20)
                "Keep things casual":
                    mc.name "I don't know... what we have has been fun, but I wasn't really looking for something serious."
                    the_person "Right... of course... no pressue, I know this is really sudden."
                    $ the_person.draw_person(position = "kissing", emotion = "sad")
                    "She steps closer to wrap you in a hug and plants a tenative kiss on your cheek."
                    $ the_person.change_stats(love = -2, happiness = -5)
        the_person "I guess I'll see you around."
        $ the_person.draw_person(position = "walking_away")
        "As she walks away you take a moment to appreciate the view."
        "Altough it took some time it seems like your serum trait is working to end relationships."
    return
