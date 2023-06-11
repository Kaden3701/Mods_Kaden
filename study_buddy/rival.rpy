label lily_study_buddy_rival(the_person):
    $ the_bottom = the_person.outfit.get_lower_top_layer()
    $ the_panties = the_person.outfit.get_panties()
    if the_panties:
        if the_panties.is_extension: #two piece item
            $ the_panties = next((x for x in the_person.outfit.get_upper_ordered() if lily.has_extension == the_panties), None)
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
            mc.name "Of course, I've got [lily.fname] trained so well that she doesn't even wear them around the house any more."
            "[the_person.possessive_title] breaks into loud laughter, but when you don't join her she hesitates."
            the_person "Wait, seriously? No you must be joking."
            "You grin at her, but neither confirm or deny."
            the_person "Man, she's lucky I like you or I'd spread that rumor all over school."
            "She drops down to sit on your bed, totatlly unconcerned with her lack of underwear."
        $ the_person.draw_person(position = "sitting")
        "You chat for a bit about her class work and your company. It is fun, but eventually she prepares to head back to your sister."
        "With her [the_panties.display_name] still laying on your desk she hesitates."
        $ the_person.draw_person()
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
        if the_person.arousal_perc >= 20:
            "You take them in your hand and are suprised to feel that they are not only warm but quite wet as well."
            mc.name "Wow, if I didn't know better I would say you were exited about standing here without underwear."
            the_person "I mean, if I'm honest it was pretty exciting. Both sitting here with you and when I got back to [lily.fname]."
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
        elif the_person.arousal_perc >=10:
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
            $ the_person.have_orgasm(the_position = None, the_object = None, half_arousal = True, force_trance = True, trance_chance_modifier = 0, sluttiness_increase_limit = 30, reset_arousal = False, add_to_log = False)
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
        $ top_list = the_person.outfit.get_tit_strip_list(visible_enough = True)
        if top_list:
            while top_list:
                $ clothing = get_random_from_list(top_list)
                $ the_person.draw_animated_removal(clothing)
                $ top_list.remove(clothing)
        if the_bra:
            $ the_person.draw_animated_removal(the_bra)
            $ the_person.change_stats(arousal = 10 * no_underwear)
        the_person "You know, if I keep giving you all of my underwear soon I won't have any to wear."
        mc.name "Would that be so bad? It seems like you are enjoying being without."
        the_person "It has been fun, but there are times when I do need to wear some."
        mc.name "We could probably find another way for you to compensate me for helping you escape my sister."
        the_person "What did you have in mind?"
        mc.name "Well I have some other needs you could take care of while you're here."
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
        the_person "None. I've been going without almost every day."
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
                if the_person.obedience > 160:
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
    elif the_person.event_triggers_dict.get("bedroom_tax", 0) == 5: #she blows you
        mc.name "I'm glad you're here [the_person.title]. Tell me, what do you have for me today?"
        the_person "I'm still not wearing any underwear, but don't worry, I will gladly provide you with some servicing instead."
        "She wastes no time, closing the door and dropping to her knees."
        call fuck_person(the_person, private = True, start_position = blowjob, start_object = mc.location.get_object_with_name("bed"), skip_intro = False, girl_in_charge = False, self_strip = True, hide_leave = False, position_locked = False, report_log = None, affair_ask_after = False, ignore_taboo = False, skip_condom = False) from _call_fuck_person_rival_visit10
        if the_person.has_role(slave_role):
            "[the_person.title] has come a long way over the last few weeks."
            "You have also already taken the opportunity to cement your relationship as her Master by taking her to your dungeon and making her a slave."
            "While you are thinking of it you may want to take advantage of her state to issue some new commands."
        elif the_person.obedience < 160 - 10*the_person.get_opinion_score("being submissive"):
            "[the_person.title] has been willing to follow specific commands, but to really progress you will have to ensure she is obedient and submissive in all situations."
        else:
            "[the_person.title] has come a long way over the last few weeks."
            "She will do basically anything for you and it is time to solidify that relationship by making her your slave."
            if mc.has_dungeon():
                "Fortunately you have just the place to do that."
                mc.name "Follow me [the_person.title], we are going someplace special so I can have an important conversation with you."
                the_person "Yes [the_person.mc_title]."
                "She gets to her feet and quickly adjusts her clothes to ensure she is presentable."
                $ mc.change_location(dungeon)
                "You lead her to the dungeon you recently had built and give her a moment to take in the room."
                if the_person.sluttiness > 60:
                    the_person "Wow, this is quite the room. I wish I had known we could've been having fun down here instead of in your room."
                else:
                    the_person "Wow, this is really something."
            mc.name "I want to talk to you about formalizing the relationship we have been developing."
            mc.name "You have been good about following commands, but I want to know that you always will."
            mc.name "That means from now on I will be your Master and you will be my slave."
            "[the_person.possessive_title] seems to be into the idea of serving you."
            $ the_person.call_dialogue("sex_obedience_accept")
            $ the_person.add_role(slave_role)
            $ the_person.event_triggers_dict["unique_sex_positions"] = slave_unique_sex_positions
            "[the_person.title] is now a willing slave of yours."
        if the_person.has_role(slave_role):
            $ the_person.event_triggers_dict["bedroom_tax"] = 6
            if stay_wet_requirement(the_person):
                call stay_wet_label(the_person) from _call_stay_wet_label_rival
            if collar_slave_requirement(the_person):
                call slave_collar_person_label(the_person) from _call_slave_collar_person_label_rival
            if slave_trim_pubes_requirement(the_person):
                call slave_trim_pubes_label(the_person) from _call_slave_trim_pubes_label_rival
            if wakeup_duty_requirement(the_person):
                call wakeup_duty_label(the_person) from _call_wakeup_duty_label_rival
            if mc.location == dungeon:
                $ mc.change_location(bedroom)
            "Her unique relationship with your sister also means it might be possible to give her some more specific instructions."
            "You could order her to tease [lily.title] more so that she comes to you for help."
            "You could order her to corrupt [lily.title] to make her more willing to give in to your desires."
            "Maybe you could even set their relationship on a new path with one being dominate while the other submits to a Mistress."
            "Or course this would depend not just on what you ahve taught [the_person.title], but what you have already done with [lily.title]."
            "You should consider your options and try to have a plan for next week."
    else:
        if mc.has_dungeon():
            mc.name "Let's go down to the dungeon so that we can have some proper privacy."
            the_person "Of course Master."
            $ mc.change_location(dungeon)

        call fuck_person(the_person) from _call_fuck_person_rival_visit11
        if the_person.has_role(trance_role):
            call check_date_trance(the_person) from _call_check_date_trance_rival2
        $ mc.business.remove_mandatory_crisis(rival_study_time)
        "Now that you have gotten what you needed from [the_person.title] it is time to give her some instruction regarding [lily.fname]."
        menu:
            "Tease [lily.fname]":
                if the_person.event_triggers_dict.get("teasing_lily", False) == 100:
                    mc.name "I've changed my mind about something. I think you should start teasing [lily.fname] more."
                    the_person "Really?"
                    mc.name "Yes, when you upset her it gives me the opportunity to influence her thought patterns. The more malleable she is the better."
                    the_person "Okay."
                $ the_person.event_triggers_dict["teasing_lily"] = 999
                $ rival_study_time = Action("Rival Study Time", lily_followup_requirement, "rival_study_time_label")
                $ mc.business.add_mandatory_crisis(rival_study_time)
            "Corrupt [lily.fname]" if the_person.sluttiness > lily.sluttiness:
                mc.name "I'd like you to work on corrupting [lily.fname]. She is far too pure and I want her to be more like you."
                the_person "Really?"
                mc.name "Yes, discuss sexuality openly and help drive the idea that it is nothing to be ashamed of into her mind."
                mc.name "I want her to be more accepting of things happening around her and eventually to her."
                the_person "Okay."
                $ influence = 100 + lily.suggestibility
                if lily.has_role(trance_role):
                    $ influence +=10
                    if lily.has_exact_role(heavy_trance_role):
                        $ influence +=10
                    elif lily.has_exact_role(very_heavy_trance_role):
                        $ influence +=20
                $ number = __builtin__.int(influence/20)
                $ lily.change_stats(happiness = -5, slut = number, max_slut = the_person.sluttiness)
                $ the_person.change_stats(happiness = 10)
            "Serve [lily.fname]" if lily.sluttiness >= 60:
                call nemesis_transition_label() from _call_nemesis_transition_label_rival
            "Dominate [lily.fname]\n{color=#ff0000}{size=18}Not Written{/color}{/size} (disabled)" if lily.obedience >= 160:
                call nemesis_transition_label_2() from _call_nemesis_transition_label_2_rival
            "Corrupt [lily.fname]\n{color=#ff0000}{size=18}Requires: Sluttiness > [lily.fname]{/color}{/size} (disabled)" if not the_person.sluttiness > lily.sluttiness:
                pass
            "Serve [lily.fname]\n{color=#ff0000}{size=18}Requires: [lily.fname] 60 Sluttiness{/color}{/size} (disabled)" if lily.sluttiness < 60:
                pass
            "Dominate [lily.fname]\n{color=#ff0000}{size=18}Requires: [lily.fname] 160 Obedience{/color}{/size} (disabled)" if lily.obedience < 160:
                pass
        if town_relationships.get_relationship(the_person, lily).type_a != "Nemesis":
            if wakeup_duty_requirement(the_person):
                call wakeup_duty_label(the_person) from _call_wakeup_duty_label_rival2
            "For now, you have accomplished all you can. [the_person.fname] puts herself back together and heads back to continue working with [lily.title]."
        return
    "Perhaps with the proper serums and a few orgasms you could convince her to change her opinions."
    if the_person.has_role(trance_role):
        call check_date_trance(the_person) from _call_check_date_trance_rival
    "For now, you have accomplished all you can. [the_person.fname] puts herself back together and heads back to continue working with [lily.title]."
    return

