init -1 python:
    def study_buddy_nora_requirement(person):
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

    def lily_followup_requirement():
        if lily.is_available:
            return True
        return False

    def rival_int_chat_requirement(person):
        if time_of_day > 0 and time_of_day < 4:
            return True
        return False

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
            if not town_relationships.get_relationship(person, lily):
                town_relationships.begin_relationship(person, lily)
            return person
        return

    def lily_willing_threesome():
        if get_person_by_identifier(sarah.event_triggers_dict.get("initial_threesome_target", None)) == the_sister:
            return True
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            return True
        if "threesome" in erica_get_wakeup_options():
            return True
        if lily.sex_record.get("threesomes", 0) > 0:
            return True
        return False

    study_buddy_serum_action = Action("Study buddy serum", study_buddy_serum_requirement, "study_buddy_serum_label")
    study_buddy_date_action = Action("Study buddy date", evening_date_trigger, "study_buddy_date_label", requirement_args=0) #it happens on a monday
    study_buddy_prep_action = Action("Study buddy prep", study_buddy_prep_requirement, "study_buddy_prep_label")

    def study_buddy_mod_initialization():
        global study_buddy_nora_action
        study_buddy_nora_action = Action("Talk to [nora.fname] about [lily.fname]'s lab partner", study_buddy_nora_requirement, "study_buddy_nora_label", menu_tooltip = "Talk to Nora about Lily's lab partner.")
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
    mc.name "I was hoping to talk to you about [the_sister.fname]'s current lab partner."
    the_person "Oh, you mean [the_other_person.fname]? Is something wrong?"
    if not town_relationships.get_relationship(the_other_person, the_sister):
        $ town_relationships.begin_relationship(the_other_person, the_sister)
    if town_relationships.get_relationship(the_other_person, the_sister).type_a =="Rival" or town_relationships.get_relationship(the_other_person, the_sister).type_a =="Nemesis":
        mc.name "Yeah, actually. They really don't get along, and I am worried that it is making it hard for them to agree on the way they should do things."
    elif town_relationships.get_relationship(the_other_person, the_sister).type_a =="Friend" or town_relationships.get_relationship(the_other_person, the_sister).type_a =="Best Friend":
        mc.name "Kind of, they are friends. Usually that would be great, but they've been spending more time chatting than working and I'm worried about it impacting [the_sister.fname]'s grades."
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
                the_person "Sorry, [the_person.mc_title], but I don't think I can justify something like this without a reason."
                mc.name "I understand, I'll get back to you if something changes."
            "Give her\n{color=#ff0000}{size=18}Requires: $5000{/size}{/color} (disabled)" if mc.business.funds < 5000:
                pass
    if change:
        "[the_person.title] pulls out her planner, flipping through to find [the_sister.fname]'s class."
        the_person "Who would you like your sister to be partnered with from now on?"
        call screen enhanced_main_choice_display(build_menu_items([["Pick Lab Partner"] + lily_classmates()], draw_hearts_for_people = True))
        $ choice = _return
        mc.name "I think it would be best if she was partnered with [choice.fname]."
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
    $ lily.set_override_schedule(lily_bedroom, the_days = [0], the_times = [3])
    $ test_outfit_lily = university_wardrobe.decide_on_outfit2(lily)
    $ lily.planned_outfit = test_outfit_lily
    $ lily.apply_planned_outfit()
    $ test_outfit = university_wardrobe.decide_on_outfit2(the_person)
    $ the_panties = test_outfit.get_panties()
    $ the_bra = test_outfit.get_bra()
    if the_person.event_triggers_dict.get("bedroom_tax", 0) > 1:
        if the_panties:
            if the_panties.is_extension: #two piece item
                $ test_outfit.remove_clothing(the_bra)
                $ the_bra = None
            else:
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
    if not town_relationships.get_relationship(the_person, lily):
        $ town_relationships.begin_relationship(the_person, lily)
    if town_relationships.get_relationship(the_person, lily).type_a == "Rival":
        if the_person.event_triggers_dict.get("teasing_lily", 999) > the_person.obedience:
            $ rival_study_time = Action("Rival Study Time", lily_followup_requirement, "rival_study_time_label")
            $ mc.business.add_mandatory_crisis(rival_study_time)
        else:
            $ the_person.event_triggers_dict["teasing_lily"] += 30
    return

