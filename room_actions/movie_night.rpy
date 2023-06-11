init 5 python:
    def home_movie_invite_requirement():
        if mc_at_home():
            if home_movie_requirement():
                return True

    def home_movie_requirement():
        if day > 20 and aunt.event_triggers_dict.get("moving_apartment", 0) == -1:
            if time_of_day == 4:
                return True
            return "Only at night"
        return False

    home_movie_invite = ActionMod("Home Movie Invite", home_movie_invite_requirement, "home_movie_invite_label",
        menu_tooltip = "Get invited to watch a movie in your house.", category = "Home", is_crisis = True, is_morning_crisis = False, priority = 5)

    home_movie_action = ActionMod("Watch a movie", home_movie_requirement, "home_movie_label", menu_tooltip = "Watch a movie with your family.", category="Home")

label home_movie_invite_label():
    $ the_person = mom
    $ the_other_person = lily
    $ scene_manager = Scene()
    $ scene_manager.add_actor(the_person, position = "sitting")
    $ scene_manager.add_actor(the_other_person, position = "sitting", display_transform = character_left_flipped)
    "As you are clearing your dishes from dinner [the_person.possessive_title] turns to look at you."
    if mc.business.event_triggers_dict.get("home_movie_start", False):
        the_person "[the_person.mc_title] now that we have our living room back I was wondering if you wanted to watch a movie with me. You know, like we used to last year."
    else:
        the_person "[the_person.mc_title] I was wondering if you wanted to watch a movie with me tonight."
    menu:
        "Yes":
            pass
        "Not tonight":
            mc.name "Sorry, I've got some stuff to do tonight. Maybe another time."
            the_person "Right, sure. Just let me know if you want to watch one some other night."
            $ the_person.change_stats(love = -5, happiness = - 5)
            if mc.business.event_triggers_dict.get("home_movie_start", False):
                "You can now try to watch movies with your family by visiting the hall at night."
                $ mc.business.event_triggers_dict["home_movie_start"] = True
                $ hall.add_action(home_movie_action)
            $ clear_scene()
            return
    mc.name "That sounds great."
    the_person "What about you [the_other_person.fname]?"
    if mc.business.event_triggers_dict.get("home_movie_start", False):
        the_other_person "Sorry, I can't tonight. Maybe another time."
    else:
        menu:
            "Get [the_other_person.title] to join":
                mc.name "Yeah, [the_other_person.title], it would be great if you could watch with us."
                the_other_person "Sure, that sounds fun! Let me just straighten up my room a bit and I'll be right back."
                the_person "I'll be there too as soon as I finish cleaning up."
                $ clear_scene()
                $ mc.change_location(hall)
                call movie_group(the_person, the_other_person) from _call_movie_group_invite
                return
            "Suggest [the_other_person.title] leaves":
                mc.name "I think she was saying something about having plans tonight."
                the_other_person "Yeah, I was going to meet some friends if that is okay?"
                the_person "Of course, have fun."
                the_other_person "You too."
    the_person "Okay, Guess it's just me and my boy then."
    mc.name "I'll go look for something to watch while you finish up."
    the_person "Great, be there soon."
    $ clear_scene()
    $ mc.change_location(hall)
    "You scroll through movies and find something fairly generic to watch by the time [the_person.title] joins you."
    $ scene_manager.add_actor(the_person, position = "sitting")
    call movie_solo(the_person) from _call_movie_solo_invite
    if mc.business.event_triggers_dict.get("home_movie_start", False):
        $ mc.business.event_triggers_dict["home_movie_start"] = True
        $ hall.add_action(home_movie_action)
    call advance_time() from _call_advance_time_family_movie_invite
    return

label home_movie_label():
    # TODO add ability to invite any two people from our home/mansion
    $ the_person = mom
    $ the_other_person = lily
    $ scene_manager = Scene()
    $ mc.change_location(the_person.location)
    $ scene_manager.add_actor(the_person, position = "sitting", emotion = "happy")
    "You make your way to [the_person.title]'s room to see if they are busy."
    mc.name "Hello [the_person.title], do you want to watch a movie with me tonight?"
    the_person "Of course, just the two of us?"
    menu:
        "See if someone else wants to join you":
            # TODO add ability to invite any two people from our home/mansion
            mc.name "Actually I was going to see if [the_other_person.fname] would join us too."
            the_person "Oh that sounds good. Why don't you go check and I'll meet you in the living room."
            $ scene_manager.clear_scene()
            $ mc.change_location(the_other_person.location)
            "You make your way down the hall and knock on [the_other_person.possessive_title]'s bedroom door."
            the_other_person "It's open!"
            $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting", emotion = "happy")
            the_other_person "What's up [the_other_person.mc_title]?"
            mc.name "[the_person.fname] and I are about to watch a movie. Do you want to join us?"
            the_other_person "Sure, I guess I'm not doing anything else."
            "She sighs."
            the_other_person "How sad is that? The most exciting thing I have to do is watch a movie with you and [the_person.fname]?"
            mc.name "I'm sure we can figure out how to make it more exciting."
            the_other_person "Alright, let me finish up here and I'll be there soon."
            call movie_group(the_person, the_other_person) from _call_movie_group_action
        "Not tonight":
            mc.name "Yeah, I've been meaning to spend more time with you one on one."
            the_person "Great, I'm ready now if you are."
            $ mc.change_location(hall)
            $ scene_manager.add_actor(the_person, position = "sitting")
            "The two of you make your way down the hall and settle onto the couch."
            "After a quick search you settle on something you are both happy to watch."
            call movie_solo(the_person, the_other_person) from _call_movie_solo_action
    call advance_time() from _call_advance_time_family_movie
    $ scene_manager.clear_scene()
    return

