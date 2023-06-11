init -1 python:
    def aunt_suitcase_search_requirement():
        if hall.has_person(aunt):
            if time_of_day == 3:
                return True
            else:
                return "Wait for dinner to distract [aunt.title]"
        return False

    def bedroom_search_requirement():
        if mc.location.get_person_count() > 0:
            person = get_random_person_in_location(mc.location)
            return "Not with " + (person.title or "someone") + " around."
        elif mc.energy < 15:
            return "Not enough {image=gui/extra_images/energy_token.png}"
        else:
            return True

    def underwear_list(person, bra = False, panties = False):
        return_list = []
        if person.wardrobe.get_count() == 0:
            the_colour = person.favorite_colour()
            color_list = []
            for col in WardrobeBuilder.color_prefs[the_colour]:
                color_list.append(WardrobeBuilder.color_prefs[the_colour][col])
            if bra:
                for clothing in [x for x in bra_list if x.slut_value <= person.sluttiness/10.0]:
                    underwear = clothing.get_copy()
                    underwear.colour = get_random_from_list(color_list)
                    if not underwear.has_extension:
                        return_list.append([person.title + "'s " + clothing_formatted_title(the_item = underwear), underwear])
            if panties:
                for clothing in [x for x in panties_list if x.slut_value <= person.sluttiness/10.0]:
                    underwear = clothing.get_copy()
                    underwear.colour = get_random_from_list(color_list)
                    if not underwear.is_extension:
                        return_list.append([person.title + "'s " + clothing_formatted_title(the_item = underwear), underwear])
        else:
            if bra:
                for outfit in [x for x in person.wardrobe.outfits + person.wardrobe.underwear_sets if x.wearing_bra()]:
                    underwear = outfit.get_bra()
                    if not underwear.has_extension:
                        return_list.append([person.title + "'s " + clothing_formatted_title(the_item = underwear), underwear])
            if panties:
                for outfit in [x for x in person.wardrobe.outfits + person.wardrobe.underwear_sets if x.wearing_panties()]:
                    underwear = outfit.get_panties()
                    if not underwear.is_extension:
                        return_list.append([person.title + "'s " + clothing_formatted_title(the_item = underwear), underwear])
        if return_list:
            return_list.append(["Nothing", "Nothing"])
        return return_list

init 0 python: #replacing a def with an extra line
    def learn_home(self): # Adds the_person.home to mc.known_home_locations allowing it to be visited without having to go through date label
        if not self.home in mc.known_home_locations + [lily_bedroom, mom_bedroom, aunt_bedroom, cousin_bedroom, hall]:
            mc.known_home_locations.append(self.home)
            self.home.add_action(random_bedroom_search_action)
            return True # Returns true if it succeeds
        return False # Returns false otherwise, so it can be used for checks.
    Person.learn_home = learn_home

init 3 python:
    def lily_room_initialization(self):
        lily_bedroom.add_action(self)
        return

    def cousin_room_initialization(self):
        cousin_bedroom.add_action(self)
        return

    def aunt_room_initialization(self):
        aunt_bedroom.add_action(self)
        return

    def aunt_suitcase_initialization(self):
        hall.add_action(self)
        return

    lily_room_search_action = ActionMod("Sister Room Search {image=gui/extra_images/energy_token.png}", bedroom_search_requirement, "mom_room_search_description_enhanced", initialization = lily_room_initialization,
        menu_tooltip = "Take a look around and see what you can find.", category = "Home")

    cousin_room_search_action = ActionMod("Cousin Room Search {image=gui/extra_images/energy_token.png}", bedroom_search_requirement, "mom_room_search_description_enhanced", initialization = cousin_room_initialization,
        menu_tooltip = "Take a look around and see what you can find.", category = "Home")

    aunt_room_search_action = ActionMod("Aunt Room Search {image=gui/extra_images/energy_token.png}", bedroom_search_requirement, "mom_room_search_description_enhanced", initialization = aunt_room_initialization,
        menu_tooltip = "Take a look around and see what you can find.", category = "Home")

    random_bedroom_search_action = ActionMod("Bedroom Search {image=gui/extra_images/energy_token.png}", bedroom_search_requirement, "mom_room_search_description_enhanced", initialization = init_action_mod_disabled,
        menu_tooltip = "Take a look around and see what you can find.", category = "Home")

    aunt_suitcase_search_action = ActionMod("Aunt Suitcase Search {image=gui/extra_images/energy_token.png}", aunt_suitcase_search_requirement, "aunt_suitcase_search_description", initialization = aunt_suitcase_initialization,
        menu_tooltip = "Take a look around and see what you can find.", category = "Home")

