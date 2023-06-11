init 5 python:
    config.label_overrides["bedroom_masturbation"] = "bedroom_masturbation_enhanced"

label bedroom_masturbation_enhanced(location_description = "home", edging_available = True, should_advance_time = True): #Baseline efficency for masturbating. Advances time, consumes energy, and releases Clarity inefficently.
    $ the_item = None
    $ caught = False
    $ the_person = None
    if location_description == "home":
        "Before getting started you take a look at your bedroom door."
        menu:
            "Lock it":
                "You turn the lock to ensure you won't be interrupted."
            "Close it":
                "You ensure the door is closed, although that won't stop everyone."
                if renpy.random.randint(0,5) == 1:
                    $ caught = True
            "Open it":
                "You open the door slightly, hoping someone will walk by."
                if renpy.random.randint(0,1) == 1:
                    $ caught = True
        if mc.get_underwear_list():
            "Deciding you want a bit of help, you reach into a drawer where you are keeping some stolen underwear."
            $ the_item = menu(mc.get_underwear_list())
            $ return_underwear(the_item)
            $ title = clothing_formatted_title(the_item = the_item)
            "You enjoy the feel of the silky material of the [title] on your skin."
        "You sit down in front of your computer and start to look around for some porn to jerk off to."
    if mc.masturbation_novelty >= 95:
        "You have the entire internet's worth of porn at your fingertips, so it's not long before you're stroking your cock to some new porn."
    elif mc.masturbation_novelty >= 75:
        "You browse the internet for something hot to watch. After a few minutes you've found enough to entertain you and start to stroke your cock."
    elif mc.masturbation_novelty >= 60:
        "You browse the internet, but it's getting hard to find good porn you haven't seen before."
        "Soon you're searching one handed as you bounce from site to site, stroking yourself to keep hard until you find that perfect video to finish to."
    else:
        "You browse the internet, but it feels as if you've seen it all before."
        "Nothing new interests you, so you pull up some old favourites and jerk off to those instead."
    if location_description == "home":
        if not people_in_mc_home():
            $ caught = False
        if caught:
            $ the_person = get_random_from_list(people_in_mc_home())
            if the_person.effective_sluttiness() >= 60:
                $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness, guarantee_output = True))
            else:
                $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_outfit(the_person.sluttiness, guarantee_output = True))
            "A few minutes later you're startled by a sound at the door."
            $ willingness_value = the_person.sluttiness + (the_person.obedience - 100)
            $ the_person.draw_person(emotion = "happy")
            the_person "Hey [the_person.mc_title], do you have a USB Cab..."
            "You spin your chair around as the door is opened suddenly. You lock eyes with [the_person.title]. Your dick is still in your hand and some girl is getting pounded on the screen behind you."
            if the_person.effective_sluttiness() > 40:
                if the_person.effective_sluttiness() > 60:
                    mc.name "Hey [the_person.title], what's up?"
                    the_person "Hey, have a moment?"
                    "You keep stroking yourself."
                    mc.name "I'm kind of in the middle of something. Come in."
                    "[the_person.title] steps into your room and closes the door."
                    the_person "I need a USB cable, do you have one lying around?"
                    mc.name "I might. I'm going to need to get off before I have time to look for it though."
                    the_person "Well, I need that cable soon. How about I help you out with that?"
                else:
                    mc.name "Oh, hey [the_person.title]."
                    the_person "Hey, do you have a moment?"
                    "You keep stroking yourself while you look at [the_person.title]."
                    mc.name "Well I'm a little busy. What do you need?"
                    the_person "I need a USB cable. Do you have one lying around?"
                    mc.name "I might, but I'm not sure where I left it."
                    the_person "Could you take a break? I kind of need it quickly."
                    mc.name "I just got settled in though. If I stop now I have to start all over. Just come over here and help me finish."
                    "[the_person.title] steps into the room and closes the door."
                    the_person "Fine, what do you need me to do?"
                $ clear_scene()
                $ willingness_value = the_person.sluttiness + (the_person.obedience - 100) + the_person.get_opinion_score("being submissive") * 10
                $ the_group = GroupDisplayManager(mc.location.people, primary_speaker = the_person)
                $ the_group.draw_group(position = "sitting")
                $ the_group.draw_person(the_person)
                menu:
                    "Make her strip while you jerk off":
                        mc.name "Well, I'd like you to give me some entertainment while I take care of this. Strip down and give me a little dance."
                        "[the_person.title] looks around the empty room, then back to you and shrugs."
                        the_person "Fine."
                        "You smile and turn your chair to face her, stroking your hard cock slowly."
                        $ the_bra = None
                        $ the_panties = None
                        $ taboo = 5
                        if the_person.has_taboo("bare_pussy"):
                            $ taboo -= 1
                            if not the_person.wearing_panties():
                                $ taboo -= 3
                        if the_person.has_taboo("bare_tits"):
                            $ taboo -= 2
                            if not the_person.wearing_bra():
                                $ taboo -= 2
                        if the_person.has_taboo("underwear_nudity"):
                            $ taboo -= 4
                        $ done_stripping = True
                        if taboo > 1: # underwear
                            $ generalised_strip_description(the_person, the_person.outfit.get_underwear_strip_list())
                            if taboo > 3: #topless
                                if taboo > 4: # everything
                                    if not panties: # everything
                                        $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())
                                elif not panties:
                                    $ done_stripping = False
                                if not the_bra: # topless
                                    $ generalised_strip_description(the_person, the_person.outfit.get_tit_strip_list())
                            elif not the_bra:
                                $ done_stripping = False
                        else:
                            $ done_stripping = False
                        if not done_stripping: #she went as far as we asked
                            if taboo < 2:
                                "[the_person.title] shifts on her feet nervously."
                                the_person "Um, I don't think I can do it with you here."
                            elif taboo < 4:
                                "Once she is in her underwear, she hesitates, and looks at you shyly."
                                the_person "I don't think I can go any further with you watching me."
                            else:
                                "Although she stripped off her top with no trouble, she seems to be hesitating with her panties."
                                the_person "I don't think I can take these off with you watching me."
                        else:
                            "When [the_person.possessive_title] is finished stripping down she puts her hands on her hips and watches you jerk off."
                            $ mc.change_locked_clarity(10)
                            $ the_person.discover_opinion("not wearing anything")
                            $ the_person.change_slut_temp(the_person.get_opinion_score("not wearing anything")+1)
                            $ the_person.change_obedience(the_person.get_opinion_score("not wearing anything")+1)
                            if the_person.get_opinion_score("not wearing anything") > 0:
                                "She doesn't seem to care about being naked in front of you; if anything she seems to be enjoying the experience."
                                the_person "Do you have a good view?"
                                $  the_person.draw_person(position = "back_peek")
                                "She gives you a quick spin."
                                $ mc.change_locked_clarity(10)
                                $ the_person.draw_person()
                            elif the_person.get_opinion_score("showing her tits") > 0:
                                if the_person.has_large_tits():
                                    "She puts an arm under her tits and lifts them up for you, leaning forward a little to emphasize their size."
                                    the_person "Do you like my tits? I know a lot of men do, they like to have a big pair of juicy titties in their face."
                                else:
                                    "She rubs her small tits, thumbing the nipples until they grow hard."
                                    the_person "Do you like my tits? I know some women have bigger ones, but I think these are still pretty cute."
                                    the_person "They're just the right size to suck on, don't you think?"
                                $ mc.change_locked_clarity(10)
                            elif the_person.get_opinion_score("showing her ass") > 0:
                                "[the_person.title] turns around unprompted and plants her hands on a desk opposite you."
                                $ the_person.draw_person(position = "standing_doggy")
                                the_person "Do you like my ass, [the_person.mc_title]? Do you want to give it a nice hard smack and make it jiggle?"
                                "She works her hips up and down, making her ass cheeks bounce and clap together."
                                $ mc.change_locked_clarity(10)
                            else:
                                the_person "Come on, I want you to cum so I can get that cable."
                        "You stroke yourself faster, enjoying [the_person.title]'s body on display right in front of you. Finally you feel your orgasm approaching."
                        $ climax_controller = ClimaxController(["Cum!","air"])
                        $ climax_controller.show_climax_menu()
                        if the_item:
                            "You lean back in your chair and grunt as you climax, blowing a hot load of cum into the [title]."
                            "[the_person.title] can't help but glance down as you do."
                            the_person "I see you've got some help there in your hand."
                            if plural_display_name(the_item):
                                mc.name "Umm... yeah, they ended up in my laundry basket and well..."
                                the_person "It's fine, just make sure they get washed again before you return them."
                            else:
                                mc.name "Umm... yeah, it ended up in my laundry basket and well..."
                                the_person "It's fine, just make sure it gets washed again before give it back."
                            mc.name "Of course."
                        else:
                            "You lean back in your chair and grunt as you climax, blowing a hot load of cum in an arc onto the floor in front of you."
                        $ climax_controller.do_clarity_release(the_person)
                        $ the_person.draw_person()
                        the_person "Wow..."
                        "It takes a few moments of deep breathing to recover from the experience."
                        mc.name "Thank you [the_person.title], that's taken care of the problem nicely."
                        "She gives you a quick smile."
                        the_person "Now, where's the cable?"
                        "You get up and pull the USB cable out from a drawer and hand it over."
                        the_person "Thanks, I'll bring it back later."
                        "She ducks out the door while you take a moment to get cleaned up."
                        $ others = None
                        $ the_person.review_outfit()
                        $ clear_scene()
                    "Make her suck you off" if not the_person.has_taboo("sucking_cock"):
                        mc.name "I want you to get under my desk and suck me off."
                        $ willingness_value += the_person.get_opinion_score("giving blowjobs") * 10
                        if willingness_value >= blowjob.slut_requirement:
                            if (the_person.get_opinion_score("public sex") > 0 and mc.location.get_person_count() > 1) or the_person.get_opinion_score("giving blowjobs") > 0:
                                the_person "Okay, if that's what you need."
                                "She gets onto her hands and knees, crawling under your desk and nestling herself between your legs."
                                $ mc.change_locked_clarity(10)
                            else:
                                the_person "Really? I..."
                                mc.name "Come on, I don't have all day. I need to get back to work."
                                "She hesitates, but after a second of thought she sighs and gets onto her hands and knees, crawling under your desk and nestling herself between your legs."
                            $ the_group.draw_person(the_person, position = "blowjob")
                            "You release your hard cock letting it fall onto [the_person.possessive_title]'s face."
                            if the_item:
                                if plural_display_name(the_item):
                                    "The [title] you were using get pressed against her face."
                                    "She pulls them away, inspecting the material."
                                    the_person "I see you had some help even before I got here."
                                    mc.name "Umm... yeah, they ended up in my laundry basket and well..."
                                    the_person "It's fine, just make sure they get washed again before you return them."
                                else:
                                    "The [title] you were using gets pressed against her face."
                                    "She pulls it away, inspecting the material."
                                    the_person "I see you had some help even before I got here."
                                    mc.name "Umm... yeah, it ended up in my laundry basket and well..."
                                    the_person "It's fine, just make sure it gets washed again before you return it."
                                mc.name "Of course."
                            "She places her hands on your thighs and slides your cock into her mouth, licking the tip to get it wet before slipping it further back."
                            $ clear_scene()
                            call fuck_person(the_person, private = False, start_position = blowjob, skip_intro = True, position_locked = True) from _call_fuck_person_bed1
                            $ the_report = _return
                            $ the_person.review_outfit()
                            if the_report.get("guy orgasms", 0) == 0:
                                if the_item:
                                    "Frustrated with her service, you let [the_person.title] out from under your desk and reach down to pick up the [title]."
                                    $ climax_controller = ClimaxController(["Cum!","masturbation"])
                                    $ climax_controller.show_climax_menu()
                                    if plural_display_name(the_item):
                                        "You grunt as you shoot your load efficiently into them."
                                    else:
                                        "You grunt as you shoot your load efficiently into it."
                                else:
                                    "Frustrated with her service, you let [the_person.title] out from under your desk and finish yourself off with your hand."
                                    $ climax_controller = ClimaxController(["Cum!","masturbation"])
                                    $ climax_controller.show_climax_menu()
                                    "You grunt as you shoot your load efficiently into some tissue."
                                $ climax_controller.do_clarity_release()
                            else:
                                "Fully spent, you let [the_person.title] out from under your desk."
                                "She smiles and stands up."
                            the_person "Now, where's the cable?"
                            "You get up and pull the USB cable out from a drawer and hand it over."
                            the_person "Thanks, I'll bring it back later."
                            if the_item:
                                "She bends down and takes the [title] as well."
                                the_person "I guess I can drop this in my laundry too."
                            "She ducks out the door while you take a moment to get cleaned up."
                        else:
                            $ the_person.draw_person(emotion = "angry")
                            the_person "What? Oh my god, I couldn't do that!"
                            $ the_person.change_love(-5)
                            $ the_person.change_happiness(-10)
                            $ the_person.change_obedience(-3)
                            "She stammers for something more to say before settling on storming out of the room instead."
                            $ clear_scene()
                            "Frustrated, her rejection has at least taken your mind off of your erection and you're able to get back to work eventually."
                            $ mc.business.change_team_effectiveness(-10)
                    "Make her fuck you" if not the_person.has_taboo("vaginal_sex"):
                        if the_item:
                            "You drop the [title] to the ground, happy to have something even better to slide into."
                        mc.name "I want you to take some responsibility for this. Come over here so I can fuck you."
                        $ willingness_value += the_person.get_opinion_score("missionary style sex") * 10
                        if willingness_value >= missionary.slut_requirement:
                            $ desk = mc.location.get_object_with_name("desk") #May be None if there's no desk where you are.
                            if desk is not None:
                                "You grab [the_person.possessive_title] by her hips and lift her up, putting her down on your desk and positioning yourself between her legs."
                            else:
                                "You grab [the_person.possessive_title] by her hips and lay her down in front of you, spreading her legs around you."
                            $ mc.change_locked_clarity(10)
                            $ the_person.draw_person(position = "missionary")
                            if the_person.relationship != "Single" and affair_role not in the_person.special_role:
                                $ so_title = SO_relationship_to_title(the_person.relationship)
                                the_person "Wait, I have a [so_title]! I shouldn't let you do this!"
                                "Despite her protest she doesn't try to stand back up or get you out from between her thighs."
                                $ mc.change_locked_clarity(10)
                            else:
                                the_person "Ah!"
                            if the_person.outfit.can_half_off_to_vagina():
                                $ generalised_strip_description(the_person, the_person.outfit.get_half_off_to_vagina_list(), half_off_instead = True, position = "missionary")
                            else:
                                $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list(), position = "missionary")
                            if the_person.vagina_visible():
                                $ mc.change_locked_clarity(20)
                                "You lay your hard cock onto [the_person.title]'s crotch. You rub the shaft against her pussy lips, teasing her with the tip each time."
                                call condom_ask(the_person) from _call_condom_ask_bed
                                if not _return:
                                    "[the_person.title]'s refusal has sucked the wind from your sails. You zip your pants up and let her leave."
                                    if the_item:
                                        "She scoops up the [title] as she gathers her clothes."
                                    "You're still horny, but your heart just isn't in it any more. You sit back down, disappointed and distracted."
                                    $ mc.business.change_team_effectiveness(-10)
                                else:
                                    "You pull back a little and line the tip of your dick up with [the_person.title]'s cunt."
                                    "With one smooth thrust you push yourself inside of her. She arches her head back and moans as you bottom out inside of her."
                                    call fuck_person(the_person, private = False, start_position = missionary, start_object = desk, skip_intro = True, skip_condom = True) from _call_fuck_person_bed2
                                    $ the_report = _return
                                    $ the_person.review_outfit()
                                    if the_report.get("guy orgasms", 0) == 0:
                                        if the_item: #use something she was wearing if you had to strip her earlier
                                            "You still haven't gotten off, so you reach down to pick up the [title] stroking your cock until you cum."
                                            $ climax_controller = ClimaxController(["Cum!","masturbation"])
                                            $ climax_controller.show_climax_menu()
                                            if plural_display_name(the_item):
                                                "You grunt as you shoot your load efficiently into them."
                                            else:
                                                "You grunt as you shoot your load efficiently into it."
                                        else:
                                            "You still haven't gotten off, so you stroke your cock until you cum."
                                            $ climax_controller = ClimaxController(["Cum!","masturbation"])
                                            $ climax_controller.show_climax_menu()
                                            "You grunt and blow your load efficiently into some tissue."
                                        $ climax_controller.do_clarity_release()
                                        "With that finally taken care of, you get yourself cleaned up."
                                    else:
                                        "You get yourself cleaned up."
                                        "When you're done you step back and admire your handiwork. [the_person.title] just pants for awhile, bent over your desk. Finally she stands up."
                                    the_person "Do you have that cable?"
                                    mc.name "Right. Here."
                                    "You grab the USB cable from a drawer and throw it to her. [the_person.title] smiles and heads for the door."
                                    the_person "Thanks, I owe you one."
                            else: #We've been thwarted somehow and can't get to her pussy.
                                "Thwarted by her clothing and unable to dress her down any further, you give up and let her go. The shame of your defeat has killed any chance you have of orgasming or focusing."
                                $ mc.business.change_team_effectiveness(-10)
                        else:
                            $ the_person.draw_person(emotion = "angry")
                            the_person "What? Oh my god, I would never let you do that!"
                            $ the_person.change_love(-5)
                            $ the_person.change_happiness(-10)
                            $ the_person.change_obedience(-3)
                            "She stammers for something more to say before settling on storming out of the room instead."
                            $ clear_scene()
                            "Her rejection has killed your erection."
                            $ mc.business.change_team_effectiveness(-10)
                    "Just leave":
                        $ caught = False
                        "I really just want to finish. Can you leave me alone for a bit?"
                $ clear_scene()
                $ the_group = None
            elif the_person.effective_sluttiness() > 25: #Does nothing, not surprised
                mc.name "Oh, hey."
                the_person "I didn't realize you were busy. Want me to come back later?"
                mc.name "No, it's fine. What's up?"
                "You keep stroking yourself while you look at [the_person.title] in the doorway."
                the_person "I need a USB cable, do you have a spare one hanging around?"
                mc.name "I think so. Come on in, I think it's in my filing cabinet. I'm a little busy though."
                the_person "Don't worry about it, I can grab it myself."
                "[the_person.title] closes the door behind her and walks over to your filing cabinet. You turn back to your monitor as the girl is fucked doggy style."
                the_person "Here it is!"
                "She glances over your shoulder at your monitor too."
                the_person "Wow, nice."
                mc.name "I know, right?"
                if the_item:
                    "She can't help but glance lower as she does so."
                    the_person "I see you've got some help there in your hand."
                    if plural_display_name(the_item):
                        mc.name "Umm... yeah, they ended up in my laundry basket and well..."
                        the_person "It's fine, just make sure they get washed again before you return them."
                    else:
                        mc.name "Umm... yeah, it ended up in my laundry basket and well..."
                        the_person "That's fine, just make sure you wash it again before putting it back."
                    mc.name "Of course."
                the_person "Thanks for the cable, have fun."
                mc.name "No problem. Close the door on your way out."
                "[the_person.title] does so, and you continue."
                $ the_person.change_slut_temp(5)
                $ the_person.change_obedience(3)
                $ caught = False
            else: #Is startled
                mc.name "Hey, ah!"
                the_person "Oh shit!"
                "[the_person.title] turns around and pulls the door shut. It slams closed suddenly."
                mc.name "Crap, sorry [the_person.title]!"
                "She talks through the door, her voice muffled."
                the_person "Ugh, some things you can't unsee!"
                mc.name "Well you should have knocked then!"
                the_person "Can't you remember to lock your door or something when you're... having some me time?"
                if the_item:
                    "Having lost all interest in jerking off, you close everything down and wipe your hand off, tossing the [title] in your hamper."
                else:
                    "Having lost all interest in jerking off, you close everything down and wipe your hand off."
                mc.name "I forgot, alright? Just, knock next time."
                the_person "Hopefully there won't be a next time. Now do you have a USB cable?"
                "You rummage around your desk for a while before finding the cable. You open the door a crack and slide it out."
                mc.name "Here."
                the_person "Thanks. Have fun I guess."
                "She heads off to use the USB cable. Your heart is still beating fast, and you definitely don't feel like finishing up now."
                $ the_person.change_slut_temp(5)
                $ the_person.change_happiness(-10)
    if not caught:
        menu:
            "Jerk off and cum":
                "You enjoy stroking yourself off for a long while."
                $ mc.change_locked_clarity(10)
                "Eventually you can feel the edge of your orgasm and push yourself towards it."
                $ climax_controller = ClimaxController(["Cum!", "masturbation"])
                $ climax_controller.show_climax_menu()
                $ climax_controller.do_clarity_release()
                if the_item:
                    "You shift the [title] as you start to cum, smothering your tip to avoid making a mess."
                    "You take a few deep breaths as your climax passes, then wad up the underwear and chuck it into your laundry basket."
                else:
                    "You grab desperately at some tissue as you start to cum, smothering your tip to avoid making a mess."
                    "You take a few deep breaths as your climax passes, then wad up the spent tissues and chuck them into the trash."
            "Try and edge yourself" if edging_available:
                "You enjoy stroking yourself off for a long while."
                $ mc.change_locked_clarity(10)
                if renpy.random.randint(0,100) < 15*mc.focus + 10:
                    # You manage to avoid climaxing
                    "For a long while you edge yourself, pushing yourself to the edge of your orgasm and then slowing down."
                    $ mc.change_locked_clarity(10)
                    "It takes focus and willpower, but you're able to avoid making yourself cum. You feel like a dam ready to burst now."
                    "You put your cock away, excited about the release you'll experience next time you climax."
                else:
                    "For a long while you edge yourself, pushing yourself right to the edge of your climax before slowing down."
                    "It only takes a momentary lapse of willpower for it all to fall apart. An unexpectedly jiggly set of internet tits and you're suddenly past the point of no return."
                    $ climax_controller = ClimaxController(["Cum!", "masturbation"])
                    $ climax_controller.show_climax_menu()
                    if the_item:
                        "You shift the [title] as you start to cum, smothering your tip to avoid making a mess."
                        "You take a few deep breaths as your climax passes, then wad up the underwear and chuck it into your laundry basket."
                    else:
                        "You grab desperately at some tissue as you start to cum, smothering your tip to avoid making a mess."
                        "You take a few deep breaths as your climax passes, then wad up the spent tissues and chuck them into the trash."
                    $ climax_controller.do_clarity_release()
    if should_advance_time:
        call advance_time() from _call_advance_time_bedroom_masturbation_enhanced
    return
