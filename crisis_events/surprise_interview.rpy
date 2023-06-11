init 2 python:
    def surprise_interview_requirement():
        if mc.business.is_open_for_business() and mc.is_at_work() and mc.business.get_employee_count() < mc.business.max_employee_count:
            if corporal_punishment.is_active():
                return True
        return False

    def surprise_teamwork_person(temp_list):
        if any(x for x in temp_list if not x.has_taboo(["sucking_cock", "condomless_sex"]) and x.get_opinion_score("threesomes") > -2):
            return get_random_from_list([x for x in temp_list if not x.has_taboo(["sucking_cock", "condomless_sex"]) and x.get_opinion_score("threesomes") > -2])
        return None

    surprise_interview_action = ActionMod("Surprise Interview", surprise_interview_requirement, "surprise_interview_label",
        menu_tooltip = "A woman shows up at the office looking for a job.", category = "Business", is_crisis = True)

label surprise_interview_label():
    $ scene_manager = Scene()
    $ the_person = interview_build_candidates_list(1)[0]
    $ the_person.set_mc_title(get_random_from_list(the_person.get_player_titles()))
    $ the_person.set_title(the_person.get_random_title())
    $ the_person.set_possessive_title(the_person.get_random_possessive_title())
    $ the_person.generate_home()
    $ the_person.change_job(unemployed_job)
    $ office.add_person(the_person)
    $ the_other_person = mc.business.hr_director
    $ threesome_person = None
    if not the_other_person:
        $ the_other_person = get_random_from_list(mc.business.hr_team)
    if not the_other_person:
        $ the_other_person = get_random_from_list(mc.business.supply_team)
    $ mc.change_location(ceo_office)
    "You are gathering some papers from the desk in your office when you hear an urgent knocking on the door."
    if the_other_person:
        "As you are turning to answer the door you hear someone in the main office start talking."
        the_other_person "Excuse me? Can I help you?"
        "The person at your door responds, but you can't quite make out her words."
        if mc.business.hr_director or get_random_from_list(mc.business.hr_team):
            the_other_person "I'm sorry, I didn't know he was expecting someone, let me check the calendar. What was your name?"
            "Her reply is indistinct again, but it sounds a bit more flustered, almost panicky."
        else:
            the_other_person "Oh, sorry we don't have anyone handling human resources right now, I'm sure he'll be right out."
    else:
        "There isn't anyone in the outer office, so you should probably see who is there."
    $ mc.change_location(office)
    $ scene_manager.add_actor(the_person)
    $ scene_manager.update_actor(the_person, position = "walking_away")
    "You make your way to the door and open it to see a stranger standing just outside."
    if the_other_person:
        $ scene_manager.add_actor(the_other_person, display_transform = character_center_flipped, emotion = "sad")
        "Right behind her is [the_other_person.possessive_title], obviously trying to figure out what to do with this person just walking into the office."
    $ scene_manager.update_actor(the_person, position = "stand2", emotion = "happy")
    the_person "Oh, hello Mr. [mc.last_name]! I'm [the_person.fname]. I'm here for my interview."
    "Interview? Did you have an interview scheduled today?"
    if get_random_from_list(mc.business.hr_team):
        the_other_person "I'm sorry [the_other_person.mc_title] I didn't see anything about an interview. Did you schedule one?"
        mc.name "I don't think so... but since she is here, can you pull up her application?"
        the_other_person "Of course."
        $ scene_manager.update_actor(the_other_person, display_transform = character_center_flipped, position = "standing_doggy")
    elif get_random_from_list(mc.business.supply_team):
        "[the_other_person.possessive_title] looks relieved to have you taking care of this and gets back to her work ordering supplies."
        $ scene_manager.update_actor(the_other_person, display_transform = character_center_flipped, position = "sitting")
    else:
        "At least no one else is here to see you messing up a simple interview schedule."
    mc.name "I'm sorry, [the_person.fname] was it? Did I set up this interview?"
    the_person "Not personally, I got an email from one of your employees."
    if not get_random_from_list(mc.business.hr_team):
        "None of your employees are even responsible for hiring..."
    mc.name "Sorry, for the confusion, could I see the email? I want to make sure we follow up so we can get you an apology from the person responsible."
    the_person "Oh... right... it should be right here."
    "She starts looking through her phone, but it is pretty clear she isn't finding the email. In fact, it seems like she doesn't even expect to find one."
    if get_random_from_list(mc.business.hr_team):
        $ scene_manager.update_actor(the_other_person, display_transform = character_center_flipped, emotion = "sad")
        "As she gets more and more flustered [the_other_person.title] walks up empty handed."
        the_other_person "I'm sorry [the_other_person.mc_title] I can't find her application."
        "She hasn't even submitted an application?"
    mc.name "Do you at least remember the name of the person who emailed you."
    $ scene_manager.update_actor(the_person, position = "kneeling1", emotion = "sad")
    "That seems to break her, she drops to her knees and seems to be practically in tears."
    the_person "Oh, this was so stupid. I'm so sorry! I don't have an interview, I've just been so frustrated with my job hunting."
    if the_person.age < 35:
        the_person "I just keep sending in applications... no one even responds... my father said... back in his day..."
    else:
        the_person "I just keep sending in applications... no one even responds... my grandfather said... back in his day..."
    the_person "I hoped... I don't know... I should just go..."
    if get_random_from_list(mc.business.hr_team):
        $ scene_manager.update_actor(the_other_person, display_transform = character_center_flipped, emotion = "angry")
        "It looks like [the_other_person.title] is about to read her the riot act."
    elif get_random_from_list(mc.business.supply_team):
        $ scene_manager.update_actor(the_other_person, display_transform = character_center_flipped, emotion = "happy", position = "sitting")
        "Out of the corner of your eye you catch [the_other_person.title] looking up from her work, struggling to contain a fit of giggles."
    menu:
        "Have mercy on her":
            mc.name "That's not necessary. Why don't you have a seat on the couch in my office and collect yourself. I'll give you a few minutes and then we can start over."
            the_person "*sniff* R-really?"
            mc.name "Yes, we can straighten this out, please stop crying."
            the_person "Oh, Thank you so much!"
            "She quickly rushes into your office, possibly a little concerned you are going to change your mind."
            $ scene_manager.remove_actor(the_person)
            if get_random_from_list(mc.business.hr_team):
                "[the_other_person.possessive_title] gives the door time to shut but it is clear she is about to turn her anger on you. You hold up your hands to forestall the tirade."
                mc.name "I know, I know, but clearly she is having a hard time. I'm just gonna talk to her a bit. Who knows she might be a good employee."
                the_other_person "Whatever, it is your business."
                "[the_other_person.title] rolls her eyes and turns to get back to her actual work."
                $ scene_manager.remove_actor(the_other_person)
            elif get_random_from_list(mc.business.supply_team):
                "You give [the_other_person.title] a glare and she quickly ducks her head back to her work."
                $ scene_manager.remove_actor(the_other_person)
            "To pass the time you walk over to the coffee machine and fill a couple of cups."
            call give_serum(the_person) from _call_give_serum_surprise
        "Kick her out":
            mc.name "I think that would be for the best. You've wasted enough of our time."
            mc.name "Do I need to escort you out of the building or do you think you can make it out properly?"
            $ scene_manager.update_actor(the_person, position = "stand2", emotion = "sad")
            "She manages to pull herself together and stand up, wiping at her eyes."
            the_person "No, I'll be fine. Sorry again."
            $ scene_manager.update_actor(the_person, position = "walking_away", emotion = "sad")
            if get_random_from_list(mc.business.hr_team):
                "She turns to go and [the_other_person.title] turns to look at you with an incredulous look on her face."
                "At a bit of a loss you just shrug your shoulders and head back into your office."
            elif get_random_from_list(mc.business.supply_team):
                "She turns to go and thankfully makes it out of the room before [the_other_person.title] breaks into full out laughter."
                "At a bit of a loss you just shrug your shoulders and head back into your office."
            else:
                "She turns to go and you watch to make sure she leaves the office, debating on if you should head down to the lobby to ensure she is gone."
            $ scene_manager.remove_actor(the_person)
            $ the_person.remove_person_from_game()
            $ clear_scene()
            $ mc.change_location(ceo_office)
            return
    $ the_person.add_situational_obedience("bribe", 30, "I need a job!")
    $ mc.change_location(ceo_office)
    $ scene_manager.add_actor(the_person, position = "sitting", emotion = "happy")
    "When you enter your office you find her waiting patiently on the couch as instructed. You walk over and offer her the coffee."
    the_person "Thank you so much, I really messed this up and I'm so sorry."
    mc.name "It's okay, let's start over. I'm going to need to take a look at your application before we proceed."
    the_person "Right of course. I have it right here."
    "She hands you a folder of papers which you look over while she starts to work on her coffee."
    call hire_select_process([the_person, 1]) from _call_hire_select_process_surprise
    $ scene_manager.add_actor(the_person, position = "sitting", emotion = "happy")
    if _return == "None":
        "After a quick read it is clear you don't actually want [the_person.fname] to work for you, but there is no reason to tell her that right away."
        "While you read she drank most of her coffee and should be ready for some questions."
    else:
        "You've read most of the relevant information from her resume, and she has had time to drink most of her coffee. Now would be a good time to see how well she will fit in with your company."
    mc.name "This looks good, but there are some things you need to know about working here before we go any further."
    the_person "Of course!"
    if corporal_punishment.is_active():
        mc.name "To ensure that everyone is completing their tasks to the best of their ability we have a system of punishments for those who fail."
        the_person "What kind of punishments?"
        mc.name "It varies, they start out small, but can escalate depending on the situation."
        mc.name "You could be assigned extra tasks, or your pay could be cut to make it up to the company."
        mc.name "However, one of the things that I've found to work best is corporal punishment."
        if strict_enforcement.is_active():
            mc.name "In some extreme situations we make an example of the employee who is being punished."
            mc.name "That can mean giving them embarrassing work to do."
            if strict_uniform_policy.is_active():
                mc.name "It can also mean forcing them to wear a uniform that is more shocking than they are used to."
            if draconian_enforcement.is_active():
                mc.name "If all else fails we may force the employee to sacrifice their time and their body to help the company recover."
        the_person "That is pretty robust, but I only have to worry about it if I do something wrong, right?"
        mc.name "Yes, but that brings me to the fact that you have already done something wrong."
        the_person "But I didn't know about these policies, and I don't even work here yet."
        mc.name "That is correct, but if you want to I'm going to need you to demonstrate your commitment."
        mc.name "We'll start out easy, a little spanking to drive the lesson home and then we can proceed."
        mc.name "Turn around and put your hands on the desk."
        if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 120: #She complains
            "She hesitates, then sighs and turns around and plants her hands flat on the desk."
            the_person "Fine..."
        else:
            "[the_person.title] follows your instructions without any hesitation."
        $ mc.change_locked_clarity(10)
        $ scene_manager.update_actor(the_person, position = "standing_doggy")
        "You stand to the side of [the_person.possessive_title] and place one hand on her hip, ready to spank her with the other."
        $ top_clothing = the_person.outfit.get_lower_top_layer()
        if top_clothing and top_clothing.can_be_half_off and top_clothing.half_off_gives_access and top_clothing.hide_below and not top_clothing.anchor_below and not top_clothing.underwear:
            menu:
                "Pull up her [top_clothing.display_name] first":
                    if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 120 and the_person.effective_sluttiness("underwear_nudity") < 30:
                        "You grab the hem of [the_person.title]'s [top_clothing.display_name]."
                        the_person "Hey! What are you doing?"
                        mc.name "Making sure your [top_clothing.display_name] doesn't get in the way of your punishment."
                        the_person "Are... Are you allowed to do that?"
                        if reduced_coverage_uniform_policy.is_active():
                            mc.name "Once you work here, I have authority over everything you wear."
                        else:
                            mc.name "No clothing is being removed, so yes I can."
                        "You pull her [top_clothing.display_name] up and leave it bunched around her waist."
                    else:
                        "You grab the hem of [the_person.title]'s [top_clothing.display_name] and pull it up around her waist."
                    $ mc.change_locked_clarity(10)
                    $ the_person.draw_animated_removal(top_clothing, position = "standing_doggy", half_off_instead = True)
                    if not the_person.outfit.wearing_panties():
                        mc.name "No panties today, I see."
                    $ the_person.update_outfit_taboos()
                "Leave her [top_clothing.display_name] in place":
                    pass
        "You rub her butt briefly, then slap it hard."
        $ not_cushioned = the_person.vagina_visible() or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered())
        if not_cushioned: #ouch!
            $ spank_factor_increment(the_person)
            "Your hand makes a satisfying smack as it makes contact with her ass cheek. Her ass jiggles for a few moments before settling down."
            the_person "Ah... That really stings..."
        else: #Not too bad.
            "Her clothing absorbs some of the blow, but you still make good contact and set her ass jiggling for a moment."
            the_person "Ah..."
        "You keep smacking her butt, putting more force behind your blow each time."
        if not_cushioned: #Ass gets red, she gets sore.
            $ mc.change_locked_clarity(10)
            "Her exposed ass jiggles with each hit, and quickly starts to turn red."
            the_person "Ah... Am I almost done [the_person.mc_title]?"
            $ spank_factor_increment(the_person)
            if the_person.get_opinion_score("being submissive") > 0: #She likes it and is getting turned on.
                "You spank her again, and she moans."
                $ the_person.discover_opinion("being submissive")
                $ the_person.change_arousal(5*the_person.get_opinion_score("being submissive"))
                the_person "I... Don't know if I can take much more of this! Mmph..."
            else:
                "You spank her again, making her gasp."
                the_person "I... Don't know how much more of this I can take!"
            mc.name "You'll take it until I think you have learned your lesson. Do you understand?"
            "Another smack, another ass jiggle."
            if the_person.get_opinion_score("being submissive") > 0:
                the_person "Yes [the_person.mc_title]! I understand! Ah!"
            else:
                "She lowers her head and grits her teeth."
                the_person "Yes [the_person.mc_title]. Ah..."
            mc.name "Do you have anything to say for your actions?"
            if the_person.get_opinion_score("being submissive") > 0:
                the_person "It won't happen again [the_person.mc_title], I..."
                "You interrupt her with a slap on the ass. She pauses, then continues."
                the_person "I'm sorry, and I see just how wrong I was now! Ah!"
            else:
                the_person "Ow... It won't happen again [the_person.mc_title], I... Ow!"
                "You interrupt her with a slap on the ass. She takes a moment to collect herself before continuing."
                the_person "I promise it won't happen again!"
            $ mc.change_locked_clarity(10)
            "You give her one last hit on her now red butt and then step back, letting her stand up."
            $ spank_factor_increment(the_person)
            $ the_person.outfit.restore_all_clothing()
            $ scene_manager.update_actor(the_person, position = "stand2")
            if the_person.get_opinion_score("being submissive") > 0:
                $ the_person.change_arousal(5*the_person.get_opinion_score("being submissive"))
                $ the_person.change_obedience(the_person.get_opinion_score("being submissive"))
                the_person "Thank you [the_person.mc_title]. I promise I'll do better."
            else:
                $ the_person.change_obedience(3)
                $ the_person.change_love(-2 + the_person.get_opinion_score("being submissive"))
                the_person "Finally. Ow..."
            mc.name "I expect you've learned your lesson. Would you like to continue?"
            the_person "Yes, I still want to work here."
        else: #Doesn't particularly mind."
            if top_clothing:
                "[the_person.title] jerks forward with each strike, but her [top_clothing.display_name] seems to be saving her from the worst of it."
            else:
                "[the_person.title] jerks forward with each strike, but she doesn't seem to mind getting spanked."
            the_person "Ah... Ow..."
            "After a few more strikes it's clear you aren't having the effect on [the_person.possessive_title] that you were hoping for."
            "You give her one last slap on the ass and step back."
            mc.name "Stand up, we're done here."
            $ the_person.outfit.restore_all_clothing()
            $ scene_manager.update_actor(the_person, position = "stand2")
            $ mc.change_locked_clarity(10)
            "She turns around, rubbing her butt."
            the_person "Can we continue the interview?"
            $ the_person.change_love(-1)
            $ the_person.change_obedience(2)
    if office_conduct_guidelines.is_active():
        mc.name "Continuing on with our expectations, there are a number of conduct guidelines we have for employees that I'd like you to ready over. "
        "You hand her the guidelines your staff have been reading along with the five latest daily emails."
        if the_person.sluttiness <20:
            "As she reads them over, she seems a bit flustered, but she doesn't object to anything that is there."
            $ the_person.change_slut(5, 20)
        else:
            "As she reads them over she doesn't seem surprised or concerned by any of the contents."
        if mandatory_staff_reading.is_active():
            mc.name "For further reading I also have this book for you."
            "You pull out a copy of \"Your Place in the Work Place\" and flip it to an especially important part."
            mc.name "I obviously don't expect you to read it all now, but this passage is one of my favorites."
            if the_person.sluttiness <20:
                $ the_person.change_happiness(-5)
            if the_person.sluttiness < 40:
                $ the_person.change_slut(5, 40)
                "As she skims the page you see some significant blushing start to color her skin."
                the_person "Wow, that is rather detailed."
            else:
                "She is still unphased by the growing sexuality of these materials."
                the_person "Wow, this book is pretty good."
            if superliminal_office_messaging.is_active():
                mc.name "I also have a company calendar and some posters for you. If you are hired you can put them in your work area or take them home."
                if the_person.sluttiness <20:
                    "She smiles at first, but when she sees they are all of nude women it falls into something approaching a frown."
                    $ scene_manager.update_actor(the_person, emotion = "sad")
                    $ the_person.change_happiness(-5)
                else:
                    "She smiles at first, it slips a bit when she notices they all feature nude women, but she manages to keep it forced in place anyway."
                $ the_person.change_slut(5, 60)
    if strict_uniform_policy.is_active():
        mc.name "You will be required to wear a uniform for work, fortunately the company will provide it for you."
        the_person "That is so generous, is there a special store I need to go to?"
        mc.name "Actually, I'm pretty sure I have one your size here. Let me check the closet."
        "As you walk over to search you continue talking over your shoulder."
        mc.name "We have a very robust uniform policy here, the clothing you are provided is exactly what you need to wear."
        if maximal_arousal_uniform_policy.is_active():
            mc.name "It can be difficult to get used to at first, but most girls get comfortable with them eventually."
            $ slut_limit = 999 #ie. no limit at all.
        elif corporate_enforced_nudity_policy.is_active():
            mc.name "It can be difficult to get used to at first, but most girls adapt over time."
            $ slut_limit = 80
        elif minimal_coverage_uniform_policy.is_active():
            mc.name "It can be difficult to get used to at first, but everyone adjusts pretty quickly."
            $ slut_limit = 60
        elif reduced_coverage_uniform_policy.is_active():
            mc.name "It can be a bit unusual, but nothing too crazy."
            $ slut_limit = 40
        elif casual_uniform_policy.is_active():
            mc.name "It is pretty basic, we just want to highlight our staff."
            $ slut_limit = 25
        elif relaxed_uniform_policy.is_active():
            mc.name "It is pretty basic, we just want to highlight our staff."
            $ slut_limit = 15
        else:
            mc.name "It is pretty basic, we just want to highlight our staff."
            $ slut_limit = 5
        call outfit_master_manager(slut_limit = slut_limit, show_outfits = False, show_underwear = False, show_overwear = True) from _call_outfit_master_manager_surprise
        $ the_outfit = _return
        if not the_outfit:
            $ the_outfit = default_wardrobe.get_random_appropriate_overwear(slut_limit, sluttiness_min = slut_limit-20, guarantee_output = True, preferences = WardrobePreference(the_person))
        mc.name "Ah, yes here it is."
        "You turn with the outfit in hand and look at [the_person.title]."
        mc.name "Let's start by having you strip down."
        if the_person.effective_sluttiness("underwear_nudity") + (the_person.get_opinion_score("not wearing anything")*10) < 30:
            the_person "You mean right here?"
            mc.name "Yes, if you are going to work here you need to be comfortable working around me, and this is a great way to see how comfortable you are."
        else:
            the_person "Of course."
        $ generalised_strip_description(the_person, strip_list = the_person.outfit.get_underwear_strip_list())
        $ scene_manager.update_actor(the_person, position = "stand2")
        if the_person.effective_sluttiness("underwear_nudity") + (the_person.get_opinion_score("not wearing anything")*10) < 30:
            "[the_person.possessive_title] blushes and tries to cover her body."
            the_person "This is so embarrassing..."
            mc.name "I'm sorry to hear that but..."
        else:
            "[the_person.possessive_title] doesn't seem too bothered, but she does use her hands to cover herself slightly."
            the_person "Can I have my uniform now?"
        if commando_uniform_policy.is_active():
            mc.name "You aren't done yet."
            mc.name "The company uniform is every piece of clothing you will wear to work, and at this time that will never include underwear of any kind."
            if the_person.effective_sluttiness(["bare_tits", "bare_pussy"]) + (the_person.get_opinion_score("not wearing anything")*10) < 50:
                the_person "You can't be serious?"
                mc.name "Absolutely! Take a walk through the building and you'll see that it is something everyone is already complying with."
            else:
                the_person "...okay."
                mc.name "You'll see, everyone else in the building is already complying."
            if the_other_person:
                the_person "I mean... I saw [the_other_person.fname], but I thought she was just some kind of exhibitionist freak."
                mc.name "Have you already forgotten our talk about punishments?"
                the_person "Sorry, no sir."
                mc.name "Good, now hurry up."
            else:
                the_person "Now that you mention it, on the way in I saw some rather unique outfits on display."
                mc.name "Exactly, now hurry up."
            $ generalised_strip_description(the_person, strip_list = the_person.outfit.get_full_strip_list())
            $ scene_manager.update_actor(the_person, position = "stand2")
            if the_person.update_outfit_taboos(): # Broke a taboo
                "[the_person.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
        else:
            if the_person.outfit.get_bra():
                $ the_outfit.add_upper(the_person.outfit.get_bra())
            if the_person.outfit.get_panties():
                $ the_outfit.add_lower(the_person.outfit.get_panties())
        mc.name "Hands down, there's no point hiding anything from me now."
        "She frowns, but follows your instructions. She lowers her hands to her sides, letting you get a good view of her body."
        "Satisfied with your view you hand over the uniform you picked out and watch as she starts to put it on."
        if mandatory_vibe_policy.is_active():
            mc.name "Oh, wait, I forgot there is one more part to your uniform I need to give you."
            "You reach into your desk drawer and pull out a bullet vibrator then take a step towards her."
            if the_person.get_opinion_score("masturbating") <=0:
                the_person "What is that, some kind of pass key?"
                mc.name "It is required when you enter the building, but it doesn't actually unlock the doors."
                mc.name "This is a vibrator, and I'm going to need to insert it into your pussy."
            else:
                the_person "A vibrator?"
                mc.name "Yes, I'm going to need to insert it into your pussy."
            if the_person.effective_sluttiness("touching_vagina") < 55:
                the_person "I think I might need to draw the line there. This is all just too much."
                mc.name "You've come so far [the_person.title]. We are nearly done. Please."
                the_person "...okay, just do it."
            else:
                the_person "If it's really nessesary."
                mc.name "Don't worry, I'll be gentle."
            "You step forward and reach out your hand resting the vibe on her lower belly."
            if not commando_uniform_policy.is_active():
                "Slowly you make your way down her body, sliding under the waist of her panties and pressing the toy firmly against her lips."
            else:
                "Slowly you make your way down her body, pressing the toy firmly against her lips."
            if the_person.effective_sluttiness("touching_vagina") < 55:
                "She shivers a bit as you start to push it in but doesn't object further."
            $ the_person.break_taboo("touching_vagina")
            "With a firm push you slip it into her and stroke her pussy as you pull your hand back."
            "Once you are done you flip the switch in your other hand and she lets out a faint moan."
        mc.name "Great, now you can get dressed."
        $ the_person.change_arousal(20)
        $ the_person.set_uniform(the_outfit, wear_now = True)
        $ scene_manager.update_actor(the_person, position = "stand2")
        if the_person.effective_sluttiness() < the_person.outfit.slut_requirement:
            the_person "Is this it? This is so embarrassing..."
        else:
            the_person "I guess this isn't so bad now that I'm dressed again."
        $ the_person.event_triggers_dict["forced_uniform"] = the_person.outfit.get_copy()
        $ slut_change = 0
        if the_person.tits_visible():
            $ slut_change += the_person.get_opinion_score("showing her tits")
        if the_person.vagina_visible():
            $ slut_change += the_person.get_opinion_score("showing her ass")
        if the_person.tits_visible() and the_person.vagina_visible():
            $ slut_change += the_person.get_opinion_score("not wearing anything")
        $ the_person.change_slut(slut_change, 30)
    if the_other_person and surprise_teamwork_person(mc.business.get_employee_list()):
        mc.name "Just one last thing, here at [mc.business.name] we are all part of a team, and it is important that you can work with the team to achieve shared goals."
        mc.name "Your first impression has left something to be desired, so I'm going to call in someone to ensure you can fit in here."
        if surprise_teamwork_person([the_other_person]):
            $ threesome_person = surprise_teamwork_person([the_other_person])
            mc.name "Since [threesome_person.fname] saw you making a scene she is going to be the best person for this."
        elif surprise_teamwork_person(mc.business.hr_team):
            $ threesome_person = surprise_teamwork_person(mc.business.hr_team)
            if the_other_person in mc.business.hr_team:
                mc.name "Since [the_other_person.fname] saw you making a scene we are going to get someone less biased from HR to conduct this test."
            else:
                mc.name "[threesome_person.fname] from our HR department is going to be the best person to conduct this test."
        elif surprise_teamwork_person(mc.business.get_employee_list()):
            $ threesome_person = surprise_teamwork_person(mc.business.get_employee_list())
            mc.name "Since [the_other_person.fname] saw you making a scene we are going to get someone less biased to conduct this test."
        if threesome_person in mc.business.hr_team or threesome_person in mc.business.supply_team:
            "You walk to the door and call out to [threesome_person.title]."
        else:
            "You pick up your phone and call down to [threesome_person.job.job_location] to get [threesome_person.title]."
        mc.name "She'll be right here."
        $ scene_manager.add_actor(threesome_person, display_transform = character_center_flipped)
        "Sure enough, [threesome_person.possessive_title] soon walks into your office. She spares a glance for [the_person.title] before turning to you."
        threesome_person "What can I do for you [threesome_person.mc_title]?"
        if threesome_person != the_other_person:
            mc.name "This is [the_person.fname], I was just telling her how important teamwork is and was hoping you could aid in a demonstration."
        else:
            mc.name "I was just telling [the_person.fname] how important teamwork is and was hoping you could aid in a demonstration."
        threesome_person "Of course, what do you need me to do?"
        mc.name "Come over here and get down on your knees."
        if threesome_person.get_opinion_score("giving blowjobs") > 0:
            threesome_person "Oh good, I love team building exercises!"
        else:
            threesome_person "Yes [threesome_person.mc_title]."
        "[threesome_person.possessive_title] quickly complies with your command, getting herself into position on the floor in front of you."
        $ scene_manager.update_actor(threesome_person, display_transform = character_center_flipped, position = "kneeling1")
        mc.name "You too [the_person.fname]."
        if the_person.effective_sluttiness("sucking_cock") + 5*the_person.get_opinion_score("giving blowjobs") < 40:
            the_person "Wait, seriously?"
            threesome_person "Don't worry, I'll help. Most of the girls here love helping out Mr. [l_name]."
            $ scene_manager.update_actor(threesome_person, display_transform = character_center_flipped, position = "blowjob", emotion = "happy", special_modifier = "blowjob")
            "Obviously not feeling the need to wait [threesome_person.title] pulls open your pants and quickly takes you into her mouth."
            "[the_person.title] averts her eyes at first, but as [threesome_person.title] moans around your rapidly hardening cock her eyes start to drift back."
            "For a couple minutes the room is quiet apart from a soft slurping sound each time [threesome_person.title] slides herself down your shaft."
            if mandatory_vibe_policy.is_active():
                $ the_person.change_arousal(10)
                "You goose the vibrator once more and [the_person.title] lets out another moan as one hand drifts to a breast the other drops to her crotch."
            else:
                "At one point you look up to see that [the_person.title]'s hands have drifted, one to her mouth and one to a breast."
            "[the_person.title] seems entranced. As you watch she starts to slowly move forward, taking small steps until she is right next to you."
            $ scene_manager.update_actor(the_person, position = "kneeling1")
            "Another moment later she lowers herself to her knees, staring at [threesome_person.title] as she works over your dick."
            "[threesome_person.title] pulls off and turns to [the_person.title] with a slobbery smile."
            threesome_person "Welcome to the team [the_person.fname], ready to get in the game?"
            "At a loss for words [the_person.title] just nods and leans forward. [threesome_person.title] gives you a quick grin and joins her."
        else:
            the_person "...okay."
            threesome_person "Don't worry, you'll like this. He has such a nice cock and is always happy to share it with us."
            "[the_person.possessive_title] also drops to her knees and although she looks less eager she prepares herself as you open up your pants."
        call start_threesome(threesome_person, the_person, start_position = threesome_double_blowjob, skip_intro = True, private = True, position_locked = True, affair_ask_after = False) from _call_start_threesome_surprise
        $ threesome_person.restore_all_clothing()
        $ scene_manager.update_actor(threesome_person, position = "stand2")
        "With her work done, [threesome_person.title] gets up and starts to straighten her clothes."
        $ scene_manager.update_actor(the_person, position = "kneeling1", display_transform = character_right)
        "[the_person.title] is a bit slower, and stays on her knees. It seems she is still shocked by how far things went."
        $ scene_manager.update_actor(threesome_person, position = "walking_away")
        "[threesome_person.title] leans over and gives [the_person.title] a kiss on the top of her head then turns to head for the door."
        if the_other_person == threesome_person:
            $ town_relationships.update_relationship(the_person, threesome_person, "Friend")
            threesome_person "I guess having you work here will be fun after all."
        else:
            $ town_relationships.update_relationship(the_person, threesome_person, "Best Friend")
            threesome_person "I'm really glad you are working here now, we are going to have so much fun together."
        $ scene_manager.remove_actor(threesome_person)
        if strict_uniform_policy.is_active():
            $ the_person.set_uniform(the_outfit, wear_now = True)
        $ scene_manager.update_actor(the_person, position = "stand2", display_transform = character_right)
        "As [threesome_person.title] leaves the office, [the_person.title] finally makes it back to her feet."
        the_person "I've never had an interview like this before. Is it done? Was that all?"
    else:
        mc.name "Great, you've done wonderful and addressed all my concerns."
        the_person "That's all?"
    mc.name "That is all, do you have any questions?"
    the_person "When can I start?"
    "Well, she certainly has some gumption. Do you want to hire her?"
    $ the_person.clear_situational_obedience("bribe")
    menu:
        "Hire her":
            call hire_someone(the_person) from _call_hire_someone_surprise
            $ the_person.change_stats(happiness = 5, love = 2)
            $ the_person.change_location(the_person.job.job_location)
            mc.name "Right now. Head down the hall to your new department and get started."
        "Not now":
            $ mc.phone.register_number(the_person)
            $ the_person.change_location(the_person.home)
            mc.name "I'm sorry, but this just isn't going to work out right now."
            mc.name "You did very well but we just aren't looking to expand."
            the_person "What!? I let you... and now you're just going to kick me out anyway?"
            mc.name "I'm very sorry, I have your number and will be sure to call if something opens up in the future."
        "Never":
            mc.name "I'm sorry, but this just isn't going to work out."
            mc.name "You came in here lying and I'd never be able to trust you. This was just a way to get revenge for you wasting my time."
            the_person "Oh my god!? I can't believe I let you... I'm gonna go home and boil my skin off in the shower."
            $ scene_manager.remove_actor(the_person)
            $ the_person.remove_person_from_game()
    $ clear_scene()
    $ clean_memory()
    return
