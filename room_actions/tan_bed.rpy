init 3 python:
    def use_tan_bed_requirement():
        if not time_of_day == 0 and not time_of_day == 4:
            if mc.business.funds > 25:
                return True
            return "You need $25"
        return "Salon not open"

    def tan_bed_initialization(self):
        mall_salon.add_action(self)
        return

    tan_action = ActionMod("Schedule a tan {image=gui/heart/Time_Advance.png}", use_tan_bed_requirement, "tan_label", initialization = tan_bed_initialization,
        menu_tooltip = "Have a person get a tan.", category="Mall")

    bath_robe_bottom = Clothing("Bathrobe bottom", 2, True, False, "Bath_Robe_Bot", False, False, 0, is_extension = True, display_name = "robe bottom",
        can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [lower_arm_region, stomach_region], half_off_gives_access = True, half_off_reveals = True)
    bath_robe = Clothing("Bathrobe", 2, True, True, "Bath_Robe", True, False, 1, has_extension = bath_robe_bottom, supported_patterns = {"Flowers":"Pattern_1"}, display_name = "robe",
        can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
        constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region])

    towel_bottom = Clothing("Towel bottom", 2, True, False, "Towel_Bot", False, False, 0, is_extension = True, display_name = "towel bottom",
        can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_gives_access = True, half_off_reveals = True)
    towel = Clothing("Towel", 2, True, True, "Towel", True, False, 1, has_extension = towel_bottom, display_name = "towel",
        can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
        constrain_regions = [torso_region, stomach_region, skirt_region])

label tan_label():
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_in_the_game(), "Tan appointment", ["Back"])]))
    $ person_choice = _return
    if person_choice != "Back":
        "You send a message to [person_choice.fname] about the appointment."
        "After some time you get a response..."
        call tan_response(person_choice) from _call_tan_response
        $ del person_choice
    return

label tan_response(the_person):
    $ the_person.draw_person()
    if the_person.personality.personality_type_prefix == "bimbo":
        $ the_person.draw_person(emotion = "happy")
        the_person "Oh, [the_person.mc_title], like, I love tanning."
    elif the_person.love > 30:
        $ the_person.draw_person(emotion = "happy")
        the_person "Thanks for the attention, [the_person.mc_title]."
    elif the_person.obedience < 80 or the_person.happiness < 100:
        $ the_person.draw_person(emotion = "sad")
        the_person "I'm not in the mood for a spa day right now."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-2)
        $ clear_scene()
        return
    elif the_person.happiness > 120 or the_person.obedience > 120:
        the_person "Yes, [the_person.mc_title]. I am on my way."
    else:
        the_person "Sounds good, I'll be right there [the_person.mc_title]."
    call use_tan_bed(the_person) from _call_use_tan_bed
    $ mc.business.change_funds(-25)
    call advance_time from _call_advance_time_tan
    return