label movie_solo(the_person):
    $ mc.change_location(hall)
    $ the_person.draw_person(position = "sitting", emotion = "happy")
    "About an hour later, [the_person.title] pauses the movie."
    the_person "[the_person.mc_title], there is a bottle of wine above the fridge. Would you mind grabbing me a glass? Feel free to take some for yourself too."
    mc.name "Sure, no problem. Back in a moment."
    "You find the bottle of wine in the kitchen and grab a glass for both of you."
    if mc.inventory.get_any_serum_count() > 0:
        menu:
            "Add serum to [the_person.title]'s drink":
                call give_serum(the_person) from _call_give_serum_movie_solo
                if _return:
                    "You mix some serum into [the_person.title]'s wine and stir it around quickly."
                    the_person "Finding it alright?"
                    mc.name "Ya, no problem, on my way back already."
                    "You return with a glass of wine in each hand and give one to [the_person.title]. She takes it and resumes the movie."
                    the_person "Perfect. Just what I needed."
                    "[the_person.title] takes the drink from you as you sit down and takes a deep drink."
                    the_person "Aaaaah."
                    "She leans back and sinks deep into the couch, staring at the paused movie on the TV."
                    mc.name "You should finish up your wine, I'm sure you'll feel even better after."
                    "[the_person.title] nods and drinks the rest of the wine. She's taken a full dose now."
                else:
                    "You return with a glass of wine in each hand and give one to [the_person.title]. She takes it and resumes the movie."
                    the_person "Perfect. Just what I needed."
                    "[the_person.title] takes the drink from you as you sit down and takes a deep drink."
                    the_person "Aaaaah."
                    "She leans back and sinks deep into the couch, staring at the paused movie on the TV."
            "Leave [the_person.title]'s drink alone":
                "You return with a glass of wine in each hand and give one to [the_person.title]. She takes it and resumes the movie."
                the_person "Perfect. Just what I needed."
                "[the_person.title] takes the drink from you as you sit down and takes a deep drink."
                the_person "Aaaaah."
                "She leans back and sinks deep into the couch, staring at the paused movie on the TV."
    mc.name "How are you feeling? Has the wine relaxed you?"
    the_person "Mmhm. Very relaxed. It's been a great evening."
    menu:
            "Just watch the movie":
                "You continue to watch the movie, just enjoying spending time with [the_person.possessive_title]."
                $ the_person.change_stats(happiness = 5, love = 5)
                "As midnight rolls around you've both finished your wine and decide to head to bed."
            "Have her take off her shirt" if not the_person.tits_visible():
                mc.name "Good. You deserve a nice relaxing evening. There's something that's definitely not helping you though."
                the_person "Oh? What's that?"
                if the_person.outfit.wearing_bra():
                    mc.name "You're still wearing a bra. Surely you don't need one when you're just watching a movie around the house. It must get so restrictive after an entire day."
                else:
                    mc.name "You're still wearing a shirt. Surely you don't need one when you're just watching a movie around the house. It must get so restrictive after an entire day."
                if the_person.suggestibility > 20 or the_person.has_role(trance_role):
                    "[the_person.title] nods slowly."
                    the_person "It does get annoying sometimes."
                    mc.name "Why don't you just take it off then? You're at home and we're all family, right?"
                    the_person "That does make sense..."
                elif not the_person.has_taboo("bare_tits") or the_person.effective_sluttiness("bare_tits") > 30:
                    "[the_person.title] nods."
                    the_person "It does get annoying sometimes."
                    mc.name "Why don't you just take it off then? You're at home and we're all family, right?"
                    the_person "You're right, and it's not like it is anything you haven't seen before."
                    mc.name "Exactly."
                else:
                    the_person "What?"
                    mc.name "Your top, you should take it off so you can be more comfortable."
                    the_person "That's what I heard, but I couldn't believe my ears."
                    the_person "Maybe this was a bad idea, I think I'm gonna just go to bed."
                    $ the_person.change_stats(happiness = -5, love = -5)
                    return
                if the_person.outfit.wearing_bra():
                    while len(the_person.outfit.get_upper_ordered()) > 1:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    "As she stands there her breasts strain against her bra."
                    the_person "Could you help me with this?"
                    "[the_person.title] turns around, presenting the back of her bra to you."
                    $ mc.change_arousal(10)
                    mc.name "My pleasure."
                    "You unhook the back and [the_person.title] shrugs it forward. She turns around as she pulls the bra off her arms."
                    $ the_person.outfit.remove(the_person.outfit.get_bra())
                else:
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                $ the_person.draw_person(position = "sitting")
                $ the_person.update_outfit_taboos()
                $ mc.change_arousal(10)
                the_person "There we go, that is much better."
                if _return:
                    "She sighs and leans back on the couch. The serum must be doing its work, she doesn't seem the least bit self conscious as you look at her chest."
                else:
                    "She sighs and leans back on the couch. She doesn't seem the least bit self conscious as you look at her chest."
                the_person "Should we start the movie again?"
                mc.name "Oh, right. The movie."
                if _return:
                    "You pick up the remote and turn the movie on again. You don't know how long the serum will last, but you can't stop yourself from staring at [the_person.title]'s tits."
                else:
                    "You pick up the remote and turn the movie on again. You can't stop yourself from staring at [the_person.title]'s tits."
                "Finally you bring yourself to speak up."
                mc.name "It's getting a little chilly, you may want to put your shirt back on [the_person.title]."
                the_person "Chilly? I didn't notice anything."
                $ the_person.apply_planned_outfit()
                if the_person.outfit.wearing_bra():
                    $ the_person.outfit.remove(the_person.outfit.get_bra())
                    "She reaches for her top anyway and puts it on. Her bra is still on the floor, and now her nipples show clearly."
                else:
                    "She moves for her top anyway and puts it on, and now her nipples show clearly through it."
                $ the_person.draw_person(position = "sitting")
                mc.name "Just a little chilly. Anyway, we should finish the movie."
                "You and [the_person.title] enjoy the rest of the movie. She gives you a kiss goodnight, and you both head to bed."
            "Have her get naked" if not the_person.has_taboo("bare_tits") and not (the_person.tits_visible() or the_person.vagina_visible()):
                mc.name "Good. You deserve a nice relaxing evening. There's definitely more you could do to relax though."
                the_person "Oh? What's that?"
                mc.name "You're still wearing clothes. Everyone knows those are way too restrictive to completely relax in. You should take them off for a while. We're at home after all."
                if the_person.suggestibility > 30 or the_person.has_role(trance_role) or the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 30:
                    "[the_person.title] nods slowly."
                    the_person "That makes sense, and this is supposed to be my time for relaxing."
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    while len(the_person.outfit.get_lower_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_lower_top_layer())
                    $ the_person.update_outfit_taboos()
                    the_person "That does feel nice, doesn't it."
                    $ the_person.draw_person(position = "sitting")
                    "You watch her tits jiggle as she sits back down on the couch."
                    if _return:
                        "You aren't sure how long the serum will last, but you enjoy a few minutes watching [the_person.title] laugh and move around completely naked."
                    else:
                        "You don't want to push your luck too much, but you enjoy a few minutes watching [the_person.title] laugh and move around completely naked."
                    mc.name "It's getting a little chilly in here, you may want to put your clothes back on. Wouldn't want to catch a cold."
                    the_person "Of course not, that would be terrible."
                    $ the_person.apply_planned_outfit()
                    if the_person.outfit.wearing_bra():
                        $ the_person.outfit.remove(the_person.outfit.get_bra())
                        "She slips her clothes back on. Her bra is left hanging over the back of the couch."
                    else:
                        "She slips her clothes back on."
                    $ the_person.draw_person(position = "sitting")
                    "You and [the_person.title] enjoy the rest of the movie. She gives you a kiss goodnight, and you both head to bed."
                else:
                    the_person "Watch the movie naked?"
                    mc.name "Think of it as being your most relaxed."
                    the_person "I don't know..."
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    the_person "I don't think I could be comfortable like that."
                    mc.name "I'm sure you will be. Don't worry about it at all."
                    $ the_person.draw_person(position = "sitting")
                    "[the_person.title] hesitates, then sits back on the couch."
                    the_person "No, I think this is good enough for me. A freer top is all I want."
                    if _return:
                        "She must be resisting the serum. No point pressing the issue farther then."
                    else:
                        "It looks like she isn't ready for that yet."
                    $ temp_item = the_person.outfit.get_lower_top_layer()
                    if temp_item:
                        "You and [the_person.title] enjoy the rest of the movie, though you keep stealing glances at her tits. You wish you could have gotten her out of her [temp_item.display_name]."
                    else:
                        "You and [the_person.title] enjoy the rest of the movie, though you keep stealing glances at her tits."
                    $ del temp_item
                    $ the_person.apply_planned_outfit()
                    "Eventually the movie ends, and [the_person.title] fixes her clothing. She gives you a goodnight kiss, and the two of you both head to bed."
            "Have her give you a handjob" if not the_person.has_taboo("bare_pussy") and not the_person.has_taboo("bare_tits"):
                mc.name "That's good. It's nice that you're able to relax so completely."
                the_person "Are you not able to relax?"
                mc.name "No, I've been having some trouble relaxing recently. I've been horny a lot, and there's no way to take care of it right now, unless you'd be willing to give me a handjob."
                if the_person.effective_sluttiness("touching_penis") > 50 or not the_person.has_taboo("touching_penis"):
                    the_person "A handjob? Here on the couch?"
                    mc.name "Sure, while we watch the movie. It'll help me relax so we can both enjoy the evening."
                    "[the_person.title] hesitates, then slides closer to you on the couch."
                    the_person "Okay, if it'll help you relax."
                    "You slide your pants down a little and pop your cock out, then resume the movie."
                    if the_person.has_taboo("touching_penis"):
                        $ the_person.call_dialogue("touching_penis_taboo_break")
                        $ the_person.break_taboo("touching_penis")
                    "[the_person.title] reaches out with her right hand and grips you by the shaft gently, then slides it up and down slowly."
                    the_person "Like this?"
                    mc.name "Perfect. Now we can just relax."
                    $ mc.change_arousal(10)
                    "You lean back on the couch and sigh as [the_person.title] gives you a slow handjob."
                    "A few minutes later the movie takes a sudden turn in tone, and you and [the_person.title] are watching the main characters make out in a closet while their friends prepare a surprise party."
                    $ mc.change_arousal(10)
                    "Neither of you say anything, but [the_person.title] starts moving her hand faster along your shaft."
                    "The main characters are getting more heated, the woman grabs her shirt and rips it open. Buttons fly past the camera."
                    $ mc.change_arousal(10)
                    "[the_person.title] speeds up even more, eyes locked on the TV."
                    "The busty blonde lead reaches down for the main character's crotch while he kisses her between her breasts."
                    "The scene and [the_person.possessive_title]'s excitement is getting you close. You're almost ready to cum."
                    while mc.arousal < 90:
                        $ mc.change_arousal(10)
                    mc.name "I'm almost there [the_person.title]."
                    "[the_person.title] doesn't look away from the TV, but reaches over her other hand and takes your full length in both her hands. She slides them up and down quickly, getting you slippery with your own precum."
                    $ mc.change_arousal(10)
                    $ ClimaxController.manual_clarity_release(climax_type = "body", the_person = the_person)
                    $ the_person.cum_on_stomach()
                    $ the_person.draw_person(position = "sitting")
                    "You tense and sigh loudly as you begin cumming. The blonde has her bra lifted up, but is pointed away from the camera, and the man slips his pants down."
                    "Your cum gushes out and down, running over [the_person.title]'s hands as she continues to stroke you. In the movie, the door to the closet is thrown open as a bunch of party guests yell \"Surprise!\""
                    "[the_person.title] slows her stroking down and finally releases you. The back of her hands have thick lines of cum running down them, and the insides look wet and slippery."
                    mc.name "There we go, that was great."
                    the_person "Feeling more relaxed now?"
                    mc.name "Definitely, I feel like I'm ready for bed right now."
                    the_person "Well the movie's almost over, let's watch the end and then call it a night."
                    "You and [the_person.title] sit on the couch for the last fifteen minutes of the movie. [the_person.title] keeps her hands folded carefully in her lap, still covered in your seed."
                    "Finally the credits roll. [the_person.title] gives you a goodnight kiss and you both head off to bed.."
                else:
                    "[the_person.title] hesitates, then reaches a hand out for your crotch."
                    the_person "You haven't been able to masturbate?"
                    if the_person == mom:
                        mc.name "No, I've been thinking about you and [lily.fname], and my own hand just isn't good enough any more."
                        "[the_person.title] brushes against your crotch, and you flex your cock in response."
                        the_person "Thinking about [lily.fname]? She's your sister though."
                        mc.name "I know, but I just can't help it. She's so sexy, I have to hold myself back all the time."
                        "[the_person.title]'s hand withdraws from your waist."
                        the_person "You can't be thinking about your sister like that though. Or me for that matter, we're family!"
                    else:
                        "[the_person.title] brushes against your crotch, and you flex your cock in response."
                        mc.name "No, I've been thinking about you, and my own hand just isn't good enough any more."
                        "[the_person.title]'s hand withdraws from your waist."
                        the_person "You can't be thinking about me like that though."
                    mc.name "But what if I can't get off any other way?"
                    the_person "I'm sure there's plenty of porn out there. Just keep it to yourself in your room and we won't bother you."
                    if _return:
                        "She's crossed her hands in her lap and is staring straight at the TV now. She must have resisted the serum."
                    else:
                        "She's crossed her hands in her lap and is staring straight at the TV now. She clearly is not in a suggestible state."
                    mc.name "Alright [the_person.title], I'll stop then. Let's get back to watching the movie."
                    "Damn, you're certain you could have made more progress, but you must have pushed her too far all at once."
                    "The movie ends and you and [the_person.title] say goodnight to each other."
            "Have her give you a blowjob" if not the_person.has_taboo("touching_penis"):
                mc.name "That's good. I know something that would help me relax a huge amount as well."
                the_person "Oh? What's that?"
                mc.name "Well I've always enjoyed blowjobs, but I've never had the chance to get one while sitting back and watching a movie. I imagine it would relax me for the entire week."
                if the_person.effective_sluttiness("sucking_cock") > 50 or not the_person.has_taboo("sucking_cock") or the_person.has_role(heavy_trance_role):
                    the_person "I could do that for you then."
                    $ mc.change_arousal(10)
                    $ the_person.draw_person(position = "kneeling1")
                    "[the_person.title] slides off the couch to her knees and pivots to end up between your legs."
                    mc.name "Thanks [the_person.title], that would be great."
                    "[the_person.title] reaches up to your waist and pulls your pants and underwear down to your thighs. Your hard cock stands ready, flexing slightly."
                    the_person "Oh wow, you do need this don't you [the_person.mc_title]."
                    $ the_person.draw_person(position = "blowjob")
                    "She reaches up and takes hold of your shaft. Her soft hand slides up and down slowly."
                    $ mc.change_arousal(10)
                    mc.name "Ya, I really needed this."
                    the_person "Just sit back and relax then."
                    "[the_person.title] grabs the remote and resumes the movie for you to watch over her head."
                    if the_person.has_taboo("sucking_cock"):
                        $ the_person.call_dialogue("sucking_cock_taboo_break")
                        $ the_person.break_taboo("sucking_cock")
                    "She gives you a gentle handjob for a minute, then leans forward and runs her tongue over the bottom of your cock."
                    $ mc.change_arousal(10)
                    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                    "She licks your shaft repeatedly along all of its sides, then finally leans it forward slightly and places the tip between her lips."
                    "[the_person.title] slides her head forward slowly, lips gliding on your wet skin until you feel your tip touch the back of her throat. Her tongue works skillfully inside her mouth."
                    "Her head bobs up and down for a few minutes, and you enjoy watching both her and the movie."
                    "She slides her head off of you, giving the tip one last kiss."
                    $ mc.change_arousal(10)
                    the_person "Enjoying yourself?"
                    mc.name "Oh ya. Your throat feels great."
                    the_person "Let me know when you're going to finish, okay?"
                    mc.name "Sure thing."
                    "With that, she returns your cock to her throat and slides you back and forth more quickly."
                    "A few more minutes of [the_person.possessive_title] pleasuring you and you feel your orgasm building up."
                    $ mc.change_arousal(10)
                    menu:
                        "Hold her down on your cock while you cum":
                            mc.name "I'm going to cum [the_person.title], get ready!"
                            "You reach your hands forward and put them around the back of her head. She tries to slide back, but you hold her in place."
                            "She tries to mumble something past your cock, but you can't hear what it is."
                            mc.name "Almost there, keep going!"
                            "[the_person.title] pauses for a moment, and you can hear her breathing through her nose, then she moves her head back and forth quickly on your cock."
                            "A few seconds of her blowing you and you tense as your orgasm comes."
                            "You move your hands and hold her deep on your cock while you spasm and pump your cum into her throat. She places her hands on your thighs and tries gently to pull back, but you don't let her."
                            $ ClimaxController.manual_clarity_release(climax_type = "mouth", the_person = the_person)
                            $ the_person.cum_in_mouth()
                            $ the_person.draw_person(position = "blowjob")
                            "Finally you finish and let your hands fall to your side. [the_person.title] slides you out of her throat right away and breathes deeply."
                            "She stays on the floor for a few moments panting heavily."
                            mc.name "You okay [the_person.title]?"
                            "[the_person.title] looks up and nods."
                            if the_person.has_cum_fetish():
                                the_person "Yes, I'm fine. You just tasted so good, I wanted to take a moment to savor it."
                            else:
                                the_person "Yes, I'm fine. I didn't realize you needed that so badly. I would have offered earlier if I knew."
                            $ the_person.draw_person(position = "sitting")
                            "She sits back down on the couch and leans close to you."
                            mc.name "Well thank you, that helped a lot."
                            the_person "Any time. How about we finish the movie now."
                            mc.name "Sure."
                        "Let her know you're about to cum":
                            mc.name "I'm going to cum [the_person.title]!"
                            "[the_person.title] throats you as quickly as she can for a few seconds, making soft slurping noises with her mouth."
                            "As you begin tensing up she slides back a little bit and smiles at you."
                            the_person "Okay [the_person.mc_title], let it go when you're ready."
                            "Her head is tilted up to you, to give you a perfect platform for you to unload on."
                            $ ClimaxController.manual_clarity_release(climax_type = "face", the_person = the_person)
                            $ the_person.cum_on_face()
                            $ the_person.draw_person(position = "blowjob")
                            "You grab your cock and stroke yourself to completion. Your cock pulses out some thick streams of cum onto [the_person.possessive_title]'s waiting face."
                            "As you finish you drop your tip onto her chin, smearing the last few drops onto her."
                            if the_person.has_cum_fetish():
                                the_person "Is that everything [the_person.mc_title]? You were really storing it up for me, weren't you."
                                mc.name "Yeah, I know how much you like it when I cum on you."
                                the_person "Aww, thank you."
                            else:
                                the_person "All finished there?"
                                mc.name "Oh ya. All done."
                                the_person "Good."
                            $ the_person.draw_person(position = "sitting")
                            "She stands up and sits close to you on the couch."
                            the_person "The movie's almost finished, how about we watch the last few minutes then call it a night."
                            "[the_person.title] doesn't seem to mind that her face is plastered with your cum right now."
                    "The two of you sit close and watch the rest of the movie. [the_person.title] gives you a goodnight kiss and you both head to bed."
                else:
                    the_person "You want me to give you a blowjob?"
                    "She slides closer to you on the couch and begins running a hand along your leg."
                    mc.name "Ya, definitely. It would help me focus so much better at work."
                    "[the_person.title] slides her hand up your thigh and under your shirt."
                    the_person "Is work making you that anxious though?"
                    mc.name "Sometimes. It's hard work, and there is a lot of pressure running my own business."
                    "[the_person.title] withdraws her hand and looks at you."
                    the_person "Well you know, if it's bothering you that much we could try to find a way to pay off the loan by selling the business."
                    mc.name "I couldn't do that, I'm committed to making this work. All I need is a little help at home."
                    the_person "I don't know about that. That much stress can't be good for you, and I can't be here for you all the time."
                    "She slides back to her initial spot."
                    mc.name "No really, it's okay."
                    the_person "Okay, but if this is too much be sure to let me know."
                    mc.name "Sure thing [the_person.title]."
                    "You watch the rest of the movie and finish around midnight. [the_person.title] gives you a goodnight hug and you both head to bed."
            "Fuck her on the couch" if not the_person.has_taboo("sucking_cock"):
                    mc.name "Good. Just stay nice and relaxed. There's plenty we could do while watching the movie to help us both relax more."
                    the_person "Oh ya? What did you have in mind?"
                    mc.name "Well, if you come and sit on my lap I can slide inside of you and we can both keep watching. Satisfy two wants at once."
                    if the_person.effective_sluttiness("vaginal_sex") > 70 or not the_person.has_taboo("vaginal_sex") or the_person.has_role(very_heavy_trance_role):
                        the_person "You think we could do that?"
                        mc.name "I think we could manage."
                        "You slide your pants down to your ankles, revealing your erect penis."
                        the_person "Wow, it looks like you really need this."
                        while len(the_person.outfit.get_lower_ordered()) > 0:
                            $ generalised_strip_description(the_person, the_person.outfit.get_lower_top_layer())
                        mc.name "Yep. I really need you to take care of me [the_person.title]."
                        while len(the_person.outfit.get_upper_ordered()) > 0:
                            $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                        $ the_person.update_outfit_taboos()
                        $ the_person.draw_person(position = "standing_doggy")
                        "She bends over, showing off her ass to you."
                        the_person "You need this, do you?"
                        "You reach forward and grab a hold of her ass with your hands, giving it a good squeeze."
                        mc.name "Come on [the_person.title], don't keep me waiting."
                        if the_person.has_taboo("vaginal_sex"):
                            $ the_person.call_dialogue("vaginal_sex_taboo_break")
                            $ the_person.break_taboo("vaginal_sex")
                        the_person "Wait, one last thing."
                        "She grabs the remote and resumes the movie."
                        $ the_person.draw_person(position = "sitting")
                        "She puts a hand behind her onto the couch and begins sitting down."
                        "You guide your cock into her slit, and slide into the wet passage."
                        $ mc.change_arousal(20)
                        $ the_person.change_arousal(20)
                        "She sits back fully on you, and you slide your full length into her pussy. [the_person.title] moans quietly as you slide in."
                        the_person "There we go, this should help."
                        $ the_person.draw_person(position = "doggy")
                        "She braces herself on your thighs and begins lifting herself up and down. Her wet cunt grips you tightly as she slides along your shaft."
                        mc.name "That feels great [the_person.title], keep going."
                        "It doesn't seem like there's any danger of her stopping. She moans and leans back, thrusting her tits into the air."
                        $ mc.change_arousal(20)
                        $ the_person.change_arousal(20)
                        "You wrap a hand around and give a breast a squeeze, then pinch a nipple. [the_person.title] moans in response and speeds up her pumps."
                        mc.name "Lean forward [the_person.title], I want to watch your ass move."
                        "[the_person.title] nods and leans forward, placing her hands on her thighs and using her hips to move her pussy up and down your cock."
                        "You take hold of [the_person.title]'s ass with both your hands, pulling it up and down to guide her faster and faster."
                        $ mc.change_arousal(20)
                        $ the_person.change_arousal(20)
                        "She's panting and moaning now, shaking from the exertion of being on top."
                        mc.name "Do you feel close [the_person.title]? I want to help you orgasm."
                        the_person "It's okay. This is all for you."
                        "You drive her ass up and down quickly, pumping your own hips up to meet her."
                        "She pants heavily and her legs spasm lightly. Her head is looking down, watching your cock slide into her."
                        "Her tight pussy is bringing you close to finishing, and you can feel it quivering around you as well, locked in mini orgasms."
                        $ mc.change_arousal(20)
                        $ the_person.change_arousal(20)
                        menu:
                            "Cum inside her":
                                mc.name "I'm almost there, finish me off [the_person.title]!"
                                "[the_person.title] pants quickly and speeds up her pumping with renewed vigor."
                                the_person "Cum whenever you want [the_person.mc_title]!"
                                "You hold on tight to her ass as you get ready to release and pull her tight against you as the first spasm hits you."
                                $ the_person.cum_in_vagina()
                                $ the_person.draw_person(position = "sitting")
                                $ ClimaxController.manual_clarity_release(climax_type = "pussy", the_person = the_person)
                                "[the_person.title] yelps and moans as you release your spunk deep inside. Her body shakes and her pussy spasms around your shaft."
                                $ the_person.have_orgasm()
                                if the_person.has_cum_fetish():
                                    the_person "Oh yes! Yes, yes, yes! Give it all to [the_person.possessive_title]!"
                                "She leans back and slumps while you finish releasing, letting her whole body weight push you deep inside her."
                                "You both sit on the couch and pant for a few moments, your cock still inside her."
                                mc.name "Wow, that felt great [the_person.title]."
                                "She nods and keeps panting. Eventually she stands up a little bit and lets you flop out of her, then sits down on your lap again."
                                $ the_person.draw_person(position = "sitting")
                                "A small trickle of cum leaks out."
                                the_person "I don't think I know what happened in the movie."
                                $ the_person.draw_person()
                                "You both laugh, and eventually she slides off of you and onto the couch. She puts her clothes back on."
                                $ the_person.apply_planned_outfit()
                                $ the_person.draw_person(position = "sitting")
                                call check_date_trance(the_person) from _check_date_trance_movie_solo
                                "She gives you a deep goodnight kiss, and you both head off to bed."
                            "Cum on her tits":
                                mc.name "I'm almost ready. I'm going to cum over your tits, okay?"
                                "[the_person.title] pants quickly and speeds up her pumping to get you ready."
                                if the_person.has_cum_fetish():
                                    the_person "That sounds great, I want you to pump it all out onto my tits for me. Come on, give it to me!"
                                else:
                                    the_person "Of course [the_person.mc_title], you can finish wherever you want."
                                "You tense up as your orgasm approaches and give [the_person.title] a quick slap on the ass to get her off."
                                $ the_person.draw_person(position = "kneeling1")
                                "She moans loudly as you slide your cock out of her one last time, then gets on her knees. She holds her tits up in both hands, kneading them softly while she watches you stroke yourself to completion."
                                mc.name "Here I come!"
                                $ ClimaxController.manual_clarity_release(climax_type = "tits", the_person = the_person)
                                $ the_person.cum_on_tits()
                                $ the_person.cum_on_stomach()
                                $ the_person.draw_person(position = "kneeling1")
                                "You release, shooting your load over [the_person.possessive_title]'s breasts. Your first string of cum lands on her left breast, then you move to her right and unload some more there."
                                "You let the last few drips land on her tits, then smear them around with your tip. Finally you let go of yourself and sit back with a loud sigh."
                                the_person "There you go, all taken care of."
                                mc.name "Ya, wow. Thanks [the_person.title]."
                                $ the_person.apply_planned_outfit()
                                $ the_person.draw_person()
                                $ temp_item = the_person.outfit.get_upper_top_layer()
                                if temp_item:
                                    "She nods and begins getting dressed again. She puts her [temp_item.display_name] on over your load without wiping it away. The fabric clings to her breasts as she moves."
                                $ del temp_item
                                the_person "Any time. I don't think I quite know what's going on in the movie now."
                                "You both laugh, and once you're ready get up to head to bed."
                                "[the_person.title] gives you a deep goodnight kiss, and the two of you head off for the night."
                            "Cum on her face":
                                mc.name "I'm almost there! I want to spray my cum on your face!"
                                "[the_person.title] pants and speeds up her pumping until you slap her ass quickly to get her off."
                                $ the_person.draw_person(position = "blowjob")
                                "She gets down on her knees and holds her tits in her hands. Her head tilts back and she opens her mouth, tongue out."
                                the_person "Ready! Finish on me [the_person.mc_title]!"
                                "You grab your cock and stroke yourself off until you tense and begin cumming."
                                $ ClimaxController.manual_clarity_release(climax_type = "body", the_person = the_person)
                                $ the_person.cum_on_face()
                                $ the_person.cum_in_mouth()
                                $ the_person.draw_person(position = "blowjob")
                                "You unload yourself on [the_person.possessive_title]'s waiting face. You land a spurt into her mouth, the rest landing over her eyes, nose, and dripping down her chin onto her tits."
                                "[the_person.title] swallows the small amount that ended up in her mouth, and you both pant for a few moments."
                                if the_person.has_cum_fetish():
                                    the_person "Ah, let's make sure I got it all."
                                    "She leans forward and starts to lick the sides and bottom of your shaft, eagerly drinking up the last few drops of cum."
                                the_person "There we go. How was that [the_person.mc_title]?"
                                mc.name "Great. You felt great."
                                $ the_person.apply_planned_outfit()
                                $ the_person.draw_person()
                                "[the_person.title] smiles and starts fixing her clothes."
                                the_person "I don't think I know what happened in the movie though."
                                "You both laugh, and once she's put back together she gives you a deep goodnight kiss."
                            "Cum in her mouth":
                                mc.name "I'm almost there! I want you to take my load in your mouth [the_person.title]!"
                                "[the_person.title] pants and speeds up her pumping until you slap her on the ass quickly to get her off."
                                $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                                "She gets down on her knees and grabs your cock up in her mouth right away."
                                "You tense quickly as she gives you a quick blowjob, licking up her own fluids from your cock."
                                mc.name "Here I come!"
                                "[the_person.title] holds your tip in her mouth and looks at you while you stroke your shaft."
                                "You begin releasing, letting your load out into her mouth. She moans and her eyes flutter while she looks at you."
                                $ ClimaxController.manual_clarity_release(climax_type = "body", the_person = the_person)
                                $ the_person.cum_in_mouth()
                                "You stroke yourself for a few seconds until you're completely finished, then let [the_person.title] let go of your cock."
                                mc.name "Let me see it."
                                $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                                "[the_person.title] leans back and opens her mouth. Her mouth is filled with your load, and she plays her tongue through the pool of white while she looks at you."
                                menu:
                                    "Spit it onto her tits":
                                        mc.name "Spit it out onto your tits [the_person.title]."
                                        "She nods. First she tilts her head up and gargles, sending bubbles through the cum and mixing her spit in with it."
                                        $ the_person.cum_on_tits()
                                        $ the_person.draw_person(position = "blowjob")
                                        "Then she leans her head forward and opens her mouth, letting out a thin stream of white for a few seconds. She moves her head around to drape the line across her tits and nipples."
                                        "She ends with a loud spit, spraying a final blob of cum onto her breasts, then looks at you and smiles."
                                        if the_person.has_cum_fetish():
                                            the_person "Ah... there we go. Do you think [the_person.possessive_title] looks good covered in your hot cum?"
                                            $ the_person.cum_on_stomach()
                                            $ the_person.draw_person(position = "blowjob")
                                            "She pouts a little and runs a finger through the pools of sperm on her breasts spreading it further down her body."
                                        else:
                                            the_person "There we go, all done."
                                        mc.name "Oh ya, you look beautiful [the_person.title]."
                                        the_person "Thank you. I don't think we've been paying attention to the movie though."
                                        "You both laugh. You enjoy looking at your cum covered [the_person.title], but eventually you both get up."
                                        "[the_person.title] collects her clothes and gives you a deep goodnight kiss."
                                    "Swallow it all":
                                        mc.name "Perfect [the_person.title]. Now swallow it all for me."
                                        $ the_person.outfit.remove_all_cum()
                                        $ the_person.draw_person(position = "blowjob")
                                        "She nods and closes her mouth. She gulps loudly, then opens her empty mouth."
                                        mc.name "Good girl."
                                        the_person "Anything for my [the_person.mc_title]. I think I've lost track of where we are in the movie though."
                                        "You both laugh, and [the_person.title] gets up from the floor. She collects her clothes and gives you a deep goodnight kiss."
                    else:
                        the_person "Slide inside of me... like have sex?"
                        "She looks at you sternly."
                        if the_person == mom:
                            the_person "I don't think that's such a good idea. [lily.fname] may come back any time now. And besides, this is the family couch!"
                        else:
                            the_person "I don't think that's such a good idea. Someone could walk in any time now."
                        "A brief look of disgust crosses her face."
                        the_person "I can't believe you even said that."
                        if _return:
                            "Damn, she must have resisted the serum. Maybe you moved too fast."
                        else:
                            "Damn, she isn't ready for that yet. You moved too fast."
                        mc.name "I was just joking! Me and some of my employees have an inside joke, but I guess it just sounds crude if you don't know it."
                        the_person "Yes, it does."
                        mc.name "I'm sorry [the_person.title]. I didn't mean for it to sound like that."
                        "Her look softens."
                        the_person "That's alright. Let's finish the movie then, shall we?"
                        "You watch the movie together, but you can't shake the feeling that you could have done more with this opportunity."
                        "Afterwards you and [the_person.title] say goodnight and head to bed."
    return

