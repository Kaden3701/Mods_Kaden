init 5 python:
    def beach_date_invite_requirement():
        if time_of_day == 2:
            if get_beach_date_person():
                return True
        return False

    def get_beach_date_person():
        temp_list = []
        for person in known_people_in_the_game():
            if person.energy > 60 and person.is_available:
                    if person.love > 40 and person.love < 70:
                        if person.relationship == "Single" or person.has_role(girlfriend_role) or person.has_role(affair_role):
                            if not person.is_at_work():
                                temp_list.append(person)
        return get_random_from_list(temp_list)

    beach_date_invite = ActionMod("Beach Date Invite", beach_date_invite_requirement, "beach_date_invite_label",
        menu_tooltip = "Someone invites you to go to the beach with them.", category = "Mall", is_crisis = True, is_morning_crisis = False, priority = 5)


init 16 python:
    standard_beach_backgrounds = room_background_image("Beach_Background.png", darken = False)
    beach_objects = [
        make_floor()
    ]
    beach = Room("beach", "The Beach", [], standard_beach_backgrounds, beach_objects,[], [], False, [], None, False, lighting_conditions = standard_outdoor_lighting)
    #list_of_places.append(beach)



    def beach_get_choice(person):
        exhibition_score = (person.get_opinion_score("public sex") + person.get_opinion_score("not wearing anything") + person.get_opinion_score("showing her tits") + person.get_opinion_score("showing her ass"))/4.0
        tan_score = person.get_opinion_score("yoga") + exhibition_score
        sport_score = person.get_opinion_score("sports") + exhibition_score
        public_score = person.get_opinion_score("hiking") + exhibition_score
        walk_score = person.get_opinion_score("hiking") - exhibition_score
        beach_list = []
        beach_list.append(["tan_score", tan_score])
        beach_list.append(["sport_score", sport_score])
        beach_list.append(["public_score", public_score])
        beach_list.append(["walk_score", walk_score])
        choice = max(beach_list)
        return choice

    def get_beach_outfit(person):
        the_colour = person.favorite_colour()
        color_list = []
        for col in WardrobeBuilder.color_prefs[the_colour]:
            color_list.append(WardrobeBuilder.color_prefs[the_colour][col])
        main_colour = get_random_from_list(color_list)
        main_colour[3] = 1
        beach_outfit = Outfit("Beach")
        random = renpy.random.randint(1, 100)
        if 170-person.sluttiness-(10*person.get_opinion_score("showing her tits")) < random:
            if 50 < random:
                beach_outfit.add_upper(heart_pasties.get_copy(), main_colour)
        else:
            if random > 70:
                beach_outfit.add_upper(lingerie_one_piece.get_copy(), main_colour)
            else:
                top_list = []
                top_list.append(sports_bra.get_copy())
                top_list.append(strapless_bra.get_copy())
                top_list.append(strappy_bra.get_copy())
                beach_outfit.add_upper(get_random_from_list(top_list), main_colour)
        if not beach_outfit.get_panties():
            bottom_list = []
            bottom_list.append(plain_panties.get_copy())
            bottom_list.append(cotton_panties.get_copy())
            bottom_list.append(panties.get_copy())
            if person.sluttiness > 40:
                bottom_list.append(cute_panties.get_copy())
                bottom_list.append(kitty_panties.get_copy())
                if person.sluttiness > 60:
                    bottom_list.append(thong.get_copy())
                    if person.sluttiness > 80:
                        bottom_list.append(tiny_g_string.get_copy())
                        bottom_list.append(string_panties.get_copy())
            beach_outfit.add_lower(get_random_from_list(bottom_list), main_colour)
        beach_outfit.add_feet(sandles.get_copy(), main_colour)
        if beach_outfit.get_panties():
            color_list.append([1,1,1,1])
            color = get_random_from_list(color_list)
            color[3] = 0.7
            if person.sluttiness > 60:
                if random < 11:
                    beach_outfit.add_dress(bath_robe.get_copy(), color)
                elif random < 41:
                    beach_outfit.add_upper(suit_jacket.get_copy(), color)
            elif person.sluttiness > 30:
                if random > 10 and random < 41:
                    beach_outfit.add_dress(bath_robe.get_copy(), color)
                else:
                    beach_outfit.add_upper(suit_jacket.get_copy(), color)
            else:
                if random > 10 and random < 41:
                    beach_outfit.add_upper(suit_jacket.get_copy(), color)
                else:
                    beach_outfit.add_dress(bath_robe.get_copy(), color)
        return beach_outfit

    Person.get_beach_outfit = get_beach_outfit

init 3 python:
    def beach_requirement():
        if time_of_day == 4:
            return "Closed for the night"
        else:
            return True

    def beach_initialization(self):
        downtown.add_action(self)
        return

    beach_wrapper_action = ActionMod("Spend time on the beach {image=gui/heart/Time_Advance.png}", beach_requirement, "select_person_for_beach",
        initialization = beach_initialization, menu_tooltip = "Bring a person to the beach.", category = "Misc")

label beach_test(the_person):
    $ the_person.change_energy(100)
    $ original_slut = the_person.sluttiness
    $ the_person.sluttiness = 20
    while the_person.sluttiness < 100:
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        call beach_walk_label(the_person) from _call_beach_walk_label2
        $ the_person.change_energy(100)
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        call beach_public_label(the_person) from _call_beach_public_label2
        $ the_person.change_energy(100)
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        call beach_swim_label(the_person) from _call_beach_swim_label2
        $ the_person.change_energy(100)
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        $ mc.change_energy(100)
        call beach_volley_label(the_person) from _call_beach_volley_label2
        $ the_person.change_energy(100)
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        call beach_tan_label(the_person) from _call_beach_tan_label2
        $ the_person.change_energy(100)
        $ get_beach_outfit(the_person)
        $ the_person.draw_person(emotion = "happy")
        call beach_change_label(the_person) from _call_beach_change_label2
        $ the_person.change_energy(100)
        $ mc.change_energy(100)
        $ the_person.change_slut(15)
    $ the_person.sluttniess = original_slut
    return

label select_person_for_beach():
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_in_the_game(), "Spend time with", ["Back"])]))
    $ the_person = _return
    if the_person != "Back":
        "You send a text message to [the_person.title] about spending some time at the beach."
        "After some time you get a response..."
        call select_person_for_beach_response(the_person) from _call_select_person_for_beach_response
        call advance_time from _call_advance_time_beach
    return

label select_person_for_beach_response(the_person):
    if the_person.happiness < 100 or the_person.obedience < 70:
        $ the_person.draw_person(emotion = "sad")
        the_person "I'm not in the mood for the beach, right now."
        $ the_person.change_obedience(-2)
        $ clear_scene()
        return
    if the_person.personality == bimbo_personality:
        the_person "Cumming right away, [the_person.mc_title]!"
    elif the_person.obedience > 140:
        the_person "Yes, Sir. I am on my way."
    elif the_person.sluttiness > 30:
        the_person "Yes, [the_person.mc_title]. I am on my way."
    elif the_person.happiness < 120 and the_person.love > 20:
        $ the_person.draw_person(emotion = "happy")
        the_person "Thanks for the attention, [the_person.mc_title]."
        $ the_person.change_happiness(+10)
    else:
        the_person "Sounds good, I'll be right there, [the_person.mc_title]."
        $ the_person.change_happiness(+10)
    call beach_wrapper(the_person) from _call_beach_wrapper_person_for_beach
    return

label beach_date_invite_label():
    $ the_person = get_beach_date_person()
    $ the_person.change_location(downtown)
    if mc_at_work():
        "As you are packing up to head home for the day you get a text from [the_person.title]."
    elif mc_at_home():
        "As you are walking down the hallway in your house you get a text from [the_person.title]."
    else:
        "As you are wandering around you get a text from [the_person.title]."
    $ mc.start_text_convo(the_person)
    the_person "Hey [the_person.mc_title]! I just got to the beach. Do you want to come hang out with me?"
    menu:
        "Go to the beach":
            pass
        "Decline the date":
            mc.name "Sorry I can't right now. I've got other plans."
            the_person "Oh, okay. but you're really missing out."
            $ mc.change_location(beach)
            $ get_beach_outfit(the_person)
            $ the_person.draw_person(emotion = "happy")
            "To emphasize her point she sends you a picture of her standing on a sunny beach."
            $ mc.change_locked_clarity(the_person.sluttiness/5)
            "It is tempting to change you mind, but you commit to your original decision. Maybe next time you are downtown you could invite her to the beach."
            mc.name "I know, but I really do have things to do."
            the_person "Alright, your loss!"
            $ mc.end_text_convo()
            $ clear_scene()
            $ the_person.apply_planned_outfit()
            return
    mc.name "Yeah, that sounds great. I can be there soon."
    the_person "Great! I'll be waiting by the changing room for you."
    mc.name "See you soon."
    $ mc.end_text_convo()
    "A little while later you walk out onto the sandy beach."
    call beach_wrapper(the_person) from _call_beach_wrapper_invite
    $ clear_scene()
    return

