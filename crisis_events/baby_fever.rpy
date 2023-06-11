init -1 python:
    def baby_fever_get_people():
        temp_list = []
        final_list = []
        for person in known_people_in_the_game():
            if person not in [lily, mom, cousin, aunt]:
                if person.location == mc.location:
                    if not person.event_triggers_dict.get("preg_knows", False): # not pregnant
                        if person.event_triggers_dict.get("last_birth", 0) < 1: # no baby
                            if person.event_triggers_dict.get("baby_fever_chat", 0) < day -14: # no recent talk
                                if pregnant_people(person):
                                    temp_list.append(person)
        if temp_list:
            while len(final_list) < 1:
                target = mc.business.event_triggers_dict.get("baby_fever", -4)
                for person in temp_list:
                    if person.get_opinion_score("creampies") + person.get_opinion_score("bareback sex") == target:
                        final_list.append(person)
                if not final_list:
                    if target == 4:
                        mc.business.event_triggers_dict["baby_fever"] = -4
                    else:
                        mc.business.event_triggers_dict["baby_fever"] = target + 1
        return final_list

    def crisis_baby_fever_requirement():
        if mc.business.event_triggers_dict.get("baby_fever_chat", 0) < day - 5:
            if baby_fever_get_people():
                return True
        return False

init 3 python:
    crisis_baby_fever_action = ActionMod("Crisis Baby Fever", crisis_baby_fever_requirement, "crisis_baby_fever_label",
        menu_tooltip = "A person is jealous of an expectant mother.", category = "Misc", is_crisis = True, is_morning_crisis = False, priority = 5)