label movie_group(the_person, the_other_person):
    "You go to the living room and start scrolling for a movie you'd all like."
    "Shortly after both [the_other_person.title] and [the_person.title] join you, and you decide to watch a comedy."
    $ scene_manager.add_actor(the_person, position = "sitting")
    $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
    "An hour passes with the three of you relaxing on the couch and laughing."
    the_person "Hey [the_person.mc_title], I have a bottle of wine above the fridge. It's been a long week and I think we could all use a little drink. Would you mind pouring us all a glass?"
    the_other_person "Wine sounds great, thanks [the_person.fname]."
    mc.name "Sure. Back in a moment."
    "[the_person.title] pauses the movie while you head to the kitchen. You find the bottle of wine and grab a glass for each of you."
    $ scene_manager.clear_scene()
    $ mc.change_location(kitchen)
    menu:
        "Add serum to [the_person.title]'s drink":
            call give_serum(the_person) from _call_give_serum_movie_group
        "Leave [the_person.title]'s drink alone":
            pass
    menu:
        "Add serum to [the_other_person.title]'s drink":
            call give_serum(the_other_person) from _call_give_serum_movie_group_2
        "Leave [the_other_person.title]'s drink alone":
            pass
    if the_person.has_role(trance_role) and the_other_person.has_role(trance_role):
        menu:
            "Take charge of the evening":
                call movie_group_lead(the_person, the_other_person) from _call_movie_group_lead
                $ scene_manager.clear_scene()
                return
            "See how events unfold":
                pass
    call movie_group_watch(the_person, the_other_person) from _call_movie_group_watch
    $ scene_manager.clear_scene()
    return

