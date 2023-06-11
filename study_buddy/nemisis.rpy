label nemesis_transition_label():
    $ the_sister = lily
    $ the_person = get_lab_partner()
    $ scene_manager = Scene()
    $ scene_manager.clear_scene()
    $ town_relationships.worsen_relationship(the_person, the_sister)
    $ the_person.outfit.restore_all_clothing()
    $ scene_manager.add_actor(the_person)
    mc.name "I've made a decision about how you can best serve me, and it will involve serving [the_sister.fname]."
    the_person "Yes [the_person.mc_title]."
    mc.name "She doesn't know this is going to happen yet, so I think we should just wait for her to come looking for you and then let her know."
    if mc.location == dungeon:
        mc.name "Let's head back up to my room and settle in to wait."
        $ mc.change_location(bedroom)
        "The two of you make your way to your room and then you take some time to pose [the_person.possessive_title] in a way that is sure to catch [the_sister.possessive_title]'s attention."
    else:
        "You take some time to pose [the_person.possessive_title] in a way that is sure to catch [the_sister.possessive_title]'s attention."
    $ the_person.outfit.strip_to_vagina(visible_enough = True)
    $ scene_manager.update_actor(the_person, position = "standing_doggy")
    "Once everything is in place you take a seat and admire the view while you wait. It isn't too long before you are rewarded with [the_sister.title]'s appearance."
    $ scene_manager.add_actor(the_sister, display_transform = character_right(xoffset = -.1))
    the_sister "Hey, has [the_person.fname] been to… what the fuck?"
    mc.name "Oh hey, I was wondering how much longer we would have to wait for you."
    the_sister "What?! Why were you waiting for me and more importantly why is [the_person.fname] bent over your desk with her ass sticking out?"
    mc.name "We had another talk about how [the_person.fname] has been treating you and finally have a solution."
    mc.name "Over the last few weeks I have taught her to obey my every command, and to test that I’ve commanded her to obey you as well."
    the_sister "That’s insane, and it still doesn’t explain what she is doing."
    mc.name "Well I figured since she has been such a pain in your ass with all her teasing this would be a good way to set things right."
    mc.name "It has the added benefit of proving her new obedience to assure you that you don’t have to worry any more."
    the_sister "So what, you want me to spank her?"
    mc.name "Not just me, she wants it too. Isn't that right?"
    the_person "Yes, please Mistress I’m so sorry. Do whatever you want to me. I want to prove that I’ll never tease you again."
    "Hesitates still clearly unsure about this but eventually walks forward to stand behind [the_person.fname]."
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.3), position = "back_peek")
    "With another glance towards you she raises her hand and brings it down firmly on [the_person.fname]'s behind."
    $ spank_factor_increment(the_person)
    mc.name "Come on you can do better than that."
    the_person "Yes please punish me for all that I’ve done."
    "There is another delay but she does bring her hand down again, harder this time."
    $ spank_factor_increment(the_person)
    "As you watch she continues unprompted, picking up speed and increasing force as she goes."
    "True to her word [the_person.fname] takes it and her gasps of shock and pain start to mix with moans of pleasure."
    "After one particularly sharp crack, followed by a louder moan, [the_sister.title] stops and rests her hand on [the_person.title]'s ass."
    $ spank_factor_increment(the_person)
    "As her hand lingers you notice it starting to move, squeezing slightly and rubbing in small circles."
    mc.name "She does have a nice ass doesn’t she?"
    $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.1))
    the_sister "Yes she does, especially when it is bright red."
    mc.name "So what do you think of your new subservient lab partner?"
    the_sister "I think I could get used to having someone who does whatever I want."
    mc.name "I’m glad you’re satisfied, and judging from that last moan I think [the_person.fname] is as well."
    mc.name "I should probably let the two of you get back to your school work."
    if the_sister.has_anal_fetish():
        the_sister "Actually, there is one more thing I want to try while you’re here to help. Do you have the strap on we bought at the mall? And maybe a bottle of lube?"
        mc.name "Yes I do, let me grab them."
        "Turns to [the_person.fname] and considers her pose."
        the_sister "Get down on the floor on your knees, face in the carpet ass in the air."
        $ scene_manager.update_actor(the_person, position = "doggy")
        $ scene_manager.update_actor(the_sister, display_transform = character_right(xoffset = -.1), position = "standing_doggy")
        "[the_person.fname] quickly complies as [the_sister.title] continues to talk."
        the_sister "You understand that you’ve been a pain in my ass correct?"
        the_person "Yes Mistress."
        the_sister "And in return I get to be a pain in your ass?"
        the_person "Yes Mistress."
        the_sister "But I haven’t yet, I was a pain on your ass. To really start over I’m going to need to do one more thing"
        the_person "Yes Mistress."

        "Turning to you [the_sister.title] looks up and asks:"
        the_sister "Have you ever done this with her before?"
        if not the_person.has_taboo("anal_sex"):
            mc.name "Yes"
        else:
            if not the_person.has_taboo("vaginal_sex"):
                mc.name "Her ass? No, we've been focused on other holes."
            else:
                mc.name "No"
            the_sister "Well then this should be fun. Let’s see how much she can take"
        "[the_sister.title] squirts some lube on her hand and rubs it down the toy. Then she drops down to her knees behind [the_person.title]."
        "She strokes it up and down the crack of [the_person.title]'s ass spreading the lube further and then lines up the head with her puckered rosebud."
        "With slow but firm pressure she pushes and you watch as the shaft starts to sink in."
        "[the_person.title] groans a bit and you look over to see her face knotted in pain."
        mc.name "Breathe just breathe."
        "[the_person.title] puffs out the air she was holding and then tries to relax, but there is still the occasional hitch as she works through the pain."
        "Looking back you see that [the_sister.title] has done it, the toy is buried nearly to the hilt in [the_person.title]'s ass."
        "You admire the view and see that [the_sister.title] is as well. It looks like she is a bit surprised at what she has done."
        mc.name "Satisfied?"
        the_sister "I am, do you think we could leave it in there while we finish studying?"
        mc.name "It’s not really designed for that."
        "And sure enough, as the two of you watch [the_person.title]'s body is starting to push the invading object out."
        "[the_sister.title] places her hand on the base and turns to look up at you."
        the_sister "Where are her panties?"
        mc.name "She doesn’t wear them, going commando was one of the first things I taught her"
        "With a sigh [the_sister.title] quickly stands up, reaches under her skirt and pulls out her own panties."
        "Bending back over to place her hand on the toy she holds them out to you."
        the_sister "Help her get these on so she can stand up without losing the remainder of her new role."
        "You do as she asks, a bit impressed at how quickly she has stepped into her new authority."
        if the_sister.has_role(slave_role):
            "You’ll have to have a conversation with her to make sure she remembers she is your slave too."
    "[the_person.title] is standing now, her breathing seems to be mostly back to normal and she has a look on her face that you can’t quite define."
    "It is like she has never seen [the_sister.title] before. A mix of wonder and shock with maybe a bit of admiration as well."
    "You may have created something a bit more than you intended, but only time will tell."
    "[the_sister.title] steps closer to you and leans in to give you a kiss."
    "[the_person.title]'s eyes widen a bit as it lingers, but she knows better than to question either of you now."
    the_sister "Thank you, you’re the best big brother ever."
    "Turning to her new slave [the_sister.possessive_title] continues:"
    the_sister "Come on, you have a lot of work to do if you want me to take that out before you go home tonight."
    the_person "Yes Mistress... Is that okay... Should I call you Mistress?"
    menu:
        "Let them be Mistress and Slave":
            the_sister "Yes, I like the sound of that, and I'll call you Slave."
            $ the_person.event_triggers_dict["titles_nemesis_lily"] = ["Mistress", "Slave"]
        "Help them pick titles":
            the_sister "I don't know... This is the first time I've done something like this."
            the_sister "What do you think [the_sister.mc_title]?"
            $ word_one = renpy.input("Pick [the_sister.fname]'s title. (Default: 'Mistress')", default='Mistress')
            while not word_one:
                $ word_one = renpy.input("Pick [the_sister.fname]'s title. (Default: 'Mistress')", default='Mistress')
            if word_one == "Mistress":
                mc.name "I like [word_one]."
            else:
                mc.name "I think [word_one] would be better."
            $ word_two = renpy.input("Pick [the_person.fname]'s title'. (Default: 'Slave')", default='Slave')
            while not word_two:
                $ word_two = renpy.input("Pick [the_person.fname]'s title'. (Default: 'Slave')", default='Slave')
            mc.name "And you should refer to [the_person.fname] as [word_two]."
            $ the_person.event_triggers_dict["titles_nemesis_lily"] = [word_one.strip(), word_two.strip()]
    $ [word_one, word_two] = the_person.event_triggers_dict.get("titles_nemesis_lily", ["Mistress", "Slave"])
    the_sister "Come along [word_two]."
    the_person "Yes [word_one]."
    $ clear_scene()
    "Once they leave you sit down at your computer, but all you can think about is the two girls down the hall."
    "It is a real shame that you don't have a way to monitor them as they continue to study... or whatever."
    $ del word_one
    $ del word_two
    return

label lily_study_buddy_nemesis(the_sister, the_person):
    call lesbian_sex(the_person, the_sister, add_to_log = False, path = ["oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2","oral2"]) from _call_lesbian_sex_nemesis
    return
