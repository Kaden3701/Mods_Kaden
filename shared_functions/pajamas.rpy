init -1 python:
    def wear_pajamas(self):
        if self.event_triggers_dict.get("pajamas", False):
            pajamas = self.event_triggers_dict.get("pajamas")
        else:
            pajamas = get_pajama_outfit(self)
        self.apply_outfit(pajamas)
        return

    def get_pajama_outfit(person):
        the_colour = person.favorite_colour()
        color_list = []
        for col in WardrobeBuilder.color_prefs[the_colour]:
            color_list.append(WardrobeBuilder.color_prefs[the_colour][col])
        color_list.append([0.15,0.15,0.15,0.95])
        color_list.append([1.0,1.0,1.0,0.95])
        main_colour = get_random_from_list(color_list)
        if len(color_list) > 1:
            color_list.remove(main_colour)
        main_colour = Color(rgb=(main_colour[0], main_colour[1], main_colour[2]), alpha = main_colour[3])
        main_colour = [main_colour.rgb[0], main_colour.rgb[1], main_colour.rgb[2], main_colour.alpha]
        main_colour[3] *= 1.0-(person.sluttiness/400.0)
        second_colour = get_random_from_list(color_list)
        if len(color_list) > 1:
            color_list.remove(second_colour)
        second_colour = Color(rgb=(second_colour[0], second_colour[1], second_colour[2]), alpha = second_colour[3])
        second_colour = [second_colour.rgb[0], second_colour.rgb[1], second_colour.rgb[2], second_colour.alpha]
        second_colour[3] *= 1.0-(person.sluttiness/300.0)
        third_colour = get_random_from_list(color_list)
        pajamas = Outfit("Pajams")
        bottom_list = []
        bottom_list.append(cotton_panties.get_copy())
        bottom_list.append(cute_panties.get_copy())
        if person.get_opinion_score("showing her ass") > 0:
            bottom_list.append(thong.get_copy())
        bottom = get_random_from_list(bottom_list)
        bottom.colour = third_colour
        if hasattr(bottom, "supported_patterns") and bottom.supported_patterns and renpy.random.randint(1, 100) > 50:
            bottom.pattern = bottom.supported_patterns[renpy.random.choice(bottom.supported_patterns.keys())]
            bottom.colour_pattern = WardrobeBuilder.get_color(person, bottom.colour)
        if person.sluttiness + person.get_opinion_score("not wearing underwear")*5 < 45:
            pajamas.add_lower(bottom)
        elif person.sluttiness + person.get_opinion_score("not wearing anything")*5 < 85:
            pajamas.add_lower(bottom)

        if person.sluttiness < 20 + Person.rank_tits(person.tits)*5 - person.get_opinion_score("not wearing underwear")*5:
            pajamas.add_upper(sports_bra.get_copy(), third_colour)
        covered = False
        lower = None
        if person.sluttiness < 15 + person.get_opinion_score("pants")*5:
            lower = leggings.get_copy()
            covered = True
        else:
            if person.sluttiness < 35 + person.get_opinion_score("pants")*5:
                lower = booty_shorts.get_copy()
                covered = True
            if renpy.random.randint(1, 100) > 70 - person.sluttiness/5:
                socks = high_socks.get_copy()
                socks.colour = second_colour
                if hasattr(socks, "supported_patterns") and socks.supported_patterns and renpy.random.randint(1, 100) > 50:
                    socks.pattern = socks.supported_patterns[renpy.random.choice(socks.supported_patterns.keys())]
                    socks.colour_pattern = WardrobeBuilder.get_color(person, socks.colour)
                pajamas.add_feet(socks)
        if lower:
            lower.colour = second_colour
            if hasattr(lower, "supported_patterns") and lower.supported_patterns and renpy.random.randint(1, 100) > 50:
                lower.pattern = lower.supported_patterns[renpy.random.choice(lower.supported_patterns.keys())]
                lower.colour_pattern = WardrobeBuilder.get_color(person, lower.colour)
            pajamas.add_lower(lower)
        upper_list = []
        if covered:
            upper_list.append(long_tshirt.get_copy())
            if person.sluttiness > 10 - person.get_opinion_score("skimpy outfits")*5:
                upper_list.append(wrapped_blouse.get_copy())
                upper_list.append(long_sweater.get_copy())
            if person.sluttiness > 15 - person.get_opinion_score("skimpy outfits")*5:
                upper_list.append(sleeveless_top.get_copy())
                upper_list.append(camisole.get_copy())
                upper_list.append(tshirt.get_copy())
            if person.sluttiness > 20 - person.get_opinion_score("skimpy outfits")*5:
                upper_list.append(tanktop.get_copy())
                upper_list.append(sports_bra.get_copy())
        else:
            if person.sluttiness >= 25 - person.get_opinion_score("skimpy outfits")*5 and person.sluttiness < 45:
                upper_list.append(sweater_dress.get_copy())
                upper_list.append(long_tshirt.get_copy())
                upper_list.append(wrapped_blouse.get_copy())
            if person.sluttiness > 35 - person.get_opinion_score("skimpy outfits")*5 and person.sluttiness < 65:
                upper_list.append(long_sweater.get_copy())
                upper_list.append(sleeveless_top.get_copy())
            if person.sluttiness > 45 - person.get_opinion_score("skimpy outfits")*5 and person.sluttiness < 85:
                upper_list.append(camisole.get_copy())
                upper_list.append(tshirt.get_copy())
                upper_list.append(nightgown_dress.get_copy())
            if person.sluttiness > 55 - person.get_opinion_score("skimpy outfits")*5:
                upper_list.append(tanktop.get_copy())
                upper_list.append(sports_bra.get_copy())
                upper_list.append(teddy.get_copy())
        if person.sluttiness + person.get_opinion_score("not wearing anything")*5 < 85:
            upper = get_random_from_list(upper_list)
            if upper:
                upper.colour = main_colour
                if hasattr(upper, "supported_patterns") and upper.supported_patterns and renpy.random.randint(1, 100) > 50:
                    upper.pattern = upper.supported_patterns[renpy.random.choice(upper.supported_patterns.keys())]
                    upper.colour_pattern = WardrobeBuilder.get_color(person, upper.colour)
                pajamas.add_upper(upper)
                pajamas.add_dress(upper)
        return pajamas

init 0 python:
    def run_move_enhanced_2(org_func):
        def run_move_enhanced_wrapper_2(person, destination):
            # run original function
            org_func(person, destination)
            # run extension code
            if time_of_day > 3:
                if person.location == person.home:
                    wear_pajamas(person)
                if not aunt.event_triggers_dict.get("invited_for_drinks", False):
                    if aunt.location == hall:
                        wear_pajamas(aunt)
                    if cousin.location == lily_bedroom:
                        wear_pajamas(cousin)
            return
        return run_move_enhanced_wrapper_2

    Person.run_move = run_move_enhanced_2(run_move_enhanced)

label pajama_test():
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_in_the_game(), "Pajama Test", ["Back"])]))
    $ person_choice = _return
    if person_choice != "Back":
        $ start_slut = person_choice.sluttiness
        $ number = 1
        while number < 100:
            $ person_choice.sluttiness = number
            $ wear_pajamas(person_choice)
            $ person_choice.draw_person(emotion = "happy")
            "Current sluttiness = [number]"
            $ number += 1
        $ person_choice.sluttiness = start_slut
        $ del person_choice
    return