label movie_group_lead(the_person, the_other_person):
    $ relationship_a = town_relationships.get_relationship(the_person, the_other_person).type_a
    $ relationship_b = town_relationships.get_relationship(the_person, the_other_person).type_b
    the_other_person "There he is!"
    the_person "Thank you [the_person.mc_title]."
    mc.name "No problem [the_person.title]. Here you go [the_other_person.title]."
    "You distribute the drinks and take a seat between the girls on the couch."
    "[the_person.title] picks up the remote and resumes the movie and the three of you relax. [the_other_person.title] and [the_person.title] both take sips from their wine glasses."
    mc.name "You two should drink up, there's plenty of wine if you want more."
    the_person "We don't want to drink too much, I've got stuff to do in the morning."
    the_other_person "Oh come on [the_person.fname], it'll be fine. We barely drink anyways."
    "[the_other_person.title] lifts her drink up and takes a large gulp."
    the_person "[the_other_person.fname], you're terrible!"
    "[the_person.title] reaches across you and slaps [the_other_person.title] on the leg, then takes her own glass and drinks some more."
    mc.name "You should finish the glass, I can get more if you want."
    "The girls don't say anything, but both of them down their entire glass of wine."
    "It is pretty clear that they are each in at least a bit of a trance, and the alcohol is helping them sink deeper."
    mc.name "Can you two both hear me?"
    the_person "Of course [the_person.mc_title]."
    the_other_person "Ya. What's up [the_other_person.mc_title]?"
    $ person_score = 1
    if the_person.has_exact_role(very_heavy_trance_role):
        $ person_score +=2
    if the_person.has_exact_role(heavy_trance_role):
        $ person_score +=1
    $ other_score = 1
    if the_other_person.has_exact_role(very_heavy_trance_role):
        $ person_score +=2
    if the_other_person.has_exact_role(heavy_trance_role):
        $ person_score +=1
    menu:
        "Have them take off their shirts." if not (the_person.tits_visible() or the_other_person.tits_visible()):
            mc.name "You've both had such a long hard week. You really earned a relaxing night in."
            "[the_person.possessive_title] and [the_other_person.possessive_title] listen and nod."
            mc.name "I think we'd all be even more relaxed without our shirts. We're all family here."
            if not the_other_person.tits_visible():
                the_other_person "Do you think so?"
                mc.name "Definitely."
            else:
                the_other_person "Way ahead of you [the_other_person.mc_title]!"
                mc.name "Exactly, doesn't it feel great?"
                the_other_person "It does, come on and join me."
            if not the_person.tits_visible():
                the_person "If you two are comfortable with it I'll play along."
            else:
                the_person "I couldn't agree more, time for you two to join me."
            mc.name "Sure. I'll go first."
            "You pull your t-shirt over your head and drop it to the floor."
            if not the_other_person.tits_visible():
                mc.name "Your turn [the_other_person.title]."
                $ the_item = the_other_person.outfit.get_upper_top_layer()
                if the_item.has_extension:
                    the_other_person "Well, my [the_item] kind of is my shirt."
                    $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "stand3")
                    "She stands up and shrugs her [the_item.display_name]es straps off and lets it fall to the ground."
                    $ the_other_person.draw_animated_removal(the_item)
                    $ mc.change_locked_clarity(10)
                    the_other_person "So I guess I don't get to wear any of it."
                    $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                    if the_other_person.outfit.wearing_panties():
                        if the_other_person.outfit.wearing_bra():
                            "She giggles, and sits back down on the couch in just her underwear."
                        else:
                            "She giggles, and sits back down on the couch in just her panties."
                    else:
                        "She giggles, and sits back down on the couch nude."
                else:
                    the_other_person "Well, alright."
                    "She pulls her [the_item] over her head and tosses it to the ground."
                    $ the_other_person.draw_animated_removal(the_item)
                    $ mc.change_locked_clarity(10)
                    if the_other_person.outfit.wearing_bra():
                        "She giggles, and leans back in her bra."
                    else:
                        "She giggles, and leans back topless."
            if not the_person.tits_visible():
                mc.name "[the_person.title]?"
                $ the_item = the_person.outfit.get_upper_top_layer()
                "[the_person.title] pulls off her top. She folds her [the_item] carefully and puts it on the coffee table."
                $ the_person.draw_animated_removal(the_item)
                $ mc.change_locked_clarity(10)
            "The three of you sit on the couch for a few minutes."
            "You aren't sure how much longer the trance will last though, so you take a few last looks and then speak up."
            mc.name "It's getting a little chilly in here. Maybe we should put our shirts on after all."
            the_other_person "I didn't notice, but ya it is."
            the_person "Good idea. We don't want to catch a cold playing around the house like this."
            $ the_person.apply_planned_outfit()
            $ the_other_person.apply_planned_outfit()
            "You all put on your clothes again and watch the rest of the movie."
            "As you say goodnight, you feel confident you made a major effect on both of them tonight."
            $ the_person.change_slut(2 + the_person.get_opinion_score("showing her tits"), 30)
            $ the_other_person.change_slut(2 + the_person.get_opinion_score("showing her tits"), 30)
        "Have them both get naked." if not (the_person.tits_visible() or the_person.vagina_visible() or the_other_person.tits_visible() or the_other_person.vagina_visible()):
            if the_person.has_taboo(["bare_tits", "bare_pussy"]):
                $ person_score -=1
            if the_other_person.has_taboo(["bare_tits", "bare_pussy"]):
                $ other_score -=1
            mc.name "We've all had such long hard weeks, I think we all need to relax as much as possible."
            "Your [the_person.possessive_title] and [the_other_person.possessive_title] listen and nod."
            mc.name "I know I'm always more relaxed when I'm naked, so I'm going to take off my clothes. I think you two should join me."
            if person_score > 0 and other_score > 0:
                if the_other_person.tits_visible() and the_other_person.vagina_visible():
                    the_other_person "I couldn't agree more!"
                else:
                    the_other_person "Do you think so?"
                mc.name "Definitely. No tight bras, no fluffy dresses. Way more relaxing."
                "You stand up and pull your shirt off, throwing it on the back of the couch."
                if the_person.tits_visible() and the_person.vagina_visible():
                    the_person "I'm glad to see you agree with me."
                else:
                    the_person "That's an interesting idea [the_person.mc_title]. I think we should give it a try."
                if not the_other_person.outfit.wearing_bra():
                    the_other_person "Jokes on you, I'm already not wearing a bra."
                elif not the_person.outfit.wearing_bra():
                    the_person "Jokes on you, I'm already not wearing a bra."
                $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list(strip_feet = True, strip_accessories = True))
                $ mc.change_locked_clarity(10)
                the_other_person "You're right [the_other_person.mc_title], this is relaxing."
                $ generalised_strip_description(the_other_person, the_other_person.outfit.get_full_strip_list(strip_feet = True, strip_accessories = True))
                $ mc.change_locked_clarity(10)
                "You pull your pants and underwear down."
                mc.name "What do you think [the_person.title]? Feeling relaxed?"
                the_person "It's a little strange to be doing this with you two, but I suppose it's a good way to get to know each other."
                mc.name "Exactly. Now let's sit down and enjoy the movie."
                "The three of you sit down. You're excited, and your cock stands hard and ready. You see [the_other_person.title] sneaking glances at you from the corner of her eye."
                mc.name "Getting an eyeful [the_other_person.title]?"
                "She blushes and looks away quickly."
                the_other_person "Just taking a look. Sorry."
                mc.name "Don't be sorry, we don't see each other naked very often. Stare away."
                the_person "Quiet you two, we're missing the movie."
                "You both stay quiet, but [the_other_person.title] now doesn't hide her staring and looks at your impressive package directly. You flex your cock for her a few times, and see her blush some more."
                "You aren't sure how long the serum will last though, so you have to cut the fun short."
                mc.name "It's getting a little cold in here, isn't it?"
                the_person "Is it?"
                mc.name "Ya, I think so. I'm going to get dressed again."
                the_other_person "Me too, it's definitely chilly."
                $ the_person.apply_planned_outfit()
                $ the_other_person.apply_planned_outfit()
                "[the_person.title] follows your lead, and a few minutes later you're all dressed."
                "When the movie ends you all say goodnight. You feel like you had a major effect on the two of them tonight."
                $ the_person.change_slut(2 + the_person.get_opinion_score("not wearing anything"), 40)
                $ the_other_person.change_slut(2 + the_person.get_opinion_score("not wearing anything"), 40)
            elif other_score > 0:
                "You grab the bottom of your t-shirt and pull it over your head."
                the_person "In front of [the_other_person.possessive_title]?"
                mc.name "Ya. We're family, it's nothing we haven't seen by accident."
                "[the_person.title] hesitates, then shakes her head."
                the_person "I don't think so, you should be setting a better example for her."
                "[the_other_person.title] nods slowly, appearing to be waking up from her trance slowly."
                $ trance_on_turn(the_person)
                $ trance_on_turn(the_other_person)
                the_other_person "I think we should just finish watching the movie."
                mc.name "Okay, if you aren't comfortable with it."
                "You put your shirt back on. [the_person.title] must not be deep enough and has warned [the_other_person.title] now."
                "After the movie the three of you say goodnight and head to bed. You probably shouldn't push so hard in that situation."
            else:
                "You grab the bottom of your t-shirt and pull it over your head."
                the_other_person "You're going to get naked here? In the living room?"
                mc.name "Ya. It'll be nice, trust me."
                the_other_person "Ew, we sit here and eat sometimes! [the_person.title], you can't let him do that."
                "[the_person.title] shakes her head, as if waking up from a nap."
                $ trance_on_turn(the_person)
                $ trance_on_turn(the_other_person)
                the_person "What?"
                the_other_person "[the_person.mc_title] is taking his clothes off to relax, on the couch."
                mc.name "Sorry, sorry. If you two don't think I should, I'll stop."
                the_person "Maybe that's a good idea. Let's just watch the movie."
                "Damn, [the_other_person.title] must not be deep enough, and she's warned [the_person.title] now."
                "The three of you watch the rest of the movie, then head to bed. You probably shouldn't push so hard in that situation."
        "Have them use their tits and hands to jerk you off." if the_person.has_large_tits() and the_other_person.has_large_tits():
            if the_person.has_taboo(["touching_body", "touching_penis"]):
                $ person_score -=1
            if the_other_person.has_taboo(["touching_body", "touching_penis"]):
                $ other_score -=1
            mc.name "We've all had a really busy week I think. It's good that we can all sit back and relax."
            "[the_other_person.title] and [the_person.title] nod slowly."
            mc.name "I know I've been really horny lately though. It would help me relax if you two could help me get off."
            if person_score > 0 and other_score > 0:
                the_other_person "Is that really the only way you could relax?"
                the_person "Well if he's that horny, probably. When a boy gets excited it can be really distracting."
                "You pull your pants down past your waist and free your cock for emphasis."
                mc.name "[the_person.title]'s right. You two would really be helping me out."
                the_person "Okay [the_other_person.title], let's help your brother out with his little problem, then we can finish the movie."
                the_other_person "Okay, what should I do?"
                mc.name "Come a little closer and rub it for me while [the_person.title] gets ready."
                "[the_other_person.title] slides closer on the couch and reaches a hand out, brushing it against your shaft."
                mc.name "That's right. Grab it and give it a rub."
                if the_person.outfit.wearing_bra():
                    while len(the_person.outfit.get_upper_ordered()) > 1:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    "She does so, while [the_person.title] drops her top on the coffee table and reaches behind herself to undo her bra."
                else:
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    "She does so, while [the_person.title] drops her top on the coffee table."
                the_other_person "Like this?"
                mc.name "Just like that. Keep stroking it for me."
                if the_person.outfit.wearing_bra():
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    "She lets the bra fall to the ground, and joins you on the couch on the other side."
                the_person "Here, let me show you [the_other_person.title]."
                "She reaches forward and takes your cock from [the_other_person.title]'s hand. [the_person.title] begins stroking you quickly and softly."
                if not the_other_person.tits_visible():
                    $ the_item = the_other_person.outfit.get_upper_top_layer()
                    "You reach up and pull the top of [the_other_person.title]'s [the_item.display_name] down past her tits. She blushes but keeps looking at you."
                    $ scene_manager.strip_to_tits(person = the_other_person, prefer_half_off = True)
                else:
                    $ the_item = None
                mc.name "You have really great tits [the_other_person.title]. Would you like [the_person.title] to show you how to use them?"
                "[the_person.title] leans over your lap and drapes her breasts across your shaft. She slides them across you a few times before taking them up in her hands and nestling you inside her cleavage."
                the_person "You've got to make sure you keep him right in the middle, between both your tits. A little bit of pressure helps, then slide him up and down."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                "She demonstrates, and [the_other_person.title] gets on her knees in front of you to watch."
                the_person "Sometimes it's a little dry. Some spit helps keep everything moving."
                "[the_person.title] stops for a moment and sits up, then spits between her tits. When she leans over again you're treated to a nice slippery tit fuck."
                the_other_person "I think I get it. Can I try?"
                "[the_person.title] nods and stops. She sits up and watches as [the_other_person.title] spits between her own tits and rubs them together, then she sits up on her knees and wraps her tits around your shaft."
                "Slowly at first, she begins to slide herself up and down your length, holding your cock deep in her cleavage with a little pressure from her hands."
                "Seeing [the_other_person.possessive_title] rub your cock, while your topless [the_person.title] watches beside you, is enough to bring you right to the edge."
                mc.name "I'm going to finish soon."
                menu:
                    "Cum on [the_other_person.title]":
                        the_person "Okay, let me take over then."
                        mc.name "I think [the_other_person.title] can handle it, she's doing a great job so far."
                        the_other_person "I don't mind."
                        "[the_person.title] nods and sits back, watching as [the_other_person.title] strokes your cock to completion with her tits."
                        "You moan and lean back as you finish. [the_other_person.title] keeps her tits sliding as you cum between them, making them even more slippery."
                        $ ClimaxController.manual_clarity_release(climax_type = "tits", the_person = the_other_person)
                        $ the_other_person.cum_on_tits()
                        $ the_other_person.cum_on_stomach()
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "stand2")
                        if the_item:
                            "As you finish your last pulse she lets your cock slide out the bottom and stands up. Your cum drips down her chest and runs into the front of her [the_item.display_name]."
                        else:
                            "As you finish your last pulse she lets your cock slide out the bottom and stands up. Your cum drips down her chest and runs onto her belly."
                        the_person "Good job [the_other_person.title]."
                        "[the_other_person.title] smiles proudly."
                        the_other_person "Thanks [the_person.title]."
                        mc.name "And thank you both. That really helped."
                        the_person "Glad we could help. Now, let's finish the movie."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                        "[the_other_person.title] sits back on the couch and you finish the last twenty minutes of the movie. Neither [the_other_person.title] nor [the_person.title] bother to cover their tits again, and [the_other_person.title] doesn't even bother wiping your cum away."
                    "Cum on [the_person.title].":
                        the_person "Okay, let me take over then."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                        "[the_other_person.title] strokes you with her breasts a few more times, then let's go and sits on the couch again."
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        "[the_person.title] gets on the floor where [the_other_person.title] had been and wraps her tits around your wet cock. Immediately she presses them tight around you and begins sliding them up and down."
                        "A minute later you're ready and begin tensing."
                        the_person "There we go, let it out."
                        $ ClimaxController.manual_clarity_release(climax_type = "tits", the_person = the_person)
                        $ the_person.cum_on_tits()
                        $ the_person.cum_on_stomach()
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        "She holds your tip at the top of her cleavage as you pulse out your load. Your cum pools around your cock, kept in place by the valley her cleavage forms."
                        "Finally she slides her tits up, and your load begins trickling between her breasts."
                        the_other_person "Wow, that looked impressive."
                        mc.name "Thanks. It was you girls who did all the work though."
                        the_person "Just glad I could help. Now, how about we finish up the movie and head to bed."
                        $ scene_manager.update_actor(the_person, position = "sitting")
                        "[the_person.title] joins you two on the couch, keeping a hand on her stomach to catch the trickles of cum. Neither her nor [the_other_person.title] bother putting their shirts on while you finish the movie."
                "Afterwards you head up to bed, feeling confident you made a major impact."
                $ the_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 40)
                $ the_other_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 40)
            else:
                "The two girls look at each other for a moment."
                if person_score > 0:
                    the_other_person "Get you off... you mean give you a handjob?"
                    mc.name "That would be one way, ya."
                    the_other_person "I would have to touch you... in front of [the_other_person.title]?"
                    the_person "Well..."
                    the_other_person "I don't think I could do that. It would be too weird."
                    mc.name "There's nothing strange about it. We're just family helping each other out, right?"
                    the_person "I think your sister is right, that would be going too far [the_person.mc_title]."
                    "Damn, [the_other_person.title] must have resisted and warned off [the_person.title]. Nothing to do now but damage control."
                else:
                    the_person "You want a handjob?"
                    mc.name "If that's what you're comfortable with, sure."
                    the_other_person "Both of us?"
                    the_person "With [the_other_person.possessive_title] here? I don't think so."
                    the_other_person "Ya, that doesn't seem right."
                    "Damn, [the_person.title] must have resisted and warned off [the_other_person.title]. Nothing to do now but damage control."
                mc.name "Ah, I'm sorry. You're right I guess. Forget I brought it up."
                "The three of you return to watching the movie. Afterwards you say goodnight and head to bed, knowing you could have had more of an effect on them tonight."
        "Have them blow you.":
            if the_person.has_taboo("sucking_cock"):
                $ person_score -=1
            if the_other_person.has_taboo("sucking_cock"):
                $ other_score -=1
            mc.name "I've had a really busy week, and it's nice to have you two here to help me de-stress."
            "[the_other_person.title] and [the_person.title] nod slowly."
            mc.name "It would help me even more if you could use your mouths to help me relax."
            if person_score > 0 and other_score > 0:
                the_person "You have been working hard all week..."
                the_other_person "He has been really busy. I think we should help."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                "[the_other_person.title] slides down to the floor on her knees. You spread your legs and undo the zipper on your pants for her."
                the_person "Okay, we'll help you take care of this, then we can get back to watching the movie."
                mc.name "Sounds great. Thanks you two."
                "[the_other_person.title] nods and reaches for your pants, sliding them down to the floor. Your cock pops out of your underwear, hard and ready for the girls."
                "[the_person.title] reaches over to your lap and starts stroking your cock. [the_other_person.title] leans forward and kisses the base of your shaft."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob")
                "[the_person.title] stops her stroking so [the_other_person.title] can lick up the bottom of your cock, circling her tongue around your tip to get it nice and wet."
                the_other_person "That should feel better."
                "[the_other_person.title] leans back to let [the_person.title] start stroking again, and you shiver slightly as her wet hand slides up and down your cock."
                the_person "Does that feel good?"
                mc.name "Yes, it feels great."
                $ scene_manager.update_actor(the_person, position = "sitting", special_modifier = "blowjob")
                "She strokes you quickly for a few seconds, then leans over and wraps her mouth around your tip. She brushes her hair out of the way and begins sliding you into her throat."
                "As [the_person.title] reaches the bottom she shakes her head left and right slightly, clenching down on your cock with her throat. Finally she pulls back and begins blowing you at a slow regular pace."
                if not the_other_person.tits_visible():
                    while len(the_other_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_other_person.outfit.get_upper_top_layer())
                "[the_other_person.title] watches from the ground on her knees, eyes following [the_person.title]'s mouth up and down."
                if not the_other_person.tits_visible():
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                "As she watches, she kneads her breast slowly."
                the_other_person "Can I give it a try?"
                "[the_person.title] pulls off your cock."
                the_person "Sorry, of course [the_other_person.fname]."
                "She sits up and straightens her hair. While [the_other_person.title] slides forward between your legs."
                if not the_person.tits_visible():
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                the_person "Here you go, you can play with my tits [the_person.mc_title]."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob", special_modifier = "blowjob")
                "[the_other_person.title] holds your shaft lightly in one hand and brings her face close. She licks you quickly, then places her mouth over the tip and starts sucking on it."
                "[the_person.title] lifts her breasts up with both hands, offering them to you."
                "You take a nipple in your mouth and suck lightly, grabbing the other tit with a hand."
                "[the_other_person.title] slides your shaft deeper into her warm mouth, licking with her tongue."
                mc.name "That's good [the_other_person.title]. See if you can go as deep as [the_person.title]."
                "She nods and starts going deeper with every stroke over her mouth. As she reaches the bottom you can hear wet gagging sounds as your tip hits the back of her throat."
                the_person "You're doing great [the_other_person.title]. Keep it up."
                mc.name "She really is a great slut [the_person.title], she knows exactly what to do."
                the_person "[the_person.mc_title]! You shouldn't say that about [the_other_person.possessive_title]."
                "[the_other_person.title] coughs with your cock in her throat, then pushes herself deeper onto it."
                mc.name "It's a compliment, she's really good at this. It's making me feel great."
                "[the_person.title] gives you a look, then nods."
                the_person "I suppose she is trying really hard."
                "You reach down and hold [the_other_person.title]'s head from either side, then pump your waist up and down to slide your cock in and out of her throat."
                "Spit runs down her mouth, dripping off her chin. Her mouth makes satisfying wet slapping sounds, but she holds her mouth as wide open as possible for you. She twists her own nipples between her fingers."
                the_person "It looks like she might need some help down there."
                "You relax your thrusts and let [the_other_person.title] take over again while [the_person.title] gets on her knees and joins her on the ground."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                "[the_other_person.title] pulls your cock out of her mouth, dripping spit down onto her tits. She pants loudly as she moves out of the way for [the_person.title]."
                the_person "Thanks [the_other_person.title]."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob", special_modifier = "blowjob")
                "[the_person.title] returns your cock to her mouth, sliding you up and down quickly."
                "You feel your orgasm building up inside you while the girls stare at your cock on their knees."
                menu:
                    "Cum on both of them.":
                        mc.name "I'm about to finish! Get together!"
                        "[the_person.title] throats you deep one last time, then pulls off with a wet sigh and slides back. She throws an arm around [the_other_person.title] and pulls her close, pressing the side of their tits together."
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        the_other_person "We're ready [the_other_person.mc_title]!"
                        the_person "Give it to us!"
                        "You sit forward on the couch and stroke your wet cock quickly. You tense and begin releasing your load, shooting thick streams of cum over first [the_other_person.title], then [the_person.title]."
                        $ the_person.cum_on_face()
                        $ the_other_person.cum_on_face()
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        "The girls stay still and wait while you finish, and you rub the last few drops of cum onto [the_other_person.title]'s nipple. Finally you sigh and sit back, looking at your cum covered [the_person.title] and [the_other_person.title]."
                        $ the_other_person.cum_on_tits()
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        the_person "There we go. Feeling better?"
                        mc.name "Much better. Thanks you two."
                        the_other_person "No problem. It was fun."
                        "[the_other_person.title] and [the_person.title] look at each other and help wipe the strings of cum out from around their eyes."
                        the_person "Now, we should finish that movie."
                    "Cum in [the_person.title]'s mouth.":
                        mc.name "I'm about to finish. Keep going [the_person.title], I want you to take my load."
                        "[the_person.title] nods slightly while blowing you and speeds up her pace."
                        "She takes you deep in her throat, tongue licking quickly. Before long you tense up and begin to release."
                        "[the_person.title] slides your tip into her mouth and places it on her tongue. She grabs your wet cock with her hand and strokes you off as you spasm and shoot your load into her mouth."
                        "After a few pulses you're finished, and she pulls you out of her mouth slowly."
                        $ the_person.cum_in_mouth()
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        "She opens her mouth to show you, then reaches for her wine glass and spits it out inside. She places the glass on the coffee table and smiles at you."
                        the_person "Good job [the_person.mc_title]. You let out a lot. Feeling better?"
                        mc.name "Much better, thank you."
                        if the_other_person.has_cum_fetish:
                            "While [the_person.title] is talking [the_other_person.title] grabs the wine glass and tilts it back, drinking up the cum [the_person.possessive_title] had spit out."
                            the_person "[the_other_person.title], what are you doing?"
                            $ the_other_person.cum_in_mouth()
                            $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                            "[the_other_person.title] swallows your load and turns back to you two."
                            the_other_person "What? We can't go wasting that."
                            "[the_person.title] thinks for a moment, then shrugs."
                            the_person "If that's what you think dear."
                        the_person "Now how about we finish the movie and get to bed."
                    "Cum in [the_other_person.title]'s mouth.":
                        mc.name "I'm about to finish. Take over [the_other_person.title], I want you to take my load."
                        "[the_person.title] pulls off your cock with a wet sigh."
                        the_person "Can you handle that honey?"
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob", special_modifier = "blowjob")
                        "[the_other_person.title] nods and grabs the base of your shaft. She slips your tip into her mouth and begins blowing you quickly."
                        "A few deep strokes of her throat you feel yourself tense up and begin to release."
                        "[the_other_person.title] keeps blowing you until the first pulse hits. She pulls your tip back into her mouth and lets the rest of your spasms shoot your load into her mouth."
                        $ the_other_person.cum_in_mouth()
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        "When you're finished she slides off slowly, careful not to let anything slip out."
                        if the_person.has_cum_fetish:
                            the_person "Good job [the_other_person.fname]. Since you got all of it do you think you could share?."
                            if the_other_person.has_cum_fetish:
                                "[the_other_person.title] shakes her head and swallows loudly. She smiles at both of you after."
                                the_other_person "Sorry, it is just too yummy to share."
                            else:
                                "[the_other_person.title] looks a bit surprised but leans towards [the_person.title] with her cheeks still puffed out."
                                "[the_person.title] pushes her way in forcefully, sucking at [the_other_person.title]'s lips to draw out all of your fluids."
                                $ the_person.cum_in_mouth()
                                $ scene_manager.update_actor(the_person, position = "kneeling1")
                        else:
                            the_person "Good job [the_other_person.fname]. Now you can go to the bathroom and spit it out if you want."
                            "[the_other_person.title] shakes her head and swallows loudly. She smiles at both of you after."
                            the_other_person "No need. I took care of it."
                        mc.name "Well done [the_other_person.title], that was great."
                        the_other_person "[the_person.title] helped too. Now let's finish the movie."
                $ scene_manager.update_actor(the_person, position = "sitting")
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                "They rejoin you on the couch, both still topless, and you watch the last few minutes of the film. When you head to bed you're satisfied you had a major effect on both of them."
                $ the_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 50)
                $ the_other_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 50)
            else:
                if person_score > 0:
                    the_other_person "You want us to kiss you?"
                    mc.name "Not exactly, no."
                    the_person "Do you mean a blowjob?"
                    "You nod. [the_person.title]'s hand rests on your thigh and starts rubbing it."
                    the_other_person "A blowjob? Here!"
                    mc.name "What's wrong? We're all family, just helping each other out."
                    the_other_person "Ew, no. Not here with [the_person.title]. Not at all!"
                    "[the_person.title] moves her hand back."
                    the_person "[the_other_person.possessive_title] is right. That's not appropriate talk young man."
                    "Damn, [the_other_person.title] must have resisted the serum and has warned [the_person.title]. Nothing to do now but damage control."
                    mc.name "You're right. I'm sorry you two."
                    the_person "Apology accepted. Let's watch the rest of the movie and get to bed."
                    "You finish the movie, then head up to bed. You can't help thinking that you could have done more to take advantage of the situation tonight."
                else:
                    the_person "You want us to give you a blowjob?"
                    the_other_person "I thought he just meant kisses."
                    mc.name "No, [the_person.title] is right. A blowjob would be perfect."
                    the_person "Perfect isn't the word I'd use. We're having a very nice time watching the movie right now."
                    mc.name "It's no big deal, we can pause the movie."
                    the_person "That still doesn't make it alright in front of [the_other_person.possessive_title]."
                    the_other_person "Ya, that sounds a little weird."
                    "Damn, [the_person.title] must have resisted the serum."
                    mc.name "Sorry, you're right. Let's just finish the movie then."
                    "The three of you watch the rest of the movie. You head to bed after, and feel that you could have done something more to take advantage of the situation."
        "Fuck them both." if person_score > 1 or other_score > 1:
            if the_person.has_taboo("vaginal sex"):
                $ person_score -=1
            if the_other_person.has_taboo("vaginal sex"):
                $ other_score -=1
            mc.name "It's been a busy week for all of us, and if you're like me you've been horny for most of it. We've got some time together to just relax. How about we pause the movie and take advantage of it."
            if person_score > 0 and other_score > 0:
                "[the_other_person.title] grabs the remote and pauses the movie right away."
                the_person "Well, it would be a good way to relax."
                the_other_person "Come on [the_person.title], it'll be fun."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "stand2")
                "[the_other_person.title] stands up and starts to undress."
                if not the_other_person.tits_visible():
                    while len(the_other_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_other_person, the_other_person.outfit.get_upper_top_layer())
                $ mc.change_locked_clarity(10)
                $ scene_manager.update_actor(the_person, position = "stand2")
                "[the_person.title] hesitates for a moment, then shrugs and stands up as well."
                while len(the_person.outfit.get_upper_ordered()) > 1 or len(the_other_person.outfit.get_lower_ordered()) > 0:
                    while len(the_person.outfit.get_upper_ordered()) > 1:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    while len(the_other_person.outfit.get_lower_ordered()) > 0:
                        $ generalised_strip_description(the_other_person, the_other_person.outfit.get_lower_top_layer())
                $ mc.change_locked_clarity(10)
                mc.name "How about you get me warmed up while [the_person.title] strips down [the_other_person.title]?"
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                "She nods and kneels between your legs while you unzip your pants and slide your cock out."
                if not the_person.tits_visible():
                    while len(the_person.outfit.get_upper_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
                    "As [the_person.title] undoes her bra and places it on the back of the couch [the_other_person.title] puts your tip into her mouth and starts gently sucking on it."
                else:
                    "[the_other_person.title] puts your tip into her mouth and starts gently sucking on it."
                the_person "Don't get too carried away you two."
                if the_person.outfit.wearing_panties():
                    while len(the_person.outfit.get_lower_ordered()) > 1:
                        $ generalised_strip_description(the_person, the_person.outfit.get_lower_top_layer())
                else:
                    while len(the_person.outfit.get_lower_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_lower_top_layer())
                "[the_other_person.title] licks the shaft a few times to get it wet, then slides the whole length into her mouth."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob", special_modifier = "blowjob")
                if the_person.outfit.wearing_panties():
                    while len(the_person.outfit.get_lower_ordered()) > 0:
                        $ generalised_strip_description(the_person, the_person.outfit.get_lower_top_layer())
                    "While [the_person.title] gets her panties off [the_other_person.title] blows you quickly, making wet gagging sounds quietly as you hit the back of her throat."
                $ scene_manager.update_actor(the_person, position = "kneeling1")
                "[the_person.title] kneels down and watches [the_other_person.title] blow you for a while, then reaches around and rubs her breasts."
                "[the_other_person.title] pulls off your cock with a wet pop."
                the_other_person "There we go, all wet and ready."
                the_person "Me too."
                "[the_person.title] stands up and turns around, spreading her lips with one hand and leaning back towards your cock."
                $ scene_manager.update_actor(the_person, position = "standing_doggy")
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                "You hold onto your shaft and guide it towards her pussy as she eases herself down onto the tip. [the_other_person.title] sits back and puts a hand between her own legs, rubbing herself gently."
                "[the_person.title] gently lowers herself until your entire length is inside her. She sighs loudly and pauses at the bottom for a moment."
                "Then she begins raising and lowering herself, making sure to stroke every inch of your cock with her body."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "missionary")
                "[the_other_person.title] sighs and sits back, legs spread, and rubs her clit quickly while watching the two of you."
                the_other_person "That looks great [the_person.title]."
                "[the_person.title] sighs and nods, speeding up her movement."
                the_person "I'll make sure not to finish him off so you can have a turn."
                "[the_other_person.title] nods and slips two fingers into herself while she waits."
                "Eventually [the_person.title] gives one last deep stroke and stands up, your cock popping out with a wet squelch."
                $ scene_manager.update_actor(the_person, position = "stand2")
                the_person "Okay, your turn."
                $ scene_manager.update_actor(the_person, position = "missionary")
                "She sits down beside you and begins fingering herself while [the_other_person.title] stands up and gets on top of you."
                $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "cowgirl")
                "[the_other_person.title] kneels on the couch, legs on either side of yours, and looks at you while you line up your shaft with her slit."
                mc.name "Okay, ready."
                "She nods and lowers herself down. She doesn't waste any time and begins riding you as quickly as she can. Her hair bounces around on her shoulders and her tits shake up and down."
                the_person "That's a good girl, make sure to get it all."
                "[the_other_person.title] does, and moans loudly as she goes. A few minutes later you can feel her legs start to quiver, only partly from exertion."
                the_other_person "Oh fuck. I think you're going to make me cum."
                "You're starting to get close to your own orgasm too."
                menu:
                    "Cum inside [the_other_person.title].":
                        mc.name "I'm getting close too."
                        the_person "Keep going [the_other_person.title]!"
                        "She slides up and down as quickly as she can, panting loudly and moaning. [the_other_person.title] rubs her own clit quickly with one hand, watching her [relationship_a] get fucked."
                        "[the_other_person.title] quivers and gasps, throwing herself onto your cock as hard as she can. Her thighs clench around your legs and she holds onto your shoulders as she shudders."
                        "[the_person.title] reaches over and grabs her by the hips, pulling her up and pushing her down."
                        the_other_person "Ah! [the_person.title]!"
                        "[the_other_person.title] screams in pleasure as she's guided up and down your cock. She shakes and spasms as she's forced to keep riding you while she orgasms."
                        $ the_other_person.have_orgasm()
                        the_person "Trust me sweetie, keep going!"
                        the_other_person "Ah! Ah! Ahhhhh!"
                        "Your orgasm builds up to the limit and you tense in preparation for your release."
                        "Finally she can take no more. She leans forward and wraps her arms around your neck and collapses completely. Her weight pushes her completely down onto your cock."
                        "You can feel her pussy tense and untense as she is wracked by her orgasm, and you begin unloading yourself inside of her."
                        $ the_other_person.cum_in_vagina()
                        "You hold her down on you for a little while while you finish, then you both sit and pant loudly."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                        "[the_other_person.title] gives her a kiss on the cheek."
                        the_person "Good girl, good girl."
                        "[the_other_person.title] gets up slowly, dripping cum from her pussy as she does. She flops onto the couch beside you."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                        $ the_person.have_orgasm()
                        "[the_person.title] rubs her clit until she spasms from her own orgasm, and the three of you rest together until you're able to get up and go to bed."
                    "Cum inside [the_person.title].":
                        mc.name "I'm getting close, it's your turn [the_person.title]!"
                        "[the_other_person.title] bounces up and down on your cock a few more times and you feel her legs start to flutter from her orgasm. She collapses beside you and begins fingering herself, gasping loudly."
                        $ the_other_person.have_orgasm()
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                        the_person "Okay, take me!"
                        $ scene_manager.update_actor(the_person, position = "standing_doggy")
                        "[the_person.title] bends over the couch and waits for you to get set up behind her. You waste no time and thrust into her while [the_other_person.title] moans and gasps beside you both."
                        "Within a few strokes you're ready to finish and you pull [the_person.title]'s ass tight against your waist. You spasm a few times, unloading deep inside her, and feel her pussy tighten in response."
                        $ the_person.cum_in_vagina()
                        $ scene_manager.update_actor(the_person, position = "standing_doggy")
                        the_person "Yes, there it is!"
                        "She shakes and moans, and reaches her own orgasm."
                        $ the_person.have_orgasm()
                        "You give [the_person.possessive_title] a few more strokes while she finishes, then pull your wet cock out and watch as a little bit of cum trickles down her thigh."
                        $ scene_manager.update_actor(the_person, position = "sitting")
                        "[the_other_person.title] screams loudly and collapses completely, and you two join her on the couch. You sit still for a long while catching your breath."
                    "Cum in their mouths.":
                        mc.name "I'm almost there, I want to cum in your mouths!"
                        the_other_person "Ahh! Okay!"
                        the_person "I'm ready!"
                        "You pump a few more times and feel [the_other_person.title] start to shake from her own orgasm. You tense up and get ready to release, and smack her ass up to get her moving."
                        $ the_other_person.have_orgasm()
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob", special_modifier = "blowjob")
                        "[the_other_person.title] slumps to the floor at your feet and throws her mouth over your tip as you pulse out a heavy load of cum."
                        $ the_other_person.cum_in_mouth()
                        "She moans and fingers herself while you release into her."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "blowjob")
                        "After a while she sits back and opens her mouth, showing you her mouthful of hard earned cum."
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        "[the_person.title] joins her on the floor and leans over her. She pulls [the_other_person.title] into a deep kiss."
                        $ the_person.cum_in_mouth()
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        "They make out for a long moment, then [the_person.title] looks up and opens her mouth to show it full of cum as well now."
                        "Both of them swallow and display their empty mouths to you after."
                        the_person "There we go, all taken care of."
                        "[the_other_person.title] just pants, shaking from exertion."
                        "The two get up and join you on the couch, recovering from the night's activities."
                    "Cum on both of them.":
                        mc.name "I'm almost there. I want to finish on top of both of you."
                        "[the_other_person.title] moans and nods her head quickly. [the_person.title] drops onto the floor and plays with her tits."
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        the_person "Okay, I'm ready."
                        "[the_other_person.title] bounces up and down a few times until she reaches her own orgasm. Her tightening pussy sets off your own, and you lift her up quickly."
                        $ the_other_person.have_orgasm()
                        "She slumps to the ground and [the_person.title] pulls her close, holding her tits up to present them to you."
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        "You stroke yourself to completion, letting your load out first onto [the_person.title]'s face, then [the_other_person.title]'s face and tits."
                        $ the_person.cum_on_face()
                        $ the_other_person.cum_on_face()
                        $ the_other_person.cum_on_tits()
                        $ scene_manager.update_actor(the_person, position = "kneeling1")
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "kneeling1")
                        mc.name "There we go, take it all!"
                        the_person "Let it out [the_person.mc_title]!"
                        "After you finish you sit back on the couch and look at [the_person.possessive_title] and [the_other_person.title] covered in your load. [the_other_person.title] is still panting, body limp from cumming."
                        "Eventually she and [the_other_person.title] join you on the couch, and you spend a few minutes catching your breath."
                        $ scene_manager.update_actor(the_person, position = "sitting")
                        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
                "Later that night you head to your room, confident you had a huge effect on both of them tonight."
                $ the_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 60)
                $ the_other_person.change_slut(2 + the_person.get_opinion_score("being submissive"), 60)
            else:
                if person_score > 0:
                    the_other_person "What did you have in mind?"
                    mc.name "Well, I was thinking that you and [the_person.title] could lean over the couch while I take you from behind."
                    the_other_person "Me and [the_person.title] together? Here in the living room. That doesn't sound okay. Are you okay with this [the_person.title]?"
                    the_person "Hmm? Oh, I guess you're right. That doesn't sound okay."
                    mc.name "It'll be fine. A great way to blow off stress in fact."
                    the_other_person "I don't think so. I just want to watch the movie."
                    the_person "Don't bother [the_other_person.possessive_title] [the_person.mc_title]. Let's just watch the movie."
                    "[the_other_person.title] must have resisted the serum. No use pushing it now."
                    mc.name "Alright, never mind. Forget I brought it up."
                    "The three of you finish the movie and head up to bed. You feel like you could have done more to take advantage of the situation."
                else:
                    the_other_person "Right here in the living room? That sounds really naughty."
                    mc.name "And you're a naughty girl, right [the_other_person.title]?"
                    the_person "[the_person.mc_title]! Don't talk about [the_other_person.possessive_title] like that."
                    mc.name "I was just saying, if she's into it she's a dirty girl."
                    the_person "And I'm saying to stop it. This is the family living room, I'm not allowing it."
                    mc.name "But it's just a way of relaxing, it'll be good for all of us."
                    the_person "I said no and that's final. Now let's just watch the rest of the movie."
                    "[the_person.title] must have resisted the serum. No point pushing it now."
                    mc.name "Alright, forget I said anything. A bad joke was all it was."
                    "The three of you watch the rest of the movie and head to bed. You feel like you could have done more to take advantage of the situation."
    return