init 5 python:
    config.label_overrides["mom_room_search_description"] = "mom_room_search_description_enhanced"

label mom_room_search_description_enhanced():
    $ the_person = None
    $ mc.change_energy(-15)
    if mc.location == mom_bedroom or lily_bedroom or aunt_bedroom or cousin_bedroom or hall:
        $ the_person = get_random_from_list(home_residents())
        if mc.location == lily_bedroom:
            $ the_person = lily
        "You take a look around [the_person.possessive_title]'s bedroom."
    if not the_person:
        $ the_person = get_random_from_list(home_residents())
        "It seems like you are alone in [the_person.title]'s home, which gives you an opportunity to explore a bit."
        if len(home_residents()) > 1:
            "You make your way upstairs and take a look down the hall, it seems like there are a few rooms you could explore."
            $ the_person = menu(home_residents())
        "Carefully opening the door you step into the bedroom and look around, ensuring you can leave everything the way you found it."
    menu:
        "Investigate her bedstand":
            call bedstand_search(the_person)
        "Check her computer" if the_person == mom: #add other computers to search
            "[the_person.title] doesn't use her computer very often, but keeps it around in case she has to do some office work from home."
            "You turn the computer on and wait for it to boot up."
            if the_person.event_triggers_dict.get("known_computer_password", False): #If you don't know the password yet, try and guess it.
                "After a short wait the login screen comes up. You enter her password."
            else:
                "After a short wait the login screen comes up."
                "COMPUTER" "INPUT PASSWORD" (what_style = "text_message_style")
                $ password_attempt = renpy.input("")
                $ success = False
                if password_attempt.lower() == mc.name.lower():
                    $ the_person.event_triggers_dict["known_computer_password"] = True
                    $ success = True
                else:
                    "COMPUTER" "INCORRECT PASSWORD" (what_style = "text_message_style")
                while not success:
                    menu:
                        "Try again":
                            "COMPUTER" "INPUT PASSWORD" (what_style = "text_message_style")
                            $ password_attempt = renpy.input("HINT: The oldest")
                            if password_attempt.lower() == mc.name.lower():
                                $ the_person.event_triggers_dict["known_computer_password"] = True
                                $ success = True
                            else:
                                "COMPUTER" "INCORRECT PASSWORD" (what_style = "text_message_style")
                        "Give up":
                            "You give up and power down [the_person.possessive_title]'s computer."
                            $ success = True
            if the_person.event_triggers_dict.get("known_computer_password", False): #If you know the password at this point, no problem logging in."
                "COMPUTER" "WELCOME [the_person.title]!" (what_style = "text_message_style")
                if the_person.event_triggers_dict.get("mom_vaginal_quest_active", False) and the_person.event_triggers_dict.get("mom_vaginal_quest_progress", 0) == 0:
                    call mom_vaginal_taboo_break_revisit_quest_1(the_person) from _call_mom_vaginal_taboo_break_revisit_quest_1_enhanced
                elif the_person.sluttiness < 15: # Nothing interesting to find
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking through files anyways."
                    "You don't find anything other than reports from work and the family budget for the month."
                    "She's cleared her search history as well. Nothing interesting to find."
                elif the_person.sluttiness < 30:
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking around anyways."
                    "All you find are work reports and the family budget. Next, you open up her browser."
                    "COMPUTER" "RESTORE BROWSING SESSION?" (what_style = "text_message_style")
                    "You hit \"Yes\", and her browser immediately takes you to \"A_Mothers_Advice.net\"."
                    "It seems to be an advice forum for mothers, and [the_person.title] was already looking at a post when she logged off last."
                    "Anon3342" "{b}(Advice Wanted) My Sex Drive is Back!?{/b}" (what_style = "text_message_style")
                    "Anon3342" "I'm the lucky single mother of two wonderful children. Both are growing up so fast, and are starting to leave the nest" (what_style = "text_message_style")
                    "Anon3342" "Raising them has always been my top priority, but lately something feels different. My libido has sky rocketed!" (what_style = "text_message_style")
                    "Anon3342" "I thought I was going to be in mother-mode for the rest of my life, but I feel like I'm a horny teenager again!" (what_style = "text_message_style")
                    "Anon3342" "Now I don't know what to do! Should I ignore this to make sure I'm around for my children 100%%?" (what_style = "text_message_style")
                    "Anon3342" "Looking for advice, signed: a horny Mom!" (what_style = "text_message_style")
                    "Did [the_person.title] write this? You scroll down to see the responses."
                    "Anon1449" "Don't feel guilty Horny Mom, you've spent your whole life caring for them. Now it's time to enjoy yourself!" (what_style = "text_message_style")
                    "MTeresa" "You aren't going to be young forever Horny Mom. Get out and meet a new man while you still can." (what_style = "text_message_style")
                    "Jocasta1" "There's at least one way to satisfy your needs without ignoring your family. Do you have a son?" (what_style = "text_message_style")
                    "Anon3342" "I do have a son Jocasta1. I also have a daughter." (what_style = "text_message_style")
                    "Jocasta1" "Well then let him take care of your sex drive! He's probably filled with hormones, and you'll be so much closer!" (what_style = "text_message_style")
                    "Anon3342 doesn't respond. You wonder if that really is [the_person.possessive_title], and what she thought about the idea."
                    $ mc.change_locked_clarity(5)
                    "Either way [the_person.title] was at least reading this. Maybe it gave her some ideas..."
                elif the_person.sluttiness < 50:
                    "[the_person.possessive_title] doesn't keep much on her computer, but she might not have cleared her browser history lately."
                    "You check and see that the last site visited was \"AphroditeNightly.com/The_Poolboy\". You bring up the site again to see what she was looking at."
                    "It's an online sex store, and [the_person.title] was looking at one of their product pages. The page features a picture of a small, discrete black vibrator."
                    "You scroll down and read through the description."
                    "\"Mr.Right not taking care of your needs? Busy mother on the go with no time for Me Time?\""
                    "\"Then The Poolboy is the toy for you. Small enough to bring with you wherever you go, powerful enough to blow your socks off.\""
                    "\"So invite the poolboy in, and let him pet your neglected kitty.\""
                    "You wonder if [the_person.title] actually ordered this, or if she was just window shopping."
                    $ mc.change_locked_clarity(10)
                    "You enjoy a moment thinking about the vibe pressed tight against [the_person.possessive_title]'s clit, then close down the browser."
                else:
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking around anyways."
                    "All you find are work reports and the family budget. Next, you open up her browser."
                    "COMPUTER" "RESTORE BROWSING SESSION?" (what_style = "text_message_style")
                    "You hit \"Yes\", and her browser immediately restores a half dozen tabs, all from \"MILFSDaily.xxx\"."
                    $ mc.change_locked_clarity(10)
                    "Each one has a video loaded, and each video features an older busty woman getting fucked in a variety of interesting ways."
                    "You flick through the tabs, noting which videos are starting half way through."
                    if the_person.discover_opinion(the_person.get_random_opinion(only_positive = True, include_known = False, include_sexy = True, include_normal = False)):
                        "Seeing [the_person.title]'s preference in porn has given you some insight into her."
                    else:
                        "Even you're surprised at how hard core some of the videos are. You have a hard time imagining [the_person.possessive_title] sitting down and watching them."
                        $ mc.change_locked_clarity(10)
                        "... But you do imagine it though."
                    "You don't notice anything else interesting, so you close down the browser."
                "You log off of [the_person.possessive_title]'s computer and power it down."
        "Look in her dresser":
            call dresser_search(the_person)
    return

