init 5 python:
    def movie_date_invite_requirement():
        if time_of_day == 3:
            if day%7 == 1 and not mc.business.event_triggers_dict.get("movie_date_scheduled", False): #movie tuesday
                if get_movie_date_person():
                    return True
        return False

    def fuck_date_invite_requirement():
        if time_of_day == 3:
            if day%7 == 3 and not mc.business.event_triggers_dict.get("fuck_date_scheduled", False): #her place thursday
                if get_fuck_date_person():
                    return True
        return False

    def dinner_date_invite_requirement():
        if time_of_day == 3:
            if day%7 == 4 and not mc.business.event_triggers_dict.get("dinner_date_scheduled", False): #dinner friday
                if get_dinner_date_person():
                    return True
        return False

    def shopping_date_invite_requirement():
        if time_of_day == 3:
            if get_shopping_date_person():
                return True
        return False

    def get_movie_date_person():
        temp_list = []
        for person in known_people_in_the_game():
            if person.energy > 60 and person.is_available:
                    if person.love > 40 and person.love < 70:
                        if person.relationship == "Single" or person.has_role(girlfriend_role) or person.has_role(affair_role):
                            temp_list.append(person)
        return get_random_from_list(temp_list)

    def get_fuck_date_person():
        temp_list = []
        for person in known_people_in_the_game():
            if person.energy > 60 and person.is_available:
                    if person.has_role(girlfriend_role) or person.has_role(affair_role):
                        if person.effective_sluttiness() < 60:
                            temp_list.append(person)
        return get_random_from_list(temp_list)

    def get_dinner_date_person():
        temp_list = []
        for person in known_people_in_the_game():
            if person.energy > 60 and person.is_available:
                    if person.love > 50 and person.love < 80:
                        if person.relationship == "Single" or person.has_role(girlfriend_role) or person.has_role(affair_role):
                            temp_list.append(person)
        return get_random_from_list(temp_list)

    def get_shopping_date_person():
        temp_list = []
        for person in known_people_in_the_game():
            if person.energy > 60:
                if person.is_available:
                    if person.has_role(girlfriend_role) or person.has_role(affair_role):
                        temp_list.append(person)
        return get_random_from_list(temp_list)

    movie_date_invite = ActionMod("Movie Date Invite", movie_date_invite_requirement, "movie_date_invite_label",
        menu_tooltip = "Someone invites you out to see a movie they like.", category = "Mall", is_crisis = True, is_morning_crisis = False, priority = 5)
    fuck_date_invite = ActionMod("Fuck Date Invite", fuck_date_invite_requirement, "fuck_date_invite_label",
        menu_tooltip = "Someone invites you over to their place to fuck them.", category = "Mall", is_crisis = True, is_morning_crisis = False, priority = 5)
    dinner_date_invite = ActionMod("Dinner Date Invite", dinner_date_invite_requirement, "dinner_date_invite_label",
        menu_tooltip = "Someone asks if you'd like to go to dinner.", category = "Mall", is_crisis = True, is_morning_crisis = False, priority = 5)
    shopping_date_invite = ActionMod("Shopping Date Invite", shopping_date_invite_requirement, "shopping_date_invite_label",
        menu_tooltip = "Someone invites you to go shopping with them.", category = "Mall", is_crisis = True, is_morning_crisis = False, priority = 5)