label beach_wrapper(the_person):
    $ choice = None
    $ mc.change_location(beach)
    #if not the_person in beach.people:
    #    $ the_person.change_location(beach)
    $ beach_outfit = get_beach_outfit(the_person)
    $ the_person.apply_outfit(beach_outfit)
    $ the_person.draw_person(emotion = "happy")
    "Once you see [the_person.title], you walk up to her."
    mc.name "Hey, [the_person.title], it's good to see you."
    the_person "Hi, [the_person.mc_title] I'm so glad to be on the beach. What do you want to do?"
    menu:
        "Pick an activity" if the_person.love + the_person.obedience > 150:
            menu:
                "Let's go for a walk":
                    the_person "That sounds like fun. Which way do you want to go?"
                    menu:
                        "Away from the crowd":
                            mc.name "Let's go for a walk and do some exploring, see what there is to see."
                            the_person "Alright. Lead the way."
                            $ choice = "Walk"
                        "The same way as everyone else":
                            mc.name "Let's go for a walk along the beach; see what else is going on here."
                            the_person "Sounds good to me, lead the way!"
                            $ choice = "Public"
                "Let's go for a swim":
                    mc.name "How about we go for a swim, the weather seems perfect for it."
                    the_person "That sounds like a great idea [the_person.mc_title], lead the way!"
                    $ choice = "Swim"
                "Let's check out the volleyball courts":
                    mc.name "There are the volleyball nets set up, let's go take a look at those."
                    the_person "Me versus you? Sounds like fun, let's go!"
                    $ choice = "Volley"
                "Let's work on our tans":
                    mc.name "I'm thinking we should find a nice sunny spot and just relax."
                    the_person "That sounds nice. Lead the way."
                    $ choice = "Tan"
                "Let's get something to eat":
                    $ choice = "Change"
        "Let her pick":
            mc.name "Why don't you decide, I want you to have fun."
            $ the_person.change_happiness(5)
            if the_person.sluttiness < 30: #She is shy and we have work to do
                the_person "I'm not really sure, let's hang out up here, maybe get something to eat."
                menu:
                    "Yes\n{color=#ff0000}{size=18}Costs: $30{/size}{/color}" if mc.business.has_funds(30):
                        mc.name "Yes, that sounds good."
                        $ mc.business.change_funds(-30)
                        $ choice = "Change"
                    "Yes\n{color=#ff0000}{size=18}Requires: $30{/size}{/color} (disabled)" if not mc.business.has_funds(30):
                        pass
                    "No":
                        mc.name "Sorry, I'm a little short on cash."
                        the_person "What? You invited me to spend time with you and you don't have any money? Shouldn't you be at work then?"
                        $ the_person.change_happiness(-10)
                        return
            else:
                $ her_choice = beach_get_choice(the_person)
                if her_choice == "tan_score":
                    the_person "Well, since we are here on such a sunny day, let's lay out and soak up the sun."
                    mc.name "That sounds nice."
                    $ choice = "Tan"
                elif her_choice == "sport_score":
                    if renpy.random.randint(0,1) == 1:
                        the_person "I think they have volleyball nets here, let's go see if we can find a ball to play with."
                        mc.name "That sounds fun."
                        $ choice = "Volley"
                    else:
                        the_person "Well, the water is right there, let's go for a swim."
                        mc.name "Of course, that sounds great."
                        $ choice = "Swim"
                elif her_choice == "public_score":
                    the_person "I'm not really sure, let's walk for a bit and see what is going on."
                    mc.name "Sure, that sounds relaxing."
                    $ choice = "Public"
                else: #walk
                    the_person "I want to see what is around, let's go exploring."
                    mc.name "That sounds exciting."
                    $ choice = "Walk"
    if choice == "Walk":
        call beach_walk_label(the_person) from _call_beach_walk_label
    if choice == "Public":
        call beach_public_label(the_person) from _call_beach_public_label
    if choice == "Swim":
        call beach_swim_label(the_person) from _call_beach_swim_label
    if choice == "Volley":
        call beach_volley_label(the_person) from _call_beach_volley_label
    if choice == "Tan":
        call beach_tan_label(the_person) from _call_beach_tan_label
    if choice == "Change":
        call beach_change_label(the_person) from _call_beach_change_label
    if the_person.has_role(trance_role):
        call check_date_trance(the_person) from _call_check_date_trance_beach
    the_person "Thank you, [the_person.mc_title]."
    mc.name "Bye [the_person.title], see you next time."
    $ the_person.draw_person(position="walking_away")
    $ the_person.apply_planned_outfit()
    return