label bedstand_search(the_person):
    $ favorite_colour = the_person.favorite_colour()
    "[the_person.title] keeps her bedstand neat and tidy, just a lamp, an old clock radio, and a charging cable for her phone."
    if the_person.on_birth_control and persistent.pregnancy_pref != 0:
        "There is also has a blister pack of small blue pills. They must be her birth control pills."
        $ the_person.update_birth_control_knowledge()
        if the_person.event_triggers_dict.get("BC_nightstand_hide_day",-7) < day:
            menu:
                "Hide her birth control":
                    $ the_person.event_triggers_dict["BC_nightstand_hide_day"] = day
                    "You take the small pack and drop it down the crack between [the_person.possessive_title]'s bed and the bedstand."
                    "She'll probably find it if she takes the time to look, and even if she doesn't, she could pick some more up at the pharmacy any time."
                    "It would be so irresponsible for her to be unprotected just because it's slightly inconvenient to get more pills..."
                    if renpy.random.randint(0,100) < 5 + 5*the_person.get_opinion_score("bareback sex"): #She doesn't bother getting more. Just asking for trouble!
                        $ manage_bc(start = False, update_knowledge = False)
                "Replace her birth control" if mc.event_triggers_dict.get("serum_pills", 0) > 0: #not built yet
                    if mc.event_triggers_dict.get("serum_pills", 0) < 1:
                        "[the_person.title]'s birth control pills look pretty generic, but you don't have anything that really looks like them."
                        # if research tier
                        "You have access to a pretty robust chemical production aparatus, but until now it has been focused on creating liquids."
                        "It might be possible to develop something in a solid form, you'll have to check with someone in the production lab."
                    else:
                        "[the_person.title]'s birth control pills look pretty generic, fortunately you have some pills that could be used to replace them."
                "Leave them alone":
                    pass
    "You slide open the single drawer to have a peek inside."
    if the_person.sluttiness < 10: # V. low sluttiness
        if the_person.age > 40:
            "The inside is as neat as the top, with a murder mystery novel sitting at the front of the otherwise empty drawer."
        elif the_person.age > 30:
            "The inside is as neat as the top, with a fantasy novel sitting at the front of the otherwise empty drawer."
        else:
            "The inside is as neat as the top, with a science fiction novel sitting at the front of the otherwise empty drawer."
        "Disappointed, you slide the drawer closed again."
    elif the_person.sluttiness < 50: # mid or Low sluttiness.
        "The inside is as neat as the top. The only thing inside is a well read, probably, second hand novel."
        if the_person.age > 40:
            "The cover features a shirtless cowboy looking out over wide open plains and a herd of cattle."
            "The title reads \"A Fist Full of Bodices\", and [the_person.possessive_title] has dog-eared a bunch of pages."
        elif the_person.age > 30:
            "The cover features a shirtless man wielding a pair of battle axes."
            "The title reads \"Sword and Sheath\", and [the_person.possessive_title] has dog-eared a bunch of pages."
        else:
            "The cover features a shirtless man set on a star filled backdrop."
            "The title reads \"The Hitchhikers Guide to the G-Spot\", and [the_person.possessive_title] has dog-eared a bunch of pages."
        if the_person.sluttiness < 30: #low
            "You aren't terribly interested in reading through her cheap romance novel, so you slide the drawer closed again."
        else: # mid
            "You notice something tucked behind the romance novel. You push it to the side, revealing a small black piece of plastic about the size of tube of lipstick."
            "It's tapered at one end, flat on the other. It takes a moment for you to realise it must be a small vibrator."
            $ mc.change_locked_clarity(10)
            "You enjoy a moment imagining [the_person.possessive_title] on her bed, vibrator planted against her clit."
            "With nothing else to do you make sure everything is back in place and close the drawer again."
    elif the_person.sluttiness < 75: # High sluttiness. A larger rabbit vibrator, plus a small container of lube."
        $ mc.change_locked_clarity(15)
        "The inside isn't as prim and proper as the top is. The first thing you see as you open the drawer is a [favorite_colour] coloured dildo."
        "Coming off the base is a small forked section, the perfect length to rub against her clit while she plays with herself."
        "Laying down beside the toy is a travel sized bottle of lube, currently half empty."
        "You check around, but there's nothing else inside of the drawer. You make sure everything is where you found it, then close it up."
    else: # V. high sluttiness.
        "The moment you open the bedstand you find a large, black, wand style vibrator jammed kitty-corner inside."
        "Beside the wand is a slightly smaller [favorite_colour] dildo and a half-empty bottle of lube. The two toys are surrounded by loose batteries, either spares or already used up."
        $ mag_name = the_person.get_appropriate_mag_name(discover_opinion = True)
        "At the bottom of the of the drawer is a magazine, titled \"[mag_name]\"."
        $ mc.change_locked_clarity(20)
        "You take a moment and enjoy the thought of [the_person.possessive_title] naked and moaning happily with her toys between her legs."
        "When you're finished imagining you double check nothing is out of position and slide the drawer shut again."
    return

