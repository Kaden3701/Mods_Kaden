init -1 python:
    def home_missing_panties_requirement():      #Use this section to set up when this crisis or action can be fired.
        if home_missing_panties_get_people():
            return True
        return False

    def home_missing_panties_get_people():
        temp_list = []
        if mc.is_home():
            for person in [x for x in people_in_mc_home()]:
                if person.event_triggers_dict.get("stolen_panties",0) > 0:
                    count = person.event_triggers_dict.get("stolen_panties",0)
                    if get_person_panties_list(person):
                        while count:
                            temp_list.append(person)
                            count -= 1
        if temp_list:
            return get_random_from_list(temp_list)
        else:
            return get_random_from_list(people_in_mc_home())
        return None

    def panties_to_person(person):
        if person.event_triggers_dict.get("stolen_panties",0) > 0:
            person.event_triggers_dict["stolen_panties"] -= 1
        return

    def get_person_panties_list(person): #Returns a list of tuples. First item is the common display name "PERSON's ITEM", the second is the item reference itself #TODO: Add unit tests
        return_list = []
        if not person.identifier in mc.stolen_underwear:
            mc.stolen_underwear[person.identifier] = []
        if person.identifier in mc.stolen_underwear:
            for item in mc.stolen_underwear[person.identifier]:
                if item in panties_list:
                    return_list.append([person.title + "'s " + clothing_formatted_title(item), item]) #TODO: Write the display code for this so it can show the little set of panties or bra with the correct colour/pattern. #TODO: might need an "empty" body type.
        if return_list:
            return_list.append(["Nothing", "Nothing"])
            return return_list
        return None

init 3 python:
    home_missing_panties_action = ActionMod("Missing Panties", home_missing_panties_requirement, "home_missing_panties_label",  #Using ActionMod automatically adds this event to the crisis list
        menu_tooltip = "A family member is looking for their panties.", category = "Home", is_crisis = True, is_morning_crisis = True, priority = 10)   #Categories include Home, Business, Fetish

label home_missing_panties_label():
    $ scene_manager = Scene()  #Clean Scene
    $ the_person = home_missing_panties_get_people()
    if not the_person:
        return
    if the_person.sluttiness >= 80:
        $ the_person.apply_outfit(Outfit("Nude"))
    elif the_person.sluttiness >= 70:
        $ apply_towel_outfit(the_person)
    elif the_person.sluttiness >= 50:
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness, guarantee_output = True))
    else:
        if the_person.has_job(sister_student_job):
            $ the_person.apply_university_outfit()
        elif the_person == mom and the_person.event_triggers_dict.get("mom_work_promotion_outfit", None):
            $ outfit = the_person.event_triggers_dict.get("mom_work_promotion_outfit", None)
            $ the_person.apply_outfit(outfit)
        elif the_person.is_employee():
            $ the_person.wear_uniform()
        else:
            $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_outfit(the_person.sluttiness, guarantee_output = True))
    if the_person.sluttiness >= 50 and the_person.sluttiness < 70:
        while not the_person.vagina_visible():
            $ the_person.outfit.remove_random_lower(top_layer_first = True)
    if the_person.wearing_panties():
        $ the_person.outfit.remove_clothing(the_person.get_panties())
    $ test_outfit = the_person.outfit.get_copy()
    $ the_person.apply_outfit(test_outfit)
    "As you are getting ready for the day you hear a knock on your door."
    if the_person.get_opinion_score("not wearing underwear")<= 0:
        $ scene_manager.add_actor(the_person, position = "stand3", emotion = "sad")
        "[the_person.title] hesitantly comes in with a frown on her face."
    else:
        $ scene_manager.add_actor(the_person, position = "stand3", emotion = "happy")
        "[the_person.title] comes in smiling, clearly having a good day already."
    mc.name "Hey, [the_person.title], how are you doing today?"
    the_person "I can't seem to find some of my laundry and I wondered if it maybe ended up getting mixed into yours."
    mc.name "I'm not sure, what were you looking for?"
    the_person "I couldn't seem to find the panties I wanted to wear with my outfit today."
    $ mc.change_locked_clarity(10)
    if the_person.get_opinion_score("not wearing underwear")<= 0:
        the_person "I really don't feel comfortable leaving the house without them."
    else:
        the_person "Although leaving the house without them wouldn't be so bad."
        $ mc.change_locked_clarity(10)
    mc.name "Let me check."
    $ item = "Nothing"
    if get_person_panties_list(the_person):
        $ item = menu(get_person_panties_list(the_person))
    else:
        "You can't imagine that you have what she is looking for, but you decide to humor her."
    if item != "Nothing":
        $ title = clothing_formatted_title(item)
        "You pull the [title] from where they were carefully concealed in your laundry basket and hand them over to [the_person.title]."
        if the_person.vagina_visible() or the_person.outfit.get_upper_top_layer() == towel:
            "She bends down and steps into them, shimmying as she works them up her legs."
            $ mc.change_locked_clarity(10)
            while not the_person.vagina_visible():
                python:
                    for the_clothing in [x for x in the_person.outfit.get_lower_ordered() if not (x.underwear or x.half_off)]:
                        renpy.say(None, "This causes her " + clothing_formatted_title(the_clothing) + " to ride high up her waist.")
                        scene_manager.draw_animated_removal(the_person, the_clothing, half_off_instead = True)
            $ the_person.outfit.add_lower(item)
            $ scene_manager.update_actor(the_person, position = "stand4", emotion = "happy")
            the_person "Thanks, [the_person.mc_title], I don't know what I would do without you."
            mc.name "No problem, I'll try and keep a better eye on what laundry I'm putting away."
            $ the_person.outfit.restore_all_clothing()
            $ scene_manager.update_actor(the_person, position = "walking_away", emotion = "happy")
            "She spins to walk away and finish getting dressed, pulling slightly at the [item.display_name] to get them settled properly."
        else: #she can't put them on without getting undressed
            "She takes them and quickly stuffs them into her pocket, shifting a bit uncomfortably now that you know she isn't wearing any panties."
            $ mc.change_locked_clarity(5)
            the_person "Thanks, [the_person.mc_title], I don't know what I would do without you."
            mc.name "No problem, I'll try and keep a better eye on what laundry I'm putting away."
            $ scene_manager.update_actor(the_person, position = "walking_away", emotion = "happy")
            "She spins to walk away and finish getting dressed."
        $ return_underwear(item)
        $ panties_to_person(the_person)
    else:
        "You make a show of digging around in your laundry basket before turning around empty handed."
        mc.name "Sorry, [the_person.title] it doesn't look like they are here."
        if the_person == lily:
            the_person "Alright, I guess I'll go see if mom has seen them."
        elif the_person == mom:
            the_person "Thanks anyway [the_person.mc_title], I'll go check with [lily.fname]."
        elif the_person == cousin:
            the_person"God dammit, I'm going to kill your sister."
        else:
            the_person "Okay, I guess I'll have to rethink my outfit for today."
        if the_person.is_employee():
            $ the_person.wear_uniform()
        if the_person.planned_uniform:
            if the_person.planned_uniform.get_panties():
                $ the_person.planned_uniform.remove_clothing(the_person.planned_uniform.get_panties())
        elif the_person.planned_outfit:
            if the_person.planned_outfit.get_panties():
                $ the_person.planned_outfit.remove_clothing(the_person.planned_outfit.get_panties())
    $ scene_manager.clear_scene()
    return