label movie_date_invite_label():
    $ the_person = get_movie_date_person()
    $ the_person.apply_outfit(the_person.wardrobe.decide_on_outfit(the_person.sluttiness + 10))
    $ is_text = False
    if mc_at_work():
        if the_person.is_employee() and the_person.is_at_office() or the_person.location == mc.location:
            "As you are packing up to head home for the day you are approached by [the_person.title]."
        else:
            "As you are packing up to head home for the day you get a text from [the_person.title]."
            $ is_text = True
    elif mc_at_home():
        if the_person in people_in_mc_home():
            "As you are walking down the hallway in your house you are approached by [the_person.title]."
        else:
            "As you are walking down the hallway in your house you get a text from [the_person.title]."
            $ is_text = True
    else:
        if the_person.location == mc.location:
            "As you are wandering around you are approached by [the_person.title]."
        else:
            "As you are wandering around you get a text from [the_person.title]."
            $ is_text = True
    if is_text:
        $ mc.start_text_convo(the_person)
    the_person "Hey [the_person.mc_title]! I was going to head out to watch a movie tonight."
    the_person "Do you want to go with me?"
    menu:
        "Go to the movie\n{color=#ff0000}{size=18}Costs: $50{/size}{/color}":
            pass
        "Decline the date":
            mc.name "Sorry I can't tonight. I've got other plans."
            the_person "Oh, okay. Have fun!"
            mc.name "Thanks, you too!"
            return
    mc.name "Yeah, that sounds great. What time is the showing?"
    the_person "There is one in about a half hour if that works for you."
    if is_text:
        mc.name "Sounds good, I'll meet you there"
        the_person "Great! See you soon."
        $ mc.end_text_convo()
        "A little while later you meet her outside the theater."
        $ mc.change_location(downtown)
        $ the_person.draw_person()
        the_person "Hey, good to see you!"
        the_person "I'm ready to go in, do you mind if I pick the movie?"
    else:
        mc.name "Sounds good, are you ready to go now?"
        the_person "Yeah, just let me grab my purse."
        "A short trip later you arrive at the theater together."
        $ mc.change_location(downtown)
        $ the_person.draw_person()
        the_person "Do you mind if I pick the movie?"
    $ renpy.show("Theater", what = theater_background, layer = "master")
    mc.name "Anything is great while I'm with you. Go ahead and pick whatever you want."
    if the_person.personality.personality_type_prefix == wild_personality.personality_type_prefix or the_person.personality.default_prefix == wild_personality.personality_type_prefix: #If it's a wild or wild derived personality type
        $ the_choice = get_random_from_list(["The Revengers", "Raiders of the Found Ark", "Die Difficult", "Mission: Improbable", "Wonderful Woman", "John Wicked: Part 3", "The Destructonator", "Waterman"])
        the_person "I've wanted to see [the_choice] for a while."
    elif the_person.personality.personality_type_prefix == reserved_personality.personality_type_prefix or the_person.personality.default_prefix == reserved_personality.personality_type_prefix:
        $ the_choice = get_random_from_list(["Olympic", "Britannic","The Workbook", "East Side Tale", "Pottery Poltergeist"])
        the_person "I thought [the_choice] would be a good fit for us."
    elif the_person.personality.personality_type_prefix == introvert_personality.personality_type_prefix or the_person.personality.default_prefix == introvert_personality.personality_type_prefix:
        $ the_choice = get_random_from_list(["that one in French", "that one in Italian", "that one in Russian", "that one in Japanese", "that one in Mandarin", "that one that's silent"])
        the_person "I haven't heard much about it, but I think we should watch [the_choice]. It should be a really unique one."
    else: #relaxed and anything else
        $ the_choice = get_random_from_list(["Spooky Movie", "Aaron Powers", "Dumber and Dumberest-er", "Ghostblasters", "Shaun of the Undead"])
        the_person "I thought we'd both enjoy [the_choice]."
    $ del the_choice
    mc.name "That sounds great, I'll go grab us some tickets."
    "You walk up to the ticket booth and get tickets for yourself and [the_person.possessive_title]."
    $ mc.business.change_funds(-50)
    "Tickets in hand, you rejoin [the_person.title] and set off to find your theater."
    menu:
        "Stop at the concession stand\n{color=#ff0000}{size=18}Costs: $20{/size}{/color}" if mc.business.has_funds(20):
            mc.name "Do you want some popcorn or anything like that?"
            the_person "Oh, yeah that would be great. Do you mind waiting in line?"
            mc.name "Not at all, you run ahead and I'll go get us some snacks."
            $ clear_scene()
            $ mc.business.change_funds(-20)
            "You give [the_person.possessive_title] her ticket and split up. At the concession stand you get a pair of drinks and some popcorn to share."
            menu:
                "Put a dose of serum in her drink" if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_person) from _call_give_serum_invite
                "Put a dose of serum in her drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass
                "Leave her drink alone":
                    pass
            "Snacks in hand you return to [the_person.title]. She takes a sip from her drink as you settle into your seat beside her."
        "Stop at the concession stand\n{color=#ff0000}{size=18}Requires: $20{/size}{/color} (disabled)" if not mc.business.has_funds(20):
            pass
        "Just go to the movie":
            "You find your theater, pick your seats, and settle down next to each other for the movie."
    $ the_person.draw_person(position = "sitting", lighting = [0.5,0.5,0.5])
    "You chat for a few minutes until the theater lights dim and the movie begins."
    "Halfway through the movie it's clear that [the_person.title] is having a great time. She's leaning forward in her seat, eyes fixed firmly on the screen."
    $ mc.change_locked_clarity(10)
    "As the movie approaches its climax she reaches her hand down and finds yours to hold."
    "When it's finished you leave the theater together, still holding hands."
    $ the_person.draw_person()
    mc.name "So, did you like the movie?"
    the_person "It was amazing! Let's watch something like that next time."
    $ the_person.change_love(10, max_modified_to = 80)
    the_person "There will be a next time, right?"
    mc.name "I'd love for there to be."
    $ the_person.change_happiness(10)
    if the_person.home in [bedroom, lily_bedroom, hall, mom_bedroom, kitchen, harem_mansion]:
        $ mc.change_locked_clarity(5)
        "She leans towards you and gives you a quick kiss."
        the_person "Let's head home then."
    else:
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10):
            $ mc.change_locked_clarity(5)
            "She leans towards you and gives you a quick kiss."
            $ the_person.call_dialogue("date_seduction")
            menu:
                "Go to [the_person.title]'s place":
                    $ mc.change_location(downtown)
                    mc.name "That sounds like a great idea. Let's get a cab."
                    if not the_person.has_role(aunt_role) and not the_person.has_role(cousin_role):
                        if not the_person.home in mc.known_home_locations:
                            $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You flag a taxi and get in with [the_person.possessive_title]."
                    "After a short ride you pull up in front her house. She leads you to the front door and invites you inside."
                    $ the_person.add_situational_slut("Romanced",15,"What a wonderful date!")
                    call date_take_home_her_place(the_person, date_type = "movie") from _call_date_take_home_her_place_invite
                    $ the_person.clear_situational_slut("Romanced")

                "Call it a night":
                    mc.name "I'd like to call it an early night today, but maybe I'll take you up on the offer some other time."
                    "Her taxi arrives. You give her a goodbye kiss and head home yourself."
        else:
            "She leans towards you and gives you a quick kiss on the cheek before saying goodbye."
    $ clear_scene()
    $ mc.change_location(bedroom)
    return "Advance Time"