label study_buddy_serum_label(the_person):
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_person.apply_planned_outfit()
    $ the_sister = lily
    $ the_sister.apply_planned_outfit()
    if the_person.event_triggers_dict.get("study_sessions", 0) < 1:
        "Typically you could expect a visit from [the_sister.fname]'s lab partner, but thanks to you she has a new one this week."
        if mc.inventory.get_any_serum_count() > 0:
            "Expecting them to be hard at work you decide to just head to the kitchen and grab some drinks to bring up."
    else:
        "You can expect a visit from [the_person.title] sometime this evening."
        if mc.inventory.get_any_serum_count() > 0:
            "Before that happens you want to take the opportunity to give her and [the_sister.possessive_title] a serum, so you head down to the kitchen and grab some drinks."
    if mc.inventory.get_any_serum_count() > 0:
        $ mc.change_location(kitchen)
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
        if the_person.event_triggers_dict.get("study_sessions", 0) < 1:
            mc.name "Oh, hello [the_person.fname]! I'm surprised to see you here today."
        else:
            mc.name "Hey girls, I brought you some water. Hard at work on your project?"
    else:
        if the_person.event_triggers_dict.get("study_sessions", 0) < 1:
            "You decide to stop in and say hello breifly."
            "When you get to the door you knock on the door frame and see [the_sister.title] and [the_person.title] turn to greet you."
        else:
            "Before that you figure you can stop and say hello breifly."
            "When you get to the door you knock on the door frame and see [the_sister.title] and [the_person.title] turn to greet you."
    if the_person.event_triggers_dict.get("study_sessions", 0) < 1:
        $ mc.change_location(lily_bedroom)
        $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
        $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
        if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
            the_person "Hi, [the_person.mc_title], nice to see you again!"
        elif town_relationships.get_relationship(the_person, the_sister).type_a =="Rival":
            the_person "Quite the pleasant surprise isn't it?"
            mc.name "I must admit that it is."
        else:
            the_person "Hello again."
        mc.name "Isn't today usually the day when you work with your lab partner, [the_sister.fname]?"
        if mc.charisma > 4:
            "With acting skills worthy of Hollywood you deftly deliver your line."
        elif mc.charisma > 2:
            "Although you are neither surprised or confused you do a passable job of making it sound that way."
        else:
            "You can't help but feel like your question is a bit wooden, fortunately they don't seem to notice."
        the_sister "Professor [nora.last_name] came into class this week with a new TA and rearranged a bunch of lab partners."
        the_sister "She said something about how adapting to changing workplaces would be an important skill to learn."
        mc.name "Well that makes sense, sometimes I have to move people around at work as priorities shift between research and production."
        the_sister "Yeah, I suppose, it's just tough starting over when the two different groups were approaching the project in different ways."
        the_person "It is somewhat beneficial though because we now have access to four people's work up to this point, even if their is some overlap in what got done."
        if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
            the_person "Plus it is great to be able to work with [the_sister.fname] so we can spend more time hanging out."
            the_sister "Yeah, that is a bonus, if we had gotten to pick partners to start with I would have wanted to work with you."
            mc.name "I'm glad this is working out for you."
        elif town_relationships.get_relationship(the_person, the_sister).type_a =="Rival":
            the_person "Of course my previous lab partner was more knowledgeable than [the_sister.fname], but over coming challenges is an imporant skill to learn too."
            the_sister "As if I'm going to be the one holding us back. If you spent more time studying I wouldn't need to spend so much explaining things to you as we work."
            mc.name "Hey now, it sounds like you might be stuck together, so you should at least try to be civil to each other."
        $ the_person.event_triggers_dict["study_sessions"] = 1
    else:
        $ mc.change_location(lily_bedroom)
        $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
        $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
        $ the_person.event_triggers_dict["study_sessions"] += 1
    "You chat with them a bit more about what their project is, and give some advice based off of your time spent with [nora.fname]."
    mc.name "I should probably let you get back to work. I'll be in my room for the night, early start tomorrow at work."
    $ scene_manager.clear_scene()
    return "Advance Time"

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
        elif mc.location == lily_bedroom:
            pass
        else:
            "Interacting with [the_person.title] is always a good way to spend an evening, of course if you have other plans you could always go out until later tonight."
            menu:
                "Stay home {image=gui/heart/Time_Advance.png}":
                    "You decide wait for [the_person.title] and head to your bedroom so she can find you."
                    pass
                "Go out":
                    "You make the short trip downtown and start looking around for something to pass the time."
                    $ mc.change_location(downtown)
                    return
        $ mc.change_location(bedroom)
    if the_person.event_triggers_dict.get("friend_with_benefits", 0) >= 3:
        call lily_study_buddy_best_friend(the_sister, the_person) from _call_lily_study_buddy_best_friend_date
    elif town_relationships.get_relationship(the_person, the_sister).type_a == "Nemesis":
        call lily_study_buddy_nemesis(the_sister, the_person) from _call_lily_study_buddy_nemesis_date
    else:
        call lily_study_buddy_visit(the_person) from _call_lily_study_buddy_visit
    "A bit of time passes, but you eventually hear the front door closing as [the_person.title] goes home for the night."
    $ mc.business.add_mandatory_crisis(study_buddy_prep_action)
    $ clear_scene()
    return "Advance Time"