label rival_study_time_label():
    $ the_person = lily
    $ the_other_person = get_lab_partner()
    $ mc.change_location(bedroom)
    "Laying in your bed, you hear a knock on your door. You hear [the_person.possessive_title] from the other side of the door."
    the_person "Hey [the_person.mc_title], you still up? I was just wondering if I could come in for a bit?"
    mc.name "It's open."
    $ the_person.draw_person(emotion = "sad")
    if not the_person.event_triggers_dict.get("teasing_lily", False):
        "[the_person.title] is standing at your door. She is holding a backpack?"
        the_person "So... do you think I'm stupid?"
        "You are caught a bit off guard by her question and take a moment."
        "As you think she walks over to your bed."
        if the_person.int >6:
            "[the_person.title] is one of the smartest people you know, why would she think that?"
            mc.name "What? No! Why would you ask me that?"
            the_person "I don't know, I was just being insecure I guess."
        elif the_person.int <3:
            "[the_person.title] doesn't exactly have book smarts, but she does have other positive qualities."
            if the_person.personality == bimbo_personality:
                "Your serums have ensured that she will never win prizes for her brains."
            menu:
                "Be honest":
                    mc.name "I would never call you stupid, you are my little airhead bimbo and I love you just the way you are."
                    mc.name "Besides brains aren't everything. There are plenty of things you can use your head for."
                "Lie":
                    mc.name "Of course not. Your head is so clever and skilled the last thing I would call you is stupid."
            if not the_person.has_taboo("sucking_cock"):
                mc.name "The other day you were so good with your head I gave you a tasty treat. Do you think someone stupid would be able to get me off so quickly?"
                the_person "No, I guess not."
            the_person "Sorry, I shouldn't have bothered you with this when you are trying to sleep."
        else:
            "[the_person.title] is fairly average. You'd probably rate her as a [the_person.int] out of 8."
            mc.name "Of course not! You might not be top of the class but you certainly are not stupid."
            the_person "Thanks, I think I just needed to hear it from someone else."
        mc.name "Where is this really coming from?"
        the_person "I was talking with [the_other_person.fname] earlier about our grades and it turns out she is doing much better than I am."
        menu:
            "Help her":
                pass
            "Refuse":
                mc.name "I'm sorry, I'm way too tired to deal with this tonight."
                the_person "Okay... sorry to bug you [the_person.mc_title]."
                $ the_person.draw_person(position = "walking_away")
                "[the_person.possessive_title] walks out of your room, leaving you to sleep."
                $ the_person.change_stats(happiness = -3, obedience = 3, love = -1)
                return
        mc.name "Look, it is no secret that you and [the_other_person.fname] don't get along. Do you even know if she is telling the truth?"
        if the_person.personality == bimbo_personality:
            the_person "Why would she lie?"
        else:
            the_person "Do you think she was lying?"
        mc.name "I don't know, but I can try to find out if you'd like."
    else:
        "[the_person.title] is standing at your door. She is holding her backpack again."
        the_person "So... [the_other_person.fname] was teasing me again today. Did you get a chance to talk to her?"
        "As you think she walks over to your bed."
        menu:
            "Talk to her":
                pass
            "Not tonight":
                mc.name "I'm sorry, I'm way too tired to deal with this tonight."
                the_person "Okay... sorry to bug you [the_person.mc_title]."
                $ the_person.draw_person(position = "walking_away")
                "[the_person.possessive_title] walks out of your room, leaving you to sleep."
                $ the_person.change_stats(happiness = -3, obedience = 3, love = -1)
                return
        mc.name "I did, I told her to stop. I hoped that would be the end of it, but I guess not."
        the_person "I was afraid of that. Do you think there is something I could do?"
        mc.name "Probably not, she seems pretty determined to dislike you."
        mc.name "I've had some success with getting her to listen to me about other things, maybe eventually she will listen to me about this too."
        the_person "Okay, I hope it works."
        mc.name "I'll talk to her again this week and hope that she at least gives you a break."
    $ rival_int_chat = Action("Rival Int Chat", rival_int_chat_requirement, "rival_int_chat_label")
    $ the_other_person.add_unique_on_talk_event(rival_int_chat)
    call rival_study_loop_label(the_person) from _call_rival_study_loop_label
    return

