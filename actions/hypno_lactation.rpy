init 0 python:
    def hypno_lactation_on_turn(person):
        person.event_triggers_dict["hypno_lactated_recently"] = False
        if person.event_triggers_dict.get("hypno_lactation_count", 0) > 0:
            if renpy.random.randint(0,10) < person.event_triggers_dict.get("hypno_lactation_count", 0):
                person.event_triggers_dict["hypno_lactation_count"] -= 1
                if person.lactation_sources > 0:
                    person.lactation_sources -= 1
        return

    def trigger_hypno_lactation_requirement(person):
        if person.event_triggers_dict.get("hypno_lactated_recently", False):
            return "She needs a break"
        if (0.1*(float(Person.rank_tits(person.tits)+person.lactation_sources))) * (person.arousal_perc) > 1:
            return "Already at maximum"
        return True

    def train_hypno_lactation_requirement(person):
        if person.has_role(hypno_lactation_role):
            return False
        if person.suggestibility < 50:
            return "Requires 50% Suggestibility"
        if pregnant_tits_requirement(person):
                return True
        if not person.knows_pregnant():
            return "Requires Pregnancy"
        return "Requires Tit Growth"

    def get_hypno_lactation_role_lactation_actions():
        trigger_hypno_lactation_action = Action("Trigger lactation", trigger_hypno_lactation_requirement, "trigger_hypno_lactation", menu_tooltip = "You've implanted a trigger word. You can make her lactate whenever you want.")
        change_hypno_lactation_word_action = Action("Change lactation command word", trigger_hypno_lactation_requirement, "change_hypno_lactation_word_label", menu_tooltip = "Change the command word used to trigger lactation.")
        return [trigger_hypno_lactation_action, change_hypno_lactation_word_action]

    hypno_lactation_role = Role("Hypno Lactation", actions = get_hypno_lactation_role_lactation_actions(), hidden = True, on_turn = hypno_lactation_on_turn)

    hypno_lactation_trainable = Trainable("hypno_lactation_train", "train_hypno_lactation", "Trigger Word Lactations", base_cost = 1000, unlocked_function = train_hypno_lactation_requirement)
    special_trainables.append(hypno_lactation_trainable)

label trigger_hypno_lactation(the_person):
    mc.name "Hey [the_person.title]..."
    the_person "Yeah?"
    $ the_person.event_triggers_dict["hypno_lactated_recently"] = True
    $ the_word = the_person.event_triggers_dict.get("trigger_hypno_word","Lactate")
    $ the_word.capitalize()
    mc.name "[the_word]."
    $ the_person.lactation_sources += 1
    if (0.1*(float(Person.rank_tits(the_person.tits)+the_person.lactation_sources))) * (the_person.arousal_perc) < 0.50:
        if the_person.arousal_perc < 30:
            $ the_person.change_arousal(30)
        $ the_person.draw_person()
        if the_person.tits_visible():
            "[the_person.title] doesn't have any idea what you did, but you can see her milk beginning to leak out of her exposed tits."
        elif the_person.outfit.wearing_bra():
            "[the_person.title] doesn't have any idea what you did, but you can see her milk beginning to leak through her bra."
        else:
            "[the_person.title] doesn't have any idea what you did, but you can see her milk beginning to soak into her clothes."
    elif (0.1*(float(Person.rank_tits(the_person.tits)+the_person.lactation_sources))) * (the_person.arousal_perc) < 1:
        if the_person.arousal_perc < 20:
            $ the_person.change_arousal(30)
        else:
            $ the_person.change_arousal(10)
        $ the_person.draw_person(emotion = "happy")
        if the_person.tits_visible():
            "[the_person.title] doesn't quite seem to realize what you did, but you can see her milk clearly dripping out of her exposed tits."
        elif the_person.outfit.wearing_bra():
            "[the_person.title] doesn't quite seem to realize what you did, but you can see her milk clearly dripping through her bra."
        else:
            "[the_person.title] doesn't quite seem to realize what you did, but you can see her milk clearly soaking into her clothes."
        "She may not be entirely aware, but you see her smile widen as the physical reaction links into her emotional connection with breast feeding."
    else:
        if the_person.arousal_perc < 10:
            $ the_person.change_arousal(30)
        else:
            $ the_person.change_arousal(20)
        $ the_person.draw_person(emotion = "orgasm")
        if the_person.tits_visible():
            "[the_person.title] gasps a bit and trembles as her milk lets down and you can see her milk flowing freely from her exposed tits."
        elif the_person.outfit.wearing_bra():
            "[the_person.title] gasps a bit and trembles as her milk lets down and you can see her milk flowing freely through her bra to drip down her abdomen."
        else:
            "[the_person.title] gasps a bit and trembles as her milk lets down and you can see her milk soaking right through her clothes."
        if the_person.arousal_perc >= 100:
            $ the_person.have_orgasm()
    "You are lost in the sight of her for a moment before you remember she asked you a question."
    mc.name "Oh, I was just saying how nice you look today."
    $ the_person.draw_person(emotion = "happy")
    the_person "Thanks [the_person.mc_title]!"
    $ del the_word
    $ clear_scene()
    return