label dresser_search(the_person):
    $ theft = 0
    "You slide open the drawers of [the_person.possessive_title]'s dresser."
    "You find her collection of socks, carefully folded shirts, and stash of makeup in the top drawer."
    $ mc.change_locked_clarity(5)
    if len(underwear_list(the_person, bra = True, panties = True)) > 0:
        "The second drawer has something much more interesting: Her underwear."
        if len(underwear_list(the_person, bra = False, panties = True)) > 0:
            "[the_person.title]'s panties are folded neatly along one edge, with styles ranging from practical to scandalous."
            "Even if she doesn't wear them she clearly likes having the choice."
        if len(underwear_list(the_person, bra = True, panties = False)) > 0:
            if the_person.has_large_tits():
                "The rest of the drawer is filled with [the_person.possessive_title]'s bras, stacked so that the large cups fit together neatly."
            else:
                "The rest of the drawer is filled with [the_person.possessive_title]'s bras."
        if len(underwear_list(the_person, bra = True, panties = True)) > 10:
            "There are so many pieces of underwear in here, [the_person.title] probably wouldn't notice if one of them went missing."
        "It would certainly give you something more interesting to jerk off into than some tissue."
        menu:
            "Steal a bra" if len(underwear_list(the_person, bra = True, panties = False)) > 0:
                $ the_bra = menu(underwear_list(the_person, bra = True))
                if the_bra != "Nothing":
                    if the_bra.slut_value > 4: #more fine tuning
                        "You grab one of [the_person.possessive_title]'s softer, fancier bras from the back of her underwear drawer."
                    elif the_bra.slut_value > 2:
                        "You grab one of [the_person.possessive_title]'s more risque bras from the middle of her underwear drawer."
                    else:
                        "You grab one of [the_person.possessive_title]'s traditional bras from the front of her underwear drawer."
                    if the_bra.slut_value*10 > the_person.sluttiness:
                        "It doesn't look like one she would be brave enough to wear, so she won't miss it. You tuck it into your back pocket."
                    elif the_bra.slut_value*5 > the_person.sluttiness:
                        "It looks like one she would wear occasionally, so she might miss it. You tuck it into your back pocket."
                    else:
                        "It looks like something she wears frequently, so she will probably miss it. You tuck it into your back pocket."
                    $ mc.steal_underwear(the_person, the_bra)
                    $ mc.change_masturbation_novelty(5)
                    $ theft = 1
                    $ the_person.event_triggers_dict.update({"stolen_bras" : the_person.event_triggers_dict.get("stolen_bras", 0) + 1})
                else:
                    pass
            "Steal a pair of panties" if len(underwear_list(the_person, bra = False, panties = True)) > 0:
                $ the_panties = menu(underwear_list(the_person, panties = True))
                if panties != "Nothing":
                    if panties.slut_value > 4:
                        "You grab one of [the_person.possessive_title]'s softer, fancier pairs of panties from the back of her underwear drawer."
                    elif panties.slut_value > 2:
                        "You grab one of [the_person.possessive_title]'s more risque pairs of panties from the middle of her underwear drawer."
                    else:
                        "You grab one of [the_person.possessive_title]'s traditional pair of panties from the front of her underwear drawer."
                    if panties.slut_value*10 > the_person.effective_sluttiness:
                        "They don't look like one she would be pantiesve enough to wear, so she won't miss them. You tuck them into your back pocket"
                    elif panties.slut_value*5 > the_person.effective_sluttiness:
                        "They look like one she would wear occasionally, so she might miss them. You tuck them into your back pocket."
                    else:
                        "They look like something she wears frequently, so she will probably miss them. You tuck them into your back pocket."
                    $ mc.steal_underwear(the_person, panties)
                    $ mc.change_masturbation_novelty(5)
                    $ theft = 1
                    $ the_person.event_triggers_dict.update({"stolen_panties" : the_person.event_triggers_dict.get("stolen_panties", 0) + 1})
                else:
                    pass
            "Leave everything alone":
                pass
        if theft == 0:
            "You decide to leave all of [the_person.possessive_title]'s underwear where it is. It wouldn't be good if she noticed any of it missing."
            "You make sure nothing has been moved around, then slide the drawer shut."
        else:
            if mc.location == mom_bedroom or lily_bedroom or hall:
                "You poke your head out the door and check to make sure that no one is around."
                "Seeing that the coast is clear you carefully make your way to your room to stash the haul."
                if theft > 1:
                    "[the_person.title] is definitely going to notice that her underwear is missing, you wonder how she will react."
                $ mc.change_location(bedroom)
            else:
                "With your recently acquired prize you figure you should get out of here."
                $ mc.change_location(downtown)
    else: #has a wardrobe without underwear
        "The second drawer is surprisingly empty."
        "You look further but it seems like [the_person.title] doesn't have any underwear at all in the room."
        "You picture her walking around without any underwear on, and think about checking to find out if it is true."
        $ mc.change_locked_clarity(10)
    return

