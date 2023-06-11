init -1 python:
    def lily_intro_one_requirement(person): #friend
        if not lily.has_job(sister_student_job):
            return False
        if not person.event_triggers_dict.get("classmate_1", False):
            return person.location == university

    def lily_intro_two_requirement(person): #rival
        if not lily.has_job(sister_student_job):
            return False
        if person.event_triggers_dict.get("classmate_2", 999) < day:
            return person.location == university

    def lily_intro_three_requirement(person): #acquaintance
        if not lily.has_job(sister_student_job):
            return False
        if person.event_triggers_dict.get("classmate_3", 999) < day:
            return person.location == university

    lily_intro_one_action = Action("Meet Lily's friend", lily_intro_one_requirement, "lily_intro_one", menu_tooltip = "Meet one of Lily's classmates.")

    def college_girls_mod_initialization():
        lily.add_unique_on_room_enter_event(lily_intro_one_action)

init 3 python:
    def lily_friend_mod_initialization(): #Add actionmod as argument#
        global lily_friend
        lily_friend = make_person(age = lily.age, personality = introvert_personality, pubes_style = default_pubes, \
            stat_array = [3,2,4], skill_array = [1,1,1,1,1], sex_skill_array = [1,1,1,1], sluttiness = 0, obedience_range = [105, 110], happiness = 119, love = 10, type = 'story', \
            mc_title = mc.name, relationship = "Single", kids = 0, force_random = True,
            forced_opinions = [["flirting", 2, False], ["skirts", 2, False], ["the colour blue", 2, False]],
            forced_sexy_opinions = [["getting head", 2, False], ["drinking cum", -2, False], ["giving blowjobs", -2, False], ["public sex", -2, False]])
        lily_friend.generate_home()
        lily_friend.set_title(lily_friend.name)
        lily_friend.set_possessive_title(lily_friend.name)
        lily_friend.change_job(student_job)
        lily_friend.set_override_schedule(lily_friend.home, the_times = [3])
        university.add_person(lily_friend)
        # set relationships
        town_relationships.update_relationship(lily, lily_friend, "Friend")
        return

    def lily_rival_mod_initialization(): #Add actionmod as argument#
        global lily_rival
        lily_rival = make_person(age = lily.age, \
            personality = wild_personality, pubes_style = shaved_pubes, \
            stat_array = [2,1,3], skill_array = [1,1,1,1,1], sex_skill_array = [5,2,2,2], sluttiness = 35, obedience_range = [115, 120], happiness = 110, love = 0, type = 'story', \
            mc_title = mc.name, relationship = "Single", kids = 0, force_random = True,
            forced_opinions = [["flirting", 2, False], ["the colour green", 2, False], ["skirts", 2, False]],
            forced_sexy_opinions = [["taking control", 2, False], ["getting head", 2, False], ["drinking cum", 2, False], ["giving blowjobs", 2, False], ["public sex", 2, False]])
        if not lily_rival.has_large_tits():
            lily_rival.tits="DD"
        lily_rival.generate_home()
        lily_rival.set_title(lily_rival.name)
        lily_rival.set_possessive_title(lily_rival.name)
        lily_rival.change_job(student_job)
        lily_rival.set_override_schedule(lily_rival.home, the_times = [3])
        university.add_person(lily_rival)
        # set relationships
        town_relationships.update_relationship(lily_friend, lily_rival, "Friend")
        town_relationships.update_relationship(lily, lily_rival, "Rival")
        return

    def lily_neutral_mod_initialization(): #Add actionmod as argument#
        global lily_neutral
        lily_neutral = make_person(age = lily.age, \
            personality = relaxed_personality, pubes_style = landing_strip_pubes, \
            stat_array = [3,2,4], skill_array = [1,1,1,1,1], sex_skill_array = [2,2,2,2], sluttiness = 15, obedience_range = [95, 100], happiness = 119, love = 0, type = 'story', \
            mc_title = mc.name, relationship = "Single", kids = 0, force_random = True,
            forced_opinions = [["flirting", 0, False], ["the colour red", 2, False], ["skirts", 2, False]],
            forced_sexy_opinions = [["getting head", 2, False], ["drinking cum", 0, False], ["giving blowjobs", 0, False], ["public sex", 0, False]])
        lily_neutral.generate_home()
        lily_neutral.set_title(lily_neutral.name)
        lily_neutral.set_possessive_title(lily_neutral.name)
        lily_neutral.change_job(student_job)
        lily_neutral.set_override_schedule(lily_neutral.home, the_times = [3])
        university.add_person(lily_neutral)
        # set relationships
        town_relationships.update_relationship(lily_friend, lily_neutral, "Friend")
        town_relationships.update_relationship(lily_rival, lily_neutral, "Acquaintance")
        town_relationships.update_relationship(lily, lily_neutral, "Acquaintance")
        return