label train_hypno_lactation(the_person):
    mc.name "There's something I want to talk to you about."
    "[the_person.possessive_title] nods and listens attentively."
    if the_person.knows_pregnant():
        if the_person.has_child_with_mc():
            mc.name "Since you are pregnant, I was wondering if you are still breastfeeding as well."
            the_person "Yes I am, once this new baby is born I'll be breastfeeding both at the same time."
            mc.name "Won't that be kind of demanding?"
            the_person "It can be, but lots of people do it. Why do you ask?"
        else:
            if the_person.kids > 0:
                mc.name "Since you are pregnant, I was wondering if your milk had started to come in."
                the_person "Not yet, but I've done this before and it should be here when I need it."
            else:
                mc.name "Since you are pregnant, I was wondering if your milk had started to come in."
                the_person "Not yet, according to what I've read it should get here right around my due date."
                mc.name "I've heard that sometimes it can be hard to get started, and even after that keeping a steady supply can be difficult."
                the_person "It can be challenging, but I'm sure I can handle it. Why do you ask?"
                mc.name "I'd like to ensure you have enough milk for your new baby, and was researching methods to increase production."
                mc.name "Worst case scenario, you would be able to save up some extra by pumping so that if you want to take a mini vacation or have a couple drinks you don't need to worry about your milk."
                the_person "That does sound pretty good, what did you have in mind?"
    else:
        mc.name "You're breastfeeding right now aren't you?"
        the_person "Yes."
        mc.name "I've heard that can be challenging, you never get to take event a short trip and you can't drink."
        the_person "Well not unless I've pumped enough to save up a bit of a extra supply."
        mc.name "Right, still it must be tough."
        the_person "It is a sacrifice, but one I'm happy to make."
        mc.name "Even so, I'd like to try and help you out."
        the_person "What did you have in mind?"
    if the_person.lactation_sources > 0:
        mc.name "I'd like to try and induce some extra lactation by trying to get you to let down on command."
    else:
        mc.name "I'd like to try and induce lactation on command."
    if mc.location.get_person_count() > 1:
        the_person "Right here? There are people around..."
        mc.name "Forget about them. It is a perfectly natural part of motherhood."
    elif the_person.love < 40:
        the_person "Right in front of you? I don't know..."
        mc.name "Forget about me, this is about what you need. Think of your baby."
    else:
        the_person "Right now? I don't know..."
        mc.name "Why not right now? Come on, you know you need this."
    "She thinks about it for a moment. Her trance makes the outcome all but guaranteed."
    the_person "Okay, I'll do it. How should we start?"
    mc.name "According to my research we need to get you to relax first so lets start with a massage."
    if the_person.sluttiness_tier() == 0:
        the_person "That sounds nice."
    elif the_person.sluttiness_tier() == 1:
        the_person "That sounds nice, let me move some of these clothes out of the way for you."
        if the_person.outfit.wearing_bra():
            while the_person.outfit.bra_covered():
                $ generalised_strip_description(the_person, the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True))
        elif not the_person.tits_visible():
            while not the_person.tits_visible():
                $ generalised_strip_description(the_person, the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True))
        $ generalised_strip_description(the_person, the_person.outfit.get_half_off_to_tits_list(), half_off_instead = True)
    elif the_person.sluttiness_tier() == 2:
        the_person "That sounds nice, let me move these clothes out of the way for you."
        $ generalised_strip_description(the_person, the_person.outfit.get_tit_strip_list())
    else:
        the_person "That sounds nice, let me get ready for you."
        $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())
    $ the_person.update_outfit_taboos()
    $ the_person.draw_person(position = "walking_away")
    "You start at [the_person.title]'s shoulders, working out some basic tension."
    "The feeling of her tension draining away is pretty empowering as you work down her back."
    if the_person.sluttiness_tier() > 1:
        mc.name "This is a good start, but to focus on the right body parts I'm going to need to work on your front too."
        the_person "Oh, of course."
        "You step around [the_person.possessive_title] taking in the lovely view of her chest."
        $ the_person.draw_person()
        mc.name "I'm going to simulate milking both of your breasts at the same time."
        the_person "That seems like the most efficent thing to do!"
        $ mc.change_locked_clarity(20)
        if the_person.lactation_sources > 0:
            "You put your hands on her engorged mammaries. The skin is hot and feels like it's pulled tight, her tits are so full of milk."
            the_person "Aahhh... I mean... it feels really good too..."
            "You start to squeeze them in rhythm. First one, then the other. It takes several seconds, but soon milk starts to dribble out of the tip."
        else:
            "You put your hands on her mammaries. The skin is hot but there doesn't seem to be much going on yet."
            the_person "Aahhh... I mean... it feels really good too..."
            "You start to squeeze them in rhythm. First one, then the other. It doesn't look like anything is happening, but you feel some slight changes."
        if the_person.sluttiness_tier() > 2:
            the_person "I think it's working, but do you think maybe using your hands is a bit unnatural."
            mc.name "What do you mean?"
            the_person "Well babies suckle, and even if I pump there is sucction there, I think just squeezing isn't giong to be enough."
            mc.name "That sounds like a perfect next step."
            $ the_person.draw_person(position = "sitting")
            the_person "Come here and sit next to me."
            if the_person.lactation_sources > 0:
                "You sit down next to [the_person.title] in an awkward move, she gently lowers you on to her lap. You look up at her full, milk laden tits hungrily."
                "You bring your lips to her nipple and begin to suckle. Tiny drips begin to escape it, giving you a taste of milk."
            else:
                "You sit down next to [the_person.title] in an awkward move, she gently lowers you on to her lap. You look up at her tits hungrily."
                "You bring your lips to her nipple and begin to suckle. It takes several seconds, but soon milk starts to dribble out of the tip."
            $ the_person.change_arousal(10)
            $ mc.change_locked_clarity(30)
            "She takes one of your hands and puts it on her other breast."
            the_person "Here... squeeze this side too..."
    "It is clear that the relaxation from the massage is turning into pressure of another kind."
    $ the_word = renpy.input("Pick her trigger word. (Default: 'Lactate')", default='Lactate')
    while not the_word:
        $ the_word = renpy.input("Pick her trigger word. (Default: 'Lactate')", default='Lactate')
    $ the_person.event_triggers_dict["trigger_hypno_word"] = the_word.strip()
    "You lean very close to [the_person.possessive_title] and whisper \"[the_word]\" into her ear."
    mc.name "Focus on that as you let go. All that pressure you're feeling..."
    mc.name "Focus it all onto that one word."
    "You guide her closer and closer to her lactation, whispering reminders in her ear that she can't let down until she hears her trigger word."
    "You lean close and whisper right into her ear."
    mc.name "[the_word]."
    $ the_person.lactation_sources += the_person.sluttiness_tier()
    $ the_person.event_triggers_dict["hypno_lactation_count"] = the_person.event_triggers_dict.get("hypno_lactation_count", 0) + the_person.sluttiness_tier()
    $ the_person.event_triggers_dict["hypno_lactated_recently"] = True
    $ mc.change_locked_clarity(30)
    if the_person.sluttiness_tier() <3:
        $ the_person.draw_person(emotion = "orgasm")
        $ the_person.draw_person(position = "sitting")
        if the_person.lactation_sources > 2:
            "[the_person.title] gives a moan, and the floodgates open as her breasts let down. Milk is now coming out in a steady stream from both tits, and every time you squeeze it spurts out forcefully."
            the_person "Oh god... that feels so good..."
            if the_person.arousal_perc < 10:
                $ the_person.change_arousal(30)
            else:
                $ the_person.change_arousal(20)
            $ mc.change_locked_clarity(30)
            "[the_person.possessive_title] is panting as her tits rapidly spray milk in front of her. She is expressing an impressive amount."
        else:
            "[the_person.title] gives a moan as she lets down. Now with each squeeze, her nipples emit a short but steady squirt."
            the_person "Mmm, that feels so good..."
            if the_person.arousal_perc < 20:
                $ the_person.change_arousal(30)
            else:
                $ the_person.change_arousal(10)
            $ mc.change_locked_clarity(10)
        $ the_person.change_stats(happiness = 5, slut = 1, max_slut = 50)
    else:
        $ the_person.draw_person(position = "sitting", emotion = "orgasm")
        if the_person.lactation_sources > 2:
            "Suddenly, the milk begins to flow much more rapidly as [the_person.possessive_title] starts to let down. Milk is pouring into your mouth at an alarming rate."
            "You quickly swallow gulp after gulp, just keeping up with her production. Her milk is smooth, sweet, and creamy."
            if the_person.arousal_perc < 5:
                $ the_person.change_arousal(30)
            else:
                $ the_person.change_arousal(25)
            $ mc.arousal += 15
            $ mc.change_locked_clarity(30)
            the_person "Oh my god, yes that's it."
            "Her hand is running through your hair. It is a very intimate encounter to suckle from her like this."
        else:
            "[the_person.possessive_title]'s milk starts to flow more freely as she lets down. You are able to spend a few seconds at a time sucking, swallow, then repeat."
            "Her milk is smooth, sweet, and creamy."
            if the_person.arousal_perc < 15:
                $ the_person.change_arousal(30)
            else:
                $ the_person.change_arousal(15)
            $ mc.arousal += 10
            $ mc.change_locked_clarity(10)
            the_person "Mmm, that feels really nice..."
    $ the_person.change_love(2)
    "She whispers and coos into your ear for a long moment, but little by little her lactation subsides."
    "When she is in control of herself again she stands under her own power and looks at you, a dumb smile spreading across her face."
    the_person "That was so intense... Do it again."
    $ the_person.draw_person()
    "You spend some more time with [the_person.possessive_title], reinforcing the strength of her trigger word."
    "When you're finished you feel confident you can use it to make her lactate on command."
    $ the_person.add_role(hypno_lactation_role)
    $ del the_word
    $ clear_scene()
    return True

label change_hypno_lactation_word_label(the_person):
    $ old_word = renpy.input("Pick her trigger word. (Default: '[old_word]')", default = old_word)
    while not new_word:
        $ new_word = renpy.input("Pick her trigger word. (Default: '[old_word]')", default = old_word)
    $ the_person.event_triggers_dict["trigger_hypno_word"] = new_word.strip()
    $ del new_word
    $ del old_word
    return