label aunt_suitcase_search_description():
    $ mc.change_energy(-15)
    $ the_person = aunt
    "It seems like [the_person.possessive_title] spends all of her time in the house, if you want to get access to her belongings you probably need a distraction."
    "Since your mom is busy preparing dinner you figure that you can send [the_person.title] to give her a hand."
    mc.name "Hey [the_person.title], are you busy?"
    the_person "Oh, [the_person.mc_title] not really. Did you need something."
    mc.name "Not for myself, but I'm a bit worried about [mom.fname], she has been pushing herself a bit hard with the extra people here."
    the_person "I know, I've been trying to think of a way to help her."
    mc.name "Well she is making dinner right now, maybe you could lend a hand."
    the_person "That's a great idea, thanks for the suggestion [the_person.mc_title]."
    "She makes her way into the kitchen and you hear her talking with your mom."
    "Finally alone you walk over to [the_person.possessive_title]'s suitcase."
    "You find her collection of socks, carefully folded shirts, and stash of makeup in the top."
    $ mc.change_locked_clarity(5)
    if  len(underwear_list(the_person, bra = True, panties = True)) > 0:
        "Underneath is something much more interesting: Her underwear."
        if len(underwear_list(the_person, bra = False, panties = True)) > 0:
            "[the_person.title]'s panties are folded neatly along one edge, with styles ranging from practical to scandalous."
            "Even if she doesn't wear them she clearly likes having the choice."
        if len(underwear_list(the_person, bra = True, panties = False)) > 0:
            if the_person.has_large_tits():
                "The rest of the suitcase is filled with [the_person.possessive_title]'s bras, stacked so that the large cups fit together neatly."
            else:
                "The rest of the suitcase is filled with [the_person.possessive_title]'s bras."
        if len(underwear_list(the_person, bra = True, panties = True)) > 10:
            "There are so many pieces of underwear in here, [the_person.title] probably wouldn't notice if one of them went missing."
        "It would certainly give you something more interesting to jerk off into than some tissue."
        menu:
            "Steal a bra" if len(underwear_list(the_person, bra = True, panties = False)) > 0:
                $ the_bra = menu(underwear_list(the_person, bra = True))
                if the_bra.slut_value > 4:
                    "You grab one of [the_person.possessive_title]'s softer, fancier bras from the back of her underwear drawer."
                elif the_bra.slut_value > 2:
                    "You grab one of [the_person.possessive_title]'s more risque bras from the middle of her underwear drawer."
                else:
                    "You grab one of [the_person.possessive_title]'s traditional bras from the front of her underwear drawer."
                if the_bra.slut_value*10 > the_person.sluttiness:
                    "They don't look like one she would be brave enough to wear, so she won't miss them. You tuck it behind your back and hurry to your room to stash it away."
                elif the_bra.slut_value*5 > the_person.sluttiness:
                    "They look like one she would wear occasionally, so she might miss them. You tuck it behind your back and hurry to your room to stash it away."
                else:
                    "They look like something she wears frequently, so she will probably miss them. You tuck it behind your back and hurry to your room to stash it away."
                $ mc.steal_underwear(the_person, the_bra)
                $ mc.change_masturbation_novelty(5)
                $ the_person.event_triggers_dict.update({"stolen_bras" : the_person.event_triggers_dict.get("stolen_bras", 0) + 1})
                $ mc.change_location(bedroom)
            "Steal a pair of panties" if len(underwear_list(the_person, bra = False, panties = True)) > 0:
                $ the_panties = menu(underwear_list(the_person, panties = True))
                if panties.slut_value > 4:
                    "You grab one of [the_person.possessive_title]'s softer, fancier pairs of panties from the back of her underwear drawer."
                elif panties.slut_value > 2:
                    "You grab one of [the_person.possessive_title]'s more risque pairs of panties from the middle of her underwear drawer."
                else:
                    "You grab one of [the_person.possessive_title]'s traditional pair of panties from the front of her underwear drawer."
                if panties.slut_value*10 > the_person.sluttiness:
                    "They don't look like one she would be pantiesve enough to wear, so she won't miss them. You tuck it behind your back and hurry to your room to stash it away."
                elif panties.slut_value*5 > the_person.sluttiness:
                    "They look like one she would wear occasionally, so she might miss them. You tuck it behind your back and hurry to your room to stash it away."
                else:
                    "They look like something she wears frequently, so she will probably miss them. You tuck it behind your back and hurry to your room to stash it away."
                $ mc.steal_underwear(the_person, panties)
                $ mc.change_masturbation_novelty(5)
                $ the_person.event_triggers_dict.update({"stolen_panties" : the_person.event_triggers_dict.get("stolen_panties", 0) + 1})
                $ mc.change_location(bedroom)
                "You poke your head out the door and check to make sure that no one is around."
                "Seeing that the coast is clear you carefully make your way to your room to stash the haul."
                "[the_person.title] is definitely going to notice that her underwear is missing, you wonder how she will react."
                $ mc.change_location(bedroom)
            "Leave everything alone":
                "You decide to leave all of [the_person.possessive_title]'s underwear where it is. It wouldn't be good if she noticed any of it missing."
                "You make sure nothing has been moved around, then slide the drawer shut."
    else:
        "You look further but it seems like [the_person.title] doesn't have any underwear at all in the suitcase."
        "You picture her walking around without any underwear on, and think about checking to find out if it is true."
        $ mc.change_locked_clarity(10)
    return