label crisis_baby_fever_label():
    $ mc.business.event_triggers_dict["baby_fever_chat"] = day
    $ the_person = get_random_from_list(baby_fever_get_people())
    $ the_person.event_triggers_dict["baby_fever_chat"] = day
    $ influence = the_person.suggestibility
    if pregnant_family(the_person):
        $ the_mother = get_random_from_list(pregnant_family(the_person))
    else:
        $ the_mother = get_random_from_list(pregnant_people(the_person))
    $ so_title = SO_relationship_to_title(the_person.relationship)
    $ opinion = the_person.get_opinion_score("creampies") + the_person.get_opinion_score("bareback sex")
    $ relationship = town_relationships.get_relationship(the_mother, the_person).type_a
    $ the_person.draw_person(emotion="happy")
    "You're not really doing anything at the moment so you take a look around the room."
    "It seems like you aren't the only one bored, [the_person.title] is also sort of staring off into space but seems to notice your eyes pass over her."
    "[the_person.possessive_title] walks up to you and strikes up a conversation. After a bit of small talk it is clear she has something specific on her mind."
    if the_mother not in known_people_in_the_game():
        the_person "I have sort of a weird question for you. Do you know [the_mother.fname] [the_mother.last_name]?"
        mc.name "Sorry, I can't say that I do."
        the_person "Oh, well I'll have to introduce you sometime."
        # on enter event: [planned_intro] = person req both together
    elif the_mother in [mom, lily, cousin, aunt]:
        the_person "Congratulations by the way. I've been meaning to talk to you for a while."
        mc.name "Congratulations?"
        the_person "Yeah, you know, [the_mother.fname] is going to have her baby soon."
        "What!? Is [the_mother.possessive_title] telling people you are the father of her baby?"
        mc.name "...oh right... thanks?"
        the_person "Sorry, I guess that is a little weird. Congratulations isn't exactly what I meant."
        mc.name "Umm..."
        if the_mother == mom:
            the_person "Still, you must be excited. Soon you are going to get to be a big brother all over again."
            "Oh right, your new sibling..."
        elif the_mother == lily:
            the_person "Still, you must be excited. You're going to be an uncle soon."
            "Oh right, your new niece or nephew..."
        elif the_person == cousin:
            the_person "Still, you must be excited. The new baby is going to be your second cousin right?"
            mc.name "Actually they will be my first cousin once removed."
            the_person "Oh, I can never keep them straight. I just call everyone in my extended family cousins."
        else:
            the_person "Still, you must be excited. Another cousin for you and your sister."
            "Oh right, your new cousin..."
        "It seems like your family tree is going to be a bit more tangled then most going forward."
        mc.name "Right. Thank you! I'm really looking forward to the new baby."
    elif the_mother in unique_character_list:
        the_person "I've been thinking about [the_mother.fname] recently."
    else:
        the_person "You know [the_mother.fname] right?"
    the_person "We were talking the other day and I couldn't help but notice her body."
    mc.name "Really? I didn't know you were interested in girls [the_person.title]."
    the_person "What, no that isn't what I mean. The way her body is changing."
    if the_mother.event_triggers_dict.get("preg_transform_day", 0) > day:
        the_person "It is subtle, but I can tell something is going on. I'm pretty sure she is pregnant."
        mc.name "Really? I guess maybe I need to spend more time staring at her boobs."
    else:
        the_person "It is pretty clear that something is different. You know she is pregnant right?"
        mc.name "Oh that, of course. I mean I'd have to be blind to miss the signs by now."
    if the_person.has_role(girlfriend_role):
        the_person "Well, don't look too hard. I would think having me around would give you enough eye candy."
    mc.name "So, is this just idle gossip or..."
    the_person "Actually, seeing her made me think about my body a bit."
    if the_person.body_type == "thin_body":
        the_person "I've always taken pride in my body, keeping it toned and fit."
    elif the_person.body_type == "standard_body":
        the_person "I've always felt comfortable in my body without working too hard."
    else:
        the_person "I've always been a little self conscious about my body."
    the_person "Seeing her, and the way she is growing has given me a new perspective."
    mc.name "Really?"
    if opinion < 0:
        the_person "Yeah, she is blowing up like a balloon. She looks like she can barely fit in her clothes."
        the_person "It gives me one more reason to avoid getting knocked up anytime soon."
        $ the_person.update_birth_control_knowledge()
        if the_person.on_birth_control:
            if opinion < -2:
                the_person "I mean, I'm on birth control and I still try to be careful about condoms."
            else:
                the_person "I mean, there is a reason I take birth control."
        else:
            if opinion < -2:
                the_person "I'm not taking birth control right now but I try to be careful with condoms."
            else:
                the_person "I should really get myself some new birth control pills."
        mc.name "Oh, well motherhood isn't for everyone."
        the_person "Exactly... although there is one aspect that does make me sort of jealous."
    else:
        the_person "Yeah, I mean she is certianly bigger than me, but it looks so natural and beautiful."
        the_person "There is this glow about her that I can't really define."
        $ the_person.update_birth_control_knowledge()
        if the_person.on_birth_control:
            if opinion < 2:
                the_person "My hormones are urging me to forget my birth control, but I'll probably keep using other protection."
            else:
                the_person "It sort of makes me want to stop my birth control and see what happens."
        else:
            if opinion < 2:
                the_person "My hormones have been a bit crazy without birth control stabilizing them."
            else:
                the_person "I'm glad I'm not on birth control, the idea of being filled up without protection is kind of exciting."
        mc.name "Well you would make an excellent mother if my opinion means anything."
        the_person "Thanks, plus there would be at least one other significant advantage to getting knocked up."
    the_person "Her tits are so full she has been practially spilling out of her clothes."
    the_person "There is something primal about seeing her swollen breasts. I get this unexplained desire that just fills my body."
    mc.name "I know exactly what you mean."
    the_person "Yeah, I'm sure you do."
    if Person.rank_tits(the_person.tits) > Person.rank_tits(the_mother.tits):
        the_person "Of course I still have the advantage on size, although if mine were to swell like hers they would be truly epic."
    else:
        the_person "It makes me think about getting a boob job so that I can keep up with her, or maybe even go further."
    the_person "I'd look incredible with bigger tits, don't you think [the_person.mc_title]?"
    if the_person.sluttiness > 40:
        "To drive her point home [the_person.title] reaches up and grabs her tits, pushing them up to accentuate her cleavage."
        $ mc.change_locked_clarity(10)
    mc.name "You absolutely would."
    "She seems lost in thought for a moment and you take advantage of the break in the conversation to stare at her body a bit."
    $ body_type = the_person.body_type
    $ tit_size = the_person.tits
    $ the_person.tits = Person.get_larger_tit(the_person.tits)
    $ the_person.draw_person(position="stand2", emotion="happy")
    "[the_person.possessive_title] does have amazing tits, but seeing them grow naturally as part of her pregnancy would be almost as enjoyable as the act of impregnanting her."
    $ the_person.tits = Person.get_larger_tit(the_person.tits)
    $ the_person.outfit.strip_to_underwear()
    $ the_person.draw_person(position="stand3", emotion="happy")
    "Watching them grow day by day until she could barely contain them in her bra would certainly make your time with her more enjoyable."
    "Then her belly would start to swell with your seed, filling her up with a new life that you created together."
    $ the_person.body_type = "standard_preg_body"
    $ the_person.draw_person(position="stand4", emotion="happy")
    "Watching her body grow and transfom in service to your needs and demands would fill you with pride."
    "Knowing her devotion and desire to serve you is such a driving force that she is willing to carry your children would certianly add to the pleasure you take in her body."
    $ the_person.draw_person(position="back_peek", emotion="happy")
    the_person "...[the_person.mc_title]?"
    $ the_person.tits = tit_size
    $ the_person.body_type = body_type
    if the_person.is_employee() and the_person.is_at_office():
        $ the_person.wear_uniform()
    else:
        $ the_person.apply_planned_outfit()
    $ the_person.draw_person(emotion="sad")
    "Oh shit! Was she talking to you?"
    mc.name "Sorry, what was that?"
    the_person "I said, do you think it would be crazy for me to try and get pregnant?"
    menu:
        "Encourage motherhood":
            $ influence +=20
            mc.name "I think getting pregnant and having a baby would be great for you."
            mc.name "You would make an incredible mother, and I'd love to see your body swell through your pregnancy."
            the_person "You really think so? [the_mother.fname] looks so fulfilled, I'd love to feel that way too."
        "Discourge motherhood":
            $ influence -=20
            mc.name "Babies might be great, but you don't want to sacrifice the life you have now."
            mc.name "I don't think you have thought about all the impacts a baby would have on your life."
            the_person "You might be right, she just looks so fulfilled."
    mc.name "You don't have to decide right now. It is a big decision, you should weigh the options."
    the_person "I know, it's just..."
    if relationship == "Mother":
        the_person "Seeing my mom pregnant again really makes me think about starting a family of my own."
        the_person "I already know she is a great mom, her baby is going to be so lucky."
    elif relationship == "Daughter":
        the_person "I'm so excited about having a grandbaby, but it really makes me think about how happy I was raising [the_mother.fname]."
        if the_mother.kids < 1:
            the_person "I can't wait to see how she does as a mother."
    elif relationship == "Sister":
        the_person "I can't wait to be an aunt, but it makes me a bit jealous of my [relationship!l] too."
        if the_person.age > the_mother.age:
            the_person "I mean, I am older than her and I don't have any kids of my own."
        else:
            the_person "Altough I guess I still have time. She is older than me after all."
    elif relationship == "Rival" or relationship == "Nemesis":
        the_person "I hate seeing her so happy."
        if the_mother.kids < 1:
            the_person "It kills me to admit it, but she is probably going to make a great mom."
    else:
        the_person "I love seeing her so happy."
        if the_mother.kids < 1:
            the_person "She has so much love to give, she'll make such a great mom."
    if not the_person.is_single() and not the_person.is_girlfriend():
        if the_person.kids < 1:
            the_person "I've started thinking about talking to [the_person.SO_name], see if maybe we could get serious about starting a family."
        else:
            the_person "I've been thinking about talking to [the_person.SO_name] about giving me a new baby."
        menu:
            "Offer an alternative":
                mc.name "You know, if you're serious about starting a family I would be happy to help you with that."
                if the_person.love > leave_SO_love_calculation(the_person) - 10:
                    the_person "Wait, are you serious? I'd love to start a family with you. I just thought I'd have to do it with my [so_title]."
                    mc.name "Absolutely, tell him you are through and the two of us can start planning for the future."
                    call transform_affair(the_person) from _call_transform_affair_baby
                    $ the_person.change_love(10)
                    $ the_person.change_obedience(5)
                    $ the_person.draw_person(position = "kissing", special_modifier = "kissing")
                    "You put your arms around her waist and she kisses you immediately. When you break the kiss she's grinning ear to ear."
                    $ the_person.draw_person(emotion = "happy")
                    $ ex_title = so_title[:4]
                    the_person "It feels so good to not have to hide anything anymore! I'll break the news to my [ex_title]... My ex-[so_title] later today."
                else:
                    the_person "You can't be serious. I already have a [so_title]. Do you really think I'd leave him for you just to have a kid?"
                    mc.name "Sorry, I wasn't thinking clearly."
            "Raise concerns":
                if the_person.relationship == "Girlfriend":
                    mc.name "Your [so_title]? Are you sure that relationship is going to last?"
                    mc.name "I don't mean to question your choice in men, but he might not be there for you long term."
                elif the_person.relationship == "Fiancée":
                    mc.name "Your [so_title]? How long have you been engaged now?"
                    mc.name "You might want to wait until the marrige to commit to such a life changing decision."
                else:
                    mc.name "Your [so_title]? That makes sense."
                    if person.kids == Person.number_of_children_with_mc():
                        mc.name "It's actually a little surprising you haven't started one already. Does he want kids?"
                    else:
                        mc.name "I mean you already have kids with him right? Does he want more?"
                    the_person "I think so..."
                the_person "Maybe you're right, I guess I need to talk with him."
                mc.name "You should definitely do that soon."
                $ the_person.on_talk_event_list.append(relation_ship_quarrel)
            "Show support":
                mc.name "That's great! I'm sure he would be thrilled to give you a child."
    elif the_person.is_girlfriend():
        the_person "I know we are just dating, but do you think we could talk about starting a family?"
        menu:
            "Absolutely":
                mc.name "I'd love to start a family with you [the_person.title]."
                the_person "That is so great to hear, I think we could raise incredible kids."
            "Not yet":
                mc.name "I don't think I'm ready for that. What we have is great, but it is still so new."
                the_person "Of course, no pressure. Just my hormones going crazy."
    else:
        the_person "I don't even have anyone that would be able to father the children."
        menu:
            "Offer your seed":
                mc.name "You know, if you are looking for a donor I would be happy to help you out."
                if the_person.has_taboo("vaginal_sex"):
                    "She is stunned by this statement and stares at you in disbelif for a moment."
                    the_person "You can't be serious? Is this some kind of weird way to try and get into my pants?"
                    mc.name "Hey, I was just offering. You can say no."
                elif the_person.has_taboo("condomless_sex"):
                    the_person "Trying to finally get into me bare [the_person.mc_title]?"
                    mc.name "I admit, that would be a perk I'll happily accept."
                else:
                    the_person "That could be fun, I'm assuming you mean trying naturally right?"
                    mc.name "Of course, no need to involve medical professionals if we can get there without them."
            "Start a relationship" if the_person.love > 60:
                mc.name "Actually I have a solution for that problem. I've been thinking about this for a while now."
                mc.name "I really like you and I hope you feel the same way about me."
                mc.name "I'd like to make our relationship official. What do you say?"
                $ the_person.change_happiness(15)
                $ the_person.change_love(5)
                if the_person.age > 40:
                    the_person "Oh I'm so happy to hear you say that! I was worried about our age difference, but I don't want that to stop us!"
                else:
                    the_person "Oh my god, I'm so happy! Yes, I want to be your girlfriend!"
                "She puts her arms around you and pulls you close."
                $ mc.change_locked_clarity(10)
                "She kisses you, and you kiss her back just as happily."
                $ the_person.add_role(girlfriend_role)
            "Stay silent":
                pass
    if opinion < 4:
        if the_person.on_birth_control:
            the_person "That also means going off birth control."
            menu:
                "Stop your birth control":
                    mc.name "You should stop taking it."
                    the_person "Do you really think so?"
                    mc.name "Yes, the sooner you stop taking those pills the sooner you can try getting knocked up."
                    $ manage_bc(the_person, start = False)
                "Keep taking birth control":
                    mc.name "Let's not be too hasty, this is something you should think about."
                    the_person "Yeah, I guess."
                    mc.name "You have time, be sure you really want this before you do anything rash."
        else:
            the_person "It's not like I've been working too hard to avoid having kids."
        if the_person.get_opinion_score("bareback sex") > 1:
            the_person "Plus it is always great to have a guy enter me raw."
            if the_person.get_opinion_score("creampies") > 1:
                the_person "And when they finish inside me I nearly always cum."
            else:
                the_person "Although cleaning up after someone fills me up can be annoying."
            $ the_person.discover_opinion("creampies")
        else:
            the_person "Altough I've always felt safer with my partner using a condom."
        $ the_person.discover_opinion("bareback sex")
        menu:
            "Try to influence her":
                $ number = -2
                if the_person.has_role(trance_role):
                    $ influence +=20
                if the_person.has_exact_role(heavy_trance_role):
                    $ influence +=20
                elif the_person.has_exact_role(very_heavy_trance_role):
                    $ influence +=40
                while number < 2:
                    if the_person.get_opinion_score("bareback sex") == number:
                        $ number = 2
                        mc.name "You know, if you really want to have amazing sex the only way to go is raw."
                        mc.name "There is nothing like feeling the pulsing heat of your partner."
                        if renpy.random.randint(1, 100) < influence:
                            the_person "I know what you mean. I've just always been too worried about the consequences."
                            $ the_person.increase_opinion_score("bareback sex")
                            the_person "Maybe I'll give it a try next time and see how it feels."
                        else:
                            the_person "Sorry, the risk just isn't worth it to me."
                    elif the_person.get_opinion_score("creampies") == number:
                        $ number = 2
                        mc.name "You know, if you've never felt a man blow his load deep inside than you don't know what you're missing."
                        mc.name "The biological clock is a powerful force, and I've know girls who cum just because their body feels like it is accomplishing that most basic imperative."
                        if renpy.random.randint(1, 100) < influence:
                            the_person "That does make sense, I've just always hated the clean up afterwards."
                            $ the_person.increase_opinion_score("creampies")
                            the_person "Maybe I'll give it a try next time and see how it feels."
                        else:
                            the_person "Sorry, the risk just isn't worth it to me."
                    else:
                        $ number +=1
            "Leave her opinions alone":
                mc.name "I guess you're right."
    elif not the_person.has_role(breeder_role):
        mc.name "You know, this conversation reminds me..."
        $ start_breeding_fetish_quest(the_person)
        call train_breeder_label(the_person) from _call_train_breeder_label_baby
        $ the_person.update_birth_control_knowledge()
    else:
        mc.name "You know, I think I have a way to make you happy."
        call breeding_fetish_bend_her_over_label(the_person) from _call_breeding_fetish_bend_her_over_label_baby
    return