init 5 python: # hijack
    add_label_hijack("normal_start", "activate_college_girls_mod_core")
    add_label_hijack("after_load", "update_college_girls_mod_core")

label activate_college_girls_mod_core(stack):
    python:
        college_girls_mod_initialization()
        execute_hijack_call(stack)
    return

label update_college_girls_mod_core(stack):
    python:
        if "lily_friend" not in globals():
            college_girls_mod_initialization()
        execute_hijack_call(stack)
    return

label lily_intro_one(the_sister): #friend
    $ scene_manager = Scene()
    $ lily_friend_mod_initialization()
    $ lily.event_triggers_dict["classmate_1"] = True
    $ lily.event_triggers_dict["classmate_2"] = day + 3
    $ the_sister = lily
    $ the_sister.apply_university_outfit()
    $ the_person = lily_friend
    $ the_person.apply_university_outfit()
    $ the_person.set_title(the_person.name)
    $ the_person.set_mc_title(mc.name)
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "walking_away", emotion = "happy")
    $ scene_manager.add_actor(the_sister, emotion = "happy")
    "As you make your way across campus you spot [the_sister.title] standing and talking to another student."
    "She spots you and waves you over to join her."
    the_sister "Hey, [mc.name], what are you doing on campus?"
    menu:
        "Visiting Nora":
            $ the_sister.change_stats(obedience = 2, happiness = -2)
            mc.name "I was on my way to see [nora.title], she has been helping me with some of the research for my business."
            the_sister "That's cool, how is it being back on campus after graduation?"
            mc.name "A little weird, not having a class to get to or a project to work on makes it feel oddly relaxed."
        "Visiting you":
            $ the_sister.change_stats(happiness = 5, love = 2)
            mc.name "We've both been so busy I figured I would come say hi while I was running some errands."
            the_sister "That's sweet, I've been busy too, never seems to be enough time to get my class work all done."
            mc.name "Yeah, I remember what it was like trying to balance classes and homework while trying to have a social life."
    $ scene_manager.update_actor(the_person, position = "stand5")
    the_person "Erm, hello..."
    the_sister "Oh, I'm so sorry, [mc.name] this is my friend [the_person.fname]. [the_person.fname], this is my brother [mc.name]."
    mc.name "It's a pleasure to meet you."
    $ the_person.set_mc_title(mc.name)
    the_person "You too. [the_sister.fname] we should be getting to class."
    "[the_sister.title] looks at her phone to check the time."
    the_sister "Yeah, you're right, sorry [mc.name] I'll see you at home tonight."
    mc.name "Alright, have fun in class. It was nice meeting you [the_person.fname]."
    $ scene_manager.update_actor(the_sister, position = "walking_away")
    the_person "Yeah, you too."
    $ scene_manager.update_actor(the_person, position = "walking_away")
    "They both turn to walk away, and you can't help but to stay and watch until they clear your line of sight."
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped(xoffset = .1, zoom = 0.8))
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.1, zoom = 0.8))
    "Your connection to [nora.fname] means that you are spending more time on campus than you expected when you graduated."
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped(xoffset = .15, zoom = 0.6))
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.15, zoom = 0.6))
    "It occurs to you that there is some pretty strong potential for you to get more involved with the student body as an alumni, not to mention the student's bodies."
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped(xoffset = .2, zoom = 0.4))
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.2, zoom = 0.4))
    "[mc.business.name] is a pretty big time commitment, but as you get things under control it might be worth seeing how you could get involved."
    $ scene_manager.update_actor(the_person, display_transform = character_left_flipped(xoffset = .225, zoom = 0.2))
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.225, zoom = 0.2))
    "With the right connections you are sure that it could be a beneficial relationship for you to grow."
    $ scene_manager.clear_scene()
    $ scene_manager = None
    python:
        lily_intro_two_action = Action("Meet Lily's rival", lily_intro_two_requirement, "lily_intro_two", menu_tooltip = "Meet one of Lily's classmates.")
        lily.add_unique_on_room_enter_event(lily_intro_two_action)
    return