label lily_first_study_buddy(the_sister, the_person):
    if mc.is_home():
        "You are puttering around the house after a long day when you hear a surprising amount of noise coming from [the_sister.title]'s bedroom."
    elif mc.is_at_work():
        "It has been a long day and you are suddenly struck by the urge to go home for the night to relax."
        $ mc.change_location(bedroom)
        "A quick trip later you are home and in your room."
        "As you are unpacking your things from the day you hear a surprising amount of noise coming from [the_sister.title]'s bedroom."
    else:
        "It has been a long day and you are suddenly struck by the urge to go home for the night to relax."
        $ mc.change_location(hall)
        "When you get home and open the door you hear a surprising amount of noise coming from [the_sister.title]'s bedroom."
    $ scene_manager = Scene()
    "Curious, you head down the hall to see what is going on."
    $ mc.change_location(lily_bedroom)
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "standing_doggy", emotion = "happy")
    $ scene_manager.add_actor(the_sister, position = "standing_doggy", emotion = "happy")
    "It looks like [the_sister.title] has company, and judging from the fact that they are both still in uniform, it must be one of her classmates."
    "They are both bent over [the_sister.title]'s desk, so you take a moment to enjoy the view before knocking on the door frame."
    mc.name "Hey girls, what are you up to?"
    $ scene_manager.update_actor(the_sister, position = "stand2")
    the_sister "Hey, [the_sister.mc_title], we've got a bit of a project for school and were working here instead of on campus."
    the_sister "Do you remember [the_person.fname]? You met briefly on campus the other day."
    if not town_relationships.get_relationship(the_person, the_sister):
        $ town_relationships.begin_relationship(the_person, the_sister)
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped, position = "stand2")
    if town_relationships.get_relationship(the_person, the_sister).type_a =="Friend":
        the_person "Hi, [the_person.mc_title], nice to see you again!"
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
    if mom.location == kitchen:
        $ scene_manager.add_actor(mom, emotion = "happy")
        "When you get to the kitchen you see [mom.possessive_title] hard at work preparing dinner."
        mc.name "Just grabbing a drink for myself and the girls."
        $ scene_manager.clear_scene()
        $ mc.change_location(hall)
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
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand3", emotion = "happy")
    $ scene_manager.add_actor(the_sister, position = "stand3", emotion = "happy")
    "You hand them each their drinks and they thank you as they start to drink."
    "You chat with them a bit more about what their project is, and give some advice based off of your time spent with [nora.fname]."
    mc.name "I should probably let you get back to work. I'll be in my room for the night, early start tomorrow at work."
    $ mc.business.event_triggers_dict["knows_study_day"] = True
    "As you make your way back to your room you realize that since you know their teacher, [nora.fname], it might be possible to change who [lily.fname] is studying with."
    "It might take some effort, but if you don't want to see [the_person.title] next week you should pay the campus a visit."
    $ the_person.event_triggers_dict["study_sessions"] = 1
    return

label lily_study_buddy_visit(the_person):
    $ the_sister = lily
    $ mc.change_location(bedroom)
    $ the_person.draw_person()
    "A bit later in the evening, you hear a knock at your open door and look up to see [the_person.title] leaning against the door frame."
    mc.name "Oh, hey [the_person.fname]. Do you need something?"
    if town_relationships.get_relationship(the_person, the_sister).type_a == "Rival": # increase obedience to progress
        the_person "Yeah, I think I've endured as much of your sister as I can for now."
        mc.name "Sorry to hear that, I know how she can be sometimes."
        the_person "Exactly, I was so glad for an excuse to come talk to you instead."
        call lily_study_buddy_rival(the_person) from _call_lily_study_buddy_rival
        if town_relationships.get_relationship(the_person, the_sister).type_a == "Nemesis":
            $ nemesis_transition = Action("Nemesis Transition", lily_followup_requirement, "nemesis_transition_label")
            $ mc.business.remove_mandatory_crisis(rival_study_time)
            $ mc.business.add_mandatory_crisis(nemesis_transition)
    elif town_relationships.get_relationship(the_person, the_sister).type_a == "Friend": # increase love to progress
        the_person "Yeah, we ran out of note cards and [the_sister.fname] thought you might have some extra."
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
            the_person "You know, this isn't really fair to [the_sister.fname]. Do you maybe want to spend time together when I'm not supposed to be working with her?"
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
                mc.name "Sorry, I'm a little surprised, based on some of the things [the_sister.fname] has said I was expecting something different."
                the_person "What? What do you mean? What has she said about me?"
                mc.name "I don't remember exactly, but I just got the impression that you weren't a great lab partner."
                the_person "Is that right? Well I guess I'll go see what makes me so terrible."
                mc.name "No, I shouldn't have said that. Please, just forgot it, maybe she was talking about someone else."
                the_person "Really?"
                mc.name "I don't know, is there anyone else named [the_person.fname] in your classes?"
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

label lily_study_buddy_jealous():
    the_sister "[the_person.fname] sure spent a lot of time with you tonight."
    # based on love, what about me? taboos/taboo quests, make her push herself further for your attention
    return

label study_buddy_test(the_person):
    $ the_person.change_location(lily_bedroom)
    $ stop = False
    while not stop:
        $ mc.change_energy(100)
        $ the_person.change_energy(100)
        call study_buddy_prep_label() from _study_buddy_prep_label_test
        call study_buddy_date_label() from _call_study_buddy_date_label_test
        menu:
            "Continue":
                pass
            "Stop":
                $ stop = True
    return
