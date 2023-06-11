label lily_offscreen_corruption(the_person, the_other_person):
    if the_person.sluttiness > the_other_person.sluttiness:
        $ x = the_other_person
    else:
        $ x = the_person
    $ influence = 100 + x.suggestibility
    if x.has_role(trance_role):
        $ influence +=10
        if x.has_exact_role(heavy_trance_role):
            $ influence +=10
        elif x.has_exact_role(very_heavy_trance_role):
            $ influence +=20
    $ number = __builtin__.int(influence/20)
    if the_person.sluttiness > the_other_person.sluttiness:
        $ the_other_person.change_stats(happiness = 10, slut = number, max_slut=the_person.sluttiness)
        $ the_person.change_stats(happiness = 10)
    else:
        $ the_person.change_stats(happiness = 10, slut = number, max_slut=the_other_person.sluttiness)
        $ the_other_person.change_stats(happiness = 10)
    $ the_person.event_triggers_dict["friend_with_benefits"] = x.sluttiness
    $ the_other_person.event_triggers_dict["friend_with_benefits"] = x.sluttiness
    if the_person.event_triggers_dict.get("friend_with_benefits", 0) < 50:
        $ corruption_followup = Action("Lily Corruption Followup", lily_followup_requirement, "corruption_followup_label")
        $ mc.business.add_mandatory_crisis(corruption_followup)
    return