label lily_intro_two(the_sister): #rival
    $ scene_manager = Scene()
    $ lily_rival_mod_initialization()
    $ lily.event_triggers_dict["classmate_2"] = 999
    $ lily.event_triggers_dict["classmate_3"] = day + 3
    $ the_sister = lily
    $ the_sister.apply_university_outfit()
    $ the_person = lily_rival
    $ the_person.apply_university_outfit()
    $ the_person.set_title(the_person.name)
    $ the_person.set_mc_title(mc.name)
    $ followup = None
    $ scene_manager.add_actor(the_sister, position = "walking_away", emotion = "happy")
    "As you make your way across campus you are enjoying the view of the undergrads wandering around in their uniforms."
    "One of them looks more familiar than the rest, and you make your way up behind [the_sister.possessive_title]."
    "You reach out and tap her on the right shoulder as you step to the left, ending up behind her as she turns."
    $ scene_manager.update_actor(the_sister, position = "stand3")
    the_sister "Hey... um... oh, there you are. Hey [the_person.mc_title]!"
    mc.name "Hey [the_sister.title], how are you doing today?"
    if the_sister.sluttiness > 40:
        the_sister "I'm alright, wishing I could be at home playing around on InstaPic instead of here worrying about class."
    elif the_sister.love > 40:
        the_sister "I'm fine, although I'd be happier if we could be hanging out at home together."
    elif the_sister.happiness < 100:
        the_sister "Honestly, I'm having a rough time. I just can't seem to get everything together."
    else:
        the_sister "Eh, you know school is school, but I'm fine."
    $ scene_manager.add_actor(the_person, position = "stand2", display_transform = character_left_flipped, emotion = "happy")
    "The two of you chat for a bit when suddenly another student steps up interjecting herself in your conversation."
    the_person "Hello there handsome, I haven't seen you around here before, planning to transfer?"
    the_sister "Excuse us, we were talking."
    the_person "That's why I stepped in, can't have you making a bad impression with one of the visitors to our campus."
    "She steps forward even more, turning her shoulder to slightly block [the_sister.title] and smiling at you."
    the_person "Hello, I'm [the_person.fname], one person welcoming committee, is there anything I can do to help you?"
    $ the_person.set_mc_title(mc.name)
    menu:
        "Stand up for [the_sister.fname]":
            $ the_sister.change_stats(love = 2, happiness = 2)
            $ the_person.change_stats(happiness = -2, obedience = -2)
            mc.name "Actually no, I'm quite happy talking with [the_sister.fname]. Why don't you go find someone else to bother?"
            the_person "Really, you'd rather spend time with her than with someone like me?"
            "She leans forward squeezing her arms together to draw further attention to her rather sizable chest."
            menu:
                "Dismiss [the_person.fname]":
                    mc.name "Wow, really just whoring it up out here. Tell me, would you expect me to pay for it after?"
                    $ scene_manager.update_actor(the_person, emotion = "angry")
                    the_sister "Don't worry, [the_sister.mc_title] she gives it away all over campus."
                    the_person "Whatever, you too have fun being prudes. [the_person.mc_title] give me a call if you ever want to have some fun, you're cute enough to get a second chance."
                    $ followup = lily
                "Give in":
                    mc.name "Well that is certainly and interesting offer. [the_sister.fname] we can catch up later tonight."
                    $ scene_manager.update_actor(the_sister, emotion = "sad")
                    the_sister "Fine, I'll see you at home. Just be sure to use protection with this one."
                    the_person "At least he won't need to put a bag over my head."
                    $ followup = lily_rival
        "Greet [the_person.fname]":
            $ the_sister.change_stats(love = -2, happiness = -2)
            $ the_person.change_stats(happiness = 2, obedience = 2)
            mc.name "Well, hello, I'm [mc.name] and I certainly wouldn't mind getting your number if you are offering."
            the_person "Of course, let me put it in your phone for you."
            "She reaches out and accepts your phone to start typing in her number."
            the_person "You can go [the_sister.fname], we won't be needing you for anything."
            $ scene_manager.update_actor(the_sister, emotion = "sad")
            "[the_sister.fname] flashes [the_person.fname] a dirty look and then looks to you, disappointment plain on her face."
            the_sister "Well, I guess I'll see you at home later tonight [the_sister.mc_title]."
            $ mc.phone.register_number(the_person)
            "[the_person.fname] hands back your phone, a sudden realization flashing across her face."
            the_person "Oh, you're family, no wonder you are wasting time with her. Can't help who you are related to."
            menu:
                "Defend [the_sister.fname]":
                    mc.name "Hey now, you may have a terrible family but I happen to love mine."
                    $ scene_manager.update_actor(the_person, emotion = "angry")
                    the_sister "Yeah, [the_person.fname], stop taking out your broken home syndrome on the rest of us."
                    the_person "Whatever, give me a call if you ever want to have some fun [the_person.mc_title], you're cute enough to get a second chance."
                    $ followup = lily
                "Let it go":
                    mc.name "Yeah... although [the_sister.fname] isn't so bad."
                    the_person "Sure, sure, gotta keep up appearances. Let's go somewhere private where you can be a bit more honest with me."
                    the_sister "Fine, I guess I know when I'm not wanted."
                    $ followup = lily_rival
    if followup == lily:
        $ the_sister.change_stats(love = 2, happiness = 2)
        $ the_person.change_stats(happiness = -2, obedience = -2)
        $ scene_manager.update_actor(the_person, position = "walking_away")
        "[the_person.title] turns to walk away, aggressively swinging her hips trying to draw more attention to herself."
        the_sister "I'm sorry about that, [the_person.fname] has been a pain in the ass since the semester started."
        $ scene_manager.remove_actor(the_person)
        mc.name "I can see that, sorry you have to deal with that on top of the normal hassles of classes."
        the_sister "Oh, class, I have to go or I'm going to be late. See you tonight."
        "[the_sister.possessive_title] turns and starts to jog off in the direction of her next class."
    else:
        $ the_sister.change_stats(love = -2, happiness = -2)
        $ the_person.change_stats(happiness = 2, obedience = 2)
        $ scene_manager.update_actor(the_sister, position = "walking_away")
        "[the_sister.possessive_title] turns and walks away, clearly upset by the way you treated her."
        the_person "You made the right decision, lets go and I'll reward you for your display of intelligence."
        $ scene_manager.remove_actor(the_sister)
        "[the_person.title] wraps herself around your arm and starts to pull you towards one of the nearby buildings."
        the_person "So... [the_sister.fname] is she super annoying at home because she sure is in class?"
        mc.name "She can be, it really depends on the day."
        the_person "You poor thing, come in here and I'll make you feel better."
        "She pulls you into an empty meeting room and locks the door."
        the_person "So, tell me, how can I reward you?"
        $ the_person.break_taboo("sucking_cock")
        call get_fucked(the_person, the_goal = "oral creampie", private= True, start_position = blowjob, skip_intro = False, ignore_taboo = True, allow_continue = True) from _call_get_fucked_lily_rival
        "Once you've finished you get dressed and head back out to campus."
        "While it was a fun distraction you feel a bit bad about the way you treated [the_sister.possessive_title]."
    $ scene_manager.clear_scene()
    $ scene_manager = None
    python:
        lily_intro_three_action = Action("Meet Lily's acquaintance", lily_intro_three_requirement, "lily_intro_three",
            menu_tooltip = "Meet one of Lily's classmates.")
        lily.add_unique_on_room_enter_event(lily_intro_three_action)
    return

