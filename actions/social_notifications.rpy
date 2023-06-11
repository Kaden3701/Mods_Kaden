init 3 python:
    def social_notification_requirement():
        if len(build_insta_scroll()) + len(build_dik_scroll()) + len(build_only_scroll()) > 6:
            return True
        return False

    def build_insta_scroll():
        temp_list = []
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("insta_known", False):
                if person.event_triggers_dict.get("insta_generate_pic", False):
                    temp_list.append(person)
        return temp_list

    def build_dik_scroll():
        temp_list = []
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("dikdok_known", False):
                if person.event_triggers_dict.get("dikdok_generate_video", False):
                    temp_list.append(person)
        return temp_list

    def build_only_scroll():
        temp_list = []
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("onlyfans_known", False):
                if person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) >= day:
                    if not person.event_triggers_dict.get("onlyfans_visited_today", True):
                        temp_list.append(person)
        return temp_list

    social_notification_action = ActionMod("Social Notification",social_notification_requirement,"social_notification_action_label",
        menu_tooltip = "Your phone lights up with notifications from social media", category="Misc", is_crisis = True)

    def insta_scroll_requirement():
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("insta_known", False):
                if person.event_triggers_dict.get("insta_generate_pic", False):
                    return True
        return "Wait for tomorrow"

    def dik_scroll_requirement():
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("dikdok_known", False):
                if person.event_triggers_dict.get("dikdok_generate_video", False):
                    return True
        return "Wait for tomorrow"

    def only_scroll_requirement():
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("onlyfans_known", False):
                if not person.event_triggers_dict.get("onlyfans_visited_today", True):
                    if person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) >= day:
                        return True
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("onlyfans_known", False):
                if person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) < day:
                    return "Renew your subscriptions"
        return "Wait for tomorrow"

    def onlyfans_subscribe_requirement():
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("onlyfans_known", False):
                if person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) < day:
                    return True
        return "All subscriptions active"

    def onlyfans_renew_subscriptions(days, renew = False):
        count = 0
        for person in known_people_in_the_game():
            if person.event_triggers_dict.get("onlyfans_known", False):
                if person.event_triggers_dict.get("onlyfans_subscription_valid_until", 0) < day:
                    if renew:
                        person.event_triggers_dict["onlyfans_subscription_valid_until"] = day + days
                    else:
                        count +=1
        return count

    def build_phone_menu_social_scroll_extended(org_func):
        def phone_menu_wrapper():
            # run original function
            phone_menu = org_func()
            # run extension code
            scroll_insta_action = Action("Scroll InstaPic", insta_scroll_requirement, "scroll_insta")
            scroll_dikdok_action = Action("Scroll Dikdok", dik_scroll_requirement, "scroll_dikdok")
            scroll_onlyfans_action = Action("Scroll OnlyFanatics", only_scroll_requirement, "scroll_onlyfans")
            onlyfans_subscribe_action = Action ("Renew OnlyFanatics Subs", onlyfans_subscribe_requirement, "onlyfans_subscribe_label")
            phone_menu[1].insert(2, scroll_insta_action)
            phone_menu[1].insert(4, scroll_dikdok_action)
            phone_menu[1].insert(6, scroll_onlyfans_action)
            phone_menu[1].insert(7, onlyfans_subscribe_action)
            return phone_menu
        return phone_menu_wrapper

    if "build_phone_menu" in globals():
        build_phone_menu = build_phone_menu_social_scroll_extended(build_phone_menu)

label scroll_insta():
    $ insta_scroll = build_insta_scroll()
    $ insta_count = len(build_insta_scroll())-1
    while insta_count > -1:
        call view_insta_enhanced(insta_scroll[insta_count]) from _call_view_insta_scroll
        menu:
            "Keep scrolling" if insta_count > 0:
                $ insta_count -= 1
            "Stop":
                $ insta_count = -1
    return