label fuck_date_invite_label():
    $ the_person = get_fuck_date_person()
    if the_person.has_role(affair_role):
        $ so_title = SO_relationship_to_title(the_person.relationship)
    $ is_text = False
    if mc_at_work():
        if the_person.is_employee() and the_person.is_at_office() or the_person.location == mc.location:
            "As you are packing up to head home for the day you are approached by [the_person.title]."
        else:
            "As you are packing up to head home for the day you get a text from [the_person.title]."
            $ is_text = True
    elif mc_at_home():
        if the_person in people_in_mc_home():
            "As you are walking down the hallway in your house you are approached by [the_person.title]."
        else:
            "As you are walking down the hallway in your house you get a text from [the_person.title]."
            $ is_text = True
    else:
        if the_person.location == mc.location:
            "As you are wandering around you are approached by [the_person.title]."
        else:
            "As you are wandering around you get a text from [the_person.title]."
            $ is_text = True
    if is_text:
        $ mc.start_text_convo(the_person)
    the_person "Hey [the_person.mc_title]! I was feeling a bit lonely and thought maybe you could keep me company tonight."
    menu:
        "Keep her company":
            pass
        "Decline the date":
            mc.name "Sorry I can't tonight. I've got other plans."
            the_person "Oh, okay. Have fun!"
            mc.name "Thanks, you too!"
            return
    if is_text:
        if the_person.home in [bedroom, lily_bedroom, hall, mom_bedroom, kitchen, harem_mansion]:
            if mc.is_home:
                mc.name "Absolutely, I'm just down the hall. Be there soon."
            else:
                mc.name "Absolutely, I should be home soon."
            the_person "I'll be waiting for you."
        else:
            if the_person.home not in mc.known_home_locations:
                mc.name "Absolutely, I just need the address."
                "She quickly responds with the details and you pull up your map app."
            else:
                mc.name "Absolutely, I'll be there soon."
    else:
        if the_person.home in [bedroom, lily_bedroom, hall, mom_bedroom, kitchen, harem_mansion]:
            if mc.is_home:
                mc.name "Absolutely!"
            else:
                mc.name "Absolutely, let's head home."
        else:
            if the_person.home not in mc.known_home_locations:
                mc.name "Absolutely, just point me in the right direction."
                "She guides you to her house quickly and efficiently."
            else:
                mc.name "Absolutely, let's go."
    $ mc.change_location(the_person.home)
    if is_text:
        "You make your way to [the_person.possessive_title]'s house. You text her to let you know you're here."
        mc.name "I'm here. Are you ready?"
        the_person "Come on in, the door is unlocked."
        $ mc.end_text_convo()
        "You go inside. The only light in the house comes from a room with its door ajar. When you swing it open you see [the_person.title] waiting."
    $ the_person.add_situational_slut("Date", 20, "There's no reason to hold back, he's here to fuck me!")
    if the_person.has_role(girlfriend_role):
        call girlfriend_fuck_date_event(the_person) from _call_girlfriend_fuck_date_event_invite
    else:
        call fuck_date_event(the_person) from _call_fuck_date_event_invite
    $ the_person.clear_situational_slut("Date")
    return "Advance Time"