label rival_study_loop_label(the_person):
    $ strip_path = False
    "You sit up and pat the bed. She sits down next to you."
    $ the_person.draw_person(position = "sitting")
    if the_person.personality == bimbo_personality:
        the_person "Wow! Thanks [the_person.mc_title]! I'm so lucky to have you here to help me."
        "With that all of her worries seem to be gone. She spins and goes to leave the room."
        $ the_person.draw_person(position = "walking_away")
        menu:
            "Stop her":
                mc.name "Wait!"
                $ the_person.draw_person(position = "back_peek")
                the_person "Huh?"
                mc.name "Since you are here we could do something fun to help you cheer up."
                the_person "Oh, right! Good idea."
            "Let her go":
                $ the_person.change_stats(happiness = 5, obedience = 5, love = 5)
                "In a moment you are alone again. Ignorance really is bliss for [the_person.possessive_title]."
                return
    else:
        the_person "Thank you [the_person.mc_title]! It is so good having someone who I can depend on to help me."
        mc.name "Of course. In the mean time, do you want to do something to ensure you are as smart as you can be?"
        the_person "What did you have in mind?"
        menu:
            "Give her a serum" if mc.inventory.get_any_serum_count() > 0:
                "You reach over to your backpack."
                mc.name "At my lab we've been developing something to boost cognition, would you like to try one and see if it helps?"
                the_person "Okay, that sounds great."
                call give_serum(the_person) from _call_give_serum_rival_study_time
                if _return:
                    "You hand her the serum. She quickly drinks it, making a sour face from the taste."
                    the_person "How do we know if it works?"
                    mc.name "Let's study for a bit and see how you feel."
                    $ the_person.apply_serum_study()
                else:
                    "After looking at your serums, you decide none of them would be useful."
                    mc.name "Actually, I don't have the right ones with me. Come on let me just help you study instead."
            "Just study":
                mc.name "Get out your text book and we will study a bit to help your grades."
            "Exercise" if mc.energy > 20 and the_person.energy > 20:
                mc.name "I've read a number of studies that find a strong connection between increased physical fitness and blood flow with increased cognition."
                if mc.max_energy > 140:
                    mc.name "I've even had some success myself recently with increasing my ability to keep going longer than I used to."
                the_person "I guess that makes sense, the brain does use a lot of blood."
                mc.name "Exactly, do you want to go get some gym clothes?"
                if the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 50:
                    $ strip_path = True
                    the_person "Actually I've heard some great things about nude yoga but always been too shy to try it in a class."
                    the_person "Would you mind if we tried that?"
                    mc.name "That sounds great, if you'd be comfortable."
                    $ the_person.draw_person(position = "stand3")
                    "[the_person.title] stands up and starts to take some clothing off..."
                    $ the_person.strip_outfit(position = "stand3")
                    $ mc.change_locked_clarity(20)
                    $ the_person.change_slut(2)
                    "You check her out when she finishes. She even strikes a little pose for you."
                    $ the_person.draw_person(position = "back_peek")
                    the_person "There. How do I look?"
                    $ mc.change_locked_clarity(20)
                    mc.name "You look incredible!"
                    "..."
                    the_person "Well... your turn."
                    "You quickly strip down, trying to keep your cock from swelling too much."
                    "She gives you a quick wolf whistle, letting you know you were only mildly successful."
                    the_person "Okay! Let's get started before we get too distracted!"
                elif the_person.outfit.wearing_panties() and the_person.effective_sluttiness("underwear_nudity") > 30:
                    $ strip_path = True
                    the_person "I don't think that's nessesary, I do yoga in my underwear all the time, I'll just strip down quick."
                    mc.name "That sounds good!"
                    if not the_person.outfit.wearing_bra():
                        if the_person.effective_sluttiness("bare_tits") > 40:
                            the_person "The only problem is I'm not wearing a bra right now."
                            mc.name "Fine with me."
                        else:
                            the_person "Sorry, I forgot I'm not wearing a bra right now."
                            mc.name "No problem."
                            the_person "Maybe not for you, but I'm not gonna show you my tits just to exercise."
                            mc.name "I mean, just go get your gym clothes."
                            $ strip_path = False
                    if strip_path:
                        the_person "I figured you wouldn't mind."
                        $ the_person.draw_person(position = "stand3")
                        "[the_person.title] stands up and starts to take some clothing off..."
                        $ the_person.strip_to_underwear(position = "stand3")
                        $ mc.change_locked_clarity(20)
                        "When she finishes, she stands there for a moment, letting you check her out."
                        $ the_person.change_slut(2)
                        the_person "Okay... let's get started before this gets more awkward!"
                if not strip_path:
                    the_person "Sure, be right back."
                    $ the_person.apply_gym_outfit()
                    $ the_person.draw_person(position = "stand3")
                "You and [the_person.possessive_title] spend a half hour working out."
                $ mc.change_energy(-20)
                $ the_person.change_energy(-20)
                if the_person.get_opinion_score("sports") != 0:
                    $ the_person.change_happiness(2*the_person.get_opinion_score("sports"))
                    if the_person.get_opinion_score("sports") > 0:
                        "She gets into the groove quickly, and seems to be having a good time."
                    elif the_person.get_opinion_score("sports") < 0:
                        "She doesn't seem very enthusiastic about the exercise."
                    $ the_person.discover_opinion("sports")
                $ the_person.change_max_energy(5)
                "She seems to be building up her endurance."
                mc.name "Now that we got the blood flowing let's get to work on some studying."
    if not strip_path and (the_person.vagina_visible() or the_person.tits_visible()):
        $ strip_path = True
    mc.name "Here, why don't you sit next to me in the bed here while we study. You'll be more comfortable that way."
    the_person "Okay."
    $ the_person.draw_person(position = "sitting")
    "You pull the covers back. Then you both sit down on the bed with your heads back against the headboard."
    if strip_path:
        "Having [the_person.possessive_title] in your bed next to you, wearing so little, gets you excited, but you try to shake the thought and concentrate on studying... for now anyway."
        $ mc.change_locked_clarity(20)
    "You get into the books and take a look at [the_person.possessive_title]'s current topics. You recognize most of the material from your own time at the university."
    if mc.int > 5:
        "The text books themselves are a newer edition, but you remember where most of the information is located."
        "You quickly mark some places with sticky notes and help [the_person.title] make a quick study guide for the future."
    elif mc.int >2:
        "The text books are a newer version, and it takes you quite a bit of time to figure out where all the information is located."
        $ mc.change_energy(-5)
        "Eventually, you are able to help [the_person.title] put together a study guide for the future."
    else:
        "It's been too long since university. The books are new editions and you barely remember the material. It takes a team effort with [the_person.title] to find it all."
        $ mc.change_energy(-15)
        "After an extended period, you finally help her put together a study guide for the future."
    the_person "Thank you [the_person.mc_title]... You're the best!"
    "She leans over and gives you a big hug, lingering with her body up against yours for several seconds."
    if strip_path:
        "Having [the_person.possessive_title] up against you quickly reminds you of her undressed state. You quickly get an erection from the close physical contact."
        $ mc.change_locked_clarity(10)
    else:
        "Eventually, [the_person.possessive_title] gets up and grabs her stuff."
        the_person "Thank you so much for the help. Good night!"
        $ the_person.draw_person(position = "walking_away")
        "[the_person.title] gets up and leaves your room, closing your door on the way out."
        $ the_person.change_stats(happiness = 3, obedience = 3, love = 3)
        return
    "She slowly sits up again. When you look down, you realize your erection is making an obvious tent in the blankets. There's no way she doesn't notice..."
    if the_person.sluttiness < 30: #Too chaste to do anything about it, but she still likes it.
        the_person "Ahhh, I'm sorry [the_person.mc_title], I didn't mean to get you excited."
        mc.name "It's okay, it happens when you're around sometimes."
        "[the_person.title] stays quiet, but you can see her blushing."
        $ the_person.change_slut(2)
        $ the_person.change_slut(3)
        $ the_person.draw_person(position = "stand2")
        "She gets up and slowly collects her books."
        mc.name "Goodnight."
        the_person "Goodnight."
        $ the_person.draw_person(position = "walking_away")
        $ the_person.change_stats(happiness = 3, obedience = 3, love = 3)
        "[the_person.title] leaves your room, closing your door on the way out."
        return
    else:
        the_person "Ahh... I see you are a little excited there."
        mc.name "Sorry, it happens when you're around sometimes."
        "Slowly, she reaches her hand over to it. She runs her finger around the tip and plays with it a bit."
        the_person "Do you want me to take care of that for you? You were so helpful tonight, I'd be glad to..."
        $ mc.change_locked_clarity(20)
        menu:
            "Ask for handjob" if mc.energy > 50:
                the_person "Okay... I can do that."
                "Her hand goes under the covers and onto your chest. She slowly rubs your body with her hand as it works it's way south."
                "When she gets to your underwear, you lift your hips up a bit as [the_person.title] pulls them down, setting your erection free."
                if the_person.has_taboo("touching_penis"):
                    "[the_person.possessive_title] begins to falter a bit. You can sense her hesitation to touch you."
                    the_person "Are you sure... this is okay? I feel like we are really crossing a line here..."
                    mc.name "It's okay. It feels so good, don't you want to make me feel good?"
                    the_person "Yes... of course I want to... I just..."
                    "You take her hand in yours. She looks at you and bites her lip. You slowly move her hand down until your cock is resting in her palm."
                    the_person "Oh my god... it's so... warm..."
                    "Her hand starts to stroke you."
                    $ the_person.break_taboo("touching_penis")
                    $ mc.change_arousal(15)
                else:
                    "[the_person.possessive_title] reaches down and takes a light hold of your erection."
                    the_person "Oh god... I don't know why, but it always surprises me how warm it is..."
                    "Her hand starts to stroke you."
                    $ mc.change_arousal(15)
                call get_fucked(the_person, start_position = handjob, the_goal = "get mc off", private = True, skip_intro = True, allow_continue = False, ) from _lily_rival_study_time_handjob_01
            "Ask for blowjob" if the_person.sluttiness >= 50 and mc.energy > 50 and not the_person.has_taboo("touching_penis"):
                the_person "Mmm, okay. I'll do that for you [the_person.mc_title]."
                $ the_person.draw_person(position = "kneeling1")
                "[the_person.possessive_title] pulls the covers down and moves down to your legs. You lift her hips up when she pulls at your shorts, setting your erection free."
                if the_person.has_taboo("sucking_cock"):
                    "[the_person.title] takes your cock in her hand and gives it a couple strokes, but you can tell she is hesitating to go any further."
                    the_person "Are you sure... this is okay? I mean... I'm about to put my brother's cock in my mouth!"
                    mc.name "It's okay. It's going to feel so good, don't you want to make me feel good?"
                    the_person "Yeah... I mean... you were very helpful tonight..."
                    "She pauses for several seconds. You start to get worried she is going to back out."
                    the_person "Okay. Just this once, okay?"
                    "You nod your approval. [the_person.possessive_title] lowers her face until you can feel her breath on your aching cock."
                    the_person "Its just a blowjob. Here it goes!"
                    "[the_person.title] opens her mouth and runs her tongue along the tip, tasting your precum. The attention makes your penis twitch with need."
                    $ the_person.break_taboo("sucking_cock")
                    "The moment of truth arrives. [the_person.possessive_title] opens her mouth wide and slowly slides your cock past her lips. Their velvet warmth feels amazing."
                    "[the_person.title] begins to slowly bob her head up and down."
                else:
                    "[the_person.title] takes your cock in her hand and gives it a couple strokes."
                    the_person "Mmm, god it feels so hard. It feels like you really need to get off."
                    mc.name "I know. This is what you do to me [the_person.title]."
                    the_person "Ahh, so this is my fault? I suppose it's only fair that I help you with this problem then."
                    "[the_person.possessive_title] lowers her face until you can feel her breath on your aching cock."
                    "[the_person.title] opens her mouth and runs her tongue along the tip, tasting your precum. The attention makes your penis twitch with need."
                    mc.name "[the_person.title]... please..."
                    the_person "Mmm, I love to hear you beg."
                    "[the_person.possessive_title] opens her mouth wide and slowly slides your cock past her lips. Their velvet warmth feels amazing."
                    "[the_person.title] begins to slowly bob her head up and down."
                call get_fucked(the_person, start_position = cowgirl_blowjob, the_goal = "get mc off", private = True, skip_intro = True, allow_continue = False, ) from _lily_rival_study_time_blowjob_01
            "Ask for quickie" if the_person.sluttiness >= 70 and mc.energy > 50 and the_person.vagina_visible() and not the_person.has_taboo("touching_penis") and not the_person.has_taboo("sucking_cock"):
                if the_person.has_taboo("vaginal_sex"):
                    the_person "Wow... you want me to just... hop on and go for a ride? That's... a little crazy, don't you think?"
                    the_person "I mean, we've never even gone that far before..."
                    mc.name "Sorry, I umm, just said the first thing that popped into my head."
                    "[the_person.possessive_title] smiles at you."
                    the_person "I mean... I didn't say no... I just wasn't expecting you to just say it so nonchalantly. Let's have a quickie."
                    "Her hand is still stroking you through the covers. It feels like she is speeding up some..."
                    the_person "It's not like I've been totally just waiting for you to ask me something like this..."
                    "[the_person.title] pulls back the covers, you lift your hips when she pulls at your shorts, freeing your cock from its confines."
                    $ the_person.draw_person(position = "kneeling1")
                    the_person "God you always look so hard... I bet you really need to get off, don't you?"
                    mc.name "I do. This is what you do to me [the_person.title]."
                    "[the_person.possessive_title] lowers her face to your cock. She opens her mouth and starts to suck on the tip, tasting your precum."
                    "She gives your dick several strokes, but then stops."
                    $ the_person.draw_person(position = "cowgirl")
                    the_person "Okay... let's do it!"
                    "[the_person.title] climbs up on top of you, your cock in her hand."
                    $ the_person.break_taboo("vaginal_sex")
                    $ mc.change_locked_clarity(50)
                else:
                    the_person "Mmm, I was hoping you would say that!"
                    "[the_person.title] pulls down the covers. You lift your hips up when she pulls at your shorts, freeing your cock from its confines."
                    "She gives it a few strokes with her hand."
                    $ the_person.draw_person(position = "cowgirl")
                    the_person "Okay... let's do it!"
                    "[the_person.title] climbs up on top of you, your cock in her hand."
                    $ mc.change_locked_clarity(30)
                if requires_condom(the_person):
                    "[the_person.possessive_title] reaches over to her backpack, she pulls a condom out of her bag."
                    the_person "Better wrap you up, don't want to have any accidents..."
                    "She opens the package, then skillfully slides the condom down your penis."
                    the_person "Mmm, now we're ready!"
                    $ mc.condom = True
                elif the_person.has_breeding_fetish():
                    "She gives your cock a couple strokes."
                    the_person "Mmm... it's so hard. Do you have a good load saved up for me? I can't wait to feel it splash inside me..."
                elif the_person.has_taboo("condomless_sex"):
                    the_person "So... I know we've never really done this before but... do you think we could skip the condom?"
                    mc.name "If that is a risk you're willing to take, I'm okay with that [the_person.title]."
                    the_person "I know it's a little risky... I just... I want to feel you inside me, with no latex sleeve between us..."
                    $ mc.condom = False
                    $ the_person.change_arousal(15)
                    $ mc.change_locked_clarity(50)
                    $ the_person.break_taboo("condomless_sex")
                "[the_person.possessive_title] lifts her hips up slightly, lining you up with her pussy. She slowly lowers herself down, your cock pushing inside of her."
                "It takes a few seconds, but with steady pressure she manages to take you all the way. She takes a few moments to adjust to the feeling, then begins to rock her hips."
                call get_fucked(the_person, start_position = cowgirl, the_goal = "get mc off", private = True, skip_intro = True, allow_continue = False) from _lily_rival_study_time_quickie_01
                $ the_report = _return
                if the_report.get("girl orgasms", 0) > 0:
                    the_person "Wow... that felt so good..."
                    "[the_person.title] takes it easy for a moment, enjoying the afterglow of her orgasm."
                    the_person "You made me cum so hard... I guess I still owe you a favor sometime?"
                elif the_report.get("guy orgasms", 0) > 0:
                    the_person "Mmm, that was hot..."
                    "[the_person.title] is a little slow to get up."
                    the_person "I think I need a little alone time in my room..."
                else:
                    "[the_person.title] seems a little disappointed that you didn't finish."
                    mc.name "I'm sorry, I think I'm just worn out."
                    the_person "That's okay. I'll just have to owe you one another time, okay?"
                "After a minute or so, [the_person.title] gets up."
            "Decline":
                mc.name "I appreciate that, but I'm just too tired tonight."
                "[the_person.title] stays quiet, but you can see her blushing."
                $ the_person.change_slut(2)
                $ the_person.change_slut(2)
        $ the_person.draw_person(position = "stand2")
        "She gets up and slowly collects her books."
        mc.name "Goodnight."
        the_person "Goodnight."
        $ the_person.draw_person(position = "walking_away")
        "[the_person.title] leaves your room, closing your door on the way out."
        $ clear_scene()
    return

