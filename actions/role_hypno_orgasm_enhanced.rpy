init 2 python:
    change_hypno_orgasm_word_action = Action("Change orgasm command word", hypno_trigger_orgasm_requirement, "change_hypno_orgasm_word_label",
        menu_tooltip = "Change the command word used to trigger orgasms.")

init 5 python:
    add_label_hijack("normal_start", "activate_hypno_orgasm_role_enhancement")
    add_label_hijack("after_load", "activate_hypno_orgasm_role_enhancement")

label change_hypno_orgasm_word_label(the_person):
    mc.name "There's something I want to talk to you about."
    "[the_person.possessive_title] nods and listens attentively."
    mc.name "I think we should change what we use to trigger your orgasms."
    the_person "Hmm? What should I focus on now?"
    $ old_word = the_person.event_triggers_dict.get("hypno_trigger_word", "Cum")
    $ new_word = renpy.input("Pick her new trigger word. (Current: '[old_word]')", default = old_word)
    while not new_word:
        $ new_word = renpy.input("Pick her trigger word. (Current: '[old_word]')", default = old_word)
    $ the_person.event_triggers_dict["hypno_trigger_word"] = new_word.strip()
    if " " in the_person.event_triggers_dict["hypno_trigger_word"]:
        mc.name "Your new phrase should be [new_word]."
    else:
        mc.name "Your new word should be [new_word]."
    the_person "Does that mean we get to train again?"
    mc.name "We do, but it should be quicker than last time."
    "You lean close and whisper right into her ear."
    mc.name "[new_word]. [old_word]. [new_word]."
    $ the_person.draw_person(emotion = "orgasm")
    $ mc.change_locked_clarity(30)
    "The results are immediate. [the_person.possessive_title] spasms, bucking her hips and gasping for breath."
    the_person "Oh god! Ah! Ah!"
    "Her orgasm is so intense that her knees buckle and she starts to collapse to the ground."
    menu:
        "Catch her":
            "You slide an arm around [the_person.title] and hold her up as she cums her brains out. She clings to you on instinct with her free hand."
            "Meanwhile, her other hand doesn't stop pumping in and out of her climaxing cunt."
            $ the_person.run_orgasm()
            $ the_person.change_love(2)
            "She gasps and moans into your ear for a long moment, but little by little her orgasm subsides."
            "When she is in control of herself again she stands under her own power and looks at you, a dumb smile spreading across her face."
        "Let her fall":
            "You step back and let her climax run its course."
            $ the_person.draw_person(position = "doggy", emotion = "orgasm")
            "[the_person.title] falls to the ground, barely catching herself at the last minute with her free hand."
            "She ends up face down, hips bucking with each new climactic spasm. Her thighs twitch in sync, all while she continues to finger herself."
            $ the_person.run_orgasm()
            $ the_person.change_slut(2)
            "She moans and writhes on the floor for a long moment, but little by little her orgasm subsides and she gains control of herself again."
            $ the_person.draw_person(position = "missionary", emotion = "happy")
            "[the_person.possessive_title] rolls over and looks up at you, a dumb smile spreading across her face."
    the_person "That was so intense... Do it again."
    $ the_person.draw_person()
    if " " in the_person.event_triggers_dict["hypno_trigger_word"]:
        "You spend some more time with [the_person.possessive_title], reinforcing the strength of her trigger phrase."
        "When you're finished you feel confident you can use it to make her cum on command with the new phrase."
    else:
        "You spend some more time with [the_person.possessive_title], reinforcing the strength of her trigger word."
        "When you're finished you feel confident you can use it to make her cum on command with the new word."
    $ del new_word
    $ del old_word
    return

label activate_hypno_orgasm_role_enhancement(stack):
    python:
        hypno_orgasm_role.add_action(change_hypno_orgasm_word_action)
        execute_hijack_call(stack)
    return
