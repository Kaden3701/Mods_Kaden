init -1 python:
    def serum_test_crisis_requirement():
        if mc.business.is_open_for_business() and mc.is_at_work():
            if mandatory_paid_serum_testing_policy.is_active():
                return not get_random_from_list([x for x in mc.business.get_employee_list() if len(x.serum_effects) > 0]) is None
        return False

init 3 python:
    serum_test_action = ActionMod("Serum Test", serum_test_crisis_requirement, "serum_test_crisis_label",
        menu_tooltip = "An employee wants to discuss some serum side effects with you.", category = "Business Crisis", is_crisis = True, priority = 10)

label serum_test_crisis_label():
    $ the_person = get_random_from_list([x for x in mc.business.get_employee_list() if len(x.serum_effects) > 0])
    $ the_serum = get_random_from_list(the_person.serum_effects)
    $ the_person.draw_person(emotion = "sad")
    "As you are working one of your employees comes up to you looking like she is having a problem."
    the_person "Hey, [the_person.mc_title] I was hoping that I could talk to you in private."
    mc.name "Sure, [the_person.title] let's go to my office."
    $ mc.change_location(ceo_office)
    "Once there you sit down at your desk and gesture for her to sit as well."
    $ the_person.draw_person(position = "sitting", emotion = "sad")
    the_person "Thanks, for taking some time for me."
    mc.name "Of course, [the_person.title]. What can I do for you?"
    the_person "I don't want to worry the other girls, but I think that there is something wrong with one of our serums."
    mc.name "What do you mean?"
    if daily_serum_dosage_policy.is_active():
        the_person "I know testing our product is an important part of the job, but today's dose is making me feel a bit off."
        if the_person in mc.business.research_team:
            $ the_serum = mc.business.r_serum
        elif the_person in mc.business.market_team:
            $ the_serum = mc.business.m_serum
        elif the_person in mc.business.production_team:
            $ the_serum = mc.business.p_serum
        elif the_person in mc.business.supply_team:
            $ the_serum = mc.business.s_serum
        elif the_person in mc.business.hr_team:
            $ the_serum = mc.business.h_serum
        if not the_serum:
            $ the_serum = get_random_from_list(the_person.serum_effects)
    elif mandatory_unpaid_serum_testing_policy.is_active():
        the_person "I know you asked me to test a serum, and I trust you, but something is making me feel a bit odd."
    elif mandatory_paid_serum_testing_policy.is_active():
        the_person "I've loved the extra income we can earn testing serums, but something has been making me feel weird today."
    mc.name "Well, it isn't good that you are having side effects, but that is one of the reasons these tests are so important."
    mc.name "Can you describe the problem so I can let our research team know what to look for?"
    the_person "Absolutely, I want to help avoid this problem in the future."
    if the_serum.has_trait(depressant_side_effect) or the_serum.has_trait(anxiety_provoking): # -happiness high_con_drugs climax_enhancer
        the_person "As soon as I took this dose I felt really depressed."
        if the_person.get_job_happiness_score() > 0:
            the_person "I usually love coming to work, but right now all I can think about is how sad I am."
        else:
            the_person "Work isn't my favorite thing, but usually I can get through it. Today it just seems impossible."
    elif the_serum.has_trait(libido_suppressant): # -sluttiness large_obedience_enhancer
        if not the_person.judge_outfit(the_person.outfit):
            the_person "This morning when I got dressed I thought this outfit would look great, but now it feels very revealing."
        else:
            the_person "It's hard to pin down, but I've just been feeling really numb today, like nothing is intersting to me."
    elif the_serum.has_trait(performance_inhibitor): # -stats sedatives_trait
        the_person "Ever since I took my dose today I've felt like I was struggling to work. My focus is all over and I can't seem to do even routine tasks."
    elif the_serum.has_trait(mood_swings): # random happiness
        the_person "I've felt really moody today. One moment I'm up and the next I'm down. It feels so strong and chaotic. It is making it hard to trust myself."
    elif the_serum.has_trait(sedative) or the_serum.has_trait(slow_release_sedative): # -energy simple_aphrodesiac
        the_person "I'm really tired, I got a full nights sleep but I keep catching myself yawning for no reason."
    elif the_serum.has_trait(uncontrollable_arousal_side_effect): # +sluttiness
        the_person "I've been feeling hot and bothered all day."
        if the_person.sluttiness > 80:
            the_person "I keep fantasizing about you walking up and taking me right here in the middle of the office."
        if the_person.sluttiness > 60:
            the_person "I keep thinking about you, and how much I'd like to find somewhere private to fool around."
        elif the_person.sluttiness > 40:
            the_person "I keep thinking that I should find somewhere private to play with myself."
        elif the_person.sluttiness > 20:
            the_person "I keep thinking I need to calm down but it is so hard to ignore."
        else:
            the_person "I'm sorry, I'm too embarrassed to elaborate."
    elif the_serum.has_trait(tryptamine_side_effect): # +obey
        if get_existing_rival_count(town_relationships, the_person) > 0:
            $ the_rival = get_random_from_list(get_existing_rivals(town_relationships, the_person))
            the_person "Usually I don't really get along with [the_rival.fname], but earlier when she asked me to do something I did it without a second of hesitation."
        else:
            the_person "I've been unusually agreeable today, earlier I kept letting people cut in front of me at the bathroom, even though I really had to go."
    elif the_serum.has_trait(oxytocin_side_effect) and the_person.love < 40: # +love if <40
        the_person "I've never had a problem with you, but today I keep thinking we should get closer."
        the_person "I caught myself doodling hearts with our names in them like a little school girl."
    elif the_serum.has_trait(caffeine_trait): # -obey aphrodisiac mood_enhancer
        the_person "I'm really disagreeable, everytime someone asks me something I snap at them."
    else:
        the_person "I'm not sure. Something is off but I can't figure out what."
    the_person "What do you think I should do?"
    menu:
        "Stay at work":
            mc.name "We knew there would be some side effects, it is best to just push through them."
            mc.name "I'm going to need you to stay at work, just make notes throughout the day about what is happening and how long it lasts."
            the_person "If you think that is best, I'll be sure to drop off my notes with the research department at the end of the day."
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(5)
            $ the_person.apply_serum_study()
            $ the_person.apply_serum_study(add_to_log = False) # I want extra progress but no spam
            $ the_person.apply_serum_study(add_to_log = False)
            mc.name "Thank you, I know you can get through this."
            "With the crisis somewhat resolved you get back to work, and trust [the_person.title] to do the same."
        "Go home":
            mc.name "That sounds serious, if you think you need to you could go home for the day."
            the_person "Really, I don't want to let you and the company down."
            mc.name "Of course, your well being is important, we can make it the rest of the day without you."
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            $ the_person.change_happiness(5)
            the_person "Thank you so much, but there is one other problem."
            mc.name "What's that?"
            the_person "I'm a little worried about going home alone, what if it gets worse?"
            if not the_person.is_single() and not the_person.is_girlfriend():
                $ so_title = SO_relationship_to_title(the_person.relationship)
                the_person "My [so_title] will be at work all day and I'll be all alone."
            mc.name "I could go with you if you want."
            the_person "Are you sure, I know you have work to do also."
            mc.name "Part of my job is studying these side effects, this would give me a chance to focus on yours and try to find a way to prevent them in the future."
            the_person "Okay, I'll meet you outside."
            $ the_person.draw_person(position = "walking_away")
            "She turns and starts to head for the lobby."
            $ clear_scene()
            "You gather up your things and head down to the parking lot where [the_person.title] is waiting."
            $ mc.change_location(downtown)
            $ the_person.draw_person()
            if the_person.home in mc.known_home_locations:
                "Once you are in the car she starts to give you directions before you interrupt her."
                mc.name "Don't worry, [the_person.title] I already know where you live."
                the_person "Oh, right, sorry I am so frazzled I forgot."
            else:
                "Once you are in the car you get it started and realize you don't know where to go."
                mc.name "I just need to know where we're going."
                the_person "Oh, right, I forgot we've never talked about my home."
                if the_person.relationship == "Single" or the_person.kids == 0:
                    $ ran_num = renpy.random.randint(4, 8)
                    $ opinion = get_random_from_list(["Peach Trees", "Nakatomi Plaza", "La Fortuna", "Villa Bonita", "St. Germaine"])
                    the_person "I have a nice little place in the [opinion] apartment block on the [ran_num]th floor."
                else:
                    $ opinion = get_random_from_list(["Lyon Estates just south of Hill Valley", "Bristol Avenue in Brentwood", "Carnarvon Park in Newbury", "Quimby Street in Cullen"])
                    the_person "We have a beautiful home at the [opinion]."
                $ the_person.learn_home()
            "After a short drive you get to [the_person.title]'s home and help her up to the door."
            $ mc.change_location(the_person.home)
            $ the_person.draw_person(position = "sitting")
            "Once she is settled in on the couch you head towards the kitchen."
            mc.name "Let me get you something to drink, what would you like."
            if renpy.random.randint(0,1) == 1:
                the_person "A glass of water would be great."
            else:
                the_person "I could really use a glass of wine, if you think that would be okay."
            mc.name "Of course, let me grab it."
            $ mc.change_location(kitchen)
            "Alone in the kitchen you have a chance to double down and add another serum to [the_person.title]'s drink."
            call give_serum(the_person) from _call_give_serum_side_effect
            "With that done it is time to figure out what you want to do alone with [the_person.possessive_title]."
            $ mc.change_location(the_person.home)
            $ the_person.draw_person(position = "sitting")
            menu:
                "Distract her from the side effects":
                    "Deciding that it would be best to just talk to her you launch into some small talk."
                    call small_talk_person(the_person, apply_energy_cost = False, is_phone = False) from _call_small_talk_person_side_effect
                    call small_talk_person(the_person, apply_energy_cost = False, is_phone = False) from _call_small_talk_person_side_effect2
                    "It works out pretty well and you have the opportunity to learn more about [the_person.title] and the side effects she is suffering at the same time."
                "Focus on the problem":
                    "The side effects in your serums have been a real problem so you take the opportunity to really drill into what is going on with the serum currently affecting [the_person.title]."
                    "You start out with a fairly basic round of questions and are able to learn a bit more about what is going on."
                    $ the_person.apply_serum_study()
                    $ the_person.change_stats(happiness = -2)
                    "She isn't trilled, but she tolerates the questioning fairly well."
                    menu:
                        "Continue":
                            "Seeing how effective it is you decide to pursue some more detailed and direct questions."
                            $ the_person.apply_serum_study(add_to_log = False)
                            $ the_person.apply_serum_study()
                            $ the_person.change_stats(happiness = -5)
                            "Unfortunately it seems like she is starting to feel like she is being grilled."
                            menu:
                                "Keep pushing":
                                    "This is the reason you are here. She will get over the frustration and discomfort just like she will get over the side effects."
                                    $ the_person.apply_serum_study(add_to_log = False)
                                    $ the_person.apply_serum_study(add_to_log = False)
                                    $ the_person.apply_serum_study()
                                    $ the_person.change_stats(happiness = -10)
                                    "She is clearly upset now. You might irrepearably damage your relationship if you persist."
                                    menu:
                                        "Dig deeper":
                                            "Throwing caution to the wind you really start to demand answers."
                                            $ the_person.apply_serum_study(add_to_log = False)
                                            $ the_person.apply_serum_study(add_to_log = False)
                                            $ the_person.apply_serum_study(add_to_log = False)
                                            $ the_person.apply_serum_study()
                                            $ the_person.change_stats(happiness = -20)
                                            "She answers what questions she can, and you feel like you really got some valuable insight from the process."
                                            "Unfortunately it is also pretty clear that she did not enjoy the way you treated her."
                                        "Relent":
                                            "Sensing that it is possible to go too far you stop of the day, although it seems like the damage has already been done."
                                "Back off":
                                    "You back off and shift focus. Wrapping up with some more gentle conversation."
                                    $ the_person.change_stats(happiness = 2)
                                    "She breathes a sign of relief, although your early actions left their mark."
                        "Stop":
                            "You wrap up with some more gentle and casual conversation to put her at ease."
                            $ the_person.change_stats(happiness = 5)
                            "She seems to appreciate it, even if you didn't make as much progress as you could have."
                "Take advantage of the alone time" if the_person.love > 40 or the_person.effective_sluttiness("touching_body") > 24:
                    "The serum research is important, but there are some other things that spring to mind when you consider what you want to do while alone with [the_person.fname]."
                    if the_person.love > 40:
                        call flirt_person(the_person) from _call_flirt_person_side_effect
                    elif the_person.effective_sluttiness("touching_body") > 24:
                        call grope_person(the_person)
                    $ the_person.apply_serum_study()
            $ day_part = time_of_day_string(time_of_day)
            "All told it has been a productive [day_part], so you head back to the office to record what notes you can."
            $ mc.change_location(ceo_office)
            $ clear_scene()
    $ the_person.apply_serum_study()
    return