label dinner_date_invite_label():
    $ the_person = get_dinner_date_person()
    $ is_text = False
    if mc_at_work():
        if the_person.is_employee() and the_person.is_at_office() or the_person.location == mc.location:
            "As you are packing up to head home for the day you are approached by [the_person.title]."
        else:
            "As you are packing up to head home for the day you get a text from [the_person.title]."
            $ is_text = True
    elif mc_at_home():
        if the_person in people_in_mc_home():
            "As you are walking down the hallway in your house you are approached by [the_person.title]."
        else:
            "As you are walking down the hallway in your house you get a text from [the_person.title]."
            $ is_text = True
    else:
        if the_person.location == mc.location:
            "As you are wandering around you are approached by [the_person.title]."
        else:
            "As you are wandering around you get a text from [the_person.title]."
            $ is_text = True
    if is_text:
        $ mc.start_text_convo(the_person)
    the_person "Hey [the_person.mc_title]! I don't feel like cooking so I was about to go grab dinner."
    the_person "Do you want to go with me?"
    menu:
        "Go on the date\n{color=#ff0000}{size=18}Costs: $100{/size}{/color}":
            pass
        "Decline the date":
            mc.name "Sorry I can't tonight. I've got other plans."
            the_person "Oh, okay. Have fun!"
            mc.name "Thanks, you too!"
            return
    mc.name "Yeah, that sounds great. Where do you want to go?"
    the_person "There is nice place in town where we can get food and something to drink."
    if is_text:
        the_person "Let me send you the address."
        mc.name "Sounds good, I'll meet you there"
        the_person "Great! See you soon."
        $ mc.end_text_convo()
        "You get yourself looking as presentable as possible and head downtown."
    else:
        mc.name "Sounds good, are you ready to go now?"
        the_person "Yeah, just let me grab my purse."
    $ mc.change_location(downtown)
    $ the_person.draw_person()
    $ the_person.draw_person(emotion = "happy")
    $ mc.business.change_funds(-100)
    $ the_person.change_love(5)
    $ the_person.change_happiness(5)
    $ renpy.show("restaurant", what = restaraunt_background, layer = "master")
    $ the_person.draw_person(emotion = "happy", position = "sitting")
    if the_person.has_role(sister_role) or the_person.has_role(mother_role):
        if the_person.sluttiness >= 20:
            "You and [the_person.possessive_title] get to the restaurant and order your meals. She chats and flirts with you freely, as if forgetting you were related."
        else:
            "You and [the_person.possessive_title] get to the restaurant and order your meals."
            "She chats and laughs with you the whole night, but never seems to consider this more than a friendly family dinner."
    else:
        "You and [the_person.possessive_title] get to the restaurant and order your meals. You chat, flirt, and have a wonderful evening."
    if renpy.random.randint(0,100) < 40: #Chance to give her some serum.
        "After dinner you decide to order dessert. [the_person.title] asks for a piece of cheesecake, then stands up from the table."
        the_person "I'm going to go find the little girls' room. I'll be back in a moment."
        $ clear_scene()
        "She heads off, leaving you alone at the table with her half finished glass of wine."
        menu:
            "Add a dose of serum to her drink" if mc.inventory.get_any_serum_count()>0:
                call give_serum(the_person) from _call_give_serum_21_invite
                if _return:
                    "You pour a dose of serum into her wine and give it a quick swirl, then sit back and relax."
                    "[the_person.possessive_title] returns just as your dessert arrives."
                else:
                    "You sit back and relax, content to just enjoy the evening. [the_person.possessive_title] returns just as your dessert arrives."
            "Add a dose of serum to her drink\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
                pass
            "Leave her drink alone":
                "You sit back and relax, content to just enjoy the evening. [the_person.possessive_title] returns just as your dessert arrives."
        $ the_person.draw_person(position = "sitting")
        the_person "Ah, perfect timing!"
        "She sips her wine, then takes an eager bite of her cheesecake. She closes her eyes and moans dramatically."
        the_person "Mmm, so good!"
    $ the_person.change_love(mc.charisma)
    $ the_person.change_happiness(mc.charisma)
    $ the_person.draw_person()
    if the_person.home in [bedroom, lily_bedroom, hall, mom_bedroom, kitchen, harem_mansion]:
        "At the end of the night you pay the bill and leave with [the_person.title]. The two of you travel home together."
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you back to her place.
            $ the_person.call_dialogue("date_seduction")
            menu:
                "Go to [the_person.title]'s room":
                    mc.name "I think I would. Lead the way."
                    $ mc.change_location(the_person.home)
                    "[the_person.possessive_title] leads you into her room and closes the door behind you."
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call fuck_person(the_person, private = True) from _call_fuck_person_16_invite
                    $ the_person.call_dialogue("sex_review", the_report = _return)
                    $ the_person.clear_situational_slut("Romanced")
                    "When you and [the_person.possessive_title] are finished you slip back to your own bedroom just down the hall."
                "Call it a night":
                    mc.name "I think we should just call it a night now. I've got to get up early tomorrow."
                    "She lets go of your hand and looks away."
                    the_person "Right, of course. I wasn't saying we should... I was just... Goodnight [the_person.mc_title]."
                    "She hurries off to her room."
        else:
            the_person "I had a great night [the_person.mc_title]. We should get out of the house and spend time together more often."
            mc.name "I think so too. Goodnight [the_person.title]."
    else:
        "At the end of the night you pay the bill and leave with [the_person.title]. You wait with her while she calls for a taxi."
        if renpy.random.randint(0,100) < the_person.sluttiness + the_person.love + (mc.charisma * 10): #She invites you back to her place.
            $ the_person.call_dialogue("date_seduction") #She invites you back to her place to "spend some more time together". She's been seduced.
            menu:
                "Go to [the_person.title]'s place":
                    $ mc.change_location(downtown)
                    mc.name "That sounds like a great idea."
                    if not the_person.has_role(aunt_role) and not the_person.has_role(cousin_role):
                        if not the_person.home in mc.known_home_locations:
                            $ mc.known_home_locations.append(the_person.home) #You know where she lives and can visit her.
                    "You join [the_person.possessive_title] when her taxi arrives."
                    "After a short ride you pull up in front of her house. She leads you to the front door and invites you inside."
                    $ the_person.add_situational_slut("Romanced",25,"What a wonderful date!")
                    call date_take_home_her_place(the_person, date_type = "dinner") from _call_date_take_home_her_place_1_invite
                    $ the_person.clear_situational_slut("Romanced")
                "Call it a night":
                    mc.name "I'd like to call it an early night today, but maybe I'll take you up on the offer some other time."
                    "Her taxi arrives. You give her a goodbye kiss and head home yourself."
        else: #She says goodnight to you here.
            the_person "I had a great night [the_person.mc_title], you're a lot of fun to be around. We should do this again."
            mc.name "It would be my pleasure."
            "[the_person.title]'s taxi arrives and she gives you a kiss goodbye. You watch her drive away, then head home yourself."
    $ clear_scene()
    $ mc.change_location(bedroom)
    return "Advance Time"