label beach_public_label(the_person):
    $ underwear_strip_description(the_person)
    $ the_person.draw_person(emotion = "happy")
    "You pick a direction along the beach and start walking by the water's edge."
    the_person "It's such a nice day out, we really got lucky."
    mc.name "Yeah, we did. I couldn't think of a better person to spend it with, either."
    the_person "Oh, very smooth. If I swoon will you catch me?"
    $ the_person.draw_person(position = "kissing")
    "She laughs and walks closer to you, wrapping one of her arms around yours."
    if the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 80 and not the_person.has_taboo("sucking_cock"):
        "After a few minutes of walking [the_person.title] slows down and lets go of your arm."
        mc.name "Everything alright?"
        while len(the_person.outfit.get_upper_ordered()) > 1:
            $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
        if the_person.outfit.get_bra():
            the_person "Yeah, I just need you to do me a favor. Pull on the knot for me, would you?"
            $ the_person.draw_animated_removal(the_person.outfit.get_bra(), position = "back_peek")
            "[the_person.title] spins around and presents the back of her swimsuit to you. You pull on the knot, and she proceeds to take the top off entirely."
            $ mc.change_locked_clarity(5)
            if the_person.outfit.get_panties():
                "Next she pulls the bottom down and steps out of it. She turns back to you, completely naked."
                $ the_person.draw_animated_removal(the_person.outfit.get_panties(), position = "back_peek")
        elif the_person.outfit.get_panties():
            the_person "Yeah, I just need to make a quick adjustment."
            $ the_person.draw_animated_removal(the_person.outfit.get_panties(), position = "back_peek")
            "She pulls her bottoms down and steps out of them, leaving herself completely naked."
        else:
            "BUG? What is she wearing?"
            $ naked_strip_description(the_person)
        $ mc.change_locked_clarity(5)
        the_person "There we go. If we're going to be walking around in the sun I don't want to end up with some ugly tan lines. Mind keeping these in your pocket?"
        "[the_person.title] hands over her suit, then holds onto your arm again. You resume your walk down the beach with [the_person.title]'s tits and pussy out in the open."
        "Not long after a group of guys further up the beach notice her and begin whistling and cheering as she passes."
        the_person "Oh, I bet they want a piece of me. Just look at them."
        if the_person.get_opinion_score("showing her tits") > 0:
            "[the_person.title] stops and turns towards them, cupping her breasts in her hands and playing with her nipples."
            $ mc.change_arousal(10)
            $ the_person.change_arousal(10)
            $ mc.change_locked_clarity(5)
            the_person "Is this what you want boys? Oh, I know it is!"
            "They cheer louder, thrusting beers into the air in celebration."
            "[the_person.title] turns back to you and runs a finger down your chest. When she reaches the waistband of your swimsuit she hooks it and pulls it down a little."
            the_person "I think we should give them a show they won't forget. Any objections?"
            mc.name "I think that's a great idea [the_person.title]."
        else:
            "[the_person.title] stops and turns to you."
            the_person "God, this got me so fucking horny. Can I suck you off, please?"
            "She reaches down and cups the bulge in your swimsuit, rubbing it slowly."
            mc.name "I'd love that [the_person.title]."
        $ the_person.draw_person(position = "blowjob")
        "She drops to her knees and pulls your swimsuit down low enough to free your hard cock."
        the_person "Oh, that looks nice. Let's have a taste."
        $ mc.change_locked_clarity(5)
        "[the_person.title] leans in and kisses the tip of your dick, then looks up at you while she slides it into her mouth."
        $ mc.change_arousal(10)
        $ the_person.change_arousal(10)
        mc.name "Damn, that feels great [the_person.title]."
        "She starts to blow you, bobbing her head up and down along your cock while she kneels in the sand. Up the beach the cheering gets even louder."
        "You rest a hand on the back of [the_person.title]'s head and run your fingers though her hair. She speeds up with each pass, her warm throat drawing you quickly towards your orgasm."
        call fuck_person(the_person, private = False, start_position = blowjob, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from call_fuck_person_beachpublicblow
        "You pull up your swimsuit and look around. The group of guys are cheering louder than ever, phones out while they take pictures of you and [the_person.title]. Other small groups of people have noticed as well, and are watching the two of you."
        mc.name "Come on, we should get going before someone comes along and gets us in any trouble."
        the_person "Right. Let's go."
        "She gets back onto her feet and takes your hand. You hurry up the beach until you've left the crowds behind."
        if the_person.has_mouth_cum() or the_person.has_face_cum():
            "[the_person.title] takes a quick trip down to the water, washing your cum off of her face before you keep going."
            $ the_person.outfit.remove_all_cum()
        "Soon you come to the end of the beach, where the sand is just a narrow strip next to the water."
        $ the_person.apply_outfit(beach_outfit)
        $ the_person.draw_person( position = "kissing")
        the_person "I guess that's all there is to see this way. I'm going to get dressed again, and then we can head back and do something else."
    elif the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 60:
        "After a few minutes of walking [the_person.title] slows down and lets go of your arm."
        mc.name "Everything alright?"
        while len(the_person.outfit.get_upper_ordered()) > 1:
            $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
        if the_person.outfit.get_bra():
            the_person "Yeah, I just need you to do me a favor. Pull on the knot for me, would you?"
            $ the_person.draw_animated_removal(the_person.outfit.get_bra(), position = "back_peek")
            "[the_person.title] spins around and presents the back of her swimsuit to you. You pull on the knot, and she proceeds to take the top off entirely."
            $ mc.change_locked_clarity(5)
            if the_person.outfit.get_panties():
                "Next she pulls the bottom down and steps out of it. She turns back to you, completely naked."
                $ the_person.draw_animated_removal(the_person.outfit.get_panties(), position = "back_peek")
        elif the_person.outfit.get_panties():
            the_person "Yeah, I just need to make a quick adjustment."
            $ the_person.draw_animated_removal(the_person.outfit.get_panties(), position = "back_peek")
            "She pulls her bottoms down and steps out of them, leaving herself completely naked."
        else:
            "BUG? What is she wearing?"
            $ naked_strip_description(the_person)
        $ mc.change_locked_clarity(5)
        the_person "There we go. If we're going to be walking around in the sun I don't want to end up with some ugly tan lines. Mind keeping these in your pocket?"
        "[the_person.title] hands over her bikini, then holds onto your arm again. You resume your walk down the beach with [the_person.title]'s tits and pussy out in the open."
        "Not long after a group of guys further up the beach notices her and begin whistling and cheering as she passes."
        the_person "Oh, I bet they want a piece of me. Just look at them."
        $ the_person.draw_person(position = "stand5")
        "She raises one arm and waves to them, bouncing her tits around a little bit while she's at it."
        mc.name "So that's why you wanted to take all that off, just so people could get a better look."
        the_person "Are you complaining? You get the best view in the house."
        $ the_person.draw_person(position = "kissing")
        "She cups a breast and pinches the hard nipple, rolling it between her thumb and forefinger."
        $ mc.change_locked_clarity(5)
        the_person "Ah... God I've gotten myself so wet..."
        $ mc.change_arousal(10)
        $ the_person.change_arousal(10)
        "[the_person.title] keeps walking, thighs held tightly together. After another ten minutes you've left most of the crowds behind, and she lowers her free hand to her pussy."
        $ the_person.draw_person(position = "walking_away")
        "She runs a finger along her slit a few times, then slips it in. She fingers herself as you walk, holding onto your arm tightly."
        the_person "Do you think those guys wanted to fuck me?"
        mc.name "Back there? Oh ya, they would have done it in a heart beat if you asked them."
        $ the_person.change_arousal(10)
        "[the_person.title] shivers against you, stumbling half a step as you walk."
        mc.name "They would have bent you over that beer cooler and fucked you raw."
        the_person "Oh god..."
        $ the_person.change_arousal(10)
        $ mc.change_locked_clarity(10)
        "She shivers again, and this time comes to a complete stop. You lean in close and whisper into her ear while she pumps a couple of fingers in and out of her cunt."
        mc.name "Then they would have cum all over you and left you there, so the whole world could see what a dirty slut you are."
        the_person "Ah!"
        $ the_person.have_orgasm()
        "[the_person.title] shouts out and wraps her free arm around you. Her hips buck a few times as she orgasms."
        "When she's done she slides her fingers out of her pussy and straightens up, taking a few deep breaths to compose herself."
        $ mc.change_locked_clarity(15)
        the_person "That was... really intense."
        mc.name "It sure looked like it."
        the_person "Come on, let's keep walking for a little bit."
        "You walk together until the beach is just a sliver of sand running along the waters edge. With nothing more to see, you turn around and stroll back towards the center of the beach."
        $ the_person.apply_outfit(beach_outfit)
        $ the_person.draw_person( position = "kissing")
        "[the_person.title] gets redressed before you get to the most populated sections, to avoid getting you both in trouble."
    elif the_person.effective_sluttiness(["underwear_nudity","bare_tits"]) > 40:
        while len(the_person.outfit.get_upper_ordered()) > 1:
            $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
        if the_person.outfit.get_bra():
            "After a few minutes of walking [the_person.title] slows down and lets go of your arm."
            mc.name "Everything alright?"
            the_person "Yeah, I just need you to do me a favor. Pull on the knot for me, would you?"
            if the_person.outfit.get_bra().has_extension:
                $ the_person.draw_animated_removal(the_person.outfit.get_bra(), half_off_instead = True)
            else:
                $ the_person.draw_animated_removal(the_person.outfit.get_bra(), position = "back_peek")
            "[the_person.title] spins around and presents the back of her swimsuit to you. You pull on the knot, and she proceeds to take the top off entirely."
            $ mc.change_locked_clarity(5)
            the_person "There we go. If we're going to be spending a lot of time walking around in the sun I don't want to end up with tan lines. Mind keeping this in a pocket or something?"
            $ the_person.draw_person( position = "kissing")
            "She hands you the top, then holds onto your arm again. You resume your walk down the beach, now with [the_person.title]'s tits out in the open."
        else:
            "You are a little suprised that she is so comfortable being topless around so many people."
            mc.name "Do you go out like this often?"
            the_person "If we're going to be spending a lot of time walking around in the sun I don't want to end up with tan lines."
            $ mc.change_locked_clarity(5)
            $ the_person.strip_to_tits(visible_enough = False)
            $ the_person.draw_person(position = "kissing")
        "Not long after a group of guys further up the beach notices her, and begin whistling and cheering as she passes. You feel [the_person.title] shiver, as if cold."
        $ the_person.change_arousal(10)
        mc.name "We can turn around if you want."
        the_person "No, it's fine. I'm sure it's nothing they haven't seen before."
        "You notice her nipples are rock hard, and she's carefully sliding her thighs together with each step."
        $ the_person.change_arousal(10)
        "Once you're past the group of men she takes a deep breath and relaxes her grip on your arm. Half an hour of walking passes, and the beach has become a thin strip of sand against the water."
        the_person "Well, I guess that's all there is to see this way. Let's head back and see if we have time to do something else."
        mc.name "Sure. Want to put your top back on?"
        "[the_person.title] shakes her head and takes your arm again, leading you back the way you came."
        the_person "No, I... I like the way it feels when people watch me like that."
        $ the_person.change_arousal(10)
        $ mc.change_locked_clarity(10)
        "You stroll back, chatting with each other as you go. [the_person.title] eagerly points out all of the men trying to take subtle glances at her tits, pressing up against your side tightly as you walk."
        $ the_person.apply_outfit(beach_outfit)
        $ the_person.draw_person(position = "kissing")
        "She finally puts her top back on when you get back to the heavily populated area of the beach, to avoid getting you both in trouble."
    elif the_person.effective_sluttiness("underwear_nudity") > 30:
        "You walk along the beach for a few minutes, passing by groups of people with umbrellas and tents set up."
        the_person "Hey, you see those guys over there?"
        "You follow [the_person.title]'s gaze up the beach, to a group of four guys standing around a cooler. They're not-so-subtly staring at [the_person.title] as she walks."
        mc.name "I'm not surprised they're interested, you're a good looking girl in a hot little bikini."
        the_person "I suppose you're right. Maybe I should give them a little peek, just to be nice."
        if the_person.outfit.get_bra():
            $ the_person.draw_animated_removal(the_person.outfit.get_bra(), half_off_instead = True)
        $ the_person.draw_person( position = "kissing")
        "She winks at you, then lets go of your arm and turns towards the group of men. With one quick movement [the_person.title] pulls her bra up over her tits, then gives them a little shake."
        "There's a pause, then the group erupts in wolf whistles and cheers."
        $ the_person.apply_outfit(beach_outfit)
        $ the_person.draw_person( position = "kissing")
        "[the_person.title] turns away and pulls her top back down, grabbing onto your arm again. You can feel her shaking a little against you."
        $ the_person.change_arousal(10)
        the_person "Come on, let's keep going."
        "You keep walking until you've left the crowds behind and the strip of sand has shrunk to a narrow sliver."
        the_person "Well, I guess that's all there is to see this way. Let's head back and see if we have time to do something else."
        mc.name "Sure. Plan on flashing those guys again?"
        the_person "I'm not sure I could take that much excitement all in one day. They'll have to be satisfied with what they got."
        "She grabs your arm and pulls you along."
        the_person "Now come on, let's get going!"
        "You stroll back, chatting with each other as you go."
    else:
        "You walk along the beach until you've left the crowds behind and the strip of sand has shrunk to a narrow sliver."
        the_person "Well, I think that's all there is to see this way. Let's head back and see if we have time to do something else."
        "You turn around and stroll back, chatting with each other as you go."
        the_person "That didn't take too much time, do you want to get something to eat when we get back?"
        menu:
            "Yes\n{color=#ff0000}{size=18}Costs: $30{/size}{/color}" if mc.business.has_funds(30):
                mc.name "Yes, that sounds good."
                $ mc.business.change_funds(-30)
                call beach_change_label(the_person) from _call_beach_change_label_public
            "Yes\n{color=#ff0000}{size=18}Requires: $30{/size}{/color} (disabled)" if not mc.business.has_funds(30):
                pass
            "No":
                mc.name "Sorry, I'm a little short on cash."
                the_person "What? You invited me to spend time with you and you don't have any money? Shouldn't you be at work then?"
                $ the_person.change_happiness(-10)
    return

label beach_change_label(the_person):
    "You and [the_person.title] head over to the snack bar, joining a long line of hungry beach goers."
    mc.name "This might take a while. There are some picnic tables up that way, you go save us one and I'll bring the food."
    the_person "Sure. Get me a hotdog, with mustard, and a drink."
    $ the_person.draw_person(position = "back_peek")
    if the_person.sluttiness > 40:
        "[the_person.title] waves goodbye and starts off towards the group of tables. More than a few heads turn to watch as she goes."
    else:
        "[the_person.title] waves goodbye and starts off towards the group of tables."
    $ clear_scene()
    "After a few minutes waiting in line you've got food for you and [the_person.possessive_title]. You stop off at a small bench to get everything organized on the tray."
    menu:
        "Leave her meal alone":
            $ the_person.draw_person(position = "sitting")
            "You catch up with [the_person.possessive_title], sitting across from her at the picnic bench."
            the_person "Thanks [the_person.mc_title], I think I really needed this!"
            mc.name "Me too. I'm starving!"
            "The two of you dig in, chatting with each other between bites. You end up talking long after you've finished your meals."
        "Put some serum in her drink" if mc.inventory.get_any_serum_count() > 0:
            call give_serum(the_person) from _call_give_serum_beach
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            if _return:
                $ dosed = True
                "You pull out some serum and mix it into [the_person.title]'s drink before catching up with her at the picnic tables."
            else:
                $ dosed = False
                "You change your mind and rush to catch up with [the_person.title] at the picnic tables."
            the_person "Thanks [the_person.mc_title], I think I really needed this!"
            mc.name "Me too. I'm starving!"
            "The two of you dig in. You wait a few minutes until [the_person.title]'s had most of her drink."
            $ influence = the_person.suggestibility
            if the_person.has_role(trance_role):
                $ influence +=20
            if the_person.has_exact_role(heavy_trance_role):
                $ influence +=20
            elif the_person.has_exact_role(very_heavy_trance_role):
                $ influence +=40
            if influence > 20:
                "Between the serum and your other influences it seems like [the_person.title] might be suggestible enough to follow orders at the moment."
                mc.name "Hey [the_person.title], I think I forgot something up by the change rooms earlier today. Would you mind coming with me while I check?"
                "[the_person.title] looks at you and nods slowly."
                the_person "Okay."
                $ the_person.draw_person(position = "stand3")
                "You lead [the_person.title] to the change rooms, finding them mostly empty at this time of day. You pick the stall farthest away from the parking lot and open up the curtain to it."
                mc.name "Hmm, I guess I was wrong. While we've got a moment up here, there's something else I wanted to do."
                the_person "What's that?"
                menu:
                    "Have her flash you her tits":
                        mc.name "I've been watching you in that swimsuit all day, and it's driving me a little wild. I was hoping you could just pull your top off and give me a look at your boobs."
                        if the_person.get_opinion_score("public sex") > 0:
                            "[the_person.title] barely even thinks about it before she pulls up her top and lets her tits fall free."
                            the_person "Are these what you wanted to see?"
                            $ the_person.strip_to_tits(visible_enough = True, prefer_half_off = True)
                            $ the_person.draw_person( position = "stands")
                            "She shakes her shoulders back and forth, jiggling her tits for you. You notice her nipples getting hard as you watch her."
                            $ mc.change_arousal(10)
                            mc.name "Yeah, just like that. You look great [the_person.title]."
                            "She smiles and cups her tits, squeezing them together."
                            the_person "Thank you. Let me know when you've seen enough."
                            "You enjoy the view for a few more seconds, until you see another couple heading your way from the beach."
                            $ mc.change_arousal(10)
                            mc.name "Okay [the_person.title], that will be enough for now."
                            $ the_person.apply_outfit(beach_outfit)
                            "She pulls her top back down, shaking her tits again to get them into place."
                        else:
                            "[the_person.title] thinks about it for a brief moment, then nods and steps into the stall. She motions for you to follow, and closes the curtain behind her."
                            $ the_person.strip_to_tits(visible_enough = True, prefer_half_off = True)
                            $ the_person.draw_person( position = "stand5")
                            "Once you're in the privacy of the changing room [the_person.title] pulls up her top, letting her tits fall free."
                            $ mc.change_arousal(10)
                            the_person "Are these what you wanted to see?"
                            "She shakes her shoulders back and forth, jiggling her tits for you. You notice her nipples getting hard as you watch her."
                            mc.name "Yeah, just like that. You look great [the_person.title]."
                            "She smiles and cups her tits, squeezing them together."
                            the_person "Thank you. Let me know when you've seen enough."
                            "You enjoy the view for a minute or two, watching [the_person.possessive_title]'s breasts bounce as she plays with them."
                            $ mc.change_arousal(10)
                            mc.name "Okay [the_person.title], that will be enough for now."
                            $ the_person.apply_outfit(beach_outfit)
                            "She pulls her top back down, shaking her tits one last time to get them into place."
                        mc.name "Let's head back to the bench and relax for a little while."
                        "You and [the_person.title] return to your seats."
                    "Have her get naked for you" if influence > 30:
                        mc.name "I've been watching you in that swimsuit all day, and it's been driving me wild. I want you to come in here and take it off for me so I can get a good look at you."
                        if the_person.sluttiness > 15:
                            "[the_person.title] barely even thinks about it before stepping into the changing room. You follow her in and close the curtain behind the two of you."
                            the_person "So, you want to see me naked then?"
                            $ the_person.strip_outfit(exclude_lower = True)
                            "She reaches behind her neck and undoes the top of her bikini, letting it fall forward first before pulling it off completely."
                            $ mc.change_arousal(10)
                            mc.name "Yeah, I do. You look amazing [the_person.title]."
                            the_person "Thank you. I guess I need to take these off too..."
                            $ the_person.strip_outfit()
                            "She pulls the knots on either side of her bikini bottom, letting it fall to the floor as it comes undone. In the small changing room, she's almost pressed up against you."
                            $ mc.change_arousal(10)
                            the_person "There you go [the_person.mc_title]. Anything else?"
                            mc.name "Turn around for me, so I can take a look at you from behind."
                            $ the_person.draw_person( position = "back_peek")
                            "She nods and turns around, planting her hands on the wooden sides of the shack and bending over as much as she can in the small space."
                            "You place a hand on her ass and give it a good squeeze, making [the_person.title] yelp."
                            $ mc.change_arousal(10)
                            the_person "Hey! Easy back there."
                            mc.name "Sorry. Just couldn't resist."
                            "You give her butt another squeeze, then let go entirely."
                            mc.name "Thank you [the_person.title], that was exactly what I wanted."
                            $ the_person.draw_person( position = "stand5")
                            "She turns back to you and picks up her bikini."
                            the_person "Good. Give me a moment to get dressed, please."
                            $ the_person.apply_outfit(beach_outfit)
                            "You step out of the change room and wait until [the_person.title] has her outfit put back together. Once that's done, you head back to your seats at the picnic bench and hang out a bit longer."
                        else:
                            "[the_person.title] thinks about it for a long moment, taking a slow step towards the changing stall."
                            the_person "You want me to take it all off? So you can see my..."
                            "She trails off, obviously unsure."
                            mc.name "That's right. I want to get a good look at my hot little [the_person.possessive_title]."
                            the_person "I'm not sure..."
                            mc.name "It's no big deal [the_person.title]. Come on, a quick peek and then we can head back to the table."
                            "She's quiet for another few seconds, then takes a step back and shakes her head."
                            the_person "I don't think I'm comfortable with that [the_person.mc_title]. If you can't find whatever you're looking for can we please just go?"
                            "She's got a sharp look in her eye now, pushing her any farther now would do more harm than good."
                            mc.name "Alright. Sorry [the_person.title], let's go get back to our seats."
                            "You and [the_person.title] return to the picnic table."
                    "Have her titfuck you" if the_person.has_large_tits() and influence > 50:
                        mc.name "I've been watching you in that swimsuit all day, and I've just wanted slip my dick between those perky tits of yours. Would you like to help me out with that?"
                        if the_person.sluttiness > 30:
                            "[the_person.title] thinks about it for a brief moment, then nods and steps past you into the stall. You follow her in, and close the curtain behind you."
                            the_person "I guess you can just lean against the wall and let me take care of you."
                            "You pull your swimsuit down, letting your hard cock spring free. [the_person.title] watches it bounce for a moment, then drops to her knees in front of you."
                            $ the_person.draw_person( position = "kneeling1")
                            mc.name "Here you go [the_person.title], go to town."
                            "You lean back while [the_person.title] takes her breasts up in her hands. She pulls them up and slips the tip of your dick between, then lets them down so you slide between her clevage."
                            "[the_person.title] pushes her tits together, sandwiching your cock, and starts to slide them together. Her bikini top stops you from sliding out the front as she goes."
                            mc.name "Ah, that feels great [the_person.title]. Keep going just like that."
                            "She nods and continues, rubbing her soft breasts up and down along your shaft. Soon your precum has gotten her cleavage nice and slippery as well."
                            call fuck_person(the_person, private = True, start_position = tit_fuck, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from call_fuck_person_beachchangetit
                            "She catches a few drips of cum with a finger as they run out from the bottom of her cleavage."
                            mc.name "I think there are some showers outside if you want to get cleaned up."
                            "[the_person.title] gets onto her feet and nods. You leave the changing room and head over to the showers. Once she's washed your sperm off of her chest, the two of you head back to your picnic bench and relax until the serum has worn off completely."
                            $ the_person.outfit.remove_all_cum()
                            $ the_person.apply_outfit(beach_outfit)
                        else:
                            "[the_person.title] thinks about it for a long moment, taking a slow step towards the changing stall."
                            the_person "You want me to use my boobs to get you off?"
                            mc.name "That's right. That bikini makes them look so good, I can't take my eyes off of them."
                            the_person "I'm not sure..."
                            mc.name "It's no big deal [the_person.title]. Come on, a quick tit fuck, then we can head back to the beach."
                            "She's quiet for another few seconds, then takes a step back and shakes her head."
                            the_person "No, I don't think so [the_person.mc_title]. You'll just have to control yourself until you get home and can jerk off or something."
                            "She's got a sharp look in her eye now, pushing her any farther now would do more harm than good."
                            mc.name "Alright. Sorry [the_person.title], let's go back to our seats."
                            "You and [the_person.title] return to the picnic table."
                    "Have her blow you" if influence > 70:
                        mc.name "I've been watching you in that swimsuit all day, and keep thinking about how good you would look on your knees in it. Let's step in here for a few minutes so you can suck me off."
                        if the_person.sluttiness > 45 and not the_person.has_taboo("sucking_cock"):
                            "[the_person.title] thinks about it for a brief moment, then nods and steps past you into the stall. You follow her in, and close the curtain behind you."
                            the_person "You just lean against the wall and leave everything to me."
                            $ the_person.draw_person( position = "kneeling1")
                            "[the_person.possessive_title] drops to her knees in front of you, pulling your swimsuit down low enough to let your hard cock spring free."
                            "She watches it bounce for a moment, then leans forward and kisses it. [the_person.title] swirls her tongue around the tip, then turns her head and runs it down the side of your shaft."
                            mc.name "That's it, get it all wet first."
                            "She changes sides and licks that side, then moves lower and licks up from your balls to the tip again. When she reaches the top she opens her mouth and slides you inside, starting off with a few shallow thrusts."
                            "[the_person.title]'s mouth is warm and wet as she blows you, going a little bit deeper with each pass."
                            mc.name "Come on, you can go deeper than that [the_person.title]."
                            "You place your hand on the back of her head and guide her, putting a little more pressure each time she slides your cock down her throat."
                            "Soon you've got her taking the full length of your cock, the tip rubbing against the back of her mouth each time she bobs her head forward."
                            mc.name "Fuck, that feels amazing [the_person.title]. You're going to have me cumming soon."
                            "[the_person.possessive_title] pulls off for air, taking a few deeps breaths before looking up at you again."
                            the_person "I don't have anything to get cleaned up with here. Just cum in my mouth, okay?"
                            mc.name "Sure. Come on, I'm almost there."
                            "You guide her gently back to your dick, and she resumes blowing you. Soon you feel your orgasm building as she throats you."
                            call fuck_person(the_person, private = True, start_position = blowjob, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from call_fuck_person_beachchangeblow
                            if the_person.has_mouth_cum():
                                "After a few seconds you've finished filling your little [the_person.possessive_title]'s mouth up with semen. She lets go of your shaft and slides your tip away from her lips."
                                mc.name "Open up for me, please."
                                "[the_person.title] rolls her eyes, then opens her mouth to show off the pools of cum you just put there."
                                mc.name "God that's so hot."
                                "[the_person.title] leans to the side and lets it all flow out into the sand. She spits out the last few drops at the end, then runs the back of her hand over her mouth."
                            if the_person.get_opinion_score("drinking cum") > 0:
                                the_person "All done. You tasted amazing [the_person.mc_title]."
                            else:
                                the_person "There, all done."
                            mc.name "Thank you [the_person.title], that was just what I needed. Let's head back to the table."
                            $ the_person.draw_person( position = "stand5")
                            "She gets up off her knees and follows you out of the changing room. You hang out together at the picnic table a bit longer."
                        else:
                            "[the_person.title] thinks about it for a long moment, taking a slow step towards the changing stall."
                            the_person "You want me to give you a blowjob? Here?"
                            mc.name "That's right. Something nice to finish the day off with."
                            the_person "I'm not sure..."
                            mc.name "It's no big deal [the_person.title]. A quick blowjob, then we can head back to the beach."
                            "She's quiet for another few seconds, then takes a step back and shakes her head."
                            the_person "No, I don't think so [the_person.mc_title]. You just go in there and jerk yourself off or something, I'm going to head back to the table."
                            "She's got a sharp look in her eye now, pushing her any farther now would do more harm than good."
                            mc.name "Alright, I'm sorry. Just forget I said anything at all, and let's get back to the table."
                            "You and [the_person.title] return to the picnic table."
                    "Fuck her" if influence > 90:
                        mc.name "I've been watching you in that swimsuit all day, wanting to rip it off of you. Let's just slip in here and have a quick fuck."
                        if the_person.sluttiness > 60 and not the_person.has_taboo("vaginal_sex"):
                            $ the_person.draw_person( position = "back_peek")
                            "[the_person.title] thinks about it for a brief moment, then steps past you into the stall. By the time you've stepped in after her and closed the curtain she's leaning against the far wall, wiggling her ass at you."
                            the_person "I'm so sorry, I didn't realize I was teasing you so badly."
                            "You step behind her and pull your swimsuit down, bouncing your hard cock against one of her ass cheeks."
                            mc.name "Well you were, and I'm going to need to take care of this now."
                            "You give her ass a smack, and she moans in response."
                            the_person "Whatever you have to do [the_person.mc_title]..."
                            "You squeeze [the_person.title]'s ass a few times, letting your cock rest between her cheeks. After that you lean forward and cup her breasts, sliding your hands under her bikini top."
                            "[the_person.title] rocks her hips against yours, grinding against your dick while you play with her tits."
                            mc.name "Turn around for me, I want to fuck you up against the wall."
                            $ the_person.draw_person( position = "stand5")
                            $ the_person.strip_outfit(exclude_lower = True)
                            "[the_person.title] stands up and turns around. You pull her top up and play with her breasts some more, enjoying the way her nipples harden as you do."
                            $ the_person.strip_outfit()
                            "Next you reach down and pull the bottom to the side, running a pair of fingers over her pussy. She gasps as you touch her, her cunt already dripping wet."
                            the_person "Oh [the_person.mc_title]... Ah..."
                            mc.name "Here, let's give you what you want."
                            "You lift up one of her legs and step forward, pinning her between the thin wooden wall of the changing room and your body. The tip of your penis brushes against her slit, making her moan again."
                            the_person "Please, please give it to me."
                            "You reach a hand down and line yourself up, then thrust forward slowly. [the_person.title] shivers against your body as you slide your cock as deep as you can into her."
                            mc.name "There we go. You're so wet [the_person.title], I can tell you need it."
                            "She nods and mumbles something, interrupted by a yelp as you start to pump in and out of her."
                            mc.name "What was that?"
                            the_person "Ah! I... I need your cock so badly!"
                            mc.name "I know you do, you dirty slut!"
                            "You lean forward and kiss [the_person.title]'s neck while you fuck her. She moans louder and rolls her hips to meet yours."
                            the_person "Oh god you feel so good! Ah! Yes!"
                            mc.name "Easy there [the_person.title], keep it down. Or maybe you want people to know how much you like getting fucked."
                            if the_person.get_opinion_score("public sex") > 0:
                                the_person "Ah! Fuck, I don't care! Just keep fucking me, I need it so badly [the_person.mc_title]. You feel so... good!"
                                "[the_person.title] moans loudly again, and you feel her pussy twitch around your cock."
                            else:
                                "[the_person.title] shakes her head and bites her lip, stifling another moan. You feel her pussy twitch around your cock."
                            call fuck_person(the_person, private = True, start_position = against_wall, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from call_fuck_person_beachchangefuck
                            "[the_person.title] follows you as you head back to the picnic table, pulling her bikini bottom back into place as you go. You hang out at the table until you've both recovered from the exertion."
                        else:
                            "[the_person.title] thinks about it for a long moment, taking a slow step towards the changing stall."
                            the_person "You really want to have sex with me? Right here?"
                            mc.name "That's right. I can't think of anything better to end the day with."
                            the_person "I'm not sure..."
                            mc.name "It's no big deal [the_person.title]. It's just a quickie, then we can head back to the beach."
                            "She's quiet for another few seconds, then takes a step back and shakes her head."
                            the_person "No, I don't think so [the_person.mc_title]. You just go in there and jerk yourself off or something, I'm going to head back to the table."
                            "She's got a sharp look in her eyes now, pushing her any farther now would do more harm than good."
                            mc.name "Alright, I'm sorry. Just forget I said anything at all, and let's get back to the table."
                            "You and [the_person.title] return to the picnic table."
            elif dosed:
                "Unfortunately the serum doesn't seem to be having a profound affect on her and she focuses on her food."
                "Maybe next time you should try to find a way to make her more docile and suggestible."
            else:
                "Unfortunately without a serum to affect her she seems happy to just eat with you."
                "Maybe you should make sure you have serums that would make her more docile or suggestible next time."
    return

label beach_swim_label(the_person):
    while len(the_person.outfit.get_upper_ordered()) > 1:
        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
    $ the_person.draw_person(emotion = "happy")
    "You and [the_person.title] wade out into the lake, walking along the sandy bottom until it is up to your waist. At that point the two of you lunge forward and begin swimming out farther."
    "[the_person.title] keeps pace with you easily, carving through the water with strong, steady, strokes."
    "Soon you slow down, a fair distance from the shore, and tread water while you catch your breath."
    mc.name "You don't even look tired... How do you do it?"
    if the_person.age < 30:
        the_person "Practice, [the_person.mc_title]. In high school I was on the swim team, and I still keep up some of the conditioning."
    else:
        the_person "Practice, [the_person.mc_title]. Back in high school I was on the swim team, it all comes back pretty quickly."
    if the_person.sluttiness > 70 and not the_person.has_taboo("vaginal_sex"):
        "[the_person.title] floats close to you and wraps her arms around your chest from behind."
        the_person "There were a few things I never got to try back then though. Would you like to try something with me?"
        "One of her hands slides below the water, feeling the bulge in your swim suit."
        mc.name "I think I would. What did you have in mind?"
        the_person "Back in high school the other girls had worked out a way of having sex in the pool, but I never got to try it."
        $ mc.change_locked_clarity(5)
        "Her hand slides inside the waist of your swimsuit, wrapping around your hard shaft."
        mc.name "Only one way to solve that then. Let me know what to do."
        "[the_person.title] pulls your cock out of your swimsuit, then lets go. She lies on her back and spreads her legs, pausing for a moment to pull her tiny swimsuit to the side."
        the_person "Pull yourself close to me, and push my hips under the water a little bit. If you just pull my bikini to the side, you should be able to slip right in."
        $ the_person.draw_person(position = "missionary")
        "You nod and grab her by the hips. It doesn't take much force to move [the_person.title] around in the water, and soon you've got her positioned on front of you, with the tip of your penis lined up with her pussy."
        $ the_person.strip_to_vagina(visible_enough = True, prefer_half_off = True, position = "missionary", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1)
        call condom_ask(the_person) from _call_condom_ask_beach_swim
        if not _return:
            "[the_person.title]'s refusal has sucked the wind from your sails. You pull your swimsuit back up."
            "At least you're no longer feeling as horny as you were, and you're able to focus on swimming."
        else:
            the_person "That's right. Now we'll have to take it slow. The water isn't as lubricating as you might think."
            "You pull her hips towards you slowly, sinking into her cunt inch by inch. [the_person.title] arches her back and moans as you enter her."
            mc.name "Damn, you feel so tight like this. It feels great."
            the_person "Oh [the_person.mc_title], you feel so big. Ah..."
            "You pause when you've gotten your full length inside of [the_person.possessive_title]. The waves on the lake bounce you both up and down, and the coolness of the water contrasted with the warmth of her pussy sends shivers up your spine."
            the_person "Okay, I think I'm wet enough for you to keep going. Oh lord..."
            mc.name "Just relax and let me take care of you [the_person.title]."
            "You start to thrust in and out of your [the_person.title], supporting yourself in the water by holding onto her hips."
            the_person "Ah... that's it. Give it to me right there. Nice and slow. Ah..."
            "The water makes you feel weightless, with each pump pushing [the_person.possessive_title] away from you. You tighten your grip on her to stop her from floating away."
            "For a few minutes you are both silent, enjoying the strange sensations."
            "You pick up the pace, sliding in and out of your the_person as fast as your position will allow."
            call fuck_person(the_person, private = True, start_position = missionary, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachswimsex
            if not the_person.has_ass_cum() or the_person.has_tits_cum() or the_person.has_stomach_cum() or the_person.has_creampie_cum():
                    "[the_person.title] takes a moment to just float, then straightens up in the water."
            else:
                    "[the_person.title] takes a moment to just float, then straightens up in the water and washes your cum off of her."
            the_person "Let's head back to shore, I'm feeling a little tired out by all of that."
        "You swim back and return to firmer ground. You notice [the_person.title]'s legs still shaking a little when she walks ashore."
    elif the_person.sluttiness > 40:
        "[the_person.title] floats close to you and wraps her arms around your chest from behind."
        the_person "I learned a few things back then; you can do almost anything in the water."
        $ mc.change_locked_clarity(5)
        "Her hands rub along your chest for a few moments, then one slips below the water and towards your crotch."
        the_person "I wanted to thank you for inviting me out here [the_person.mc_title]. It's so nice to get some time to spend with my [the_person.mc_title], and to get to go swimming again."
        if mc.arousal < 30:
            $ mc.change_arousal(30)
        mc.name "It's no problem at all [the_person.title]. My pleasure."
        "Her hand slides into your swimsuit, brushing against your already hard cock."
        the_person "Just relax and let me thank you properly. I know my swimsuit got you excited. Those trunks really don't hide it very well."
        $ mc.change_locked_clarity(5)
        "She pulls the waist of your swimsuit down, then wraps her hand around your shaft and strokes it gently. The water is a little chilly, but her hand is warm and soft."
        "You and [the_person.title] tread water while she holds onto you from behind, hand sliding up and down your cock."
        mc.name "That feels great [the_person.title]."
        the_person "Good. Cum whenever you're ready."
        call get_fucked(the_person, the_goal = "get mc off", sex_path = None, private= True, start_position = handjob, start_object = None, skip_intro = True, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_beachswimhand
        "She strokes you off as you climax, pulsing your load out into the water. When you're done lets go and pulls your swimsuit back into place."
        the_person "There we go, all done."
        "[the_person.title] pushes away from you and lies down, floating on her back. You do the same, floating next to [the_person.possessive_title] for an hour."
        if the_person.energy > mc.energy:
            "When you're ready to head back to shore you make it a race, and [the_person.title] beats you by a mile."
            mc.name "Next time, ah... I'll beat you next time..."
            the_person "I'm sure you will [the_person.mc_title]. I'll try not to tire you out so much next time."
        elif the_person.energy + 50 > mc.energy:
            "When you're ready to head back to shore you make it a race, and [the_person.title] is surprised by how close you get to beating her."
            mc.name "Next time, ah... I'll beat you next time..."
            the_person "You actually might [the_person.mc_title]. I'll have to try to tire you out more next time."
        else:
            "When you're ready to head back to shore you make it a race, and [the_person.title] is stunned when you beat her."
            the_person "Next time, ah... I'll beat you next time..."
            mc.name "I'm sorry [the_person.title]. I guess you already got your work out for the day."
    else:
        "She lies on her back, taking a deep breath."
        the_person "It's so nice to be out here. I used to go swimming every day, but there just isn't any time now."
        mc.name "We'll have to do this more often then. I'm sure there are a lot of things you could teach me."
        if the_person.sluttiness > 20:
            the_person "I'd like that. I certainly learned a lot back in high school, but I'm not sure it would be all that useful to you."
            mc.name "Oh? Like what?"
            the_person "The swim team used to practice every morning, and us being teenagers we were swimming in hormones just as much as water."
            the_person "The guys couldn't keep their hands off us in our little swimsuits, and some of the girls were more than happy for the attention."
            the_person "So some of the team got pretty good at sneaking in a little fun while the rest of us were practicing. We'd be swimming laps while some couple had a quicky in the deep end."
            $ mc.change_locked_clarity(5)
            mc.name "What about you, did you ever get up to that kind of stuff?"
            the_person "Me? Oh, nothing serious. I never worked up the courage to go all the way in the pool, the most I ever did was jerk a guy off in the water."
            $ mc.change_locked_clarity(5)
            mc.name "Lucky guy."
            the_person "Oh stop. Come on, let's just relax for a little bit."
            "You and [the_person.title] float in the water next to each other for an hour."
        else:
            the_person "I'd like that. Here, let me start with this."
            "[the_person.title] straightens up in the water and floats close to you."
            the_person "You'll tire yourself out if you keep flailing your arms around like that. Just take a deep breath and relax, move your legs slowly and let the water support you."
            "You inhale and slow your arms a little. You slip lower down in the water, but nowhere close to sinking below the surface."
            the_person "There you go. You could keep that up for hours if you had to."
            "[the_person.title] lies back down again in the water, and the two of you just float for an hour."
        if the_person.energy > mc.energy:
            "When you're ready to head back to shore you make it a race, and [the_person.title] beats you by a mile."
            mc.name "Next time, ah... I'll beat you next time..."
            the_person "I'm sure you will [the_person.mc_title]. I'll try not to tire you out so much next time."
        elif the_person.energy + 50 > mc.energy:
            "When you're ready to head back to shore you make it a race, and [the_person.title] is surprised by how close you get to beating her."
            mc.name "Next time, ah... I'll beat you next time..."
            the_person "You actually might [the_person.mc_title]. I'll have to try to tire you out more next time."
        else:
            "When you're ready to head back to shore you make it a race, and [the_person.title] is stunned when you beat her."
            the_person "Next time, ah... I'll beat you next time..."
            mc.name "I'm sorry [the_person.title]. I guess you already got your work out for the day."
    return

label beach_walk_label(the_person):
    $ the_person.draw_person(emotion = "happy")
    "You pick one direction along the beach and walk by the water's edge. You pass by the volleyball courts, taking a moment to watch a set between two pairs."
    "Past that, the beach gets narrower and narrower, the water coming closer to a small cliff on one side."
    "Soon you've left the crowds behind, with only the occasional stranger passing by. [the_person.title] steps closer to you and takes your hand in hers."
    the_person "Thank you for inviting me out here [the_person.mc_title]."
    mc.name "No problem at all [the_person.title]. It's my pleasure."
    the_person "I'm sure it is, you've been staring at me in this swimsuit all day."
    mc.name "Guilty as charged. You look great in it."
    "[the_person.title] giggles and pulls closer to you, pressing up against your arm while you walk."
    "Eventually you come to a rocky outcropping that runs from the cliff down to the water, blocking your path."
    mc.name "I guess this is the end of the road. Come on, let's head back."
    if the_person.sluttiness > 30:
        $ the_person.draw_person(position = "walking_away")
        "[the_person.title] lets go of your hand and heads over to the rocks, climbing the first few to get a better view."
        the_person "Oh cool, there's a little cove back here. Come on, we can just swim around the side."
        mc.name "Fine, just be a little careful."
        while len(the_person.outfit.get_upper_ordered()) > 1:
            $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
        "You follow [the_person.title] and wade through the chest high water until you can clear the rocks, then head up the beach onto the other side. You find a small cove; twenty feet of private beach with a short cliff blocking the far side."
        the_person "This is great! It's so private back here. In fact..."
        if the_person.sluttiness > 80 and not the_person.has_taboo("anal_sex"): # needs a better intro
            "[the_person.title] presses herself against you before you can even get clear of the water, wrapping her arms around your waist and grinding her hips against yours."
            $ the_person.draw_person(position = "stand2")
            the_person "Mmm, I can feel how hard you are already. I'm sorry I've been teasing you all day with this swimsuit."
            "You wrap your arms around [the_person.possessive_title], hands on her ass. You give her a quick spank, making her gasp."
            $ spank_factor_increment(the_person)
            mc.name "You aren't sorry, and I know it."
            "She giggles and nods, pressing her tits against your chest."
            $ mc.change_locked_clarity(5)
            the_person "I'm not, but I want to do something about it now that we have the chance."
            $ mc.change_arousal(10)
            $ the_person.change_arousal(10)
            "[the_person.title] reaches for your swimsuit and pulls it down, your hard cock springing free to rub against her stomach."
            "She gasps and runs a finger along it's length."
            the_person "Oh, it's so big... Here, I know exactly what you want."
            "She spins around in your grip and bends forward, grinding her ass against you now."
            $ the_person.strip_to_vagina(visible_enough = True, prefer_half_off = True, position = "stand2", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1)
            "You hook a finger under [the_person.title]'s tiny swimsuit and pull it to the side. She moans softly when you rub the tip of your cock against her pussy."
            mc.name "I think you want this just as badly as me, right? You're dripping wet already."
            $ mc.change_arousal(10)
            $ the_person.change_arousal(10)
            "[the_person.title] moans louder and nods."
            the_person "Go ahead, please. I want you to fuck me."
            "[the_person.title] wiggles her ass at you, pressing her hips back a little so your wet tip starts to slide inside."
            "You pull back on  [the_person.possessive_title]'s arms while you push forward, plunging your cock balls deep into her ass."
            the_person "Fuck! Ah!"
            call fuck_person(the_person, private = True, start_position = SB_anal_standing, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = False, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachwalkanal
            mc.name "That felt great [the_person.title]. Thanks."
            the_person "It really did. Ah..."
            "You hang around in the cove for a few minutes while you both catch your breath, then wade back around the rock outcropping again."
            $ the_person.apply_outfit(beach_outfit)
            "[the_person.title] takes your hand in hers while you take a slow stroll back to the center of the beach."
        elif the_person.sluttiness > 60 and not the_person.has_taboo("vaginal_sex"):
            "[the_person.title] presses herself against you before you can even get clear of the water, wrapping her arms around your waist and grinding her hips against yours."
            the_person "Mmm, I can feel how hard you are already. I'm sorry I've been teasing you all day with this swimsuit."
            "You wrap your arms around [the_person.possessive_title], hands on her ass. You give her a quick spank, making her gasp."
            $ spank_factor_increment(the_person)
            mc.name "You aren't sorry, and I know it."
            "She giggles and nods, pressing her tits against your chest."
            $ mc.change_locked_clarity(5)
            the_person "I'm not, but I want to do something about it now that we have the chance."
            $ mc.change_arousal(10)
            $ the_person.change_arousal(10)
            "[the_person.title] reaches for your swimsuit and pulls it down, your hard cock springing free to rub against her stomach."
            "She gasps and runs a finger along it's length."
            the_person "Oh, it's so big... Here, I know exactly what you want."
            "She spins around in your grip and bends forward, grinding her ass against you now."
            $ the_person.strip_to_vagina(visible_enough = True, prefer_half_off = True, position = "standing_doggy", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1)
            "You hook a finger under [the_person.title]'s tiny swimsuit and pull it to the side. She moans softly when you rub the tip of your cock against her pussy."
            mc.name "I think you want this just as badly as me, right? You're dripping wet already."
            $ mc.change_arousal(10)
            $ the_person.change_arousal(10)
            "[the_person.title] moans louder and nods."
            the_person "Go ahead, please. I want you to fuck me."
            call condom_ask(the_person) from _call_condom_ask_beach_walk
            if not _return:
                "[the_person.title]'s refusal has sucked the wind from your sails. You pull your swimsuit back up."
                "At least you're no longer feeling as horny as you were, and you're able to focus on the scenery."
            else:
                "You plunge inside of her, sliding your full length in on the first stroke."
                the_person "Oh fuck! Ah!"
                mc.name "God that feels good!"
                call fuck_person(the_person, private = True, start_position = SB_doggy_standing, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachwalksex
                mc.name "That felt great [the_person.title]. Thanks."
                the_person "It really did. Ah..."
            "You hang around in the cove for a few minutes while you both catch your breath, then wade back around the rock outcropping again."
            $ the_person.apply_outfit(beach_outfit)
            "[the_person.title] takes your hand in hers while you take a slow stroll back to the center of the beach."
        elif the_person.sluttiness > 40 and not the_person.has_taboo("sucking_cock"):
            $ the_person.draw_person(position = "kneeling1")
            "[the_person.title] turns back to you and drops to her knees; the water laps up against her thighs with each little wave."
            the_person "Pull down your swimsuit and let me give you a proper thank you for inviting me out here."
            "She licks her lips and winks at you, then watches while you pull your cock out for her."
            mc.name "Here you go, is this what you wanted?"
            "She nods and runs a finger along your hard shaft, tracing it's shape."
            $ mc.change_arousal(10)
            $ mc.change_locked_clarity(5)
            the_person "That's exactly what I wanted [the_person.mc_title]."
            "[the_person.title] leans forward and kisses the tip of your dick, then runs her tongue in circles around it. After getting it wet she bobs her head forward, slipping you into her mouth."
            mc.name "Oh fuck..."
            "[the_person.possessive_title] moans something in response, slowly sliding your cock in and out of her mouth."
            call get_fucked(the_person, the_goal = "get mc off", sex_path = None, private= True, start_position = blowjob, start_object = None, skip_intro = True, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_beachwalkblow
            $ the_person.draw_person(position = "stand3")
            "She gets up off her knees and looks around the cove."
            the_person "This place is nice, but we should probably head back soon if we want to do anything else today."
            mc.name "I suppose you're right. Come on, I'll lead."
            $ the_person.apply_outfit(beach_outfit)
            "You and [the_person.title] wade around the rock outcropping again, joining up on the other side. She takes your hand in hers, and the two of you take a slow stroll back to the center of the beach."
        else:
            "[the_person.title] looks around, then bites her lip and motions for you to come closer."
            the_person "I know you've gotten yourself a little worked up. Your swimsuit doesn't exactly leave much to the imagination. Just sit down here and let me take care of it for you, as a way of saying thanks."
            $ the_person.draw_person(position = "kneeling1")
            "You sit down on a mostly flat rock next to [the_person.title] She gets down onto her knees and gives you a wink, running her hand over the bulge in your swim trunks."
            mc.name "Here, let me get those out of the way for you."
            if mc.arousal < 30:
                $ mc.change_arousal(30)
            "You pull your swimsuit down, letting your hard cock free. [the_person.title] looks at it for a moment, then reaches out and takes it in her hand."
            the_person "It's so warm..."
            $ mc.change_locked_clarity(5)
            "[the_person.possessive_title] starts to stroke you off, running her hand up and down the length of your cock. You lean back and relax, enjoying the feeling for a few minutes."
            mc.name "That feels great [the_person.title] keep doing that."
            "She smiles and speeds up, playing idly with a breast while she jerks you off."
            call get_fucked(the_person, the_goal = "get mc off", sex_path = None, private= True, start_position = handjob, start_object = None, skip_intro = True, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_beachwalkhand
            $ the_report = _return
            if the_person.has_mouth_cum() or the_person.has_face_cum():
                the_person "Wow, that was hot."
                mc.name "Ah, yeah. Thanks [the_person.title]"
                $ the_person.draw_person(position = "walking_away")
                "She stands up and heads back to the waters edge, washing your semen off."
                $ the_person.outfit.remove_all_cum()
            else:
                the_person "I'm sorry, [the_person.mc_title]."
                mc.name "It's okay, I appreciate the effort."
            $ the_person.apply_outfit(beach_outfit)
            $ the_person.draw_person(position = "stand3")
            the_person "No problem. We should probably start heading back if we want to have time to do something else."
            "You get up and join [the_person.possessive_title], wading back out and around the rock outcropping. From there the two of you take a slow stroll back to the center of the beach."
    else:
        "[the_person.title] nods, and the two of you begin the slow stroll back to the center of the beach."
        the_person "That didn't take too much time, do you want to get something to eat when we get back?"
        menu:
            "Yes\n{color=#ff0000}{size=18}Costs: $30{/size}{/color}" if mc.business.has_funds(30):
                mc.name "Yes, that sounds good."
                $ mc.business.change_funds(-30)
                call beach_change_label(the_person) from _call_beach_change_label_walk
            "Yes\n{color=#ff0000}{size=18}Requires: $30{/size}{/color} (disabled)" if not mc.business.has_funds(30):
                pass
            "No":
                mc.name "Sorry, I'm a little short on cash."
                the_person "What? You invited me to spend time with you and you don't have any money? Shouldn't you be at work then?"
                $ the_person.change_happiness(-10)
    return

label beach_volley_label(the_person):
    while len(the_person.outfit.get_upper_ordered()) > 1:
        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
    $ the_person.draw_person(emotion = "happy")
    "You head off to the volleyball nets and take one of the empty sections of sand."
    the_person "Is there anywhere for us to get a ball? I didn't even think about bringing one."
    mc.name "Me neither. I didn't see anywhere that might have them."
    the_person "Oh well, we'll remember next time I guess."
    "Stranger" "Hey, I don't mean to eavesdrop, but we've got an extra ball if you need one."
    "The team on the court beside you has taken a break, and one of the players has a volleyball in one hand."
    the_person "That would be great, actually! Thanks!"
    "Stranger" "No problem at all. Just send it back over when you're done."
    "He throws [the_person.title] the ball and turns back to his friends."
    the_person "Alright [the_person.mc_title], let's do this! Ready?"
    mc.name "Ready, serve whenever you're ready."
    "[the_person.title] serves the ball to you, and you return it with a bump on your forearms. You rally it back and forth for a few minutes, one or the other ocacsionally scoring a point."
    "The game beside you ends, with two of the four players heading off down the beach. The two remaining players watch you and [the_person.title] play until you reach a natural breaking point."
    "Stranger" "You two are looking pretty good! What do you say to a team game, us vs you two."
    the_person "Sure, let's do it. Come on [the_person.mc_title]. Get over here and let's do this!"
    if the_person.effective_sluttiness("bare_tits") > 30:
        mc.name "Alright, you serve and I'll play up front [the_person.title]."
        "You get set up across from the other team. [the_person.title] serves, and they return the ball to you. After a short rally you jump and block the ball, scoring a point."
        "Stranger" "Damn! Nice one!"
        the_person "Nice [the_person.mc_title]!"
        "The four of you play for half an hour with the points surprisingly close."
        "Stranger" "Okay, this will have to be the last play for us guys. Ready?"
        the_person "I haven't been keeping count, so let's just make this winner takes all."
        "Stranger" "And what's the prize?"
        the_person "Well..."
        if the_person.effective_sluttiness("public_sex") > 50 and not the_person.has_taboo("sucking_cock"):
            "[the_person.title] cups her breasts and bounces them around a little."
            the_person "I don't have much in the way of cash that I could offer, but I'm sure there's something else I could do for you."
            "She runs a finger along her lips, sucking on it seductively at the end."
            the_person "What do you say [the_person.mc_title]?"
            mc.name "Well it's hard to say no to that. Let's just make sure we win, okay?"
            "[the_person.title] gives you a wink, then faces the other team."
            the_person "Okay, let's do this then!"
            "You play out the rally, barely saving the ball when it's spiked down past your guard. You pass it to [the_person.title], who's able to bump it over the net. The other team scrambles to return it, bumping it high in the air."
            the_person "Oh boys!"
            $ the_person.strip_to_tits(visible_enough = True, prefer_half_off = True)
            $ the_person.draw_person( position = "stand5")
            "[the_person.title] yells to get their attention, then pulls the top of her bikini up and lets her tits free."
            "Stranger" "Oh shit! Fuck!"
            "The two players on the other team stumble into each other, both missing the ball entirely. It falls to the sand, making you and [the_person.title] the winners."
            the_person "Yes! Woo!"
            "Stranger" "Damn! You cheated!"
            the_person "Me? No, I just used my natural charms."
            "[the_person.title] smiles innocently, her tits still out in the open."
            "Stranger" "I suppose. Well, good game, we've got to get going."
            the_person "Oh, you two aren't going to stay and watch me give our winner his prize?"
            "She steps up next to you and cups your package, rubbing it through your swimsuit."
            "Stranger" "Well, we weren't planning on it..."
            the_person "Come on, stay just a few minutes. It would mean a lot to me."
            "She drops to her knees and pulls your swimsuit down, letting your hard cock flop down onto her cheek."
            "Stranger" "Oh shit, this girls a freak!"
            "[the_person.title] opens her mouth wide and slides you in, looking up as she takes your cock down her throat. She pauses for a few seconds when her nose bumps against your stomach, her throat constricting and relaxing rythmically around your shaft."
            mc.name "Yeah she is. Look at her take that down. You love it, don't you [the_person.title]."
            "[the_person.title] nods as well as she can manage, then starts to bob her head up and down along your wet dick."
            "The two volleyball players watch while [the_person.title] sucks you off, right in the middle of the beach. Eventually some other people notice too, either turning to watch or turning away and pretending not to see anything."
            menu:
                "Cum on her face":
                    call get_fucked(the_person, the_goal = "facial", sex_path = None, private= False, start_position = blowjob, start_object = None, skip_intro = True, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_beachvolleyblow2
                    "When you're done you let your arms fall limp at your sides. [the_person.title] slides the tip of your cock back into her mouth and sucks off the last few drops of cum."
                    "After that, she pulls off again and turns towards the volleyball players, cleaning some of your semen off her face while she looks at them."
                    the_person "Maybe you'll get lucky next time guys!"
                    mc.name "Come on, we should probably go for a quick walk before someone shows up to throw us out of here."
                    "[the_person.title] pulls her bikini top back on, wiggling her tits into place, and follows you as you walk down the beach. You head inland a little bit and wait a few minutes in the shade under some trees before heading back."
                "Cum down her throat":
                    call get_fucked(the_person, the_goal = "oral creampie", sex_path = None, private= False, start_position = blowjob, start_object = None, skip_intro = True, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_beachvolleyblow
                    the_person "Thank you [the_person.mc_title], Ah... That felt great!"
                    "She turns to her side and winks at the two volleyball players."
                    the_person "Maybe you'll get lucky next time guys!"
                    mc.name "Come on, we should probably go for a quick walk before someone shows up to throw us out of here."
                    "[the_person.title] pulls her bikini top back on, wiggling her tits into place, and follows you as you walk down the beach. You head inland a little bit and wait a few minutes in the shade under some trees before heading back."
        elif the_person.effective_sluttiness(["bare_tits","bare_pussy"]) > 30:
            "[the_person.title] cups her breasts and bounces them around a little."
            the_person "How about I give the winner a good look at me. Sound good to you [the_person.mc_title]?"
            mc.name "Sounds fine to me, I'm sure we're going to win."
            the_person "I like the confidence. Let's do this then!"
            "You play out the rally, barely saving the ball when it's spiked down past your guard. You pass it to [the_person.title], who's able to bump it over the net. The other team scrambles to return it, bumping it high in the air."
            the_person "Oh boys!"
            $ the_person.strip_to_tits(visible_enough = True, prefer_half_off = True)
            $ the_person.draw_person( position = "stand5")
            "[the_person.title] yells to get their attention, then pulls the top of her bikini up and lets her tits free."
            "Stranger" "Oh shit! Fuck!"
            "The two players on the other team stumble into each other, both missing the ball entirely. It falls to the sand, making you and [the_person.title] the winners."
            the_person "Yes! Woo!"
            "Stranger" "Damn! You cheated!"
            the_person "Me? No, I just used my natural charms."
            "[the_person.title] smiles innocently, her tits still out in the open."
            "Stranger" "I suppose. Well, good game, we've got to get going."
            $ the_person.apply_outfit(beach_outfit)
            $ the_person.draw_person( position = "stand5")
            "[the_person.title] pulls down her bikini top and passes them their volleyball. They take it and head off, looking over their shoulders at [the_person.title]."
            the_person "Now, I think this was the deal if we won..."
            $ the_person.strip_outfit(exclude_lower = True)
            "She pulls her top up, letting her tits out. She gives them a quick shake for you, bouncing them left and right."
            the_person "Hmm, maybe you want a look at my pussy too, right? Here."
            $ the_person.strip_outfit(position = "doggy")
            "She turns around and bends over, pulling her swimsuit to the side."
            mc.name "Wow, you're looking really good today [the_person.title]."
            $ the_person.change_arousal(10)
            the_person "Thanks, all that activity got me worked up. Watching you play like that helped too, I'm a little bit wet actually."
            "She runs a finger along her pussy, pausing to play with her clit for a moment."
            $ the_person.change_arousal(10)
            "[the_person.title] gives her ass a quick smack, then stands up and pulls her swimsuit back into position."
            $ the_person.apply_outfit(beach_outfit)
            $ the_person.draw_person( position = "stand5")
            the_person "Alright, we should get moving before someone comes along to get us in trouble."
            mc.name "Yeah, you're right."
            "The two of you head back towards the center of the beach."

        else:
            the_person "Bragging rights of course."
            "Stranger" "Deal. Let's go!"
            "You play out a short rally, with the game ending when your opponent spikes the ball down past your block."
            the_person "No!"
            mc.name "Good game guys."
            "Stranger" "Yeah, that was fun. If we see you around some other time we'll have to do this again."
            the_person "Definitely. Would you two like your prize now?"
            "Stranger" "What prize?"
            $ the_person.strip_to_tits(visible_enough = True, prefer_half_off = True)
            $ the_person.draw_person( position = "kissing")
            "[the_person.title] slips her arms out of the top of her swimsuit, then pulls it down past her tits."
            "She gives them a quick shake, then pulls it back up again."
            $ the_person.apply_outfit(beach_outfit)
            the_person "That prize. See you next time."
            "She winks and passes the ball back to them."
            the_person "Come on [the_person.mc_title], let's head back towards the center of the beach."
    else:
        mc.name "Alright, you serve and I'll play up front [the_person.title]."
        "You get set up across from the other team. [the_person.title] serves, and they return the ball to you. After a short rally you jump and block the ball, scoring a point."
        "Stranger" "Damn! Nice one!"
        the_person "Nice [the_person.mc_title]!"
        "The four of you play for half an hour with the points surprisingly close."
        "Stranger" "Ah, that was fun you two. We've got to head out, but we're up for a game if you're ever around again."
        "You and [the_person.title] give them high fives and pass their ball back before they leave."
        the_person "Whew, that really got the blood flowing. Come on, let's head back."
    return

label beach_tan_label(the_person):
    $ the_person.draw_person(emotion = "happy")
    "You and [the_person.title] head down the beach, looking for a nice sandy spot without many people around."
    "After a few minutes of walking you find an ideal spot. You and [the_person.title] lay out your towels next to each other, facing towards the lake."
    while len(the_person.outfit.get_upper_ordered()) > 1:
        $ generalised_strip_description(the_person, the_person.outfit.get_upper_top_layer())
    $ the_person.draw_person(position = "stand2")
    "[the_person.title] lies back on her towel, closing her eyes and soaking in the sun."
    the_person "Excellent spot [the_person.mc_title]. Oh, before I forget..."
    "[the_person.title] sits up again and digs through the small bag she's brought with her. After a quick search she's got a bottle of sunscreen in hand."
    the_person "Do you need any?"
    mc.name "Sure, thanks."
    if the_person.sluttiness < 30:
        "[the_person.title] gives you a squirt of sunscreen, then plops some into her own hand and starts to spread it around."
    elif the_person.sluttiness < 50:
        if the_person.outfit.get_bra():
            "[the_person.title] lifts up the straps of her swimsuit a few times, then sighs and stands up. She pulls the straps over her shoulders, then pulls the entire thing off."
            the_person "This is just going to give me some terrible tan lines anyway."
            if the_person.outfit.get_bra().has_extension:
                $ the_person.strip_to_tits(visible_enough = True)
            else:
                $ the_person.strip_to_tits(visible_enough = False)
        else:
            the_person "I'm so glad I don't have to worry about tan lines from a top."
            $ the_person.strip_to_tits(visible_enough = False)
        $ the_person.draw_person(position = "stand3")
    else:
        if the_person.outfit.get_bra():
            "[the_person.title] gives you a squirt of sunscreen, then puts the bottle down and stands up. She pulls the straps of her swimsuit over her shoulders, then pulls the whole thing down and off."
        else:
            "[the_person.title] gives you a squirt of sunscreen, then puts the bottle down and stands up. She grabs the waist of her swimsuit, then pulls the whole thing down and off."
        $ the_person.strip_outfit()
        $ the_person.draw_person(position = "stand3")
        "She she kicks the swimsuit to the side and sits back down, taking a squirt of sunscreen for herself. She rubs it over the front of her body, paying special attention to her breasts. That done, she lies face down on her towel."
        the_person "[the_person.mc_title], could you get my back for me please?"
        $ the_person.draw_person(position = "walking_away")
        mc.name "No problem at all."
    if the_person.sluttiness > 75 and not the_person.has_taboo("sucking_cock"):
        the_person "Thank you. Once you're finished with me I'll make sure to repay the favors."
        "You take the bottle of sunscreen and lay a long line out over [the_person.title]'s back, stretching from her shoulder blades down to her ass. Then you start to spread it around and rub it in, working your way from top to bottom."
        "You spend a while playing with her butt when you reach it, kneading her cheeks with your hands as you rub the sunscreen in."
        $ the_person.draw_person(position = "sitting")
        "Eventually she rolls over and sits up."
        the_person "Thank you [the_person.mc_title]. Now you lie down and I'll make sure to take care of everything for you."
        "You lie down on your own towel, face down, and wait. [the_person.title] kneels beside you, squirts some sunscreen into her hand, and begins to rub your back."
        "She works her way down to your waist, then down to your legs."
        the_person "Roll over for me."
        $ the_person.draw_person(position = "cowgirl")
        "When you roll over [the_person.title] swings one leg across your body, straddling you. She rubs her hands down your chest, pausing for a brief moment to brush her thumbs over your nipples. Your erection rubs against her crotch, seperated only by your swimsuit."
        "[the_person.title] works her way lower, shuffling back as she goes. When she reaches your waist she pauses, hand resting on your hard shaft."
        the_person "Oh my. I'll have to take care of this while I'm at it I suppose."
        "She pulls your swimsuit down, letting your cock spring free. She leans forward and licks your shaft from balls to tip. When she reaches the top she opens her mouth and slides you in, quickly sliding you to the back of her throat."
        mc.name "Oh god that feels good."
        "[the_person.title] places her hands on your thighs while she blows you, taking every inch of your hard cock down her throat with each pass."
        call fuck_person(the_person, private = True, start_position = blowjob, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachtanblow
        "She reaches for her own towel and uses it to clean her face off, then lays it out again and lies down next to you. Feeling completely relaxed, you spend an hour dozing in the warm sun."
    elif the_person.sluttiness > 50:
        the_person "Thank you. Take as long as you need with my butt, I would hate to get a burn there."
        "You take the bottle of sunscreen and lay a long line out over [the_person.title]'s back, stretching from her shoulder blades down to her ass. Then you start to spread it around and rub it in, working your way from top to bottom."
        "Heading her advice, you take a good long time on her ass. [the_person.title] sighs softly while you play with her."
        the_person "That feels really good. Keep doing that, please."
        "You kneed her butt a little harder, enjoying how it feels in your hands. [the_person.title] seems to be having just as much fun, sighing occasionaly."
        the_person "Mmm, I think I've gotten a little wet. Could you check and make sure?"
        mc.name "Let's see..."
        "You reach a hand between [the_person.title]'s legs and run a finger along her pussy. She gasps when you brush past her clit."
        the_person "Oh, do that again."
        "You make little circles around [the_person.title]'s clit with your finger. She responds by arching her back and moaning quietly, her pussy now dripping wet."
        mc.name "Yes, you seem to be a little wet [the_person.title]."
        the_person "Keep touching me... Ah..."
        "She moans again, louder this time. You slide a pair of fingers into her cunt and start to finger her."
        "[the_person.title] grabs handfuls of her towel and gasps, her hips twitching against your hand."
        the_person "Keep going! Ah!"
        call fuck_person(the_person, private = True, start_position = standing_finger, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachtanfinger
        the_person "Thank you [the_person.mc_title]. Ah..."
        "You lie down on your own towel next to her. You pass an hour and a half in the sun, enjoying the warm summer day while you stare at [the_person.title]'s tits."
    elif the_person.sluttiness > 30:
        "She kicks the swimsuit to the side, then sits back down. She rubs some sunscreen over the front of her body, paying special attention to her breasts. That done, she lies face down on her towel."
        $ the_person.draw_person(position = "walking_away")
        the_person "[the_person.mc_title], could you do me a favor and get my back for me?"
        mc.name "No problem. It would suck to end up with a sunburn after a great day like this."
        "You take another squirt of sunscreen and kneel behind [the_person.title]. You run your hands along her back, starting with her shoulder blades and working down to her waist."
        the_person "And my legs, if you don't mind."
        mc.name "Of course not."
        "She spreads her legs a little, letting you run your hands along the inside and outside of her thighs."
        the_person "A little higher too. I don't want a burned butt, after all."
        "You take another squirt of sunscreen and move up to her ass, rubbing it in gently. [the_person.title] sighs softly while you kneed her butt cheeks."
        call fuck_person(the_person, private = True, start_position = standing_grope, start_object = None, skip_intro = True, girl_in_charge = True, self_strip = False, hide_leave = False, position_locked = True, affair_ask_after = False, ignore_taboo = False, skip_condom = True) from _call_fuck_person_beachtangrope
        the_person "Thank you [the_person.mc_title]. That was a huge help."
        mc.name "My pleasure [the_person.title]."
        "You lie down on your own towel next to her. You pass an hour and a half in the sun, enjoying the warm summer day while you stare at [the_person.title]'s tits."
    else:
        "Once she's covered her front she lies down on her towel, face down this time."
        $ the_person.draw_person(position = "walking_away")
        the_person "Could you do me a favor and get my back [the_person.mc_title]?"
        mc.name "No problem. It would suck to end up with a sunburn after a great day like this."
        if the_person.outfit.get_bra():
            "You take another squirt of sunscreen and kneel next to [the_person.title]. You run your hands along her back, lifting up the straps on her swimsuit to get all of her shoulder blades."
        else:
            "You take another squirt of sunscreen and kneel next to [the_person.title]. You run your hands along her bare back."
        the_person "Thank you. If you could get the back of my legs too, it would be a huge help."
        "You move down, give yourself another squirt of sunscreen, and start to rub her legs."
        the_person "Perfect. Just a little higher."
        "You move your hands up, spreading the sunscreen over her thighs. She spreads her legs a little, letting you reach her inner thighs."
        $ the_person.change_arousal(10)
        the_person "Ah... A little more, please."
        "You move higher still, now rubbing the lower part of [the_person.title]'s butt. She seems totally relaxed."
        the_person "Just pull the swimsuit up a little if you have to, make sure you get some sunscreen all around the edge."
        $ the_person.change_arousal(10)
        mc.name "Whatever you say [the_person.title]."
        "You work your hands around the periphery of her swimsuit, fingers slipping under the edge. [the_person.title] sighs softly as you run your hands over her ass."
        $ the_person.change_arousal(10)
        "[the_person.title] shows no sign that you should stop. For another minute you play with her ass, making sure every inch is covered with sunscreen. Eventually she rolls over onto her back again."
        $ the_person.draw_person(position = "stand3")
        the_person "Thank you [the_person.mc_title]. That was a huge help."
        mc.name "Any time [the_person.title]."
        "You lie down on your own towel next to her. You pass an hour and a half in the sun, just enjoying the warm summer day."
    return

label beach_outfit_test():
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_in_the_game(), "Beach Outfit Test", ["Back"])]))
    $ person_choice = _return
    if person_choice != "Back":
        $ start_slut = person_choice.sluttiness
        $ number = 1
        while number < 100:
            $ person_choice.sluttiness = number
            $ person_choice.apply_outfit(get_beach_outfit(person_choice))
            $ person_choice.draw_person(emotion = "happy")
            "Current sluttiness = [number]"
            $ number += 1
        $ person_choice.sluttiness = start_slut
        $ del person_choice
    return
    