label view_insta_enhanced(the_person):
    $ posted_today = True
    if the_person.event_triggers_dict.get("insta_new_boobs_brag", None) is not None:
        $ the_person.event_triggers_dict["insta_new_boobs_brag"] = None
        $ skimpy_outfit = insta_wardrobe.pick_random_outfit()
        $ the_person.apply_outfit(skimpy_outfit)
        $ rand_num = renpy.random.randint(0,2)
        if rand_num == 0:
            $ the_person.draw_person(the_animation = None)
        else:
            $ the_person.draw_person(position = "kneeling1", the_animation = None)
        $ mc.change_locked_clarity(15)
        the_person "Went to the doc and got some upgrades! Don't they look great?!" (what_style = "text_message_style")
        $ the_person.apply_outfit() # Reset them to their normal daily wear.
        $ del skimpy_outfit
    elif the_person.event_triggers_dict.get("insta_special_request_outfit", None):
        $ the_person.apply_outfit(the_person.event_triggers_dict.get("insta_special_request_outfit", insta_wardrobe.pick_random_outfit()))
        $ ran_num = renpy.random.randint(0,3)
        if ran_num == 0:
            $ the_person.draw_person(the_animation = None)
        elif ran_num == 1:
            $ the_person.draw_person(position = "kneeling1", the_animation = None)
        elif ran_num == 2:
            $ the_person.draw_person(position = "back_peek", the_animation = None)
        $ mc.change_locked_clarity(10)
        the_person "Wearing something special today: a design sent in by a fan!" (what_style = "text_message_style")
        $ the_person.event_triggers_dict["insta_special_request_outfit"] = None
    elif the_person.effective_sluttiness() + the_person.get_opinion_score(["showing her ass", "showing her tits"]) * 5 > 20: #TODO: Decide what slut_requirement should be.
        $ skimpy_outfit = insta_wardrobe.pick_random_outfit()
        $ the_person.apply_outfit(skimpy_outfit)
        $ ran_num = renpy.random.randint(0,3)
        if ran_num == 0:
            $ the_person.draw_person(position = "stand3", the_animation = None)
            $ mc.change_locked_clarity(5)
            the_person "Thought this outfit looked sexy. What do you think?" (what_style = "text_message_style")
        elif ran_num == 1:
            $ the_person.draw_person(position = "kneeling1", the_animation = None)
            $ mc.change_locked_clarity(10)
            the_person "Hey everyone, what do you think of this pose? I think it makes my tits look great!" (what_style = "text_message_style")
        elif ran_num == 2:
            $ the_person.draw_person(position = "back_peek", the_animation = None)
            $ mc.change_locked_clarity(5)
            the_person "Ass was looking great, just had to take a pic!" (what_style = "text_message_style")
        elif ran_num == 3:
            $ the_person.draw_person(position = "kneeling1", the_animation = None)
            $ mc.change_locked_clarity(10)
            the_person "Do I look good down on my knees?" (what_style = "text_message_style")
        if the_person.has_role(dikdok_role) and the_person.event_triggers_dict.get("dikdok_generate_video", False):
            the_person "If you liked that, come see me getting into trouble on DikDok! Hurry, I might get banned soon!" (what_style = "text_message_style")
            $ the_person.event_triggers_dict["dikdok_known"] = True
        elif the_person.has_role(onlyfans_role) and the_person.event_triggers_dict.get("instafans_generate_content", False):
            the_person "If you like that, subscribe to my OnlyFanatics and see soooo much more!" (what_style = "text_message_style")
            $ the_person.event_triggers_dict["onlyfans_known"] = True
        $ the_person.apply_outfit() # Reset them to their normal daily wear.
        $ del skimpy_outfit
    elif the_person.is_wearing_uniform() and not (the_person.vagina_visible() or the_person.tits_visible()):
        $ ran_num = renpy.random.randint(0,1)
        if ran_num == 0:
            $ mc.change_locked_clarity(5)
            $ the_person.draw_person(the_animation = None)
            the_person "Getting dressed for work. I make this uniform work!" (what_style = "text_message_style")
        elif ran_num == 1:
            $ mc.change_locked_clarity(10)
            $ the_person.draw_person(position = "back_peek", the_animation = None)
            the_person "I think my boss makes me wear this just because it makes my butt look good. At least he's right!" (what_style = "text_message_style")
    else:
        $ ran_num = renpy.random.randint(0,1)
        if ran_num == 0:
            $ the_person.draw_person(the_animation = None)
            the_person "Good morning everyone!"
        elif ran_num == 1:
            $ the_person.draw_person(position = "back_peek", the_animation = None)
            the_person "About to head out the door. I've got a full day ahead of me!"
    $ clear_scene()
    $ the_person.event_triggers_dict["insta_generate_pic"] = False
    return