label rival_int_chat_label(the_person):
    $ teasing_boost = 0
    $ the_sister = lily
    if not the_person.event_triggers_dict.get("teasing_lily", False):
        "After listening to [the_sister.title] complain about [the_person.title] you take some time to track her down."
        if day%7 == 1:
            mc.name "Yesterday after you left [the_sister.fname] came to me and told me you were making fun of her."
        else:
            mc.name "The other day after you left [the_sister.fname] came to me and told me you were making fun of her."
        the_person "Well yeah, but just a little."
        mc.name "She has been worried about her grades and you aren't helping by making her doubt herself every week."
        if the_person.int > the_sister.int:
            the_person "The truth is I am smarter than her."
            if the_person.int > 6:
                the_person "Honestly, I'm probably one of the smartest people on campus. I just don't rub it in most of their faces."
            elif the_person.int >4:
                the_person "I'm a bit above average, fortunately she really isn't."
            elif the_person.int >2:
                the_person "Seriously, it is nice to find someone who struggles more than me."
            else:
                the_person "It's really not that much of an accomplishment, I've met smarter dogs."
        elif the_sister.int > the_person.int:
            the_person "She belived me? Maybe I am smarter than her."
            mc.name "I'm not sure innocence and intelligence are that strongly connected."
            the_person "Well, more worldly than."
        else:
            the_person "Honestly, we are about the same. I just happen to be getting better grades."
            if the_person.sluttiness > 60 and persistent.show_ntr:
                the_person "Some of the professors can be quite... friendly if you ask them for help."
            elif the_person.sluttiness > 40 and persistent.show_ntr:
                the_person "I've been finding another student to help tutor me for... compensation."
            else:
                the_person "It surprised me a bit too."
        the_person "Is this the part where you play the big brother and tell me to leave her alone?"
    else:
        if day%7 == 1:
            mc.name "Yesterday after you left [the_sister.fname] came to me and told me you were making fun of her again."
        else:
            mc.name "The other day after you left [the_sister.fname] came to me and told me you were making fun of her again."
        the_person "So?"
    menu:
        "Leave [the_sister.fname] alone":
            if not the_person.event_triggers_dict.get("teasing_lily", False):
                mc.name "That's exactly what this is."
                the_person "Well, go ahead. Issue your orders [the_person.mc_title]."
            if the_person.obedience > 180:
                mc.name "Listen here [the_person.title], you are to leave [the_sister.fname] alone from this day forward."
                mc.name "She is your better in every way and you will tell her that every time you see her."
                mc.name "You've been a good girl so far for me, now prove it and be a good girl for [the_sister.fname] too."
                the_person "Mmmm, yes sir."
                $ the_person.change_arousal(20)
                the_person "While you're issing orders... is there anything else I can do for you [the_person.mc_title]?"
                if "action_mod_list" in globals():
                    call screen enhanced_main_choice_display(build_menu_items([build_command_person_actions_menu(the_person)]))
                else:
                    call screen main_choice_display([build_command_person_actions_menu(the_person)])
                if isinstance(_return, Action):
                    $ _return.call_action()
            elif the_person.obedience > 140:
                mc.name "Leave [the_sister.fname] alone. She doesn't deserve your mistreatment"
                mc.name "Be a good girl for me and I'll find some way to reward you."
                the_person "Okay, I'll play nice for you [the_person.mc_title]."
            elif the_person.obedience > 100:
                mc.name "Can you leave [the_sister.fname] alone for me?"
                mc.name "She is still uncertian and I'd really appreciate you not harrasing her."
                if the_person.obedience - (10*(the_person.int - the_sister.int)) + the_person.love > 100:
                    the_person "Okay, I can do that for you."
                else:
                    the_person "Don't think so. Teasing her is just too fun."
                    $ teasing_boost += 20
            else:
                mc.name "[the_person.title] can you please lea-"
                the_person "Fuck no! What is up with your family?"
                if not the_person.event_triggers_dict.get("teasing_lily", False):
                    the_person "I can't believe you thought that would work. You might be even dumber than she is."
                $ teasing_boost +=50
        "Keep it up":
            if not the_person.event_triggers_dict.get("teasing_lily", False):
                mc.name "Fuck no, I think it is hilarious. You should see how far you can push her."
            else:
                mc.name "I just wanted to tell you to keep it up. You are really putting her in her place."
            the_person "God, you're sick. I almost had her in tears last time."
            mc.name "If you can do it be sure to send me a video."
            $ teasing_boost += 100
        "Nothing for now":
            if not the_person.event_triggers_dict.get("teasing_lily", False):
                mc.name "Would it matter if I was?"
            mc.name "I just wanted to check if she was telling the truth."
            the_person "I wouldn't put lying past her, but this time she was being honest."
            the_person "Thanks for the extra ammo by the way, now I'll be able to make fun of her for that too."
            $ teasing_boost += 20
    $ the_person.event_triggers_dict.update({"teasing_lily" : the_person.event_triggers_dict.get("teasing_lily", 100) + teasing_boost})
    if the_person.event_triggers_dict.get("teasing_lily", 0) > the_person.obedience:
        "[the_person.title] is going to continue to tease [the_sister.title]. If you want to stop her you should find a way to make her more obedient."
    else:
        "[the_person.title] has promised to behave. As long as you keep her obedient enough she should do what you want."
    $ del teasing_boost
    $ clear_scene()
    return