label corruption_followup_label():
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ the_person.apply_planned_outfit()
    $ wear_pajamas(the_sister)
    if the_person.sluttiness > the_sister.sluttiness: # lily needs work
        "Some time late in the night, you're awoken by the buzz of your phone getting a text. You roll over and ignore it."
        "A few minutes later it buzzes again, then again. You're forced to wake up and see what is the matter."
        $ mc.phone.add_non_convo_message(the_person, "Hey, are you awake?")
        $ mc.phone.add_non_convo_message(the_person, "I want to ask you about [the_sister.fname]")
        $ mc.phone.add_non_convo_message(the_person, "She is being a bit of a prude")
        "[the_person.title] has been texting you. She's sent you several messages, with the last ending:"
        $ mc.start_text_convo(the_person)
        the_person "Hello? I really need your help"
        mc.name "Sorry, I was sleeping. What's up?"
        the_person "Well, we've been spending a lot of time together, but she just doesn't seem to be interested in taking things to the next level"
        if not the_person.has_taboo("vaginal_sex") or not the_person.has_taboo("anal_sex"):
            the_person "I figured, being related to you, she would have no problem with physical relationships but she is holding back"
        elif not the_person.has_taboo("sucking_cock"):
            the_person "I mean, you and me didn't go too fast, but she is really reluctant to take the next step"
        else:
            the_person "I know you and I didn't really do much, but I was hoping to get a bit more physical with her"
        mc.name "And this is my problem how?"
        the_person "Please I don't know who else to go to with this. I was hoping maybe you could find some way to encourage her more wild side"
        mc.name "Okay, I'll see what I can do. You're gonna owe me one"
        the_person "Oh my god, thank you so much!"
        $ the_person.change_stats(happiness = 10)
        mc.name "Going back to sleep now"
        the_person "Right, sorry"
        the_person "Good night"
        the_person "Sorry"
        $ mc.end_text_convo()
        "You should probably find some time this week to try and corrupt [the_sister.title]. If you slip her a serum on Monday night it wouldn't hurt."
    elif the_sister.sluttiness > the_person.sluttiness: # person needs work
        $ the_sister.draw_person()
        "As you are getting comfortable [the_sister.title] steps into the room and closes the door."
        the_sister "Hey, [the_person.mc_title] do you have a few minutes to talk?"
        mc.name "For you? Always."
        the_sister "It's about [the_person.fname]. We have been having fun lately, a lot of fun, but she seems reluctant to go further."
        mc.name "Well not everyone is as free spirited as we are."
        the_sister "I know, but you have done so much this year to help me open up..."
        if not the_sister.has_taboo("anal_sex"):
            "You reach out and give her ass a squeeze."
            mc.name "In more ways than one."
            "She moans slightly, but playfully swats your hand away."
            the_sister "I'm serious."
        mc.name "You're wondering if I could help her open up too?"
        the_sister "Yes, exactly. If you did I would be happy to repay you. Maybe I could even get [the_person.fname] to help."
        mc.name "For such a noble cause I'd be happy to help."
        the_sister "Great, maybe next time she is here you could talk to her."
        mc.name "Of course, I'll try to swing by with some drinks for you again. Make some excuse to leave the room and we will talk."
        the_sister "Awesome, I'm so excited to be able to spend time with both of you."
        $ the_sister.draw_person(position = "walking_away")
        "With her problem taken care of for the night [the_sister.possessive_title] turns to head back to her room for the night."
        if not the_sister.has_taboo("sucking_cock"):
            menu:
                "Stop her":
                    mc.name "Wait!"
                    $ the_sister.draw_person(position = "back_peek")
                    the_sister "Yeah?"
                    mc.name "Instead of repaying me after I help what if you prepaid me now?"
                    call fuck_person(the_sister, private = True, start_position = blowjob, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = True, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_corruption_visit
                "Let her go":
                    pass
    else: # they need a push
        "It is hard to tell from your room, but it seems like [the_sister.title] and [the_person.title] are taking things slow in their relationship."
        "If you want them to get more physical with one another you are probably going to have to give them a push. Maybe some serums slipped in their drinks Monday evening could get the job done."
    "You roll over and try to get to sleep."
    $ clear_scene()
    return

label lily_overnight_label_not_in_use(): # find another way to hook this up
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ the_sister.draw_person(position = "sitting", emotion = "sad")
    "You are stirred awake as your bed shifts at the weight of someone else climbing on the edge."
    $ the_sister.draw_person()
    "Opening your eyes you are not terribly surprised to see [the_sister.possessive_title] looking at you with a bashful smile."
    the_sister "Sorry to wake you, [the_sister.mc_title], I was having trouble getting to sleep and thought you could help me."
    mc.name "Okay, I don't mind as long as you aren't keeping me up all night."
    if the_sister.arousal_perc < 50:
        the_sister "I hope I don't, but I need some help."
    elif the_sister.arousal_perc < 66:
        the_sister "That's okay, this shouldn't take too long."
    else:
        the_sister "That's okay. This should be quick."
    "[the_sister.title] slips under the covers next to you."
    "You can feel the heat radiating from her body, and she can't seem to settle down, shifting back and forth endlessly."
    "You roll onto your side and put your arm around [the_sister.title], pulling her close so you can spoon."
    if not the_sister.has_taboo("vaginal_sex"):
        "As soon as she is in position she pushes back and starts to grind against you."
        mc.name "Were you looking for more than just cuddling [the_sister.title]?"
        the_sister "Sorry, yes. [the_person.fname] and I were fooling around earlier and she couldn't get me off, even after I took care of her."
        "[the_sister.title] sighs and snuggles closer to you."
        if not the_sister.vagina_visible() or not the_sister.tits_visible():
            mc.name "I don't think I'll be able to help you in all those clothes."
        "[the_sister.title] nods and slips out of your arms. She quickly strips out of everything, including her panties, then slides back into bed."
        $ the_sister.outfit.strip_to_vagina()
        $ the_sister.outfit.strip_to_tits()
        $ the_sister.draw_person()
        the_sister "Is this better?"
        mc.name "Much."
        "You slip an arm around her chest and grab hold of a tit, then grind your hips against her ass a little bit."
        $ the_sister.change_arousal(5)
        "[the_sister.title] just lays next to you and moans softly while you play with her."
        "After a few minutes you slide your pants down and pull your cock out."
        mc.name "You've got me all worked up now too [the_sister.title]. We're going to have to take care of this before I can get to sleep."
        the_sister "I'm sorry. Do whatever you want, It's my fault anyway."
        "You slip your cock between her legs and run the tip along her pussy. [the_sister.title] moans softly, but stays perfectly still for you."
        $ the_sister.change_arousal(5)
        mc.name "That's a good girl, stay just like that until I'm finished."
        "Once you've gotten your tip wet from her juices you slide all the way into your sister."
        "[the_sister.title] gasps the first few times you pump into her, but before long the only noise she's making are soft moans. You pinch her nipple and roll it between your fingers while you fuck her."
        $ the_sister.change_arousal(5)
        "With her legs together [the_sister.title]'s pussy is incredibly tight, and within a few minutes you're ready to finish."
        $ the_sister.change_arousal(5)
        "You pump faster, bumping your hips into her ass each time, then begin to fire your load inside of her."
        if the_sister.has_role(breeder_role):
            the_sister "Oh god, yes! Fill me up!"
            "[the_sister.title] quivers with pleasure, suddenly climaxing at the same time as you."
        else:
            "[the_sister.title] gasps in surprise, but still doesn't move."
        $ the_sister.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = 50, reset_arousal = False, add_to_log = True)
        "You hold yourself tight against her, then give a few final thrusts before pulling out. [the_sister.title] sighs as you slip out of her, going limp against you."
        mc.name "That was great [the_sister.title]. Now we can get to bed."
        if the_sister.has_role(breeder_role) or the_sister.on_birth_control:
            "[the_sister.title] nods and cuddles closer to you. You fall asleep together, your cum dripping slowly out of her pussy."
        else:
            the_sister "We have to be more careful in the future [the_sister.mc_title], that or I need to start taking my birth control again. Eventually you're going to get me pregnant like this..."
            "[the_sister.title] cuddles closer to you. You fall aslep together, your cum dripping slowly out of her pussy."
    elif not the_sister.has_taboo("touching_vagina"):
        the_sister "Oh, hey there."
        mc.name "There isn't much room on the bed, so we're going to have to get nice and close."
        the_sister "You're right. In that case..."
        $ the_sister.draw_person()
        $ the_sister.outfit.strip_to_underwear()
        $ mc.change_locked_clarity(10)
        "[the_sister.title] slips out of your arms and stands up, pulling her pajamas off and leaving them in a pile. When she's down to just her underwear she slips back in and slides against you."
        $ the_sister.draw_person()
        the_sister "I don't want to get too hot, if we're right next to each other."
        if the_sister.tits_visible():
            "She pulls your arm around her again, planting your hand firmly on one of her naked tits. While she's getting comfortable she also rubs her ass up and down against your hard cock."
        else:
            "She pulls your arm around her again, planting your hand firmly on one of her tits. While she's getting comfortable she also rubs her ass up and down against your hard cock."
        $ the_sister.draw_person()
        $ mc.change_locked_clarity(10)
        mc.name "Easy there [the_sister.title], or I'm going to have to repay the favour."
        "You pinch her nipple between a finger and thumb and she gasps."
        $ the_sister.change_arousal(5)
        mc.name "Or maybe that's what you want, right? To be played with?"
        "You slip your other hand down her legs, rubbing the inside of her thighs."
        the_sister "No, I just couldn't sleep and want to be comfortable."
        "[the_sister.title] moans while you play with her tits, then gasps again when you rub a finger between her legs along the length of her pussy."
        $ the_sister.change_arousal(5)
        mc.name "You're already wet, what's really going on?"
        the_sister "Okay... so me and [the_person.fname] were fooling around and well... I couldn't finish."
        mc.name "So you came to me to see if I could help you get off?"
        $ the_sister.outfit.strip_to_underwear()
        "You pull her panties to the side and slip two fingers inside her, causing her to moan and arch her back a little bit."
        $ the_sister.change_arousal(5)
        the_sister "No, I just... ah..."
        mc.name "Don't say a word, I'll take care of you."
        "You knead your sister's breast with one hand while you finger her with the other. She was already wet when you slid your hand down, and now she's completely soaked."
        $ the_sister.change_arousal(5)
        "[the_sister.title] pants and moans, gasping any time your fingers brush against her clit. After a few minutes you feel her thighs start to tighten up around your hand."
        $ the_sister.change_arousal(5)
        mc.name "Are you getting close?"
        "[the_sister.title] whimpers and nods, legs clenching up."
        $ the_sister.change_arousal(5)
        "You finger her faster for a while, then pull out and rub her clit as fast as you can with two fingers."
        $ the_sister.change_arousal(5)
        "[the_sister.title] tenses up, curling into a ball and moaning loudly. Her breathing comes in short gasps for a few moments while you keep playing with her through her orgasm."
        $ the_sister.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = 50, reset_arousal = False, add_to_log = True)
        "Finally you stop and let her recover. She straightens out on the bed again and pushes herself back against you."
        mc.name "Was that good?"
        the_sister "Mmhm. Thank you."
        mc.name "Good. Now let's get to sleep."
        "You hold [the_sister.title] next to you as you both drift off to sleep."
    elif not the_sister.has_taboo("touching_body"):
        the_sister "Hey!"
        mc.name "There isn't much room on the bed [the_sister.title]. If you want to sleep in here we're going to have to be close to each other."
        "[the_sister.title] thinks for a moment, then nods and pulls closer to you. You wrap an arm around her torso, ending up with one hand cupping a boob."
        $ mc.change_locked_clarity(10)
        the_sister "Comfortable?"
        mc.name "Ya, that feels good. Goodnight [the_sister.title]."
        the_sister "Goodnight [the_sister.mc_title]."
        "You both drift off to sleep cuddling with each other."
        $ the_sister.change_stats(happiness = 5, slut = 2)
    else:
        the_sister "Hey!"
        mc.name "There isn't much room on the bed [the_sister.title]. If you want to sleep in here we're going to have to be close to each other."
        the_sister "Sorry, this was a bad idea. I'll just go back to my room."
        $ the_sister.change_stats(slut = 2)
    $ clear_scene()
    return
