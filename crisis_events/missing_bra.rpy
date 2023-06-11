init -1 python:
    def home_missing_bra_requirement():      #Use this section to set up when this crisis or action can be fired.
        if home_missing_bra_get_people():
            return True
        return False

    def home_missing_bra_get_people():
        temp_list = []
        if mc.is_home():
            for person in [x for x in people_in_mc_home()]:
                if person.event_triggers_dict.get("stolen_bras",0) > 0:
                    count = person.event_triggers_dict.get("stolen_bras",0)
                    if get_person_bra_list(person):
                        while count:
                            temp_list.append(person)
                            count -= 1
        if temp_list:
            return get_random_from_list(temp_list)
        else:
            return get_random_from_list(people_in_mc_home())
        return None

    def bra_to_person(person):
        if person.event_triggers_dict.get("stolen_bras",0) > 0:
            person.event_triggers_dict["stolen_bras"] -= 1
        return

    def get_person_bra_list(person): #Returns a list of tuples. First item is the common display name "PERSON's ITEM", the second is the item reference itself #TODO: Add unit tests
        return_list = []
        if not person.identifier in mc.stolen_underwear:
            mc.stolen_underwear[person.identifier] = []
        if mc.stolen_underwear[person.identifier]:
            for item in mc.stolen_underwear[person.identifier]:
                if item in bra_list:
                    return_list.append([person.title + "'s " + clothing_formatted_title(item), item]) #TODO: Write the display code for this so it can show the little set of bra or bra with the correct colour/pattern. #TODO: might need an "empty" body type.
        if return_list:
            return_list.append(["Nothing", "Nothing"])
            return return_list
        return None

init 3 python:
    home_missing_bra_action = ActionMod("Missing Bra", home_missing_bra_requirement, "home_missing_bra_label",  #Using ActionMod automatically adds this event to the crisis list
        menu_tooltip = "A family member is looking for their bra.", category = "Home", is_crisis = True, is_morning_crisis = True, priority = 10)

label home_missing_bra_label():
    $ scene_manager = Scene()  #Clean Scene
    $ the_person = home_missing_bra_get_people()
    if not the_person:
        return
    if the_person.sluttiness >= 70:
        $ the_person.apply_outfit(Outfit("Nude"))
    elif the_person.sluttiness >= 60:
        $ apply_towel_outfit(the_person)
    elif the_person.sluttiness >= 40:
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
    if the_person.sluttiness >= 30 and the_person.sluttiness < 60:
        while not the_person.tits_visible():
            $ the_person.outfit.remove_random_upper(top_layer_first = True)
    if the_person.wearing_bra():
        $ the_person.outfit.remove_clothing(the_person.get_bra())
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
    the_person "I couldn't seem to find the bra I was going to wear with my outfit today."
    $ the_person.update_outfit_taboos()
    $ mc.change_locked_clarity(10)
    if the_person.get_opinion_score("not wearing underwear")<= 0:
        the_person "I really don't feel comfortable leaving the house without it."
    else:
        the_person "Although leaving the house without it wouldn't be so bad."
        $ mc.change_locked_clarity(5)
    mc.name "Let me check."
    $ item = "Nothing"
    if get_person_bra_list(the_person):
        $ item = menu(get_person_bra_list(the_person))
    else:
        "You can't imagine that you have what she is looking for, but you decide to humor her."
    if item != "Nothing":
        $ title = clothing_formatted_title(item)
        "You pull the [title] from where it was carefully concealed in your laundry basket and hand it over to [the_person.title]."
        if the_person.tits_visible():
            "She threads her arms through the holes and starts to work it onto her breasts."
            $ mc.change_locked_clarity(10)
            $ scene_manager.update_actor(the_person, position = "back_peek", emotion = "happy")
            "Then she spins around and takes a step back towards you."
            the_person "Since I'm here anyway, would you mind closing the clasp for me?"
            $ mc.change_locked_clarity(10)
            mc.name "Of course."
            $ test_outfit.add_upper(item)
            $ the_person.apply_outfit(test_outfit)
            $ scene_manager.update_actor(the_person, position = "back_peek", emotion = "happy")
            "You quickly close it, brushing your fingers along her smooth back as you do so."
            the_person "Thanks, [the_person.mc_title], I don't know what I would do without you."
            mc.name "No problem, I'll try and keep a better eye on what laundry I'm putting away."
        elif the_person.outfit.get_upper_top_layer() == towel:
            $ test_outfit.add_lower(get_random_from_list(underwear_list(the_person, bra = False, panties = True)[1]).get_copy())
            $ test_outfit.remove_clothing(towel)
            $ the_person.apply_outfit(test_outfit)
            $ scene_manager.update_actor(the_person, position = "stand", emotion = "happy")
            "Holding the [the_item.display_name] in one hand she uses the other to drop her towel so that she can put it on immediately."
            $ mc.change_locked_clarity(10)
            the_person "Thanks, [the_person.mc_title], I don't know what I would do without you."
            $ test_outfit.add_upper(item)
            $ the_person.apply_outfit(test_outfit)
            mc.name "No problem, I'll try and keep a better eye on what laundry I'm putting away."
        else: #she can't put it on without getting undressed
            "She takes the bra and quickly stuffs it into her pocket, shifting a bit uncomfortably now that you know she isn't wearing any bra."
            $ mc.change_locked_clarity(5)
            the_person "Thanks, [the_person.mc_title], I don't know what I would do without you."
            mc.name "No problem, I'll try and keep a better eye on what laundry I'm putting away."
        $ scene_manager.update_actor(the_person, position = "walking_away", emotion = "happy")
        "She spins to walk away and finish getting dressed."
        $ return_underwear(item)
        $ bra_to_person(the_person)
    else:
        "You make a show of digging around in your laundry basket before turning around empty handed."
        mc.name "Sorry, [the_person.title] it doesn't look like it is here."
        if the_person == lily:
            the_person "Alright, I guess I'll go see if mom has seen it."
        elif the_person == mom:
            the_person "Thanks anyway [the_person.mc_title], I'll go check with [lily.fname]."
        elif the_person == cousin:
            the_person"God dammit, I'm going to kill your sister."
        else:
            the_person "Okay, I guess I'll have to rethink my outfit for today."
        if the_person.is_employee():
            $ the_person.wear_uniform()
        if the_person.planned_uniform:
            if the_person.planned_uniform.get_bra():
                $ the_person.planned_uniform.remove_clothing(the_person.planned_uniform.get_bra())
        elif the_person.planned_outfit:
            if the_person.planned_outfit.get_bra():
                $ the_person.planned_outfit.remove_clothing(the_person.planned_outfit.get_bra())
    $ scene_manager.clear_scene()
    return