label lily_baby_fever():
    $ the_person = lily
    $ the_mothers = pregnant_people(the_person)
    $ the_mother = get_random_from_list(the_mothers)
    if the_mother == mom:
        the_person "I can't believe mom is pregnant at her age."
        the_person "I guess she isn't really that old, but by the time this baby is grown up she will be."
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            the_person "Why did you have to cum inside her so much [the_person.mc_title]?"
            the_person "I know you're the father, it's not like the two of you have been careful about using protection."
            the_person "I swear, the number of cum stains I've seen in her bedroom makes it look like you are the one who lives in there."
            the_person "Do you love her more than me?"
            the_person "I'm here for you too and my tight young pussy has got to be way more fertile than hers."
            the_person "Seeing the way she has been glowing the last few days has got me thinking."
        else:
            the_person "Who even is the father? It's not like she has been dating anyone."
            the_person "Do you think it could be someone she works with? That is the only place she really goes when she isn't home."
        the_person "There's no way that I really remember nursing from her, but sometimes when she leans over by me I get this bizarre muscle memory reaction like I want to suckle from her."
        mc.name "You know, if you wanted to ask her about her milk she might want some help."
        mc.name "She doesn't really have a use for it yet and I'm sure the pressure can get painful when they fill up too much."
        #write another morning crisis
    if the_mother == cousin:
        the_person "Have you seen how big [the_mother.fname] is getting?"
        the_person "She has always been a bit bigger than me but it is getting ridiculous as she swells up with her baby."
        the_person "And have you seen her tits? They are huge and starting to leak a bit. When I see them I get the weirdly compelling thirst."
        the_person "Do you know who the father is? Everytime I try to discuss it she gets mad at me."
        the_person "TEXT"
    if the_mother == aunt:
        pass
    if the_mother == erica and "threesome" in erica_get_wakeup_options():
        pass
    if the_mother == sarah and get_person_by_identifier(sarah.event_triggers_dict.get("initial_threesome_target", None)) == the_person:
        pass
    if the_person.sex_record.get(oral, 0) > 0:
        if the_person.sex_record.get("vaginal_sex", 0) == 0:
            the_person "I know we haven't gone all the way yet, but I've been thinking that maybe we could try it."
        if the_person.sex_record.get(anal, 0) > 0:
            the_person "I love it in my ass, but my pussy is ready for you too."
        else:
            if the_person.sex_record.get("condomless_sex", 0) > 0:
                the_person "You've always been careful about wearing a condom, but I think I'm ready to feel what it is like to get fucked by you bare."
            elif the_person.sex_record.get("vaginal_creampies", 0) > 0:
                the_person "You've been so careful not to cum inside me, but I'm starting to hope that you will."
                the_person "I want to know what if feels like to have your cum slosh around inside my pussy, and if you knock me up that wouldn't be so bad."
        the_person "I think I'm ready to go off birth control and have you breed me. I can't imagine a more perfect way for you to express your love than to give me a baby."
        the_person "I'm already off birth control, you'll just have to cum inside me more often so that I can be bred by you."
    return