label scroll_dikdok():
    $ dik_scroll = build_dik_scroll()
    $ dik_count = len(build_dik_scroll())-1
    while dik_count > -1:
        call view_dikdok(dik_scroll[dik_count]) from _call_view_dik_scroll
        menu:
            "Keep scrolling" if dik_count > 0:
                $ dik_count -= 1
            "Stop":
                $ dik_count = -1
    return

label scroll_onlyfans():
    $ only_scroll = build_only_scroll()
    $ only_count = len(build_only_scroll())-1
    while only_count > -1:
        call view_onlyfans(only_scroll[only_count]) from _call_view_onlyfans_scroll
        menu:
            "Keep scrolling" if only_count > 0:
                $ only_count -= 1
            "Stop":
                $ only_count = -1
    return

label social_notification_action_label():
    $ insta_count = len(build_insta_scroll())-1
    $ dik_count = len(build_dik_scroll())-1
    $ only_count = len(build_only_scroll())-1
    $ insta_scroll = build_insta_scroll()
    $ dik_scroll = build_dik_scroll()
    $ only_scroll = build_only_scroll()
    if time_of_day == 0:
        "As you reach for your phone where it was charging over night you see the screen light up."
    elif time_of_day == 4:
        "After you plug your phone in for the night you see it light up with some kind of message."
    elif mc.is_at_work():
        "As you are working you get what turns out to be a phantom vibration from the phone in your pocket, but while checking it you see something on the screen."
    elif mc.is_home():
        "As you walk back into your room after a quick bathroom break you see your phone screen light up."
    else:
        "You pull out your phone to pass a bit of down time and notice something on the screen."
    if insta_count >= dik_count:
        if insta_count >= only_count:
            $ choice = "InstaPic"
            $ number = insta_count+1
        else:
            $ choice = "OnlyFanatics"
            $ number = only_count+1
    elif dik_count >= only_count:
        $ choice = "DikDok"
        $ number = dik_count+1
    else:
        $ choice = "OnlyFanatics"
        $ number = only_count+1
    "It looks like you just got a notification from [choice]."
    "As a matter of fact, you've racked up [number] notifications from [choice] since you last checked it out."
    $ number = mc.location.get_person_count()
    if number < 1:
        "You're alone, so you don't have to worry about what comes up on your screen."
    elif number < 2:
        "There is only one person around, as long as you are careful she shouldn't see or hear anything on your phone."
    else:
        "There are a few people around, but you can angle your phone so they can't see anything."
    menu:
        "Take a look":
            $ done = False
            "You've got some time so you scan the room again and settle into a comfortable position."
            "You attach your earbuds just to be safe and unlock your phone."
        "Ignore them":
            $ done = True
            "You don't have time for this, you get back to what you were doing."
    while not done:
        $ insta_count = len(build_insta_scroll())-1
        $ dik_count = len(build_dik_scroll())-1
        $ only_count = len(build_only_scroll())-1
        $ insta_scroll = build_insta_scroll()
        $ dik_scroll = build_dik_scroll()
        $ only_scroll = build_only_scroll()
        if choice == "InstaPic":
            while insta_count > -1:
                call view_insta(insta_scroll[insta_count]) from _call_view_insta_event
                menu:
                    "Keep scrolling":
                        $ insta_count -= 1
                    "Stop":
                        $ insta_count = -1
        elif choice == "DikDok":
            while dik_count > -1:
                call view_dikdok(dik_scroll[dik_count]) from _call_view_dik_event
                menu:
                    "Keep scrolling":
                        $ dik_count -= 1
                    "Stop":
                        $ dik_count = -1
        elif choice == "OnlyFanatics":
            while only_count > -1:
                call view_onlyfans(only_scroll[only_count]) from _call_view_onlyfans_event
                menu:
                    "Keep scrolling":
                        $ only_count -= 1
                    "Stop":
                        $ only_count = -1
        $ insta_count = len(build_insta_scroll())
        $ dik_count = len(build_dik_scroll())
        $ only_count = len(build_only_scroll())
        "You close out the [choice] app, but while holding your phone you are reminded of the other social media apps you have sitting unused."
        "Would you like to check one of them?"
        menu:
            "Check InstaPic [insta_count]" if not choice == "InstaPic" and insta_count > 0:
                $ choice = "InstaPic"
            "Check DikDok [dik_count]" if not choice == "DikDok" and dik_count > 0:
                $ choice = "DikDok"
            "Check OnlyFanatics [only_count]" if not choice == "OnlyFanatics" and only_count > 0:
                $ choice = "OnlyFanatics"
            "No":
                $ done = True
    $ clear_scene()
    $ del insta_count
    $ del dik_count
    $ del only_count
    $ del insta_scroll
    $ del dik_scroll
    $ del only_scroll
    $ del done
    $ del choice
    $ del number
    return