label use_tan_bed(the_person):
    $ the_person.draw_person()
    "Once she gets there you show her around the salon a bit."
    mc.name "And here is the tanning bed, I think it would do you a world of good."
    if the_person in mc.business.get_employee_list():
        the_person "Oh yes, you know the office could have bigger windows. Everyone there is so pale after working all week."
    else: # more unique people
        the_person "Oh yes, I don't spend nearly as much time outside as I'd like."
    mc.name "Great, now we just need to decide what you wear in there."
    if the_person.sluttiness > 80: #opinion showing
        the_person "I should probably just get naked."
        mc.name "I don't know, sometimes tan lines look good."
    else:
        the_person "Oh, right, it is kind of public here."
    the_person "What do you think I should do?"
    $ the_bra = the_person.outfit.get_bra()
    $ the_panties = the_person.outfit.get_panties()
    $ tan_style = normal_tan
    menu:
        "Tan in your underwear":
            mc.name "Whatever underwear you have on is fine, most people won't ever see your tan lines."
            if not panties:
                if not bra:
                    the_person "But, I'm not wearing any underwear."
                    mc.name "Then I guess you'll have to get naked."
                else:
                    the_person "But, I'm not wearing panties."
                    mc.name "Then you better take your bra off, it would be pretty weird to only have tan lines on the top."
                    $ the_bra = None
            else: # has panties
                if not bra:
                    the_person "But, I'm not wearing a bra."
                    mc.name "That's fine, plenty of people tan topless."
        "Tan topless" if the_person.sluttiness > 40:
            mc.name "You should go topless, that way you don't have to be as careful about what you wear in the future."
            if bra:
                if bra.has_extension:
                    $ the_panties = None
                $ the_bra = None
            if not panties:
                the_person "Ok, but I'm not wearing panties right now."
                mc.name "Then I guess you won't have any tan lines."
        "Tan naked" if the_person.sluttiness > 60:
            mc.name "You should get naked, if you are going to tan you might as well do it properly."
            $ the_bra = None
            $ the_panties = None
    the_person "Ok, if you think that's best."
    if bra is None:
        if panties is None:
            $ tan_style = None
        else:
            $ tan_style = slutty_tan
    elif bra.has_extension:
        $ tan_style = one_piece_tan
    elif bra.slut_value > 3:
        $ tan_style = sexy_tan
    $ the_person.tan_style = tan_style
    call strip_with_taboos(the_person, bra = the_bra, panties = panties) from _call_strip_with_taboos_tan
    if done_stripping:
        the_person "Thanks, [the_person.mc_title]. I guess I better go get started."
        # pose/tease
        $ the_person.draw_person(position = "walking_away")
        "You watch her go, enjoying the view. Then sit down to wait."
    "After some time passes you see [the_person.title] coming out in a robe."
    $ towel_outfit = Outfit("Towel")
    if renpy.random.randint(0,1) == 1:
        $ upper = bath_robe.get_copy()
        if hasattr(upper, "supported_patterns") and upper.supported_patterns and renpy.random.randint(1, 100) > 50:
            $ upper.pattern = upper.supported_patterns[renpy.random.choice(upper.supported_patterns.keys())]
            $ upper.colour_pattern = WardrobeBuilder.get_color(the_person, upper.colour)
        $ towel_outfit.add_dress(upper)
    else:
        $ towel_outfit.add_dress(towel.get_copy())
    if bra:
        $ towel_outfit.add_upper(bra.get_copy())
    if panties:
        $ towel_outfit.add_lower(panties.get_copy())
    $ the_person.apply_outfit(towel_outfit)
    $ the_person.draw_person()
    mc.name "How did it go?"
    the_person "Pretty good."
    if done_stripping:
        the_person "Do you want to see?"
        mc.name "Absolutely."
        $ generalised_strip_description(the_person, the_person.outfit.get_underwear_strip_list(visible_enough = True))
        the_person "What do you think?"
        mc.name "You look amazing, this was a great idea."
    else:
        mc.name "Can I see?"
        the_person "Maybe if you keep doing nice thing for me you'll get to see eventually."
        mc.name "I'll have to keep working on that."
        $ the_person.change_slut_temp(5)
    $ the_person.change_happiness(5)
    "You pay for the tanning session and head your separate ways."
    return

label strip_with_taboos(the_person, bra = None, panties = None):
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
            if not bra: # topless
                $ generalised_strip_description(the_person, the_person.outfit.get_tit_strip_list())
        elif not bra:
            $ done_stripping = False
    else:
        $ done_stripping = False
    if done_stripping: #she went as far as we asked
        "With her brief strip show finished [the_person.title] looks at you with a smile."
        mc.name "Wow, [the_person.title], you look incredible."
    else: # not ready to strip in front of us
        if taboo < 2:
            "[the_person.title] shifts on her feet nervously."
            the_person "Um, I need to get ready, but I don't think I can do it with you here."
        elif taboo < 4:
            "Once she is in her underwear, she hesitates, and looks at you shyly."
            the_person "I don't think I can go any further with you watching me."
        else:
            "Although she stripped off her top with no trouble, she seems to be hesitating with her panties."
            the_person "I don't think I can take these off with you watching me."
        mc.name "Of course, let me give you some privacy."
    $ clear_scene()
    return done_stripping