label movie_group_watch(the_person, the_other_person):
    $ mc.change_location(hall)
    $ lowest_slut = 0
    if the_person.effective_sluttiness < the_other_person.effective_sluttiness:
        $ lowest_slut = the_person.effective_sluttiness
    else:
        $ lowest_slut = the_other_person.effective_sluttiness
    if lowest_slut > 70 and mc.event_triggers_dict.get("movie_progress", 0) > 2:
        $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list(strip_feet = True))
        $ generalised_strip_description(the_other_person, the_other_person.outfit.get_full_strip_list(strip_feet = True))
        $ scene_manager.add_actor(the_person, position = "sitting")
        $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
        the_other_person "Hey [the_person.mc_title], we were getting a little bored of the movie. Mind if we change it?"
        "[the_person.title] and [the_other_person.title] have both stripped while you were getting the drinks. You pass out the glasses of wine, then sit down in the middle of the couch."
        mc.name "Sure, put on whatever you two want."
        the_person "We'll make sure it's something you'll enjoy."
        the_other_person "Now come on, we can't be here naked with you all bundled up like that. Relax, we're at home!"
        "[the_other_person.title] pulls at your shirt, encouraging you to take it off. You stand up and take off not only your shirt, but your pants and underwear too. [the_other_person.title] smiles when your hard cock comes out."
        the_other_person "There we go. Feeling better now?"
        mc.name "Ya. I think so."
        "You sit back down and watch while [the_person.title] scrolls through the different movies. She's gone straight to the adult film section and picks a parody porn film called \"Rock Hard: Deep Undercover\"."
        the_other_person "Ooh, that looks good. I think I've seen the first one."
        "The three of you sit back on the couch, completely naked, while the movie goes through the motions of introducing a plot. It doesn't take long before the main character, Rock Hard, is fucking a biker chick to earn her trust."
        "[the_other_person.title] moans softly while she watches another girl get railed, and rubs her pussy a little bit. [the_person.title] keeps her composure, but you can tell she's enjoying it."
        mc.name "You know girls, I'm feeling a little left out here..."
        "[the_person.title] looks over and stares at your erect penis."
        the_person "Oh, I'm sorry dear. How about we help you take care of that. Okay [the_other_person.fname]?"
        "[the_other_person.title] nods, her attention still on the girl getting railed in the movie."
        $ scene_manager.update_actor(the_person, position = "blowjob")
        "[the_person.title] gets down on her knees in front of you, taking your cock into her hand and rubbing it gently. After a few moments, she licks you from base to tip, then slides you into her mouth and starts blowing you."
        $ scene_manager.update_actor(the_person, position = "blowjob", special_modifier = "blowjob")
        mc.name "Wow, that feels great."
        "[the_person.title] nods a little and keeps going, while [the_other_person.title] fingers herself beside you."
        mc.name "Come on [the_other_person.title]. You're going to have to pull your weight around here!"
        $ scene_manager.update_actor(the_person, position = "kneeling1")
        $ scene_manager.update_actor(the_other_person, display_transform = character_left_flipped, position = "cowgirl")
        "You reach over and grab her by the waist, pulling her around and on top of you. [the_person.title] lets go of your cock and watches as you get [the_other_person.title] positioned above your lap, kneeling on the couch with her legs spread around you."
        mc.name "Ready?"
        "[the_other_person.title] looks down at your cock, already rubbing against her lips. She moans and nods."
        the_other_person "I'm all ready."
        "You hold onto her waist as she lowers herself onto you. Her pussy is already dripping wet, and you have no trouble sliding all the way in on the first stroke."
        the_person "That's a good girl [the_other_person.fname]. You're doing great."
        call fuck_person(the_other_person, private = False, start_position = cowgirl, start_object = make_couch(), skip_intro = True, girl_in_charge = True, position_locked = True)
        if the_other_person.has_creampie_cum():
            "She rocks her hips up and down a little until you're completely finished, then pulls up just enough to let you slip out and collapses sideways onto the couch."
            the_person "Wow, good job, both of you!"
            mc.name "Thanks [the_person.title]. You did a great job taking that load [the_other_person.title]."
            "[the_other_person.title] nods and smiles at you two while your cum leaks out of her pussy."
            the_person "[the_other_person.fname], you remember that talk we had about protection, right?"
            "[the_other_person.title] sits up carefully and cups a hand between her legs, catching your semen before it can drip onto the couch."
            the_other_person "Of course [the_person.fname], I'm being careful."
            the_person "I know, I just worry sometimes. Anyways, it's getting late. You should go get yourselves cleaned up."
            "The three of you say goodnight and head upstairs."
        elif the_person.has_creampie_cum():
            "She rocks her hips up and down a little until you're completely finished, then pulls up just enough to let you slip out and collapses sideways onto the couch."
            the_other_person "Wow, that was so hot!"
            mc.name "Thanks [the_other_person.title]. You did a great job taking that load [the_person.title]."
            "[the_person.title] nods and smiles at you two while your cum leaks out of her pussy."
            the_person "Now, [the_other_person.fname] why don't you clean this up for me"
            the_other_person "I'd love to [the_person.fname]."
            "[the_other_person.title] crawls between her legs and starts to suck out your cum."
            mc.name "Right. Goodnight then you two."
            "You head upstairs, leaving [the_other_person.title] and [the_person.title] to continue their fun."
        else:
            the_person "How was that [the_person.mc_title]? Feeling good?"
            mc.name "Oh ya. You both were amazing."
            the_person "Well, I better get all of this cleaned up, and you two should be heading to bed."
            mc.name "Right. Goodnight then you two."
            # split other cum locations
            "You head upstairs, leaving [the_other_person.title] collapsed on the couch and [the_person.title] wiping your cum off her tits."
    elif lowest_slut > 50 and mc.event_triggers_dict.get("movie_progress", 0) > 1:
        $ mc.event_triggers_dict["movie_progress"] = 3
        $ the_clothing = the_other_person.outfit.get_upper_top_layer()
        $ generalised_strip_description(the_person, the_person.outfit.get_underwear_strip_list())
        $ generalised_strip_description(the_other_person, the_other_person.outfit.get_underwear_strip_list())
        $ scene_manager.add_actor(the_person, position = "sitting")
        $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
        "You come back with the glasses of wine carefully balanced. [the_other_person.title] has just finished pulling her [the_clothing.display_name] off and chucks it into the corner of the room, while [the_person.title] is sitting down on the couch in just her underwear."
        the_other_person "Hey. Ready to start?"
        the_person "We were talking, what do you think about a different movie?"
        the_other_person "This one is kind of boring, to be honest."
        "You distribute the drinks and sit down between the girls."
        mc.name "Sure, whatever you two want."
        the_other_person "And come on, there's no way you're comfortable wearing all that. It's the weekend, relax a little!"
        "[the_other_person.title] pulls at your shirt while [the_person.title] brings up the movie list and starts scrolling through it."
        mc.name "Fine, fine. Here."
        "You pull your shirt off, then stand up and drop your pants too. Your hard cock presses against your underwear, and you see [the_other_person.title] notice it."
        mc.name "Happy?"
        the_other_person "Very."
        the_person "What do you guys want to watch?"
        the_other_person "Ooh, what about that? \"Rock Hard\". I think we saw the first one already."
        "You sit back down while [the_person.title] starts the movie."
        "The movie seems to follow a police officer, Rock Hard, through his daily life. Your memory is a little foggy about the original, but you're certain it had a higher production budget than this."
        "It's only when Rock arrests a girl and she pouts at him and asks \"Isn't there anything I could do to get out of this, officer?\" that you realize this isn't the sequel to the cop movie you watched before."
        "[the_other_person.fname] gasps a little when Rock pulls his cock out of his pants and flops it over the girl's face."
        the_person "Well! That took a sudden turn!"
        the_other_person "Are they allowed to show that?"
        the_person "It did say rated R..."
        "The girl in the back of the squad car opens her mouth wide and slips Rock's cock inside. She looks up at the camera with big eyes as she slides it back and forth."
        "You think about saying something, but decide to just watch how this plays out."
        "After a few minutes of deepthroating the girl, Rock turns her around and bends her over in the back of the car. [the_other_person.title] and [the_person.title] are both watching, eyes fixed on the screen while they pant softly."
        "[the_other_person.title]'s hand slides in between her legs, a single finger rubbing up and down her slit."
        "You reach a hand over and rub [the_other_person.title]'s leg, causing her to sigh a little. When your hand slides up her inner thigh she spreads her legs a little and pulls her own hand back."
        "[the_person.title] glances over and watches as you start to rub [the_other_person.fname]'s pussy through her panties."
        the_person "[the_other_person.fname], don't be selfish."
        "[the_other_person.title] nods and reaches over to your waist to pull your underwear down. With that out of the way she takes a hold of your cock and starts to jerk you off. You pull her panties out of the way and slip a finger inside of her."
        the_other_person "Of course. Sorry [the_person.fname]."
        call fuck_person(the_other_person, private = False, start_position = handjob, skip_intro = True, girl_in_charge = True, position_locked = True, ignore_taboo = False)
        "For a few minutes you all just sit and catch your breath, watching the credits roll on a movie you now notice is called \"Rock Hard: Precinct 69\"."
        the_person "I'll get this cleaned up. You two should get to bed."
        mc.name "Sure [the_person.title]. Thanks."
        "[the_other_person.title] stays on the couch for a while longer after you head upstairs, still breathing heavily."
    elif lowest_slut > 30 and mc.event_triggers_dict.get("movie_progress", 0) > 0:
        $ mc.event_triggers_dict["movie_progress"] = 2
        $ the_clothing = the_other_person.outfit.get_upper_top_layer()
        $ generalised_strip_description(the_person, the_person.outfit.get_underwear_strip_list())
        $ generalised_strip_description(the_other_person, the_other_person.outfit.get_underwear_strip_list())
        $ scene_manager.add_actor(the_person, position = "sitting")
        $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
        "You come back with the glasses of wine carefully balanced. [the_other_person.title] has just finished pulling her [the_clothing.display_name] off and chucks it into the corner of the room, while [the_person.title] is sitting down on the couch in just her underwear."
        the_other_person "Hey. We were just getting comfortable. Ready to start?"
        mc.name "Uh, ya. Sure."
        "You hand out the drinks and sit down on the couch between the girls."
        the_person "Me and [the_other_person.fname] were talking. Do you mind if we changed the movie to something more exciting? This is kind of..."
        the_other_person "Terrible, this movie is terrible."
        mc.name "No problem there. Put on whatever you would like."
        "[the_person.title] and [the_other_person.title] talk with each other while they scroll through your list of movies. Finally they agree on one titled \"Rock Hard: Precinct 131\", which looks like some sort of action movie."
        "The movie follows the story of Rock Hard, a loose cannon cop who doesn't play by the rules."
        "The girls gasp and turn away during the gunfights, but neither bat an eye when Rock takes a girl back to his squad car and shows her that his name isn't just for show."
        "As midnight rolls around the movie ends, Rock Hard victorious over the criminals and loved by all. [the_other_person.title] and [the_person.title] get their clothes back on, then head upstairs."
    else:
        $ mc.event_triggers_dict["movie_progress"] = 1
        $ scene_manager.add_actor(the_person, position = "sitting")
        $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, position = "sitting")
        "You return with the glasses of wine balanced carefully. The movie is put back on, and you all enjoy the evening relaxing with family."
        "As midnight rolls around the movie ends, and the three of you retire to your beds."
    $ scene_manager.clear_scene()
    return