label onlyfans_subscribe_label():
    $ days = -1
    $ count = onlyfans_renew_subscriptions(0, renew = False)
    $ total_count = len(build_only_scroll()) + count
    $ day_cost = 5*count
    $ week_cost = 20*count
    $ month_cost = 60*count
    "You follow [total_count] people on OnlyFanatics but [count] of your subscriptions have lapsed so you can't see their content."
    "Would you like to renew all of your inactive subsriptions?"
    menu:
        "Subscribe for a day\n{color=#ff0000}{size=18}Costs: $[day_cost]{/size}{/color}" if mc.business.has_funds(day_cost):
            $ mc.business.change_funds(-day_cost)
            $ days = 0
        "Subscribe for a day\n{color=#ff0000}{size=18}Costs: $[day_cost]{/size}{/color} (disabled)" if not mc.business.has_funds(day_cost):
            pass
        "Subscribe for a week\n{color=#ff0000}{size=18}Costs: $[week_cost]{/size}{/color}" if mc.business.has_funds(week_cost):
            $ mc.business.change_funds(-week_cost)
            $ days = 7
        "Subscribe for a week\n{color=#ff0000}{size=18}Costs: $[week_cost]{/size}{/color} (disabled)" if not mc.business.has_funds(week_cost):
            pass
        "Subscribe for a month\n{color=#ff0000}{size=18}Costs: $[month_cost]{/size}{/color}" if mc.business.has_funds(month_cost):
            $ mc.business.change_funds(-month_cost)
            $ days = 30
        "Subscribe for a month\n{color=#ff0000}{size=18}Costs: $[month_cost]{/size}{/color} (disabled)" if not mc.business.has_funds(month_cost):
            pass
        "Not now":
            pass
    if days > -1:
        $ onlyfans_renew_subscriptions(days, renew = True)
        $ only_count = len(build_only_scroll())-1
        $ only_scroll = build_only_scroll()
        "With your subscriptions renewed you have [only_count] unseen posts waiting for you. Would you like to watch them now?"
        menu:
            "Yes":
                while only_count > -1:
                    call view_onlyfans(only_scroll[only_count]) from _call_view_onlyfans_sebscribe
                    menu:
                        "Keep scrolling":
                            $ only_count -= 1
                        "Stop":
                            $ only_count = -1
            "No":
                pass
        $ del only_count
        $ del only_scroll
    $ del days
    $ del count
    $ del total_count
    $ del day_cost
    $ del week_cost
    $ del month_cost
    return
