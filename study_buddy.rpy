init -1 python:
    def study_buddy_nora_requirement(the_person):
        if lily.has_job(sister_student_job):
            if mc.business.event_triggers_dict.get("knows_study_day", False):
                if time_of_day < 3:
                    return True
        return False

    def study_buddy_prep_requirement(): # monday morning
        if lily.event_triggers_dict.get("study_buddy", False):
            if lily.has_job(sister_student_job):
                if lily.is_available:
                    if day%7 == 0:
                        if time_of_day == 0:
                            return True
        return False

    def study_buddy_serum_requirement(person):
        return person.location == lily.location and time_of_day == 3 and day%7 == 0

    def lily_classmates():
        classmates = []
        for person in known_people_in_the_game(excluded_people = [lily]):
            if person.has_role(student_role):
                classmates.append([person.name, person])
        return classmates

    def get_lab_partner():
        students = []
        for person in known_people_in_the_game(excluded_people = [lily]):
            if person.event_triggers_dict.get("study_buddy", False):
                return person
        for person in known_people_in_the_game(excluded_people = [lily]):
            if person.has_role(student_role):
                students.append(person)
        if students:
            person = get_random_from_list(students)
            person.event_triggers_dict["study_buddy"] = True
            return person
        return

    study_buddy_serum_action = Action("Study buddy serum", study_buddy_serum_requirement, "study_buddy_serum_label")
    study_buddy_date_action = Action("Study buddy date", evening_date_trigger, "study_buddy_date_label", requirement_args=0) #it happens on a monday
    study_buddy_prep_action = Action("Study buddy prep", study_buddy_prep_requirement, "study_buddy_prep_label")

    def study_buddy_mod_initialization():
        global study_buddy_nora_action
        study_buddy_nora_action = Action("Talk to [nora.name] about [lily.name]'s lab partner", study_buddy_nora_requirement, "study_buddy_nora_label", menu_tooltip = "Talk to Nora about Lily's lab partner.")
        nora_role.actions.append(study_buddy_nora_action)
        mc.business.add_mandatory_crisis(study_buddy_prep_action)


init 5 python: # hijack
    add_label_hijack("normal_start", "activate_study_buddy_mod_core")
    add_label_hijack("after_load", "update_study_buddy_mod_core")

label activate_study_buddy_mod_core(stack):
    python:
        study_buddy_mod_initialization()
        # continue on the hijack stack if needed
        execute_hijack_call(stack)
    return

label update_study_buddy_mod_core(stack):
    python:
        if "study_buddy_nora_action" not in globals():
            study_buddy_mod_initialization()
        execute_hijack_call(stack)
    return

label study_buddy_nora_label(the_person):
    $ the_person = nora
    $ the_sister = lily
    $ the_other_person = get_lab_partner()
    if not the_other_person:
        return
    $ change = True
    mc.name "I was hoping to talk to you about [the_sister.name]'s current lab partner."
    the_person "Oh, you mean [the_other_person.name]? Is something wrong?"
    if not town_relationships.get_relationship(the_other_person, the_sister):
        $ town_relationships.begin_relationship(the_other_person, the_sister)
    if town_relationships.get_relationship(the_other_person, the_sister).type_a =="Rival" or town_relationships.get_relationship(the_other_person, the_sister).type_a =="Nemisis":
        mc.name "Yeah, actually. They really don't get along, and I am worried that it is making it hard for them to agree on the way they should do things."
    elif town_relationships.get_relationship(the_other_person, the_sister).type_a =="Friend" or town_relationships.get_relationship(the_other_person, the_sister).type_a =="Best Friend":
        mc.name "Kind of, they are friends. Usually that would be great, but they've been spending more time chatting than working and I'm worried about it impacting [the_sister.name]'s grades."
    else:
        mc.name "Not really, but I was thinking that she could have a better partner to really shine in your class."
    the_person "That makes sense, but I can't just go changing lab partners in the middle of the semester."
    mc.name "Surely you've had to do it in the past."
    the_person "Occasionally. I should have said I can't change them without a reason. A good one, not just because someone asks."
    if the_person.love > 50:
        mc.name "Someone huh, I didn't think I was just someone to you."
        if the_person.is_girlfriend():
            the_person "That's not what I meant, you know I love you [the_person.mc_title]."
        else:
            the_person "I know we've been getting close, but I can't let every fling impact my career."
        mc.name "This is important to me, and any chance we have at a future is going to involve my sister. Surely you want her to be happy as much as I do."
        the_person "Okay, let me see if I can move people around a bit."
    elif the_person.obedience > 160:
        mc.name "Sorry, I wasn't really asking. I need you to do this for me."
        the_person "Yes [the_person.mc_title]. Sorry, I sometimes forget myself in teacher mode."
    else:
        mc.name "What if I could find a way to make it worth your while?"
        the_person "I suppose a sizable grant for my research would nessecitate some reorganization of class groups to allow me to focus on other priorities."
        menu:
            "Give her\n{color=#ff0000}{size=18}Costs: $5000{/size}{/color}" if mc.business.funds >= 5000:
                mc.name "Well I think we could arrange something along those lines. What do you think you'll need?"
                the_person "I imagine that $5000 would be enough to require me to shift focus, maybe bring in another teaching assistant."
                mc.name "I can certainly handle that."
                $ mc.business.change_funds(-5000)
                "You hand over the funds and she tucks them into her purse."
            "Reconsider":
                $ change = False
                mc.name "What do you think it would take to justify something like that?"
                the_person "I imagine that $5000 would be enough to require me to shift focus, maybe bring in another teaching assistant."
                mc.name "That's a bit steeper than I was hoping."
                the_person "Sorry, [mc.name], but I don't think I can justify something like this without a reason."
                mc.name "I understand, I'll get back to you if something changes."
            "Give her\n{color=#ff0000}{size=18}Requires: $5000{/size}{/color} (disabled)" if mc.business.funds < 5000:
                pass
    if change:
        "[the_person.title] pulls out her planner, flipping through to find [the_sister.name]'s class."
        the_person "Who would you like your sister to be partnered with from now on?"
        call screen enhanced_main_choice_display(build_menu_items([["Pick Lab Partner"] + lily_classmates()], draw_hearts_for_people = True))
        $ choice = _return
        mc.name "I think it would be best if she was partnered with [choice.name]."
        $ the_other_person.set_override_schedule(the_other_person.home, the_times = [3])
        $ the_other_person.event_triggers_dict["study_buddy"] = False
        $ choice.event_triggers_dict["study_buddy"] = True
        if day%7 == 0:
            call study_buddy_prep_label from _call_study_buddy_prep_label_nora
        the_person "Alright, I'll let them know the next time that we have class."
        mc.name "Thank you [the_person.title], I knew I could count on you to help me and my sister."
        the_person "Of course, is there anything else you need?"
    return

label study_buddy_prep_label():
    $ the_person = get_lab_partner()
    $ the_person.set_override_schedule(lily_bedroom, the_days = [0], the_times = [3])
    $ test_outfit = university_wardrobe.decide_on_outfit2(lily)
    $ lily.planned_outfit = test_outfit
    $ lily.apply_planned_outfit()
    $ test_outfit = university_wardrobe.decide_on_outfit2(the_person)
    $ the_panties = test_outfit.get_panties()
    $ the_bra = test_outfit.get_bra()
    if the_person.event_triggers_dict.get("bedroom_tax", 0) > 1:
        if the_panties:
            if the_panties.is_extension: #two piece item
                $ the_panties = next((x for x in test_outfit.get_upper_ordered() if x.has_extension == the_panties), None)
                $ the_bra = None
            $ test_outfit.remove_clothing(the_panties)
    else:
        if not the_panties:
            $ test_outfit.add_lower(panties.get_copy(),colour_white)
    if the_person.event_triggers_dict.get("bedroom_tax", 0) > 4:
        if the_bra:
            $ test_outfit.remove_clothing(the_bra)
    else:
        if not the_bra:
            $ test_outfit.add_upper(bra.get_copy(),colour_white)
    $ the_person.planned_outfit = test_outfit
    $ the_person.apply_planned_outfit()
    if mc.business.event_triggers_dict.get("knows_study_day", False):
        $ the_person.add_unique_on_room_enter_event(study_buddy_serum_action)
    $ mc.business.add_mandatory_crisis(study_buddy_date_action)
    return

label study_buddy_serum_label(the_person):
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_person.apply_planned_outfit()
    $ the_sister = lily
    $ the_sister.apply_planned_outfit()
    if the_person.event_triggers_dict.get("study_sessions", 0) < 1:
        "Typically you could expect a visit from [the_sister.name]'s lab partner, but thanks to you she has a new one this week."
        if mc.inventory.get_any_serum_count() > 0:
            "Expecting them to be hard at work you decide to just head to the kitchen and grab some drinks to bring up."
            $ mc.change_location(kitchen)
            $ mc.location.show_background()
            menu:
                "Add serum to [the_person.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_person) from _call_give_serum_new_study_buddy
                    if _return:
                        "You add a dose to her drink, then top it off with water."
                    else:
                        "You think about adding a dose of serum to her drink, but decide against it."
                "Add serum to [the_person.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass
                "Leave her drink alone":
                    "You top it off with water."
            menu:
                "Add serum to [the_sister.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_sister) from _call_give_serum_new_study_buddy2
                    if _return:
                        "You add a dose to her drink, then top it off with water."
                    else:
                        "You think about adding a dose of serum to her drink, but decide against it."
                "Add serum to [the_sister.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass
                "Leave her drink alone":
                    "You top it off with water."
            "With your hands full you announce yourself as you approach the door."
            mc.name "Hey girls, I brought you some water. Hard at work on your project?"
        else:
            "You decide to stop in and say hello breifly."
            "When you get to the door you knock on the door frame and see [the_sister.title] and [the_person.title] turn to greet you."
        $ mc.change_location(lily_bedroom)
        $ mc.location.show_background()
        $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
        $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
        if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
            the_person "Hi, [mc.name], nice to see you again!"
        elif town_relationships.get_relationship(the_person, the_sister).type_a =="Rival":
            the_person "Quite the pleasant suprise isn't it?"
            mc.name "I must admit that it is."
        else:
            the_person "Hello again."
        mc.name "Isn't today usually the day when you work with your lab partner?"
        if mc.charisma > 4:
            "With acting skills worthy of Hollywood you deftly deliver your line."
        elif mc.charisma > 2:
            "Although you are neither suprised or confused you do a passable job of making it sound that way."
        else:
            "You can't help but feel like your question is a bit wooden, fortunately they don't seem to notice."
        the_sister "Professor [nora.last_name] came into class this week with a new TA and rearranged a bunch of lab partners."
        the_sister "She said something about how adapting to changing workplaces would be an important skill to learn."
        mc.name "Well that makes sense, sometimes I have to move people around at work as priorities shift between research and production."
        the_sister "Yeah, I suppose, it's just tough starting over when the two different groups were approaching the project in different ways."
        the_person "It is somewhat beneficial though because we now have access to four people's work up to this point, even if their is some overlap in what got done."
        if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
            the_person "Plus it is great to be able to work with [the_sister.name] so we can spend more time hanging out."
            the_sister "Yeah, that is a bonus, if we had gotten to pick partners to start with I would have wanted to work with you."
            mc.name "I'm glad this is working out for you."
        elif town_relationships.get_relationship(the_person, the_sister).type_a =="Rival":
            the_person "Of course my previous lab partner was more knowledgeable than [the_sister.name], but over coming challenges is an imporant skill to learn too."
            the_sister "As if I'm going to be the one holding us back. If you spent more time studying I wouldn't need to spend so much explaining things to you as we work."
            mc.name "Hey now, it sounds like you might be stuck together, so you should at least try to be civil to each other."
        "You chat with them a bit more about what their project is, and give some advice based off of your time spent with [nora.name]."
        mc.name "I should probably let you get back to work. I'll be in my room for the night, early start tomorrow at work."
        $ scene_manager.clear_scene()
        $ the_person.event_triggers_dict["study_sessions"] = 1
    else:
        "You can expect a visit from [the_person.title] sometime this evening."
        if mc.inventory.get_any_serum_count() > 0:
            "Before that happens you want to take the opportunity to give her and [the_sister.possessive_title] a serum, so you head down to the kitchen and grab some drinks."
            $ mc.change_location(kitchen)
            $ mc.location.show_background()
            menu:
                "Add serum to [the_person.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_person) from _call_give_serum_old_study_buddy
                    if _return:
                        "You add a dose to her drink, then top it off with water."
                    else:
                        "You think about adding a dose of serum to her drink, but decide against it."
                "Add serum to [the_person.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass

                "Leave her drink alone":
                    "You top it off with water."
            menu:
                "Add serum to [the_sister.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_sister) from _call_give_serum_old_study_buddy2
                    if _return:
                        "You add a dose to her drink, then top it off with water."
                    else:
                        "You think about adding a dose of serum to her drink, but decide against it."
                "Add serum to [the_sister.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass
                "Leave her drink alone":
                    "You top it off with water."
            "With your hands full you announce yourself as you approach the door."
            mc.name "Hey girls, I brought you some water. Hard at work on your project?"
        else:
            "Before that you figure you can stop and say hello breifly."
            "When you get to the door you knock on the door frame and see [the_sister.title] and [the_person.title] turn to greet you."
        $ mc.change_location(lily_bedroom)
        $ mc.location.show_background()
        $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
        $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
        "You chat with them a bit more about what their project is, and give some advice based off of your time spent with [nora.name]."
        mc.name "I should probably let you get back to work. I'll be in my room for the night, early start tomorrow at work."
        $ scene_manager.clear_scene()
        $ the_person.event_triggers_dict["study_sessions"] += 1
    return