label shopping_date_invite_label():
    $ the_person = get_shopping_date_person()
    $ is_text = False
    if mc_at_work():
        if the_person.is_employee() and the_person.is_at_office() or the_person.location == mc.location:
            "As you are packing up to head home for the day you are approached by [the_person.title]."
        else:
            "As you are packing up to head home for the day you get a text from [the_person.title]."
            $ is_text = True
    elif mc_at_home():
        if the_person in people_in_mc_home():
            "As you are walking down the hallway in your house you are approached by [the_person.title]."
        else:
            "As you are walking down the hallway in your house you get a text from [the_person.title]."
            $ is_text = True
    else:
        if the_person.location == mc.location:
            "As you are wandering around you are approached by [the_person.title]."
        else:
            "As you are wandering around you get a text from [the_person.title]."
            $ is_text = True
    if is_text:
        $ mc.start_text_convo(the_person)
    the_person "I was going to head to the mall, but it's always more fun shopping with a friend."
    the_person "Wanna come with me?"
    menu:
        "Go shopping":
            mc.name "Sure, that sounds like fun."
            if not is_text:
                "[the_person.possessive_title] smiles and nods in agreement."
            $ the_person.change_happiness(5)
        "Not right now":
            mc.name "Sorry [the_person.title], I'm busy right now actually."
            the_person "Aww, alright. I've got to get going, see ya later!"
            if not is_text:
                "[the_person.possessive_title] hurries past you leaves."
            return
    if is_text:
        "You arange a meeting place at the mall and then head downtown to spend some time with [the_person.possessive_title]."
        $ mc.end_text_convo()
    else:
        "You and [the_person.possessive_title] head downtown, to the largest shopping mall around."
    call shopping_date_intro(the_person, skip_intro = True) from _call_shopping_date_intro_invite
    return
