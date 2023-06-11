init -1 python:
    def katie_intro_requirement(person):
        return katie.location == strip_club

    def paige_intro_requirement(person):
        if 'katie' in globals():
            if katie in known_people_in_the_game():
                the_friend = None
                for x in all_people_in_the_game():
                    if x.name == "Paige" and x.last_name == "Sallow":
                        the_friend = x
                if not the_friend:
                    return False
                for relationship in town_relationships.get_business_relationships(["Best Friend"]):
                    if relationship.person_a == katie:
                        if relationship.person_b == the_friend:
                            return False
                    if relationship.person_a == the_friend:
                        if relationship.person_b == katie:
                            return False
                return person.location == strip_club
        return False

    katie_intro_action = Action("Meet Katie", katie_intro_requirement, "katie_intro", menu_tooltip = "Meet Katie at the strip club.")
    paige_intro_action = Action("Meet Paige", paige_intro_requirement, "paige_intro", menu_tooltip = "Meet Katie's friend at the strip club.")

    def katie_mod_initialization():
        katie_initialization()
        soni_initialization()
        katie.add_unique_on_room_enter_event(katie_intro_action)
        katie.add_unique_on_room_enter_event(paige_intro_action)
        return

init 3 python:
    def katie_initialization(): #Add actionmod as argument#
        global katie
        katie = make_person(name = "Katie", last_name = "Maclachlan", age = 19, body_type = "thin_body", face_style = "Face_8", tits = "E", height = 0.91, hair_colour = "knight red", hair_style = shaved_side_hair, pubes_style = shaved_pubes, skin = "white", \
            eyes = "green", personality = relaxed_personality, stat_array = [7,7,7], skill_array = [4,4,8,4,4], sex_skill_array = [3,1,1,0], \
            sluttiness = 100, obedience_range = [145, 150], happiness = 100, love = 0, type = 'story', relationship = "Single", kids = 0)
        katie.generate_home()
        katie.change_job(student_job)
        katie.event_triggers_dict["strip_club_shifts"] = 1
        katie.set_schedule(stripclub_stripper_job.job_location, the_times = [4])
        katie.add_role(stripclub_stripper_role)
        stripclub_strippers.append(katie)
        strip_club.add_person(katie)
        return

    def soni_initialization(): #Add actionmod as argument#
        global soni
        soni = make_person(name = "Soni", last_name = "Kusanagi", age = 27, body_type = "curvy_body", face_style = "Face_7", height = 0.95, skin = "white", eyes = "green", tits = "F", hair_colour = "knight red", hair_style = ponytail, pubes_style = shaved_pubes,
            personality = wild_personality, stat_array = [8,8,8], skill_array = [4,4,8,4,4], sex_skill_array = [2,3,4,1], relationship = "Single", kids = 0 ,sluttiness = 40, type = 'story', obedience_range = [145, 150])
        soni.home = katie.home
        soni.home.add_person(soni)
        soni.set_override_schedule(soni.home, the_times = [0,4])
        # set relationships
        town_relationships.update_relationship(soni, katie, "Cousin")
        return

init 5 python:
    add_label_hijack("discover_stripclub_label", "activate_katie_mod_core")

label activate_katie_mod_core(stack):
    "Katie is a maxed out stripper/student built by special request."
    "She has no significant story and comes precorrupted."
    "Would you like to meet Katie?"
    menu:
        "Yes":
            python:
                katie_mod_initialization()
        "No":
            pass
    python:
        # continue on the hijack stack if needed
        execute_hijack_call(stack)
    return

label katie_intro(the_person):
    $ scene_manager = Scene()
    $ the_person = katie
    $ scene_manager.add_actor(the_person, position = "walking_away")
    "As you enter the strip club your eyes are immediatly drawn to one of the girls walking between the tables."
    "Her back is towards you, but you start to make your way in her direction."
    $ scene_manager.update_actor(the_person, position = "stand3")
    call person_introduction(the_person, girl_introduction = True) from _call_person_introduction_katie
    $ scene_manager = None
    return

label paige_intro(person_one):
    $ person_one = katie
    $ person_two = next(x for x in all_people_in_the_game() if x.name == "Paige" and x.last_name == "Sallow")
    $ person_two.location == strip_club
    python:
        scene_manager = Scene()
        scene_manager.add_actor(person_one, position = "stand4", emotion = "happy", display_transform = character_center_flipped)
        scene_manager.add_actor(person_two, position = "stand3")
    person_one "Oh, hello [person_one.mc_title], how nice to see you here."
    mc.name "Hello [person_one.title], nice to see you too."
    python:
        formatted_title = person_two.create_formatted_title(person_two.name + " " + person_two.last_name)
        title_choice = person_two.get_random_title()
        person_two.set_title(title_choice)
        person_two.set_possessive_title(person_two.get_random_possessive_title())
    person_one "Let me introduce my friend..."
    person_two "You mean best friend!"
    person_one "Right... my BEST friend [formatted_title]."
    $ town_relationships.update_relationship(person_one, person_two, "Best Friend")
    if person_two in known_people_in_the_game():
        person_two "The introduction is nice, but we already know each other."
        person_one "Really?"
        if person_two.is_employee():
            mc.name "Yes, I hired her the other day. She works for me."
        else:
            mc.name "Yes, we met the other day."
    else:
        "[formatted_title] holds her hand out to shake yours."
        python:
            title_choice = get_random_from_list(person_two.get_player_titles())
            person_two.set_mc_title(title_choice)
        if person_one.is_employee():
            person_one "And this is my boss, [title_choice]."
        else:
            person_one "And this is my friend, [title_choice]."
        mc.name "It's a pleasure to meet you, [formatted_title]."
        $ scene_manager.update_actor(person_two, emotion = "happy")
        $ person_two.change_love(5)
        person_two "The pleasure is all mine, [person_two.mc_title]."
        if formatted_title != person_two.title:
            person_two "But please, call me [person_two.title]."
    if person_one.sluttiness > 20 or person_one.love > 20:
        if person_one.is_employee() and not person_two.is_employee():
            if person_one.sluttiness > 40:
                person_one "You should get to know him more intimately [person_two.fname], you should apply for a position in the company."
            else:
                person_one "I promise you [person_two.fname], he is a great boss. You should go out with him sometime."
        else:
            if person_one.sluttiness > 40:
                person_one "He can show you a really good time [person_two.fname], if you know what I mean."
            else:
                person_one "I have to tell you [person_two.fname], he is a great person to hang out with."
        $ person_two.change_stats(happiness = 10, love = 5)
        if person_two.sluttiness > 30:
            person_two "Well, he's very handsome [person_one.fname], I wouldn't mind going on a date with him."
        elif person_two.sluttiness > 10:
            person_two "He is very cute [person_one.fname], I might just do that."
        else:
            person_two "I trust your judgement [person_one.fname], perhaps we could go out sometime."
    mc.name "It was great meeting you both here. I'll see you around [person_two.title]."
    if person_two.has_role(prostitute_role):
        person_two "If you ever want some company, give me call, I'm sure we can come to some kind of arrangement."
        "She hands you a business card with her phone number."
        $ mc.phone.register_number(person_two)
    $ scene_manager.update_actor(person_two, position = "back_peek")
    $ scene_manager.update_actor(person_one, position = "walking_away")
    "While walking away [person_two.title] looks back at you smiling."
    python: # Release variables
        scene_manager.clear_scene()
        title_choice = None
        formatted_title = None
        del person_two
        del person_one
    return