label study_buddy_date_label():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_person.apply_planned_outfit()
    $ the_sister = lily
    $ the_sister.apply_planned_outfit()
    if not mc.business.event_triggers_dict.get("knows_study_day", False):
        call lily_first_study_buddy(the_sister, the_person) from _call_lily_first_study_buddy
    else:
        "Today is the normal day for [the_sister.title] to study with her lab partner."
        if not mc.is_home():
            "Interacting with [the_person.title] is always a good way to spend an evening, of course if you have other plans you could always stay out until later tonight."
            menu:
                "Go home {image=gui/heart/Time_Advance.png}":
                    "You make the short trip home and put your things in your room."
                "Stay where you are":
                    "You decide not to head home today. There is always next week."
                    return
        else:
            "Interacting with [the_person.title] is always a good way to spend an evening, of course if you have other plans you could always go out until later tonight."
            menu:
                "Stay home {image=gui/heart/Time_Advance.png}":
                    "You decide wait for [the_person.title] and head to your bedroom so she can find you."
                    pass
                "Go out":
                    "You make the short trip downtown and start looking around for something to pass the time."
                    $ mc.change_location(downtown)
                    $ mc.location.show_background()
                    return
        $ mc.change_location(bedroom)
        $ mc.location.show_background()
    if the_person.event_triggers_dict.get("nemisis_with_benefits", 0) > 0:
        pass
    else:
        call lily_study_buddy_visit(the_person) from _call_lily_study_buddy_visit
    "A bit of time passes, but you eventually hear the front door closing as [the_person.title] goes home for the night."
    $ mc.business.add_mandatory_crisis(study_buddy_prep_action)
    $ clear_scene()
    return "Advance Time"

label lily_first_study_buddy(the_sister, the_person):
    if mc.is_home():
        "You are puttering around the house after a long day when you hear a suprising amount of noise coming from [the_sister.title]'s bedroom."
    elif mc.is_at_work():
        "It has been a long day and you are suddenly struck by the urge to go home for the night to relax."
        $ mc.change_location(bedroom)
        $ mc.location.show_background()
        "A quick trip later you are home and in your room."
        "As you are unpacking your things from the day you hear a suprising amount of noise coming from [the_sister.title]'s bedroom."
    else:
        "It has been a long day and you are suddenly struck by the urge to go home for the night to relax."
        $ mc.change_location(hall)
        $ mc.location.show_background()
        "When you get home and open the door you hear a suprising amount of noise coming from [the_sister.title]'s bedroom."
    $ scene_manager = Scene()
    "Curious, you head down the hall to see what is going on."
    $ mc.change_location(lily_bedroom)
    $ mc.location.show_background()
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "standing_doggy", emotion = "happy")
    $ scene_manager.add_actor(the_sister, position = "standing_doggy", emotion = "happy")
    "It looks like [the_sister.title] has company, and judging from the fact that they are both still in uniform, it must be one of her classmates."
    "They are both bent over [the_sister.title]'s desk, so you take a moment to enjoy the view before knocking on the door frame."
    mc.name "Hey girls, what are you up to?"
    $ scene_manager.update_actor(the_sister, position = "stand2")
    the_sister "Hey, [the_sister.mc_title], we've got a bit of a project for school and were working here instead of on campus."
    the_sister "Do you remember [the_person.name]? You met briefly on campus the other day."
    if not town_relationships.get_relationship(the_person, the_sister):
        $ town_relationships.begin_relationship(the_person, the_sister)
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped, position = "stand2")
    if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
        the_person "Hi, [mc.name], nice to see you again!"
    elif town_relationships.get_relationship(the_person, the_sister).type_a =="Rival":
        the_person "I'm sure he remembers me, after all who could forget a body like mine?"
    else:
        the_person "Hello again."
    mc.name "I was about to grab something to drink from the kitchen, would you like me to get you something too?"
    the_sister "Yeah, that would be great. I'll take a cola."
    the_person "Just water for me, thanks."
    mc.name "Alright, be right back."
    $ scene_manager.clear_scene()
    $ mc.change_location(kitchen)
    $ mc.location.show_background()
    if mom.location == kitchen:
        $ scene_manager.add_actor(mom, emotion = "happy")
        "When you get to the kitchen you see [mom.possessive_title] hard at work preparing dinner."
        mc.name "Just grabbing a drink for myself and the girls."
        $ scene_manager.clear_scene()
        $ mc.change_location(hall)
        $ mc.location.show_background()
    else:
        "When you get to the kitchen it doesn't take long for you to grab the drinks."
    if mc.inventory.get_any_serum_count() > 0:
        "With a moment of privacy you have the opportunity to slip some serum into the drinks."
        menu:
            "Add serum to [the_person.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                call give_serum(the_person) from _call_give_serum_first_study_buddy
                if _return:
                    "You add a dose to her drink."
                else:
                    "You think about adding a dose of serum to her drink, but decide against it."
            "Add serum to [the_person.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass
            "Leave her drink alone":
                "You think about adding a dose of serum to her drink, but decide against it."
        menu:
            "Add serum to [the_sister.title]'s drink" if mc.inventory.get_any_serum_count() > 0:
                call give_serum(the_sister) from _call_give_serum_first_study_buddy2
                if _return:
                    "You add a dose to her drink."
                else:
                    "You think about adding a dose of serum to her drink, but decide against it."
            "Add serum to [the_sister.title]'s drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass
            "Leave her drink alone":
                "You think about adding a dose of serum to her drink, but decide against it."
    $ mc.change_location(lily_bedroom)
    $ mc.location.show_background()
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
    $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
    "You hand them each their drinks and they thank you as they start to drink."
    "You chat with them a bit more about what their project is, and give some advice based off of your time spent with [nora.name]."
    mc.name "I should probably let you get back to work. I'll be in my room for the night, early start tomorrow at work."
    $ mc.business.event_triggers_dict["knows_study_day"] = True
    "As you make your way back to your room you realize that since you know their teacher, [nora.name], it might be possible to change who [lily.name] is studying with."
    "It might take some effort, but if you don't want to see [the_person.title] next week you should pay the campus a visit."
    $ the_person.event_triggers_dict["study_sessions"] = 1
    return

label lily_study_buddy_visit(the_person):
    $ the_sister = lily
    $ mc.change_location(bedroom)
    $ mc.location.show_background()
    $ the_person.draw_person()
    "A bit later in the evening, you hear a knock at your open door and look up to see [the_person.title] leaning against the door frame."
    mc.name "Oh, hey [the_person.name]. Do you need something?"
    if town_relationships.get_relationship(the_person, the_sister).type_a == "Rival": # increase obedience to progress
        the_person "Yeah, I think I've endured as much of your sister as I can for now."
        mc.name "Sorry to hear that, I know how she can be sometimes."
        the_person "Exactly, I was so glad for an excuse to come talk to you instead."
        call lily_study_buddy_rival(the_person) from _call_lily_study_buddy_rival
    elif town_relationships.get_relationship(the_person, the_sister).type_a == "Friend": # increase love to progress
        the_person "Yeah, we ran out of note cards and [the_sister.name] thought you might have some extra."
        mc.name "I think I can help you out, why don't you come in and talk with me while I look?"
        $ the_person.draw_person(position = "sitting")
        if the_person.love < 10:
            call small_talk_person(the_person, apply_energy_cost = False, is_phone = False)
        elif the_person.love < 20:
            call compliment_person(the_person)
        elif the_person.love < 25:
            call flirt_person(the_person)
        elif the_person.love < 35:
            call small_talk_person(the_person, apply_energy_cost = False, is_phone = False)
        else:
            call flirt_person(the_person)
        if the_person.love >= 20:
            $ planned_date = False
            the_person "You know, this isn't really fair to [the_sister.name]. Do you maybe want to spend time together when I'm not supposed to be working with her?"
            mc.name "That is a great idea, actually..."
            if the_person.love >= 40:
                if not mc.business.event_triggers_dict.get("dinner_date_scheduled", False):
                    call dinner_date_plan_label(the_person) from _call_dinner_date_plan_label_study
                    $ planned_date = True
            if the_person.love >= 30 and not planned_date:
                if not mc.business.event_triggers_dict.get("movie_date_scheduled", False):
                    call movie_date_plan_label(the_person) from _call_movie_date_plan_label_study
                    $ planned_date = True
            if not planned_date:
                if the_person.love < 50:
                    $ planned_date = True
                    mc.name "...did you have something in mind?"
                    the_person "I don't know, I'm pretty busy with school, but I usually have some free time in the middle of the day."
                    the_person "Maybe if you find yourself on campus we could get lunch together sometime."
                    mc.name "That sounds great, I'll try to arrange my schedule to have lunch free."
                    "[the_person.title] will be on campus every weekday afternoon, you should go invite her to lunch before next week."
            if not planned_date:
                "You chat for a bit, but things have gone about as far as they can in your room. If you want to do more you should probably ensure you are free to do other things."
                if mc.business.event_triggers_dict.get("dinner_date_scheduled", False) and the_person.love >= 40:
                    "You should probably ensure you are free to take her to dinner next Friday."
                if mc.business.event_triggers_dict.get("movie_date_scheduled", False) and the_person.love >= 30:
                    "You should probably ensure you are free to take her to the movies next Tuesday."
        "After your talk [the_person.title] gets up to go."
        if the_person.love >= 70:
            $ town_relationships.improve_relationship(the_person, the_sister)
    elif town_relationships.get_relationship(the_person, the_sister).type_a == "Best Friend":
        call lily_study_buddy_best_friend(the_sister, the_person) from _call_lily_study_buddy_best_friend
    else: # pick a path
        if not town_relationships.get_relationship(the_person, the_sister):
            $ town_relationships.begin_relationship(the_person, the_sister)
        the_person "Your sister had to go help your mom with dinner. I did a bit of work alone, but figured I would come chat with you a bit instead."
        if mom.has_job(mom_secretary_job) or mom.has_job(mom_associate_job):
            mc.name "Yeah, our mom has been working a bit harder than normal lately and as a result we end up helping out more around home."
        elif mom.is_employee():
            mc.name "Yeah, our mom has been working for my company which can mean long days sometimes."
        else:
            mc.name "Sorry about that, sometimes she just can't get everything done in a day."
        the_person "That's undertandable, family comes first, we have all week to work on this stuff."
        "[the_person.title] doesn't seem to have developed much of a relationship with [the_sister.possessive_title] yet, which means you can probably influence how they get along."
        "There could be some serious repurcutions of interferring with their relationship, but then again, there could be some benefits as well."
        "It seems like maybe you have been thinking about the possibilities a bit too long and [the_person.title] has noticed."
        the_person "You seem a little distracted, would it be better if I left?"
        menu:
            "Bring them together":
                mc.name "Sorry, I was just thinking how lucky my sister is to have a friend like you."
                the_person "Oh, I mean we are lab partners, but we barely know each other outside of class."
                mc.name "Really? I got the impression that you two were really hitting it off."
                the_person "She is nice, sweet, but the semester hasn't been going that long and well..."
                mc.name "That's fine, I just thought... she seems so happy on days she has class with you."
                the_person "I guess I thought she was just always happy, so upbeat. I don't really see her on the days when we aren't in class together."
                "She stops to consider your words. It is early, but it seems like she might be seeing thier relationship in a new light."
                $ town_relationships.improve_relationship(the_person, the_sister)
            "Drive them apart":
                mc.name "Sorry, I'm a little suprised, based on some of the things [the_sister.name] has said I was expecting something different."
                the_person "What? What do you mean? What has she said about me?"
                mc.name "I don't remember exactly, but I just got the impression that you weren't a great lab partner."
                the_person "Is that right? Well I guess I'll go see what makes me so terrible."
                mc.name "No, I shouldn't have said that. Please, just forgot it, maybe she was talking about someone else."
                the_person "Really?"
                mc.name "I don't know, is there anyone else named [the_person.name] in your classes?"
                the_person "Well we don't share all the same classes..."
                mc.name "Look, I don't want the two of you to fight, and you're probably stuck together for the semester so it would be best if you forget I said anything."
                "She stops to consider your words, but it is pretty clear that you have driven a wedge between them and they'll probably never be friends."
                $ town_relationships.worsen_relationship(the_person, the_sister)
        "You let the pause linger, but it starts to get a bit awkward."
        mc.name "So... um... sorry for overstepping a bit. I didn't mean to kill the conversation."
        the_person "No, it's okay. I should probably be getting back anyway. We do have work to do tonight."
        mc.name "Okay, good luck and have a good night."
        the_person "Thanks, I'll probably see you next week if we are still studying here."
    $ clear_scene()
    return