label lily_intro_three(the_sister): #acquaintance
    $ scene_manager = Scene()
    $ lily_neutral_mod_initialization()
    $ lily.event_triggers_dict["classmate_3"] = 999
    $ the_sister = lily
    $ the_sister.apply_university_outfit()
    $ the_person = lily_neutral
    $ the_person.apply_university_outfit()
    $ the_person.set_title(the_person.name)
    $ the_person.set_mc_title(mc.name)
    "Another day, and you once again find yourself on campus. When you graduated you never imagined you would spend so much time back here, but at least you get to see [the_sister.title] more often as a result."
    "You are fairly familiar with her schedule now and it doesn't take long to spot her making her way between buildings."
    $ scene_manager.add_actor(the_sister, emotion = "happy")
    mc.name "Hey, [the_sister.title], how are you doing today?"
    the_sister "Pretty good, just making my way to my next class, what about you."
    mc.name "I'm great, just stopping by to drop off some papers for [nora.fname] and figured we could chat for a bit while I was here."
    $ scene_manager.add_actor(the_person, display_transform = character_left_flipped, position = "stand4", emotion = "happy")
    "Suddenly, another girl steps up from behind you, slightly out of breath."
    the_person "Hey, [the_sister.fname], no time to flirt, we have class in two minutes."
    the_sister "I'm not flirting, this is my brother [mc.name]. [mc.name] this is [the_person.fname]"
    mc.name "It's a pleasure to meet you."
    $ the_person.set_mc_title(mc.name)
    the_person "Sorry, nice to meet you, but we really do have to go."
    "She grabs [the_sister.fname]'s hand and gently pulls her away"
    $ scene_manager.update_actor(the_person, position = "walking_away")
    $ scene_manager.update_actor(the_sister, position = "back_peek")
    the_sister "Sorry, we really do have to go."
    mc.name "Alright, have a good time in class."
    $ scene_manager.update_actor(the_sister, position = "walking_away")
    "Once they are turned around they both break into a jog to try and make it to class in time."
    $ the_sister.event_triggers_dict["study_buddy"] = True
    $ scene_manager.clear_scene()
    $ scene_manager = None
    return