label lily_study_buddy_rival(the_person):
    $ the_bottom = the_person.outfit.get_lower_top_layer()
    $ the_panties = the_person.outfit.get_panties()
    if the_panties:
        if the_panties.is_extension: #two piece item
            $ the_panties = next((x for x in the_person.outfit.get_upper_ordered() if x.has_extension == the_panties), None)
            $ the_bra = None
    else:
        $ the_bra = the_person.outfit.get_bra()
    $ no_underwear = the_person.get_opinion_score("not wearing underwear")
    if no_underwear < 0:
        $ no_underwear = 0
    if the_person.event_triggers_dict.get("bedroom_tax", 0) > 2:
        if the_person.event_triggers_dict.get("bedroom_tax", 0) < 5:
            $ the_person.change_stats(arousal = 10 * no_underwear)
        else:
            $ the_person.change_stats(arousal = 20 * no_underwear)
    $ the_person.draw_person()
    if the_person.event_triggers_dict.get("bedroom_tax", 0) < 1: #ask for panties
        $ the_person.event_triggers_dict["bedroom_tax"] = 1
        mc.name "Well I don't mind having some company, but there is a service charge for providing sanctuary."
        the_person "A service charge?"
        mc.name "Yes, a token of your appreciation for my assistance."
        mc.name "I want you to give me your panties..."
        if the_panties:
            $ the_person.draw_animated_removal(the_panties)
            $ the_person.change_stats(obedience = 5, slut = 1, max_slut = 30)
        "[the_person.possessive_title] takes a quick look at the door and pulls off her [the_panties.display_name], placing them in your hand."
        $ the_person.change_stats(arousal = 5 * no_underwear)
        $ the_person.discover_opinion("not wearing underwear")
        if the_person.get_opinion_score("not wearing underwear") < 0:
            $ the_person.change_stats(happiness = 2*the_person.get_opinion_score("not wearing underwear"))
            the_person "I can't believe I did that."
            "She brushes at her skirt trying to smooth it lower down her legs, it almost looks like she wants to pull it lower."
            mc.name "Relax [the_person.title] I can't see anything, promise. Why don't you have a seat?"
            "She moves to the bed, and while holding her legs together tightly lowers herself to sit, you can tell she is still self conscious."
        elif the_person.get_opinion_score("not wearing underwear") == 0:
            the_person "This feels kind of weird, do you mind if I sit down?"
            mc.name "Go ahead, there is plenty of room on the bed."
            "She moves a little stiffly, like she is trying to watch herself walk but she settles down just fine."
        else:
            the_person "Kinky! Tell me, do you make all the girls who come in your room strip for you?"
            mc.name "Of course, I've got [lily.name] trained so well that she doesn't even wear them around the house any more."
            "[the_person.possessive_title] breaks into loud laughter, but when you don't join her she hesitates."
            the_person "Wait, seriously? No you must be joking."
            "You grin at her, but neither confirm or deny."
            the_person "Man, she's lucky I like you or I'd spread that rumor all over school."
            "She drops down to sit on your bed, totatlly unconcerned with her lack of underwear."
        $ the_person.draw_person(position = "sitting")
        "You chat for a bit about her class work and your company. It is fun, but eventually she prepares to head back to your sister."
        "With her [the_panties.display_name] still laying on your desk she hesitates."
        the_person "So... do I get those back when I leave?"
        mc.name "Nope, those are mine now. You'll have to bring another pair next week if you want to hang out again."
        if the_person.get_opinion_score("not wearing underwear") < 0:
            the_person "God you are such a pervert... but I'll think about it."
        elif the_person.get_opinion_score("not wearing underwear") == 0:
            the_person "Fine, but just know you are kind of weird."
        else:
            the_person "I'll wear something special for you."
        $ the_person.draw_person(position = "walking_away")
        "As you watch her leave you think that you have taken a good first step."
        if the_person.get_opinion_score("not wearing underwear") < 1:
            "She seems willing to follow your orders, but to really progress you will have to ensure she loves not wearing underwear."
        else:
            "She seems willing to follow your orders, and eager to not wear underwear. Next week should be exciting."
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) == 1: #she offers panties
        if the_person.get_opinion_score("not wearing underwear") > 0:
            $ the_person.event_triggers_dict["bedroom_tax"] = 2
        "She takes a look back at the hallway and then steps into your room and reaches up under her skirt."
        if the_panties:
            $ the_person.draw_animated_removal(the_panties)
        $ the_person.change_stats(obedience = 5, slut = 1, arousal = 10 * no_underwear, max_slut = 30)
        "When she pulls her hands back out they are gripping her [the_panties.display_name] and she is quick to hold them out to you."
        the_person "Don't worry, I remembered your service charge."
        if the_person.arousal >= 20:
            "You take them in your hand and are suprised to feel that they are not only warm but quite wet as well."
            mc.name "Wow, if I didn't know better I would say you were exited about standing here without underwear."
            the_person "I mean if I'm honest it was pretty exciting. Both sitting here with you and when I got back to [lily.name]."
            the_person "In fact, on my way home I took advantage of the easy access, and nearly ran a red light."
            mc.name "Well if you want some help before you leave I think I could lend you a hand."
            "She grins at you and pushes the door closed behind her."
            the_person "I've been hoping you would say that."
            $ the_person.draw_animated_removal(the_bottom, position = "missionary", half_off_instead = True)
            "She drops down onto your bed, spreading her legs for you and hiking up her skirt."
            menu:
                "Use your hand":
                    call fuck_person(the_person, private = True, start_position = standing_finger, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit1
                "Use your tongue":
                    call fuck_person(the_person, private = True, start_position = standing_cunnilingus, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit2
        elif the_person.arousal >=10:
            "You take them in your hand are suprised to feel that they are not only warm but a bit damp."
            mc.name "Is someone excited to see me?"
            "She blushes a bit, but smiles at the same time."
            the_person "I admit the thought of spending more time with you did cross my mind."
            the_person "I've been thinking about you on and off all day, and now that I'm here... well..."
            $ the_person.draw_animated_removal(the_bottom, position = "stand2", half_off_instead = True)
            "She hikes up her skirt to show you her glistening pussy lips."
            $ the_person.break_taboo("bare_pussy")
            mc.name "Wow, [the_person.title] you are incredible."
            the_person "With compliments like that I might let you touch it sometime."
            mc.name "What about right now?"
            the_person "Why don't you sit next to me and we can take it slow."
            call fuck_person(the_person, private = True, start_position = kissing, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit3
        else:
            mc.name "So eager to strip as soon as you're in my presence?"
            the_person "No... it's not like that... I just kept thinking about last time."
            the_person "I couldn't focus on anything else, and I think my body got confused."
            mc.name "As someone who frequently had to deal with raging hormones I think I know what that is like."
            mc.name "In fact, if you let me I think I know a way to help you with your predicament."
            the_person "Really? Some kind of meditation or calming exercises to refocus my mind."
            mc.name "Oh, sorry that might be possible but I have a more direct and simple solution."
            the_person "What do you mean more direct?"
            mc.name "Well you know... finding release..."
            "It takes a moment but suddenly realization dawns across her face as her mouth drops open."
            the_person "You can't be serious. At someone else's house, in your bedroom?"
            mc.name "I don't mind. You have my permission. I just want to help."
            if the_person.has_taboo("touching_pussy"):
                "A look of horror, or possibly disgust crosses her face."
                the_person "No, absolutely not!"
                mc.name "Not with my hands, just with a safe place for you to find what you need."
            if the_person.has_taboo("bare_pussy"):
                the_person "You just want to watch is what."
                mc.name "I mean... I would, but if you'll feel better I can keep watch outside."
            else:
                the_person "That's nice I guess, but I couldn't with your family out there."
                mc.name "Well if you think you can handle it alone I'll keep guard outside for you."
            "Without really giving her a chance to respond you step out into the hallway."
            $ mc.change_location(hall)
            $ mc.location.show_background()
            $ the_person.run_orgasm(show_dialogue = False, trance_chance_modifier = the_person.get_opinion_score("masturbating"), add_to_log = False, fire_event = False)
            "It is a bit boring in the hallway, and despite your best efforts you can't hear what is happening in your room."
            "Eventually the door opens and [the_person.title] steps out. She looks a bit flushed but she was before you stepped out too."
            "She looks at you and opens her mouth to say something then stops. You give her a grin which seems to make up her mind for her."
            the_person "I'm gonna go... Don't say anything. Let's pretend this didn't happen."
        if  the_person.get_opinion_score("not wearing underwear") < 1:
            "It seems like [the_person.title] has accepted giving you her panties, but to really progress you will have to ensure she enjoys not wearing underwear."
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) == 2: #she isn't wearing panties
        if the_person.get_opinion_score("showing her tits") > 0:
            $ the_person.event_triggers_dict["bedroom_tax"] = 3
        mc.name "Not that I mind spending time with you, but don't you owe me a pair of panties?"
        the_person "I would love to do that [the_person.mc_title], except I'm not wearing any..."
        mc.name "Really? So today at school you were walking around bare?"
        the_person "Yeah, I've been doing it more and more often since I started hanging out with you."
        mc.name "As exciting as that is, it does leave us with a bit of a problem."
        if the_person.get_opinion_score("not wearing underwear") == 2:
            the_person "Oh right! Well here, you can have my bra instead today."
        else:
            the_person "Oh right... I didn't think about that."
            mc.name "That's fine. I'll take your bra instead today."
        if the_person.has_taboo("bare_tits"):
            $ the_person.break_taboo("bare_tits")
        $ the_person.discover_opinion("showing her tits")
        $ top_list = the_person.outfit.get_tit_strip_list(visible_enough = True)
        if top_list:
            while top_list:
                $ clothing = get_random_from_list(top_list)
                $ the_person.draw_animated_removal(clothing)
                $ top_list.remove(clothing)
        if the_bra:
            $ the_person.draw_animated_removal(the_bra)
            $ the_person.change_stats(arousal = 5 * no_underwear)
        if the_person.has_large_tits():
            mc.name "You know, while you have those out I think I could find a use for them."
            call fuck_person(the_person, private = True, start_position = tit_fuck, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit4
        else:
            mc.name "You know, seeing you standing there topless is going to cause me a bit of a problem."
            mc.name "Fortunately it is a problem you could help me with."
            call fuck_person(the_person, private = True, start_position = handjob, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = True, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit5
        if the_person.get_opinion_score("showing her tits") < 1:
            "It seems like [the_person.title] was willing to show you her tits, but to really progress you will have to ensure she enjoys doing so."
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) == 3: #she offers bra
        if the_person.get_opinion_score("not wearing underwear") > 1:
            if the_person.get_opinion_score("showing her tits") > 1:
                $ the_person.event_triggers_dict["bedroom_tax"] = 4
        while the_person.outfit.bra_covered():
            $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
            $ the_person.draw_animated_removal(the_item, half_off_instead = True)
        if the_bra:
            $ the_person.draw_animated_removal(the_bra)
            $ the_person.change_stats(arousal = 10 * no_underwear)
        the_person "You know, if I keep giving you all of my underwear soon I won't have any to wear."
        mc.name "Would that be so bad? It seems like you are enjoying being without."
        the_person "It has been fun, but there are times when I do need to wear some."
        mc.name "We could probably find another way for you to compensate me for helping you escape my sister."
        the_person "What did you have in mind?"
        mc.name "Well I have some other needs you could take care of while you are here."
        "You make a significant gesture towards your pants and she quickly gets the idea."
        $ the_person.discover_opinion("sucking cock")
        if the_person.get_opinion_score("sucking cock") > 1:
            the_person "Oh, that sounds like fun. Maybe next week I'll forget to wear any underwear."
            $ the_person.event_triggers_dict["bedroom_tax"] = 4
        if the_person.get_opinion_score("sucking cock") == -2:
            the_person "No, no way. I'm not going to blow you just to avoid your sister."
        else:
            if the_person.has_taboo("sucking_cock"):
                the_person "You want me to suck your cock?"
                mc.name "Sure, I mean we've been doing some other stuff, don't you think it is time to move on?"
                if the_person.has_taboo("licking_pussy"):
                    the_person "I suppose we could, but maybe you should go first."
                    mc.name "Of course, I'm ready now if you want to close the door."
                else:
                    the_person "I suppose that would only be fair, after all you've taken care of me before."
                    mc.name "Exactly, in fact I could help you now and next week you can return the favor."
                call fuck_person(the_person, private = True, start_position = standing_cunnilingus, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit6
            else:
                the_person "Oh, I guess I could do that. Although I'm not sure it's worth it just to avoid your sister."
                mc.name "We could probably find a way for you to enjoy it too."
                call fuck_person(the_person, private = True, start_position = SB_sixty_nine, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit7
        if the_person.get_opinion_score("not wearing underwear") < 2:
            "It seems like [the_person.title] was willing to not wear underwear, but to really progress you will have to ensure she loves going commando."
        if the_person.get_opinion_score("showing her tits") < 2:
            "It seems like [the_person.title] was willing to show you her tits, but to really progress you will have to ensure she loves doing so."
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) == 4: #she isn't wearing underwear
        if the_person.get_opinion_score("giving blowjobs") > 0:
            $ the_person.event_triggers_dict["bedroom_tax"] = 5
        mc.name "I'm glad you're here [the_person.title]. Tell me, what do you have for me today?"
        the_person "I'm sorry [the_person.mc_title], I have a problem. I don't have any underwear today."
        mc.name "Really? None at all?"
        the_person "None. Ever since last week I've been going without every day."
        mc.name "Well, as happy as I am that you have grown to accept not wearing underwear that does present an issue."
        mc.name "I wonder if there is something else you could give me tonight..."
        the_person "I'm not really wearing enough clothes anymore to get rid of them."
        mc.name "Well it has been clothing in the past but there are other things that you can give me. Lets think services instead of goods."
        if the_person.has_taboo("sucking_cock"):
            the_person "What do you mean?"
            mc.name "I've got a problem here that you should be able to solve."
            "She doesn't seem to understand at first, but with a emphatic gesture you are able to help her figure it out."
            if the_person.get_opinion_score("giving blowjobs") < 0:
                the_person "No. That's not going to happen."
                if the_person.obedience > 180:
                    mc.name "Sorry, I wasn't asking. I need you to do this for me."
                else:
                    mc.name "Come on, [the_person.title]. I'll make it worth your while."
                    if the_person.get_opinion_score("giving blowjobs") == -2:
                        the_person "No means no. You're gonna have to think of something else or I'll leave."
                    else:
                        the_person "Well I guess that wouldn't be so bad if you return the favor."
                        call fuck_person(the_person, private = True, start_position = SB_sixty_nine, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit8
        else:
            the_person "Oh, right. What would you like me to do for you?"
            mc.name "Thinking about your visit has caused me a bit of a problem."
            "You walk towards her, pulling the zipper of your pants down."
            mc.name "Get on your knees, I think you can solve both our problems at once."
        call fuck_person(the_person, private = True, start_position = blowjob, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit9
        if the_person.get_opinion_score("giving blowjobs") < -1:
            "It seems like [the_person.title] hates sucking cock, to really progress you will have to ensure she enjoys doing so."
        elif the_person.get_opinion_score("giving blowjobs") < 1:
            "It seems like [the_person.title] was willing to suck your cock, but to really progress you will have to ensure she enjoys doing so."
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) >= 5: #she blows you repeat
        if the_person.obedience >= 180:
            $ the_person.event_triggers_dict["bedroom_tax"] = 6
        mc.name "I'm glad you're here [the_person.title]. Tell me, what do you have for me today?"
        the_person "I'm still not wearing any underwear, but don't worry, I will gladly provide you with some servicing instead."
        "She wastes no time, closing the door and dropping to her knees."
        call fuck_person(the_person, private = True, start_position = blowjob, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = False, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit10
        if the_person.obedience < 180:
            "[the_person.title] has been willing to follow specific commands, but to really progress you will have to ensure she is obedient in all situations."
        if not the_person.event_triggers_dict.get("story_over", False):
            $ the_person.event_triggers_dict["story_over"] = True
            "END OF STORYLINE"
            "You can continue to have [the_person.title] study with [the_sister.name], but there is no more content."
            "I have an idea to continue, but it may never materialize."
            "You can find her a new partner by talking to [nora.name] [nora.last_name]."
    "Perhaps with the proper serums and a few orgasms you could convince her to change her opinions."
    if the_person.has_role(trance_role):
        call check_date_trance(the_person) from _call_check_date_trance_rival
    "For now, you have accomplished all you can. [the_person.name] puts herself back together and heads back to continue working with [lily.title]."
    return

label lily_study_buddy_best_friend(the_sister, the_person):
    if the_person.event_triggers_dict.get("anger", 1) > 0:
        call study_friend_transition(the_sister, the_person) from _call_study_friend_transition
    elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 1:
        $ the_person.event_triggers_dict["friend_with_benefits"] = 1
        call lily_first_best_friend(the_sister, the_person) from _call_lily_first_best_friend
    # elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 2:
    #     $ the_person.event_triggers_dict["friend_with_benefits"] = 2
    #     call lily_second_best_friend(the_sister, the_person) from _call_lily_second_best_friend
    # elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 3:
    #     $ the_person.event_triggers_dict["friend_with_benefits"] = 3
    #     call lily_third_best_friend(the_sister, the_person) from _call_lily_third_best_friend
    # elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 4:
    #     $ the_person.event_triggers_dict["friend_with_benefits"] = 4
    #     call lily_forth_best_friend(the_sister, the_person) from _call_lily_forth_best_friend
    # elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 100:
    #     call lily_offscreen_corruption(the_sister, the_person) from _call_lily_offscreen_corruption
    # else:
    #     call lesbian_sex(the_sister, the_person) from _call_lesiban_sex_FWB
    else:
        "END OF STORYLINE"

label study_friend_transition(the_sister, the_person):
    if the_person.event_triggers_dict.get("anger", 0) == 0:
        $ the_person.event_triggers_dict["anger"] = 0
        $ happy = 10
        the_person "[the_person.mc_title], can we talk?"
        mc.name "Sure, what's up?"
        if the_person.event_triggers_dict.get("study_sessions", 0) > 6:
            the_person "I've been having a lot of fun with you the last few months."
        else:
            the_person "I've been having a lot of fun with you the last few weeks."
        if the_person.has_role(girlfriend_role):
            the_person "There's no easy way to say this, so I'll just say it: I think we should break up."
        else:
            the_person "I just don't see a real future for us together so I wanted to stop things before they develop further."
        $ the_person.draw_person(emotion = "sad")
        menu:
            "Be dismissive":
                mc.name "Oh, that's fine. I was thinking the same thing actually."
                the_person "Oh... um... well I've been developing feelings for someone else... and..."
                mc.name "That's fine, I hope they make you happy."
                if the_person.has_role(girlfriend_role):
                    the_person "Nothing happened."
                    mc.name "I believe you, it's fine. We are both young, plenty of fish and all that."
            "Be understanding":
                mc.name "Oh, really?"
                the_person "I'm sorry I just don't feel a spark, I think I want to see what else is out there."
                mc.name "Oh, well okay. School is a great time to explore. I hope you can find happiness."
                the_person "Thanks, you too."
            "Get angry":
                $ happy +=10
                $ the_person.event_triggers_dict["anger"] += 1
                if the_person.has_role(girlfriend_role):
                    mc.name "You're breaking up with me? I'm the best thing that ever happened to you."
                    the_person "I'm not sure that's true, but I think I'm looking for something else."
                    mc.name "Oh yeah, what is his name? Have you already started cheating on me?"
                    $ the_person.draw_person(emotion = "angry")
                    the_person "It's not like that, nothing happened."
                    mc.name "Oh, but there is someone else? One of the other students?"
                    the_person "What... no."
                    "It seems like you might have hit pretty close to the mark there, but she doesn't seem like she is going to elaborate."
                if the_person.number_of_children_with_mc() > 0:
                    if the_person.number_of_children_with_mc() > 1:
                        mc.name "What about our kids?"
                    else:
                        mc.name "What about our kid?"
                    the_person "I'm not going to spend the next 20 years with someone just so they can have their parents in the same house."
                    the_person "We'll figure something out if you actually want to be a part of their life."
        the_person "I'm sorry, but it's just the way things are."
        menu:
            "Let her go":
                $ the_person.draw_person(emotion = "sad")
                mc.name "I guess this is goodbye?"
                the_person "Well I'll still be around, but probably going to stick to your sister's room a bit more when we study."
            "Be cruel":
                $ happy +=10
                $ the_person.event_triggers_dict["anger"] += 1
                mc.name "Well at least now I don't have to keep hiding my other girls from you."
                mc.name "I've got this one, you should see her..."
                $ the_person.draw_person(emotion = "angry")
                if not the_person.has_large_tits():
                    mc.name "You can actually tell she is a girl with tits big enough to find under her shirt."
                elif the_person.body_type == "curvy_body":
                    mc.name "She actually takes care of herself, not waddling around like your fat ass."
                elif the_person.int < 3:
                    mc.name "In addition to the body she has a brain, I never have to explain things to her."
                else:
                    mc.name "She should be a model, not like your ugly mug."
                mc.name "I can't believe I put up with you so long."
                the_person "I can't believe I was agonizing over this decision, I should have made it weeks ago."
        $ the_person.remove_role(girlfriend_role)
        $ the_person.change_stats(love = -40, happiness = -happy)
    else:
        the_person "Yeah, your sister ran out of note cards again. I think she wants us to talk."
        if the_person.event_triggers_dict.get("anger", 0) > 1:
            mc.name "Because it worked so well last time?"
            the_person "I know, but I think she is worried about me, and probably about you too."
            mc.name "She does have a tendency to care about the people around her."
            the_person "Yeah, she can be annoyingly great that way..."
            "The conversation stalls as you both reflect on what has happened."
            $ the_person.draw_person(emotion = "sad")
            the_person "I'm leaving."
            mc.name "No, wait we can talk."
            the_person "I don't just mean right now, I... I'm transfering schools. There is too much baggage here, and it's really easy to change schools this early."
            "That is pretty huge, you could probably stop her if you wanted to, but she might be gone forever after this."
            menu:
                "Let her go":
                    mc.name "Thats... a big step, but if you think you need to go I'm not going to stop you."
                    the_person "I didn't figure you would, I just feel bad about [the_sister.name]. I don't want her blaming herself."
                    mc.name "I'll talk to her, that is at least one thing we can agree on. I'll make sure she is okay."
                    the_person "Thanks, and well goodbye I guess."
                    mc.name "Goodbye."
                    $ the_person.remove_person_from_game()
                    "Things sort of spiralled out of control there. [the_sister.title] is going to need a new study buddy. You'll have to see who it is next week."
                    $ get_lab_parter()
                "Stop her":
                    mc.name "Wait, you don't need to do that. We can get past this."
                    the_person "Can we? Really?"
                    mc.name "Look, [the_sister.name] really likes spending time with you and I don't want to break that up."
                    mc.name "I could have handled this better, why don't we give it another week and see if things can get better."
                    the_person "Okay, I'll see you next week I guess."
                    "Things are better, but if you really want to patch things up you are probably going to have to apologize next week."
                    $ the_person.change_happiness(10)
                    $ the_person.event_triggers_dict["anger"] -= 1
        else:
            mc.name "Yeah, sure. Maybe you'd like to mooch off of me some more."
            $ the_person.draw_person(emotion = "angry")
            the_person "It's not like that, she knows things are broken between us it is upsetting her."
            "Things are a bit rough, but you could probably salvage the situation if you are willing to be the bigger person."
            menu:
                "Apologize":
                    mc.name "I know, she can care so much. It is one of the best things about her."
                    $ the_person.draw_person(emotion = "sad")
                    the_person "Something we can agree on, she really is great."
                    mc.name "Look, for what it's worth I am sorry. I got carried away in the moment."
                    the_person "You did let a bit of rage show, but I was breaking up with you, can't expect something like that to go well."
                    mc.name "I still should have handled it better, really I am sorry. Can we put that behind us, maybe be friends."
                    the_person "I think I'd like that, after all, I'm still going to be hanging around with your sister all the time."
                    mc.name "Right, that's good. I guess I'll see you next week."
                    the_person "Yeah, thanks [the_person.mc_title]."
                    $ the_person.event_triggers_dict["anger"] -= 1
                    $ the_person.change_happiness(20)
                    $ town_relationships.improve_relationship(the_person, the_sister)
                "Taunt her":
                    mc.name "Remind me whose fault that is? You're the one who broke things."
                    the_person "I know, but that doesn't mean we can't be civil."
                    mc.name "Civil? Tell me, did you find the something else you were looking for? Is he rocking your world?"
                    the_person "Look, I'm trying to salvage this for [the_sister.name], surely you care about her even if you don't care about me."
                    mc.name "She's a big girl, if she wants us to get along she'll just have to be unhappy."
                    the_person "Fine, whatever, I can't believe I thought this would work. Hopefully she won't make me do this again next week."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-10)
                    $ the_person.event_triggers_dict["anger"] += 1
    "With that she leaves you alone in your room to think."
    return

label lily_first_best_friend(the_sister, the_person):
    $ scene_manager = Scene
    $ scene_manager.add_actor(the_person)
    mc.name "I've got some note cards right here if you need more."
    "You give a weak smile and she returns it, shaking her head a bit at the joke."
    the_person "No... I wanted to apologize again. I know I kind of blind sided you and I wanted to make sure things were good between us."
    mc.name "I admit it was suprising, but I'll get over it. Does that mean you'll still be around."
    the_person "At least for the semester, and after that... well I hope to keep spending time with [the_sister.name]. If that's okay with you."
    mc.name "Of course, I'd never put some minor awkwardness over the happiness of my sister."
    the_person "Thank you, spending time with [the_sister.name] is important to my happiness too."
    mc.name "It is good that you two get along so well. I know it can sometimes be hard to find friends in a class."
    the_person "Friends... right, has she... um... said anything about our friendship?"
    mc.name "She likes you, thinks you are smart and hard working."
    the_person "Oh, likes me as a classmate, that is good I suppose."
    mc.name "As a person too, she thinks you are fun to spend time with."
    $ scene_manager.update_actor(the_person, emotion = "sad")
    the_person "Yeah... she is great too..."
    "Something about the way she looks off into space as she talks about [the_sister.name] catches your attention."
    mc.name "Were you hoping maybe for something more than just friendship with my sister?"
    "[the_person.name] blushes and turns her head slightly."
    $ scene_manager.update_actor(the_person, emotion = "happy")
    the_person "I never see her with boys at school, it's like she just doesn't see them. So I started to wonder if she was, you know..."
    the_person "Sorry, is this going to make things more awkward?"
    mc.name "It doesn't have to, in fact it might make it less so. I mean I don't have to worry about what I did wrong if [the_sister.name] is the reason you broke off our relationship."
    the_person "That was a big part of it, I meant it when I said I was looking for something different. I didn't think explaining it at the time would help."
    mc.name "At the time it probably wouldn't have, but I understand."
    the_person "At the risk of making it awkward again... do you know if [the_sister.name] would ever consider someone like me?"
    "That is a tough question, you might want to be careful how you answer. It could have a pretty big impact on how your relationships progress."
    menu:
        "Absolutely (not fully written) (disabled)":
            mc.name "She would definitely be open to the idea of spending time with another woman."
            mc.name "She has done it before, but usually with a man present as well."
            the_person "Wow, I didn't think she was that adventurous. Do you happen to know what guy it was with?"
            menu:
                "Tell her":
                    mc.name "It was me, we have been fucking for awhile, and recently our mom joined us as well."
                    mc.name "If you'd like, I could suggest that you join us the next time we are looking for an extra partner."
                    "[the_person.title]'s face clearly shows her shock. She stands there frozen not sure how to react."
                    mc.name "I'm serious, if you'd like we can go ask right now. I'm sure she wouldn't mind."
                    "She stammers a bit, but clearly can't form a coherent response."
                    "You figure it might be better to cut to the chase, so you take her by the wrist and gently pull her down the hall to your sister's room."
                    $ scene_manager.update_actor(the_sister, position = "sitting")
                    mc.name "Hey, [the_sister.title], [the_person.name] thinks you are hot and wondered if you would ever consider someone like her."
                    if willing_to_threesome(the_person, the_sister):
                        the_sister "That is sweet, she is pretty sexy too. Do you think we should get together."
                        mc.name "Absolutely, you two would be so hot together. I'd love to watch, or maybe even join in."
                        the_sister "Sounds good to me, what do you think [the_person.name]."
                        "[the_person.name] still can't figure out what to do, and stands there stunned."
                        "[the_sister.name] grins and starts to walk forward, slowly pulling at the hem of her shirt to expose part of her midriff."
                        if willing_to_threesome(the_person, the_sister):
                            "[the_person.name] is still frozen, but it is clear she wants this to happen."
                            "By the time [the_sister.title] is next to [the_person.name] her shirt is off, and she leans forward to kiss her tentatively."
                            the_person "God, this is going so fast but I am so excited."
                            $ the_person.event_triggers_dict["friend_with_benefits"] = 100




                        else:
                            "[the_person.name] takes a step back, horror starting to appear on her face."
                            "Suddenly, [the_sister.name] doubles over laughing, dropping her seductive act."
                            the_sister "I'm so sorry, [the_person.name]. I couldn't resist playing along. The look on your face."
                            "[the_sister.name] shoots you a dirty look while [the_person.name] isn't watching."
                            $ the_sister.change_happiness(-5)
                            the_person "Wait, what do you mean?"
                            mc.name "I'm sorry [the_person.title], I was just messing with you."
                            the_sister "I should have warned you about my brother, he can be so inappropriate sometimes."
                            the_person "Oh, right, I should have known you wouldn't be interested in me."
                            "[the_person.title] looks crestfallen as she takes another step back"
                            the_sister "Wait, he didn't make up that part?"
                            "[the_person.title] stammers a bit but can't get anything coherent out, instead she turns and rushes down the hall towards the bathroom."
                            the_sister "God, [mc.name], you have a real way with people you know that."
                            mc.name "I just don't see any reason to hesitate, I was trying to help."
                            the_sister "Well I think you've done enough, why don't you leave us alone for a bit."
                            $ the_person.change_happiness(-5)
                            $ the_person.event_triggers_dict["friend_with_benefits"] = 4
                            "Well, that was interesting. You head back to your room while [the_sister.title] goes to try and talk with [the_person.title]."


                    else:
                        the_sister "Not funny, mc.name. I've told you not to harass my friends when they are over."
                        $ the_sister.change_happiness(-5)
                        $ the_sister.change_love(-5)




                "Be cautious":
                    mc.name "It's not really something I got a ton of details about..."
                    the_person "Right, of course. She is your sister after all."
                    mc.name "Exactly, but if you want I can try and talk to her and find out more. See if maybe you have a chance."
                    the_person "Really? Thanks, [mc.name] that would be great."
                    $ the_person.change_happiness(5)
                    mc.name "Come see me next week and I'll give you an update."
        "Possibly":
            mc.name "I know she has been fairly non-traditional with relationships in the past."
            mc.name "I don't see any reason why it wouldn't work with you."
            the_person "Oh, good, I've been so nervous about scaring her away if it wasn't something she wants."
            mc.name "I could talk to her if you want, see what she thinks of the idea."
            the_person "That would be great, thanks [the_person.mc_title]!"
            mc.name "Come see me next week and I'll give you an update."
        "Maybe":
            mc.name "I'm not really sure, we haven't spent a lot of time talking about her sexual preferences."
            the_person "Oh, right, of course. I just meant has she ever dated anyone like me?"
            mc.name "Sorry, [the_person.name], you would be the first but that doesn't mean it can't happen."
            mc.name "I could try and bring the topic up, get a feel for which way should would lean."
            the_person "Really? That would be awesome, thanks [the_person.mc_title]!"
            mc.name "Come see me next week and I'll give you an update."
        "No":
            mc.name "I can't imagine that she would."
            $ scene_manager.update_actor(the_person, emotion = "sad")
            if not the_sister.has_taboo("sucking_cock") or not the_sister.has_taboo("vaginal_sex") or not the_sister.has_taboo("anal_sex"):
                mc.name "I am confident that she likes dick and is currently getting all she needs."
            else:
                mc.name "I've never known her to show an interest in other girls. You should probably look elsewhere."
            mc.name "If you want, I could try to help you find someone who is interested."
            if the_person.sluttiness > 160: # currently disabled
                the_person "You know that would be kind of nice."
                # crisis to find her a partner
                mc.name "Come see me next week and I'll give you an update."
            else:
                the_person "No, that isn't really what I'm looking for."
                the_person "I guess I'll just keep hanging out with your sister and see if anything develops."
                mc.name "Alright, I'm here if that doesn't work out."
            $ the_person.event_triggers_dict["friend_with_benefits"] = 4 # she has to do it alone
    the_person "Alright, have a good night."
    "[the_person.title] waves goodbye as she leaves to get back to [the_sister.name]."
    $ willing = False
    if get_person_by_identifier(sarah.event_triggers_dict.get("initial_threesome_target", None)) == the_sister:
        $ willing = True
        "[the_sister.title] has already readily agreed to have a threesome with [sarah.title]."
    if mc.business.event_triggers_dict.get("family_threesome", False) == True:
        $ willing = True
        "[the_sister.title] has already been joining in sex with [mom.title] and you. Sometimes they even start things when you aren't around."
    if "threesome" in erica_get_wakeup_options():
        $ willing = True
        "[the_sister.title] climbed into bed with you and [erica.title], and they have been spending nights together every week."
    if the_sister.sex_record.get("threesomes", 0) > 0:
        $ willing = True
    if willing:
        "[the_sister.title] is certainly willing to do things with another girl."
    else:
        "You aren't sure what [the_sister.title] thinks of sex with another girl."
    "You definitely need to talk to her about this. Of course you also need to decide what you want her to do."
    if the_sister.event_triggers_dict.get("vaginal_revisit_complete", False) == True:
        "She has become your fuck toy and getting her into a new relationship might change that."
    elif the_sister.event_triggers_dict.get("anal_revisit_complete", False) == True:
        "She has been letting you fuck her ass, and getting her into a new relationship might put a stop to that."
    elif the_sister.event_triggers_dict.get("oral_revisit_complete", False) == True:
        "Now that she is willing to suck you off you aren't sure you want her to find someone else."
    "Should you encourage her to start dating [the_person.title]? If you do is there any possibility that you end up joining them in the future?"
    $ mc.business.add_mandatory_crisis(lily_first_followup)
    $ clear_scene()
    return

label lily_first_followup():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ sleeping = False
    "As you are getting ready for bed you decide there is no time like the present and make your way to [the_sister.possessive_title]'s room."
    $ mc.location = lily_bedroom
    $ old_location = mc.location #Record these so we can have it dark, but restore it to normal later.
    $ old_lighting = old_location.lighting_conditions
    $ mc.location.show_background()
    $ scene_manager.add_actor(the_sister, position = "sitting")
    if cousin.location == lily_bedroom:
        $ mc.location.move_person(cousin, downtown)
        mc.name "Hey, [the_sister.title], where is [cousin.name]?"
        the_sister "Don't know, don't care. Just happy to have some alone time."
        mc.name "Oh, sorry, I can go."
        the_sister "No, wait..."
    else:
        mc.name "Hey, [the_sister.title] how are you doing?"
        the_sister "Pretty good, how about you?"
    the_sister "Is everything okay?"
    mc.name "Yeah, why wouldn't it be?"
    the_sister "I don't know, [the_person.name] was a bit weird today and when I tried to bring it up she brushed me off."
    mc.name "Don't worry about it, I'm sure she'll be fine next week."
    if the_sister.has_role(girlfriend_role):
        the_sister "Don't be like that, I love you and telling me not to worry will just make me worry more."
        "She does love you, telling her would probably be for the best."
    else:
        the_sister "Fine, bury your feelings."
        "As she says that you can see her interest growing, if you don't tell her it will just make her more curious."
    mc.name "Alright, we sort of broke up I guess."
    the_sister "Oh, I'm sorry, was it serious?"
    if the_sister.has_role(girlfriend_role):
        "While it is clear she is concerned you also see a hint of jealousy in her eyes."
        mc.name "Nothing you needed to worry about, we were just having some fun."
    else:
        "Her compassion eases some of the pain you had been feeling."
        mc.name "Not really, she is fun but I didn't think we were going to get married or anything."
    the_sister "Still break ups can be rough. Is there anything I can do for you?"
    mc.name "As a matter of fact I am feeling a bit lonely, do you think we could spend some time together?"
    the_sister "Of course."
    $ scene_manager.update_actor(the_sister, position = "stand4")
    "[the_sister.title] stands up and approaches you, wrapping her arms around you in a tight hug."
    if not the_sister.has_taboo("kissing"):
        $ scene_manager.update_actor(the_sister, position = "kissing")
        "The hug is nice, but you want more so you gently tilt her head up and lower yours to plant a gentle kiss on her lips."
        "As it lingers you feel her mouth start to part and you push forward more."
        "A slight moan runs through her as her body melts against yours."
        $ mc.change_arousal(10)
        $ the_sister.change_arousal(10)
    if not the_sister.has_taboo("touching_body"):
        "The warmth and closesness is amazing and you feel tension you were not aware of pouring out of your body."
        "Your cock begins to stir and as it hardens you press it into [the_sister.possessive_title]'s warm crotch."
        "She moans more audibly and starts to run her hands over your body, taking the hug from comforting to sexual."
        $ mc.change_arousal(10)
        $ the_sister.change_arousal(10)
    "The hug lingers, but eventually [the_sister.title] pulls away and you reluctantly let her go."
    if not the_sister.has_taboo("sucking_cock") and the_sister.has_taboo("vaginal_sex"):
        $ the_person.event_triggers_dict["lily_comfort"] = "oral"
        the_sister "Why don't you lay down on my bed? I'll get the door and then do something you take your mind off [the_person.name]."
        $ scene_manager.update_actor(the_sister, position = "walking_away")
        "You drop back onto her bed and sprawl out, leaving your legs hanging down to the floor while [the_sister.title] goes and turns off the lights."
        $ mc.location.lighting_conditions = dark_lighting
        $ mc.location.show_background()
        $ scene_manager.update_actor(the_sister, position = "blowjob")
        "By the time your eyes adjust to the darkness she is standing at the end of the bed and lowers herself down to her knees in front of you."
        "She rests her hands on your knees and slowly starts to run them up your thighs. Getting the idea you are quick to help her open them up so that she has easier access."
        the_sister "Well, someone is eager!"
        $ mc.change_arousal(10)
        if the_sister.get_opinion_score("giving blowjobs") > 0:
            the_sister "I have to admit I'm a bit excited to get a taste of you too."
            if the_sister.get_opinion_score("being submissive") > 0:
                the_sister "You know I'm always happy to serve you when want me too."
                $ the_sister.change_arousal(10)
        else:
            the_sister "Don't expect this everytime you get a little sad."
        $ scene_manager.update_actor(the_sister, position = "kneeling1")
        "By the time she has herself in postion you are already standing at attention for her. She kisses the head and then licks the shaft a few times."
        "It is pretty clear you don't need any more prep and she opens her mouth to take your tip into her mouth, gently sucking on it and licking up your precum."
        "Next she opens wider and slowly slides down your shaft, taking more and more into her soft mouth."
        call get_fucked(the_sister, the_goal = "oral creampie", sex_path = None, private= True, start_position = blowjob, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False, condition = None) from _call_get_fucked_comfort1
        mc.name "Thank you [the_sister.title], I think that was exactly what I needed."
        the_sister "Good, does that mean you are feeling better?"
        mc.name "Absolutely, I'm going to sleep like a rock tonight."
        the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
        mc.name "You want me to sleep with you?"
        the_sister "Not like that, just a little cuddling to further comfort you."
        mc.name "That sounds nice, thank you."
    else:
        the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
        mc.name "You want me to sleep with you?"
        if not the_sister.has_taboo("vaginal_sex"):
            $ the_person.event_triggers_dict["lily_comfort"] = "sex"
            the_sister "I was just going to comfort you a bit, but you never know where the night will go."
            the_sister "I'll get the lights, you make yourself comfortable."
            "Not wanting to waste this opportunity you quickly strip and climb under the covers."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
            $ the_sister.outfit.strip_to_underwear()
            "It is hard to see in the sudden darkness, but you hear clothing shifting as [the_sister.title] prepares to join you."
            $ mc.change_locked_clarity(10)
            "You leave room for her to fit next to you, but aren't terribly surprised when she instead climbs on top of you, dropping a leg to each side and lowering her body to yours."
            $ scene_manager.update_actor(the_sister, position = "cowgirl")
            if the_sister.tits_available():
                if the_sister.has_large_tits():
                    "Her sizable breasts press warmly against your bare chest as she settles down."
                else:
                    "Her firm nipples point into your chest as she settles down."
            else:
                "Her bra lessens the experience as she settles down."
            the_sister "So... do you want to talk about [the_person.name]?"
            mc.name "Sorry, who?"
            the_sister "Funny... but I'm serious. Do you need to talk?"
            if the_sister.has_role(girlfriend_role):
                the_sister "I know our relationship has its challeneges, but I don't just want to be a rebound for you when something else doesn't work out."
                mc.name "I know, and I love you as both my sister and my girlfriend."
            else:
                the_sister "I'll save you from making a terrible decision while you are on the rebound, but I also want to be here if you need to talk."
                mc.name "I know, and I'm so grateful to have someone who I can talk to about anything."
            mc.name "Honestly, it wasn't that serious. I miss her a bit but I'm sure I'll be fine in a few days."
            the_sister "Alright, in that case..."
            "She lowers her face to yours, resuming the kiss but with more passion. She also begins to grind her pelvis against yours."
            if the_sister.vagina_available():
                if not the_sister.pubes_style == shaved_pubes:
                    "Her fine hairs send tingles along your skin where it brushes you and you can feel the heat radiating from her pussy"
                else:
                    "Her bare skin is incredibly smooth and you can feel the heat radiating from her pussy."
            else:
                "Her silky panties rub against you but don't dampen the heat radiating from her pussy."
            "It isn't long before you stiffen enough for her to feel your cock pressing against her folds."
            "You slide your hands down to her ass, pulling her more tightly against you and grinding harder."
            if the_sister.vagina_available():
                "She slides her hands between your hips and lifts up a bit so she can spread her lips with one and grasp your rock hard pole with the other."
            else:
                "She slides her hands to her crotch, pulling her panties aside with one and grasping your rock hard pole with the other."
                $ the_sister.outfit.strip_to_vagina(half_off_instead = True)
            "She makes a few more passes, spreading her juices along the length of your cock, before lifting her hips and guiding you into her waiting hole."
            "She sinks down slowly enveloping you in her tight warm pussy and stopping once you are buried to the hilt."
            the_sister "God, you always make me feel so full [the_sister.mc_title]."
            mc.name "And you always feel so tight. I must be the luckiest man in the world."
            "She smiles down at you and then starts to move, at first just slowly sliding up and down about an inch."
            call get_fucked(the_sister, the_goal = "vaginal creampie", sex_path = None, private= True, start_position = cowgirl, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False, condition = None) from _call_get_fucked_comfort2
            mc.name "That was amazing [the_sister.title]. I'm not sure if comforted is the right word, but I definitely feel better."
            if the_sister.get_opinion_score("vaginal sex") > 0:
                the_sister "I have to admit I enjoyed myself too."
            if the_sister.get_opinion_score("being submissive") > 0:
                the_sister "You know how much I love satisfying your needs and giving you pleasure."
            "[the_sister.title] drapes herself over you, wrapping her arms around you as much as she can."
            "You are struck by how it can be so similar and at the same time wildly different than the hug you got when you first entered the room."
            "You smile to yourself at how lucky you are to have [the_sister.title] as you drift off to sleep."
            $ sleeping = True
        elif not the_sister.has_taboo("touching_penis"):
            $ the_person.event_triggers_dict["lily_comfort"] = "hand"
            the_sister "Not like that... but maybe we can find a way to help you relax."
            $ mc.change_arousal(10)
            the_sister "I'll get the lights, you make yourself comfortable."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
            "Not wanting to presume too much you strip, but only to your boxers, before you climb into her bed."
            "She quickly joins you, pressing her body up against yours as you squeeze into the bed together."
            $ mc.change_arousal(10)
            the_sister "Roll onto your side [the_sister.mc_title]. I'll be the big spoon and soothe you to sleep."
            "You comply, and feel her press against your bare back as she settles into place."
            "She wraps her top arm around you, pulling tighter, sort of like a hug."
            "It is comforting, but when her hand starts to wander down towards your waist other thoughts enter your mind."
            the_sister "Give me a bit of help here."
            "She starts to pull at the waist of your boxers and you lift your hips to let her pull them down."
            $ mc.change_arousal(10)
            "Her hand then travels back up and she gently strokes your stomach, brushing her hand against your rapidly harding cock as she does so."
            call get_fucked(the_sister, the_goal = "get mc off", sex_path = None, private= True, start_position = handjob, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False, condition = None) from _call_get_fucked_comfort3
            mc.name "That was amazing [the_sister.title], I'm not sure I've ever been so relaxed."
            the_sister "Good, does that mean you are feeling better?"
            mc.name "Absolutely, I'm going to sleep like a rock tonight."
            the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
            mc.name "You want me to sleep with you?"
            the_sister "Not like that, just a little cuddling to further comfort you."
            mc.name "That sounds nice, thank you."
        else:
            the_sister "Get your mind out of the gutter [the_sister.mc_title], I just thought you might be lonely."
            the_sister "It's not like we never shared a bed before, I'll just keep you company."
            the_sister "I'll get the lights, you make yourself comfortable."
            $ scene_manager.update_actor(the_sister, position = "walking_away")
            "You drop your pants, but decide it would be prudent to keep your boxers and shirt on before you climb into bed."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
    if not sleeping:
        "You press your back against the wall, leaving plenty of room for [the_sister.title] to fit as well."
        "She climbs in and lays on her back, then turns towards you and then away, trying to find a comfortable position."
        $ scene_manager.update_actor(the_sister, position = "stand2")
        the_sister "Maybe I was wrong, we are going to have to get a little closer if we ever want to get to sleep."
        mc.name "I can go if you want..."
        the_sister "No, just scoot away from the wall a bit and I'll cuddle up to you."
        mc.name "Alright."
        "You position yourself and feel her slide up against your body. It is a bit surprising how natural she seems to fit in your arms."
        the_sister "See, this is nice. Although, I was supposed to be comforting you and you seem to be the one holding me."
        mc.name "It's fine, having you here is comforting even if you are in my arms instead of me being in yours."
        the_sister "Alright, good night [the_sister.mc_title]."
        mc.name "Good night."
        if the_sister.love > 50:
            the_sister "..."
            "She seems to tense up, like she wants to say something more."
            the_sister "..."
            the_sister "I love you."
            "She mumbles, almost too quite to hear."
            menu:
                "Respond":
                    mc.name "I love you too."
                    "The tension bleeds out of her body as she relaxes back against you."
                    $ the_sister.change_stats(happiness = 5, love = 5)
                "Stay silent":
                    mc.name "..."
                    "You stay quite, the tension seems to grow a bit, but you deepen your breathing, like you somehow fell asleep already."
                    "It seems like she isn't going to make an issue of it, but she isn't happy."
                    $ the_sister.change_stats(happiness = -5, love = -5)
    $ old_location.lighting_conditions = old_lighting
    $ clear_scene()
    # call advance_time_move_to_next_day() from _call_advance_time_move_to_next_day_lily_first_followup
    # call lily_first_followup_morning(the_person) from _call_lily_first_followup_morning
    return "Advance Time"

label lily_first_followup_morning():
    $ mc.change_location(lily_bedroom)
    $ mc.location.show_background()
    $ the_mom = mom
    $ the_sister = lily
    $ wear_pajamas(the_mom)
    $ wear_pajamas(the_sister)
    $ mom_slutty = False
    $ sis_slutty = False
    $ the_cousin = None
    if aunt.event_triggers_dict.get("moving_apartment", 0) == -1: # disabled
        $ the_cousin = cousin
        $ the_aunt = aunt
        $ wear_pajamas(the_cousin)
        $ wear_pajamas(the_aunt)
        $ aunt_slutty = False
        $ cousin_slutty = False
        if the_cousin.effective_sluttiness() > 60:
            $ cousin_slutty = True
        if the_aunt.effective_sluttiness() > 60:
            $ aunt_slutty = True
        if the_mom.effective_sluttiness() > 60:
            $ mom_slutty = True
        if the_sister.effective_sluttiness() > 60:
            $ sis_slutty = True
        $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], the_mom)
    else:
        $ the_group = GroupDisplayManager([the_mom, the_sister], the_mom)
        if the_mom.effective_sluttiness() > 50:
            $ mom_slutty = True
        if the_sister.effective_sluttiness() > 50:
            $ sis_slutty = True
    $ lily_bedroom.show_background()
    "When you wake up in the morning you are briefly disoriented until you remember where you are."
    "[the_sister.title]'s room is recognizable. You just aren't used to seeing it from her bed, especially after spending the night with her."
    "You were right about sleeping like a rock, you never even noticed [the_sister.possessive_title] getting out of bed this morning."
    if mc.event_triggers_dict.get("lily_comfort", None) == "sex":
        "Still naked from your late night activities you look to the thankfully closed door."
        "You get out of bed and get yourself dressed."
    elif mc.event_triggers_dict.get("lily_comfort", None) == "hand":
        "Thankfully the door is closed so you get out of bed and pull on your pants."
    elif mc.event_triggers_dict.get("lily_comfort", None) == "oral":
        "Fortunately you pulled your clothes back on last night, but you are still glad the door is closed."
        "You climb to your feet and strech out some kinks from the unfamiliar bed."
    "It seems like [the_sister.title] has already started her day, and you figure you should probably follow suit."
    if the_cousin:
        "Suddenly you remember that [the_cousin.title] has been sleeping in here. She was out last night but must have come home at some point. Did she see you and [the_sister.title] sleeping together?"
        "This could be bad... you better get out there and see if you need to do damage control."
        "You head to your bedroom first and are somewhat relieved to see that the bed was slept in. Hopefully [the_cousin.possessive_title] just took advantage of the free bed and doesn't care about the reason."
    "You head for the kitchen to see who is around."
    $ mc.change_location(kitchen)
    $ mc.location.show_background()
    $ the_group.draw_group(position = "sitting", emotion = "happy")
    $ the_group.draw_person(the_mom, position = "walking_away")
    if mom_slutty:
        if the_mom.outfit.wearing_panties():
            "[the_mom.possessive_title] is just in her underwear in front of the stove, humming as she scrambles a pan full of eggs."
            $ mc.change_locked_clarity(5)
        else:
            "[the_mom.possessive_title] is in front of the stove naked, humming as she scrambles a pan full of eggs."
            $ mc.change_locked_clarity(10)
    else:
        "[the_mom.possessive_title] is at the stove and humming to herself as she scrambles a pan full of eggs."
    $ the_mom.update_outfit_taboos()
    $ the_group.draw_person(the_mom, position = "back_peek")
    the_mom "Good morning [the_mom.mc_title]. I'm almost ready to serve, have a seat."
    if sis_slutty:
        if the_sister.outfit.wearing_panties():
            "[the_sister.possessive_title] is sitting at the kitchen table wearing her underwear. She gives a dramatic yawn before nodding to you."
            $ mc.change_locked_clarity(5)
        else:
            "[the_sister.possessive_title] is sitting at the kitchen table naked. She gives a dramatic yawn before nodding to you."
            $ mc.change_locked_clarity(10)
    else:
        "[the_sister.possessive_title] is sitting at the kitchen table and gives a dramatic yawn before nodding to you."
    $ the_sister.update_outfit_taboos()
    the_sister "Good morning [the_sister.mc_title]."
    if the_cousin:
        if aunt_slutty:
            if the_aunt.outfit.wearing_panties():
                "[the_aunt.possessive_title] is also sitting at the kitchen table. You are a bit surprised she is just wearing her underwear."
                $ mc.change_locked_clarity(5)
            else:
                "[the_aunt.possessive_title] is also sitting at the kitchen table. Shockingly she is naked."
                $ mc.change_locked_clarity(10)
        else:
            "[the_aunt.possessive_title] is also sitting at the kitchen table."
        "There is no sign of [the_cousin.possessive_title], but you settle down at the table with the rest of your family."
    else:
        if mom_slutty and sis_slutty:
            $ the_group.draw_person(the_mom, position = "walking_away")
            "Your mother takes the pan off the stove and begins to slide the contents off onto three plates."
            $ the_group.draw_person(the_mom, )
            "She turns around and hands one plate to you and one plate to [the_sister.title]."
            $ the_group.draw_person(the_sister, position = "sitting")
            if mom.lactation_sources > 0 and mom.tits_available():
                mom "Want a little milk for your coffee, honey?"
                "[mom.title] gives you a quick wink."
                mc.name "Sure mom."
                "[mom.possessive_title] bends slightly over your coffee. She takes one of her breasts in her hand and starts to squeeze."
                "It takes a second, but soon a stream of her milk is pouring out into you coffee."
                mom "Just say when!"
                "You let her continue for a few more moments, until you can see the cream start to circulate around your hot coffee."
                $ mom.change_stats(slut = 1, max_slut = 40, happiness = 5)
                mc.name "That's good!"
                lily "Thanks Mom, you're the best!"
            elif lily.lactation_sources > 0 and lily.tits_available():
                mom "Want some coffe, honey?"
                mc.name "Sure mom."
                mom "Here you go, maybe [lily.name] could help you out with some milk."
                "[mom.title] gives you a quick wink."
                lily "Really, Mom?"
                mc.name "I mean... if you don't mind it would be nice."
                "[lily.possessive_title] gives an exasperated sigh, but then bends slightly over your coffee. She takes one of her breasts in her hand and starts to squeeze."
                "It takes a second, but soon a stream of her milk is pouring out into you coffee."
                lily "Let me know when you have enough."
                "You let her continue for a few more moments, until you can see the cream start to circulate around your hot coffee."
                $ lily.change_stats(slut = 1, max_slut = 40, happiness = 5)
                mc.name "That's good!"
            else:
                lily "Thanks Mom, you're the best!"
            $ the_group.draw_person(the_mom, position="sitting")
            the_mom "No problem, I'm just happy to spend my morning relaxing with my two favorite people!"
            "You enjoy a relaxing breakfast bonding with your mother and sister. [the_mom.possessive_title] seems particularly happy she gets to spend time with you."
            "Neither [the_sister.title] or [the_mom.possessive_title] seem to think it's strange to relax in their underwear."
            $ mc.change_locked_clarity(10)
            $ the_sister.change_love(3)
            $ the_sister.change_slut(2, 60)
            $ the_mom.change_love(3)
            $ the_mom.change_slut(2, 60)
            $ the_mom.change_happiness(10)
        elif mom_slutty and not sis_slutty:
            #Lily thinks her mom is embarrassing and weird but Mom pulls rank.
            the_sister "Oh my god Mom, what are you wearing?"
            $ the_group.draw_person(the_mom, position = "back_peek")
            the_mom "What? It's the weekend and it's just the three of us. I didn't think anyone would mind if I was a little more casual."
            $ the_group.draw_person(the_sister, position = "sitting")
            if the_mom.outfit.vagina_visible():
                the_sister "Mom, I don't think you know what casual means. Could you at least put on some panties or something?"
            elif the_mom.outfit.tits_visible():
                the_sister "Mom, I don't think you know what casual means. I mean, couldn't you at least put a bra?"
            else:
                the_sister "Mom, you're prancing around the kitchen in your underwear. In front of your son and daughter. That's weird."
                "[the_sister.title] looks at you."
                the_sister "Right [the_sister.mc_title], that's weird?"
            if the_mom.obedience > 115:
                $ the_group.draw_person(the_mom, position = "back_peek")
                the_mom "What do you think [the_mom.mc_title], do you think it's \"weird\" for your mother to want to be comfortable in her own house?"
                $ mc.change_locked_clarity(5)
                menu:
                    "Side with Mom":
                        mc.name "I think Mom's right [the_sister.title]. It's nothing we haven't seen before, she's just trying to relax on her days off."
                        $ the_mom.change_obedience(-5)
                        $ the_sister.change_obedience(5)
                        "[the_sister.title] looks at the two of you like you're crazy then sighs dramatically."
                        the_sister "Fine, but this is really weird, okay?"
                        $ the_group.draw_person(the_mom, position = "sitting")
                        "[the_mom.possessive_title] dishes out three portions and sits down at the table with you. [the_sister.title] eventually gets used to her mother's outfit and joins in on your conversation."
                        $ the_sister.change_slut(2, 30)
                        $ the_mom.change_happiness(10)
                    "Side with [the_sister.title]":
                        mc.name "I actually think [the_sister.title] is right, this is a little weird. Could you go put something on, for our sakes?"
                        $ the_sister.change_obedience(-2)
                        $ the_sister.change_slut(1, 30)
                        $ the_mom.change_obedience(5)
                        the_mom "Oh you two, you're so silly. Fine, I'll be back in a moment. [the_sister.title], could you watch the eggs?"
                        $ the_group.draw_person(the_sister, position = "walking_away")
                        "Your mother leaves to get dressed. [the_sister.possessive_title] ends up serving out breakfast for all three of you."
                        $ the_mom.apply_outfit(the_mom.planned_outfit)
                        the_sister "She's been so weird lately. I don't know what's going on with her..."
                        $ the_group.draw_person(the_mom, position = "sitting")
                        $ the_sister.change_happiness(5)
                        $ the_mom.change_happiness(5)
                        "When [the_mom.possessive_title] gets back she sits down at the table and the three of you enjoy your breakfast together."
            else:
                #She likes what she likes
                $ the_group.draw_person(the_mom, position = "back_peek")
                the_mom "Well luckily I'm your mother and it doesn't matter what you think. I'm going to wear what makes me comfortable."
                "She takes the pan off the stove and slides the scrambled eggs out equally onto three plates."
                the_mom "Now, would you like some breakfast or not?"
                "[the_sister.title] sighs dramatically."
                the_sister "Fine, but this is really weird, okay?"
                $ the_sister.change_slut(1, 30)
                $ the_mom.change_happiness(10)
                $ the_group.draw_person(the_mom, position = "sitting")
                "[the_mom.possessive_title] gives everyone a plate and sits down. [the_sister.title] eventually gets used to her mother's outfit and joins in on your conversation."
                "When you're done you help Mom put the dirty dishes away and get on with your day."
        elif sis_slutty and not mom_slutty:
            #Mom thinks lilly is way too underdressed and sends her back to get dressed.
            $ the_group.draw_person(the_sister, position = "sitting")
            "Your mother turns around and gasps."
            $ the_group.draw_person(the_mom, emotion = "angry")
            the_mom "[the_sister.title]! What are you wearing?"
            $ the_group.draw_person(the_sister, position = "sitting")
            the_sister "What do you mean? I just got up, I haven't had time to pick out an outfit yet."
            $ the_group.draw_person(the_mom, emotion = "angry")
            the_mom "You shouldn't be running around the house naked. Go put some clothes on young lady."
            $ the_group.draw_person(the_sister, position = "sitting", emotion = "angry")
            "[the_sister.possessive_title] scoffs and rolls her eyes."
            the_sister "Come on Mom, you're being ridiculous. This is my house too, I should be able to wear whatever I want!"
            "Your mother and sister lock eyes, engaged in a subtle battle of wills."
            if the_sister.obedience > the_mom.obedience:
                $ the_group.draw_person(the_mom, position = "walking_away")
                "Mom sighs loudly and turns back to the stove."
                the_mom "Fine! You're so stubborn [the_sister.title], I don't know how I survive around here!"
                $ the_sister.change_obedience(-2)
                $ the_sister.change_happiness(10)
                $ the_sister.change_slut(2, 50)
                $ the_mom.change_obedience(10)
                $ the_group.draw_person(the_sister, position = "sitting", emotion = "happy")
                "[the_sister.possessive_title] looks at you, obviously pleased with herself, and winks."
            else:
                "[the_sister.title] finally sighs loudly and looks away. She pushes her chair back and stands up in defeat."
                $ the_group.draw_person(the_sister, emotion = "angry")
                the_sister "Fine! I'll go put on some stupid clothes so my stupid mother doesn't keep worrying."
                $ the_group.draw_person(the_sister, position = "walking_away")
                "[the_sister.title] sulks out of the kitchen."
                $ the_group.draw_person(the_mom, )
                the_mom "I don't know how I manage to survive with you two around!"
                $ the_sister.apply_outfit(the_sister.planned_outfit)
                #$ the_sister.outfit = the_sister.planned_outfit.get_copy() changed v0.24.1
                $ the_sister.change_obedience(10)
                $ the_sister.change_happiness(-5)
                $ the_mom.change_obedience(-2)
                $ the_group.draw_person(the_sister, position = "sitting")
                "[the_sister.possessive_title] is back by the time Mom starts to plate breakfast. She sits down and starts to eat without saying a word."
            "When you're done you help Mom put the dirty dishes away and get on with your day."
        else:
            #Neither of them are particularly slutty, so it's just a normal breakfast.
            $ the_group.draw_person(the_sister, position = "sitting")
            the_sister "So what's the occasion Mom?"
            $ the_group.draw_person(the_mom, )
            "[the_mom.possessive_title] takes the pan off the stove and scoops the scrambled eggs out equally onto three waiting plates."
            the_mom "Nothing special, I just thought we could have a nice quiet weekend breakfast together."
            "She slides one plate in front of you and one plate in front of [the_sister.title], then turns around to get her own before sitting down to join you."
            $ the_group.draw_person(the_mom, position = "sitting")
            the_mom "Go ahead, eat up!"
            $ the_sister.change_love(3)
            $ the_mom.change_love(3)
            $ the_mom.change_happiness(5)
            "You enjoy a relaxing breakfast bonding with your mother and sister. Your mom seems particularly happy she gets to spend time with you."
            "When you're done you help Mom put the dirty dishes away and get on with your day."
    return

label lily_second_best_friend(the_sister, the_person):
    the_person "So... did you talk to [the_sister.name] about... things."
    "Oh shit, you completely forgot to actually talk to her last week."
    if the_person.event_triggers_dict.get("lily_comfort", None) == "sex":
        "To be fair, she did kind of jump you."
    elif the_person.event_triggers_dict.get("lily_comfort", None) == "oral":
        "To be fair, her mouth was a bit busy."
    elif the_person.event_triggers_dict.get("lily_comfort", None) == "hand":
        "To be fair, she did distract you a bit."
    else:
        "To be fair, she was more concerned with how you were doing."
    menu:
        "Tell the truth (mostly)":
            mc.name "Sorry, [the_person.title], I went to talk to her but it was a difficult topic to bring up."
            mc.name "We talked about you, she knows something was going on with us and that it ended."
            mc.name "From there the conversation kinda got away from me. I didn't see a good way to steer it back to you and her."
            if mc.event_triggers_dict.get("lily_comfort", None) == "sex":
                "Especially after she fucked you to exhaustion."
            elif the_person.event_triggers_dict.get("lily_comfort", None) == "oral":
                "Especially after you sucked you off."
            elif mc.event_triggers_dict.get("lily_comfort", None) == "hand":
                "Especially after she jerked you off."
            the_person "Okay, do you think you could talk to her again?"
            mc.name "Yeah, I will for sure."
        "Lie":
            mc.name "Yes, absolutely. We talked about you last week."
            "Your mind races as you scramble for an answer that will satisfy her and be relatively factual."
            menu:
                "She is curious":
                    mc.name "She is certainly curious. When I brought up the idea of her dating a girl she seemed intrigued."
                    mc.name "If I had to guess she has thought about it before, but probably liked boys enough to go with the flow."
                    mc.name "I think I could get her to ask you out if you give me a bit of time."
                    $ the_person.event_triggers_dict["lily_lie"] = 2
                "Give her time":
                    mc.name "She seemed a little surprised when I asked, sort of like she had never really thought about it before."
                    mc.name "When we finished talking it seemed like she was deep in thought."
                    mc.name "I think you need to give her some time, let her come around to the idea of seeing you as more than a friend."
                    mc.name "I'll be sure to bring it up again, see if I can help nudge her in the right direction."
                    $ the_person.event_triggers_dict["lily_lie"] = 1
                "Not going to happen":
                    mc.name "She likes you, she really does, but nothing is going to happen."
                    mc.name "I don't think she is ever going to return your feelings."
                    mc.name "I'll talk to her again, but I think you might need to look elsewhere."
                    $ the_person.event_triggers_dict["lily_lie"] = -1
            the_person "Well, that is good to know. At least I have some idea of what to expect."
            the_person "I guess no matter what I'm still gonna be hanging around. Maybe I'll be able to sway her a bit more while we are studying."
            mc.name "Sure, you never know what will happen."
            "You better make sure that your story checks out before [the_person.title] catches you in a lie."
            "Maybe your serums could help out. Can you convince [the_sister.title] that she wants to do what you already promised [the_person.title]?"
    the_person "Thanks again. I know this is kind of awkward and I really appreciate the help."
    if the_person.height < 0.9:
        "She steps forward goes up on her toes and kisses you on the cheek."
    else:
        "She steps forward and gives you a kiss on the cheek."
    $ mc.business.add_mandatory_crisis(lily_second_followup)
    $ clear_scene()
    return

label study_buddy_test(the_person):
    $ the_person.change_location(lily_bedroom)
    $ stop = False
    while not stop:
        $ mc.change_energy(100)
        $ the_person.change_energy(100)
        call study_buddy_date_label from _call_study_buddy_date_label_test
        menu:
            "Continue":
                pass
            "Stop":
                $ stop = True
    return
