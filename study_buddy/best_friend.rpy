label lily_study_buddy_best_friend(the_sister, the_person):
    if the_person.event_triggers_dict.get("anger", 1) > 0:
        call study_friend_transition(the_sister, the_person) from _call_study_friend_transition
    elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 1:
        $ the_person.event_triggers_dict["friend_with_benefits"] = 1
        call lily_first_best_friend(the_sister, the_person) from _call_lily_first_best_friend
    elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 2:
        $ the_person.event_triggers_dict["friend_with_benefits"] = 2
        call lily_second_best_friend(the_sister, the_person) from _call_lily_second_best_friend
    elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 3:
        $ the_person.event_triggers_dict["friend_with_benefits"] = 3
        call lily_third_best_friend(the_sister, the_person) from _call_lily_third_best_friend
    else:
        "Unsurprisingly you do not get a visit during [the_sister.possessive_title]'s study time with [the_person.title]."
        if the_person.event_triggers_dict.get("friend_with_benefits", 0) < 50:
            call lily_offscreen_corruption(the_sister, the_person) from _call_lily_offscreen_corruption_hub
            "You do occasionally hear the murmur of them talking. Maybe you should try to find a way to spy on their dates in the future."
        else:
            if the_person.event_triggers_dict.get("friend_with_benefits", 0) < 70:
                call lesbian_sex(the_sister, the_person) from _call_lesibian_sex_FWB_1
                $ (sister_orgasm, person_orgasm) = _return
                "You do occasionally hear what could be muffled moans. Some kind of spy camera is definitely sounding like a good investment."
            else:
                call lesbian_sex(the_sister, the_person) from _call_lesibian_sex_FWB_2
                $ (sister_orgasm, person_orgasm) = _return
                "From time to time you hear a bed squeaking and once or twice it crashes into the wall. When it does there is some giggling followed by extreme silence."
                "You wonder if they really think their activities are going unnoticed, and once again wish you had picked up a camera."
            if the_person.event_triggers_dict.get("first_overnight", True) and person_orgasm < 1:
                $ best_friend_overnight = Action("Best Friend Overnight", lily_followup_requirement, "best_friend_overnight_label")
                $ mc.business.add_mandatory_crisis(best_friend_overnight)
            elif the_sister.event_triggers_dict.get("first_overnight", True) and sister_orgasm < 1:
                $ lily_overnight = Action("Lily Overnight", lily_followup_requirement, "lily_overnight_label")
                $ mc.business.add_mandatory_crisis(lily_overnight)
            elif (sister_orgasm + other_orgasm) < 1 and the_person.event_triggers_dict.get("friend_with_benefits", 0) < 80:
                $ best_friend_threesome = Action("Best Friend Threesome", lily_followup_requirement, "best_friend_threesome_label")
                $ mc.business.add_mandatory_crisis(best_friend_threesome)
            elif sister_orgasm < 1:
                $ lily_overnight = Action("Lily Overnight", lily_followup_requirement, "lily_overnight_label")
                $ mc.business.add_mandatory_crisis(lily_overnight)
            elif person_orgasm < 1:
                $ best_friend_overnight = Action("Best Friend Overnight", lily_followup_requirement, "best_friend_overnight_label")
                $ mc.business.add_mandatory_crisis(best_friend_overnight)
            else:
                "The fact that [the_sister.title] and [the_person.title] are there for each other now does have some drawbacks."
                "Your ability to influence them by satisfying their sexual needs is greatly reduced when they have another source for release."
                "Perhaps if one of them was unable to perform to the other's satisfaction they would need to come to you for help."
            $ the_person.event_triggers_dict["friend_with_benefits"] += (sister_orgasm + other_orgasm)*5
            $ the_sister.event_triggers_dict["friend_with_benefits"] += (sister_orgasm + other_orgasm)*5
    return

label study_friend_transition(the_sister, the_person):
    if the_person.event_triggers_dict.get("anger", 0) == 0:
        $ the_person.event_triggers_dict["anger"] = 0
        $ happy = 10
        the_person "[the_person.mc_title], can we talk?"
        mc.name "Sure, what's up?"
        if the_person.event_triggers_dict.get("study_sessions", 0) > 6:
            the_person "I've been having a lot of fun with you the last few months."
        else:
            the_person "I've been having a lot of fun with you the last few weeks."
        if the_person.has_role(girlfriend_role):
            the_person "There's no easy way to say this, so I'll just say it: I think we should break up."
        else:
            the_person "There's no easy way to say this, I just don't see a real future for us together. I wanted to stop things before they develop further."
        $ the_person.draw_person(emotion = "sad")
        menu:
            "Be dismissive":
                mc.name "Oh, that's fine. I was thinking the same thing actually."
                the_person "Oh... um... well I've been developing feelings for someone else... and..."
                mc.name "That's fine, I hope they make you happy."
                if the_person.has_role(girlfriend_role):
                    the_person "Nothing happened."
                    mc.name "I believe you, it's fine. We are both young, plenty of fish and all that."
            "Be understanding":
                mc.name "Oh, really?"
                the_person "I'm sorry I just don't feel a spark, I think I want to see what else is out there."
                mc.name "Oh, well okay. School is a great time to explore. I hope you can find happiness."
                the_person "Thanks, you too."
            "Get angry":
                $ happy +=10
                $ the_person.event_triggers_dict["anger"] += 1
                if the_person.has_role(girlfriend_role):
                    mc.name "You're breaking up with me? I'm the best thing that ever happened to you."
                    the_person "I'm not sure that's true, but I think I'm looking for something else."
                    mc.name "Oh yeah, what is his name? Have you already started cheating on me?"
                    $ the_person.draw_person(emotion = "angry")
                    the_person "It's not like that, nothing happened."
                    mc.name "Oh, but there is someone else? One of the other students?"
                    the_person "What... no."
                    "It seems like you might have hit pretty close to the mark there, but she doesn't seem like she is going to elaborate."
                if the_person.number_of_children_with_mc() > 0:
                    if the_person.number_of_children_with_mc() > 1:
                        mc.name "What about our kids?"
                    else:
                        mc.name "What about our kid?"
                    the_person "I'm not going to spend the next 20 years with someone just so they can have their parents in the same house."
                    the_person "We'll figure something out if you actually want to be a part of their life."
        the_person "I'm sorry, but it's just the way things are."
        menu:
            "Let her go":
                $ the_person.draw_person(emotion = "sad")
                mc.name "I guess this is goodbye?"
                the_person "Well I'll still be around, but probably going to stick to your sister's room a bit more when we study."
            "Be cruel":
                $ happy +=10
                $ the_person.event_triggers_dict["anger"] += 1
                mc.name "Well at least now I don't have to keep hiding my other girls from you."
                mc.name "I've got this one, you should see her..."
                $ the_person.draw_person(emotion = "angry")
                if not the_person.has_large_tits():
                    mc.name "You can actually tell she is a girl with tits big enough to find under her shirt."
                elif the_person.body_type == "curvy_body":
                    mc.name "She actually takes care of herself, not waddling around like your fat ass."
                elif the_person.int < 3:
                    mc.name "In addition to the body she has a brain, I never have to explain things to her."
                else:
                    mc.name "She should be a model, not like your ugly mug."
                mc.name "I can't believe I put up with you so long."
                the_person "I can't believe I was agonizing over this decision, I should have made it weeks ago."
        $ the_person.remove_role(girlfriend_role)
        $ the_person.change_stats(love = -40, happiness = -happy)
    else:
        the_person "Yeah, your sister ran out of note cards again. I think she wants us to talk."
        if the_person.event_triggers_dict.get("anger", 0) > 1:
            mc.name "Because it worked so well last time?"
            the_person "I know, but I think she is worried about me, and probably about you too."
            mc.name "She does have a tendency to care about the people around her."
            the_person "Yeah, she can be annoyingly great that way..."
            "The conversation stalls as you both reflect on what has happened."
            $ the_person.draw_person(emotion = "sad")
            the_person "I'm leaving."
            mc.name "No, wait we can talk."
            the_person "I don't just mean right now, I... I'm transfering schools. There is too much baggage here, and it's really easy to change schools this early."
            "That is pretty huge, you could probably stop her if you wanted to, but she might be gone forever after this."
            menu:
                "Let her go":
                    mc.name "Thats... a big step, but if you think you need to go I'm not going to stop you."
                    the_person "I didn't figure you would, I just feel bad about [the_sister.fname]. I don't want her blaming herself."
                    mc.name "I'll talk to her, that is at least one thing we can agree on. I'll make sure she is okay."
                    the_person "Thanks, and well goodbye I guess."
                    mc.name "Goodbye."
                    $ the_person.remove_person_from_game()
                    "Things sort of spiralled out of control there. [the_sister.title] is going to need a new study buddy. You'll have to see who it is next week."
                    $ get_lab_partner()
                "Stop her":
                    mc.name "Wait, you don't need to do that. We can get past this."
                    the_person "Can we? Really?"
                    mc.name "Look, [the_sister.fname] really likes spending time with you and I don't want to break that up."
                    mc.name "I could have handled this better, why don't we give it another week and see if things can get better."
                    the_person "Okay, I'll see you next week I guess."
                    "Things are better, but if you really want to patch things up you are probably going to have to apologize next week."
                    $ the_person.change_happiness(10)
                    $ the_person.event_triggers_dict["anger"] -= 1
        else:
            mc.name "Yeah, sure. Maybe you'd like to mooch off of me some more."
            $ the_person.draw_person(emotion = "angry")
            the_person "It's not like that, she knows things are broken between us it is upsetting her."
            "Things are a bit rough, but you could probably salvage the situation if you are willing to be the bigger person."
            menu:
                "Apologize":
                    mc.name "I know, she can care so much. It is one of the best things about her."
                    $ the_person.draw_person(emotion = "sad")
                    the_person "Something we can agree on, she really is great."
                    mc.name "Look, for what it's worth I am sorry. I got carried away in the moment."
                    the_person "You did let a bit of rage show, but I was breaking up with you, can't expect something like that to go well."
                    mc.name "I still should have handled it better, really I am sorry. Can we put that behind us, maybe be friends."
                    the_person "I think I'd like that, after all, I'm still going to be hanging around with your sister all the time."
                    mc.name "Right, that's good. I guess I'll see you next week."
                    the_person "Yeah, thanks [the_person.mc_title]."
                    $ the_person.event_triggers_dict["anger"] -= 1
                    $ the_person.change_happiness(20)
                    $ town_relationships.improve_relationship(the_person, the_sister)
                "Taunt her":
                    mc.name "Remind me whose fault that is? You're the one who broke things."
                    the_person "I know, but that doesn't mean we can't be civil."
                    mc.name "Civil? Tell me, did you find the something else you were looking for? Is he rocking your world?"
                    the_person "Look, I'm trying to salvage this for [the_sister.fname], surely you care about her even if you don't care about me."
                    mc.name "She's a big girl, if she wants us to get along she'll just have to be unhappy."
                    the_person "Fine, whatever, I can't believe I thought this would work. Hopefully she won't make me do this again next week."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-10)
                    $ the_person.event_triggers_dict["anger"] += 1
    "With that she leaves you alone in your room to think."
    return

label lily_first_best_friend(the_sister, the_person):
    $ scene_manager = Scene()
    $ scene_manager.add_actor(the_person)
    mc.name "I've got some note cards right here if you need more."
    "You give a weak smile and she returns it, shaking her head a bit at the joke."
    the_person "No... I wanted to apologize again. I know I kind of blind sided you and I wanted to make sure things were good between us."
    mc.name "I admit it was suprising, but I'll get over it. Does that mean you'll still be around."
    the_person "At least for the semester, and after that... well I hope to keep spending time with [the_sister.fname]. If that's okay with you."
    mc.name "Of course, I'd never put some minor awkwardness over the happiness of my sister."
    the_person "Thank you, spending time with [the_sister.fname] is important to my happiness too."
    mc.name "It is good that you two get along so well. I know it can sometimes be hard to find friends in a class."
    the_person "Friends... right, has she... um... said anything about our friendship?"
    mc.name "She likes you, thinks you are smart and hard working."
    the_person "Oh, likes me as a classmate, that is good I suppose."
    mc.name "As a person too, she thinks you are fun to spend time with."
    $ scene_manager.update_actor(the_person, emotion = "sad")
    the_person "Yeah... she is great too..."
    "Something about the way she looks off into space as she talks about [the_sister.fname] catches your attention."
    mc.name "Were you hoping maybe for something more than just friendship with my sister?"
    "[the_person.fname] blushes and turns her head slightly."
    $ scene_manager.update_actor(the_person, emotion = "happy")
    the_person "I never see her with boys at school, it's like she just doesn't see them. So I started to wonder if she was, you know..."
    the_person "Sorry, is this going to make things more awkward?"
    mc.name "It doesn't have to, in fact it might make it less so. I mean I don't have to worry about what I did wrong if [the_sister.fname] is the reason you broke off our relationship."
    the_person "That was a big part of it, I meant it when I said I was looking for something different. I didn't think explaining it at the time would help."
    mc.name "At the time it probably wouldn't have, but I understand."
    the_person "At the risk of making it awkward again... do you know if [the_sister.fname] would ever consider someone like me?"
    "That is a tough question, you might want to be careful how you answer. It could have a pretty big impact on how your relationships progress."
    menu:
        "Absolutely (not fully written) (disabled)":
            mc.name "She would definitely be open to the idea of spending time with another woman."
            mc.name "She has done it before, but usually with a man present as well."
            the_person "Wow, I didn't think she was that adventurous. Do you happen to know what guy it was with?"
            menu:
                "Tell her":
                    mc.name "It was me, we have been fucking for awhile, and recently our mom joined us as well."
                    mc.name "If you'd like, I could suggest that you join us the next time we are looking for an extra partner."
                    "[the_person.title]'s face clearly shows her shock. She stands there frozen not sure how to react."
                    mc.name "I'm serious, if you'd like we can go ask right now. I'm sure she wouldn't mind."
                    "She stammers a bit, but clearly can't form a coherent response."
                    "You figure it might be better to cut to the chase, so you take her by the wrist and gently pull her down the hall to your sister's room."
                    $ scene_manager.add_actor(the_sister, position = "sitting")
                    mc.name "Hey, [the_sister.title], [the_person.fname] thinks you are hot and wondered if you would ever consider someone like her."
                    if willing_to_threesome(the_person, the_sister):
                        the_sister "That is sweet, she is pretty sexy too. Do you think we should get together."
                        mc.name "Absolutely, you two would be so hot together. I'd love to watch, or maybe even join in."
                        the_sister "Sounds good to me, what do you think [the_person.fname]."
                        "[the_person.fname] still can't figure out what to do, and stands there stunned."
                        "[the_sister.fname] grins and starts to walk forward, slowly pulling at the hem of her shirt to expose part of her midriff."
                        if willing_to_threesome(the_person, the_sister):
                            "[the_person.fname] is still frozen, but it is clear she wants this to happen."
                            "By the time [the_sister.title] is next to [the_person.fname] her shirt is off, and she leans forward to kiss her tentatively."
                            the_person "God, this is going so fast but I am so excited."
                            $ the_person.event_triggers_dict["friend_with_benefits"] = 100




                        else:
                            "[the_person.fname] takes a step back, horror starting to appear on her face."
                            "Suddenly, [the_sister.fname] doubles over laughing, dropping her seductive act."
                            the_sister "I'm so sorry, [the_person.fname]. I couldn't resist playing along. The look on your face."
                            "[the_sister.fname] shoots you a dirty look while [the_person.fname] isn't watching."
                            $ the_sister.change_happiness(-5)
                            the_person "Wait, what do you mean?"
                            mc.name "I'm sorry [the_person.title], I was just messing with you."
                            the_sister "I should have warned you about my brother, he can be so inappropriate sometimes."
                            the_person "Oh, right, I should have known you wouldn't be interested in me."
                            "[the_person.title] looks crestfallen as she takes another step back"
                            the_sister "Wait, he didn't make up that part?"
                            "[the_person.title] stammers a bit but can't get anything coherent out, instead she turns and rushes down the hall towards the bathroom."
                            the_sister "God, [mc.name], you have a real way with people you know that."
                            mc.name "I just don't see any reason to hesitate, I was trying to help."
                            the_sister "Well I think you've done enough, why don't you leave us alone for a bit."
                            $ the_person.change_happiness(-5)
                            $ the_person.event_triggers_dict["friend_with_benefits"] = 4
                            "Well, that was interesting. You head back to your room while [the_sister.title] goes to try and talk with [the_person.title]."


                    else:
                        the_sister "Not funny, [mc.name]. I've told you not to harass my friends when they are over."
                        $ the_sister.change_happiness(-5)
                        $ the_sister.change_love(-5)




                "Be cautious":
                    mc.name "It's not really something I got a ton of details about..."
                    the_person "Right, of course. She is your sister after all."
                    mc.name "Exactly, but if you want I can try and talk to her and find out more. See if maybe you have a chance."
                    the_person "Really? Thanks, [mc.name] that would be great."
                    $ the_person.change_happiness(5)
                    mc.name "Come see me next week and I'll give you an update."
        "Possibly":
            mc.name "I know she has been fairly non-traditional with relationships in the past."
            mc.name "I don't see any reason why it wouldn't work with you."
            the_person "Oh, good, I've been so nervous about scaring her away if it wasn't something she wants."
            mc.name "I could talk to her if you want, see what she thinks of the idea."
            the_person "That would be great, thanks [the_person.mc_title]!"
            mc.name "Come see me next week and I'll give you an update."
        "Maybe":
            mc.name "I'm not really sure, we haven't spent a lot of time talking about her sexual preferences."
            the_person "Oh, right, of course. I just meant has she ever dated anyone like me?"
            mc.name "Sorry, [the_person.fname], you would be the first but that doesn't mean it can't happen."
            mc.name "I could try and bring the topic up, get a feel for which way should would lean."
            the_person "Really? That would be awesome, thanks [the_person.mc_title]!"
            mc.name "Come see me next week and I'll give you an update."
        "No":
            mc.name "I can't imagine that she would."
            $ scene_manager.update_actor(the_person, emotion = "sad")
            if not the_sister.has_taboo("sucking_cock") or not the_sister.has_taboo("vaginal_sex") or not the_sister.has_taboo("anal_sex"):
                mc.name "I am confident that she likes dick and is currently getting all she needs."
            else:
                mc.name "I've never known her to show an interest in other girls. You should probably look elsewhere."
            mc.name "If you want, I could try to help you find someone who is interested."
            if the_person.sluttiness > 160: # currently disabled
                the_person "You know that would be kind of nice."
                # crisis to find her a partner
                mc.name "Come see me next week and I'll give you an update."
            else:
                the_person "No, that isn't really what I'm looking for."
                the_person "I guess I'll just keep hanging out with your sister and see if anything develops."
                mc.name "Alright, I'm here if that doesn't work out."
            $ the_person.event_triggers_dict["friend_with_benefits"] = 4 # she has to do it alone
    the_person "Alright, have a good night."
    "[the_person.title] waves goodbye as she leaves to get back to [the_sister.fname]."
    $ willing = lily_willing_threesome()
    if willing:
        "[the_sister.title] is certainly willing to do things with another girl."
    else:
        "You aren't sure what [the_sister.title] thinks of sex with another girl."
    "You definitely need to talk to her about this. Of course you also need to decide what you want her to do."
    if the_sister.event_triggers_dict.get("vaginal_revisit_complete", False) == True:
        "She has become your fuck toy and getting her into a new relationship might change that."
    elif the_sister.event_triggers_dict.get("anal_revisit_complete", False) == True:
        "She has been letting you fuck her ass, and getting her into a new relationship might put a stop to that."
    elif the_sister.event_triggers_dict.get("oral_revisit_complete", False) == True:
        "Now that she is willing to suck you off you aren't sure you want her to find someone else."
    "Should you encourage her to start dating [the_person.title]? If you do is there any possibility that you end up joining them in the future?"
    $ lily_first_followup = Action("Lily First Followup", lily_followup_requirement, "lily_first_followup_label")
    $ mc.business.add_mandatory_crisis(lily_first_followup)
    $ clear_scene()
    return

label lily_first_followup_label():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ sleeping = False
    "As you are getting ready for bed you decide there is no time like the present and make your way to [the_sister.possessive_title]'s room."
    $ mc.location = lily_bedroom
    $ old_location = mc.location
    $ old_lighting = old_location.lighting_conditions
    $ mc.location.show_background()
    $ scene_manager.add_actor(the_sister, position = "sitting")
    if cousin.location == lily_bedroom:
        $ mc.location.move_person(cousin, downtown)
        mc.name "Hey, [the_sister.title], where is [cousin.fname]?"
        the_sister "Don't know, don't care. Just happy to have some alone time."
        mc.name "Oh, sorry, I can go."
        the_sister "No, wait..."
    else:
        mc.name "Hey, [the_sister.title] how are you doing?"
        the_sister "Pretty good, how about you?"
    the_sister "Is everything okay?"
    mc.name "Yeah, why wouldn't it be?"
    the_sister "I don't know, [the_person.fname] was a bit weird today and when I tried to bring it up she brushed me off."
    mc.name "Don't worry about it, I'm sure she'll be fine next week."
    if the_sister.has_role(girlfriend_role):
        the_sister "Don't be like that, I love you and telling me not to worry will just make me worry more."
        "She does love you, telling her would probably be for the best."
    else:
        the_sister "Fine, bury your feelings."
        "As she says that you can see her interest growing, if you don't tell her it will just make her more curious."
    mc.name "Alright, we sort of broke up I guess."
    the_sister "Oh, I'm sorry, was it serious?"
    if the_sister.has_role(girlfriend_role):
        "While it is clear she is concerned you also see a hint of jealousy in her eyes."
        mc.name "Nothing you needed to worry about, we were just having some fun."
    else:
        "Her compassion eases some of the pain you had been feeling."
        mc.name "Not really, she is fun but I didn't think we were going to get married or anything."
    the_sister "Still break ups can be rough. Is there anything I can do for you?"
    mc.name "As a matter of fact I am feeling a bit lonely, do you think we could spend some time together?"
    the_sister "Of course."
    $ scene_manager.update_actor(the_sister, position = "stand4")
    "[the_sister.title] stands up and approaches you, wrapping her arms around you in a tight hug."
    if not the_sister.has_taboo("kissing"):
        $ scene_manager.update_actor(the_sister, position = "kissing")
        "The hug is nice, but you want more so you gently tilt her head up and lower yours to plant a gentle kiss on her lips."
        "As it lingers you feel her mouth start to part and you push forward more."
        "A slight moan runs through her as her body melts against yours."
        $ mc.change_arousal(10)
        $ the_sister.change_arousal(10)
    if not the_sister.has_taboo("touching_body"):
        "The warmth and closesness is amazing and you feel tension you were not aware of pouring out of your body."
        "Your cock begins to stir and as it hardens you press it into [the_sister.possessive_title]'s warm crotch."
        "She moans more audibly and starts to run her hands over your body, taking the hug from comforting to sexual."
        $ mc.change_arousal(10)
        $ the_sister.change_arousal(10)
    "The hug lingers, but eventually [the_sister.title] pulls away and you reluctantly let her go."
    if not the_sister.has_taboo("sucking_cock") and the_sister.has_taboo("vaginal_sex"):
        $ the_person.event_triggers_dict["lily_comfort"] = "oral"
        the_sister "Why don't you lay down on my bed? I'll get the door and then do something you take your mind off [the_person.fname]."
        $ scene_manager.update_actor(the_sister, position = "walking_away")
        "You drop back onto her bed and sprawl out, leaving your legs hanging down to the floor while [the_sister.title] goes and turns off the lights."
        $ mc.location.lighting_conditions = dark_lighting
        $ mc.location.show_background()
        $ scene_manager.update_actor(the_sister, position = "blowjob")
        "By the time your eyes adjust to the darkness she is standing at the end of the bed and lowers herself down to her knees in front of you."
        "She rests her hands on your knees and slowly starts to run them up your thighs. Getting the idea you are quick to help her open them up so that she has easier access."
        the_sister "Well, someone is eager!"
        $ mc.change_arousal(10)
        if the_sister.get_opinion_score("giving blowjobs") > 0:
            the_sister "I have to admit I'm a bit excited to get a taste of you too."
            if the_sister.get_opinion_score("being submissive") > 0:
                the_sister "You know I'm always happy to serve you when you want me too."
                $ the_sister.change_arousal(10)
        else:
            the_sister "Don't expect this everytime you get a little sad."
        $ scene_manager.update_actor(the_sister, position = "kneeling1")
        "By the time she has herself in postion you are already standing at attention for her. She kisses the head and then licks the shaft a few times."
        "It is pretty clear you don't need any more prep and she opens her mouth to take your tip into her mouth, gently sucking on it and licking up your precum."
        "Next she opens wider and slowly slides down your shaft, taking more and more into her soft mouth."
        call get_fucked(the_sister, the_goal = "oral creampie", sex_path = None, private= True, start_position = blowjob, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_comfort1
        mc.name "Thank you [the_sister.title], I think that was exactly what I needed."
        the_sister "Good, does that mean you are feeling better?"
        mc.name "Absolutely, I'm going to sleep like a rock tonight."
        the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
        mc.name "You want me to sleep with you?"
        the_sister "Not like that, just a little cuddling to further comfort you."
        mc.name "That sounds nice, thank you."
    else:
        the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
        mc.name "You want me to sleep with you?"
        if not the_sister.has_taboo("vaginal_sex"):
            $ the_person.event_triggers_dict["lily_comfort"] = "sex"
            the_sister "I was just going to comfort you a bit, but you never know where the night will go."
            the_sister "I'll get the lights, you make yourself comfortable."
            "Not wanting to waste this opportunity you quickly strip and climb under the covers."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
            $ the_sister.outfit.strip_to_underwear()
            "It is hard to see in the sudden darkness, but you hear clothing shifting as [the_sister.title] prepares to join you."
            $ mc.change_locked_clarity(10)
            "You leave room for her to fit next to you, but aren't terribly surprised when she instead climbs on top of you, dropping a leg to each side and lowering her body to yours."
            $ scene_manager.update_actor(the_sister, position = "cowgirl")
            if the_sister.tits_visible():
                if the_sister.has_large_tits():
                    "Her sizable breasts press warmly against your bare chest as she settles down."
                else:
                    "Her firm nipples point into your chest as she settles down."
            else:
                "Her bra lessens the experience as she settles down."
            the_sister "So... do you want to talk about [the_person.fname]?"
            mc.name "Sorry, who?"
            the_sister "Funny... but I'm serious. Do you need to talk?"
            if the_sister.has_role(girlfriend_role):
                the_sister "I know our relationship has its challeneges, but I don't just want to be a rebound for you when something else doesn't work out."
                mc.name "I know, and I love you as both my sister and my girlfriend."
            else:
                the_sister "I'll save you from making a terrible decision while you are on the rebound, but I also want to be here if you need to talk."
                mc.name "I know, and I'm so grateful to have someone who I can talk to about anything."
            mc.name "Honestly, it wasn't that serious. I miss her a bit but I'm sure I'll be fine in a few days."
            the_sister "Alright, in that case..."
            "She lowers her face to yours, resuming the kiss but with more passion. She also begins to grind her pelvis against yours."
            if the_sister.vagina_visible():
                if not the_sister.pubes_style == shaved_pubes:
                    "Her fine hairs send tingles along your skin where it brushes you and you can feel the heat radiating from her pussy"
                else:
                    "Her bare skin is incredibly smooth and you can feel the heat radiating from her pussy."
            else:
                "Her silky panties rub against you but don't dampen the heat radiating from her pussy."
            "It isn't long before you stiffen enough for her to feel your cock pressing against her folds."
            "You slide your hands down to her ass, pulling her more tightly against you and grinding harder."
            if the_sister.vagina_visible():
                "She slides her hands between your hips and lifts up a bit so she can spread her lips with one and grasp your rock hard pole with the other."
            else:
                "She slides her hands to her crotch, pulling her panties aside with one and grasping your rock hard pole with the other."
                $ the_sister.outfit.strip_to_vagina()
                $ the_sister.draw_person()
            "She makes a few more passes, spreading her juices along the length of your cock, before lifting her hips and guiding you into her waiting hole."
            "She sinks down slowly enveloping you in her tight warm pussy and stopping once you are buried to the hilt."
            the_sister "God, you always make me feel so full [the_sister.mc_title]."
            mc.name "And you always feel so tight. I must be the luckiest man in the world."
            "She smiles down at you and then starts to move, at first just slowly sliding up and down about an inch."
            call get_fucked(the_sister, the_goal = "vaginal creampie", sex_path = None, private= True, start_position = cowgirl, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_comfort2
            mc.name "That was amazing [the_sister.title]. I'm not sure if comforted is the right word, but I definitely feel better."
            if the_sister.get_opinion_score("vaginal sex") > 0:
                the_sister "I have to admit I enjoyed myself too."
            if the_sister.get_opinion_score("being submissive") > 0:
                the_sister "You know how much I love satisfying your needs and giving you pleasure."
            "[the_sister.title] drapes herself over you, wrapping her arms around you as much as she can."
            "You are struck by how it can be so similar and at the same time wildly different than the hug you got when you first entered the room."
            "You smile to yourself at how lucky you are to have [the_sister.title] as you drift off to sleep."
            $ sleeping = True
        elif not the_sister.has_taboo("touching_penis"):
            $ the_person.event_triggers_dict["lily_comfort"] = "hand"
            the_sister "Not like that... but maybe we can find a way to help you relax."
            $ mc.change_arousal(10)
            the_sister "I'll get the lights, you make yourself comfortable."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
            "Not wanting to presume too much you strip, but only to your boxers, before you climb into her bed."
            "She quickly joins you, pressing her body up against yours as you squeeze into the bed together."
            $ mc.change_arousal(10)
            the_sister "Roll onto your side [the_sister.mc_title]. I'll be the big spoon and soothe you to sleep."
            "You comply, and feel her press against your bare back as she settles into place."
            "She wraps her top arm around you, pulling tighter, sort of like a hug."
            "It is comforting, but when her hand starts to wander down towards your waist other thoughts enter your mind."
            the_sister "Give me a bit of help here."
            "She starts to pull at the waist of your boxers and you lift your hips to let her pull them down."
            $ mc.change_arousal(10)
            "Her hand then travels back up and she gently strokes your stomach, brushing her hand against your rapidly harding cock as she does so."
            call get_fucked(the_sister, the_goal = "get mc off", sex_path = None, private= True, start_position = handjob, start_object = make_bed(), skip_intro = True, report_log = None, ignore_taboo = False, prohibit_tags = [], unit_test = False, allow_continue = False) from _call_get_fucked_comfort3
            mc.name "That was amazing [the_sister.title], I'm not sure I've ever been so relaxed."
            the_sister "Good, does that mean you are feeling better?"
            mc.name "Absolutely, I'm going to sleep like a rock tonight."
            the_sister "It is a little small, but if you wanted to sleep in here tonight I could make room for you."
            mc.name "You want me to sleep with you?"
            the_sister "Not like that, just a little cuddling to further comfort you."
            mc.name "That sounds nice, thank you."
        else:
            the_sister "Get your mind out of the gutter [the_sister.mc_title], I just thought you might be lonely."
            the_sister "It's not like we never shared a bed before, I'll just keep you company."
            the_sister "I'll get the lights, you make yourself comfortable."
            $ scene_manager.update_actor(the_sister, position = "walking_away")
            "You drop your pants, but decide it would be prudent to keep your boxers and shirt on before you climb into bed."
            $ mc.location.lighting_conditions = dark_lighting
            $ mc.location.show_background()
    if not sleeping:
        "You press your back against the wall, leaving plenty of room for [the_sister.title] to fit as well."
        "She climbs in and lays on her back, then turns towards you and then away, trying to find a comfortable position."
        $ scene_manager.update_actor(the_sister, position = "stand2")
        the_sister "Maybe I was wrong, we are going to have to get a little closer if we ever want to get to sleep."
        mc.name "I can go if you want..."
        the_sister "No, just scoot away from the wall a bit and I'll cuddle up to you."
        mc.name "Alright."
        "You position yourself and feel her slide up against your body. It is a bit surprising how natural she seems to fit in your arms."
        the_sister "See, this is nice. Although, I was supposed to be comforting you and you seem to be the one holding me."
        mc.name "It's fine, having you here is comforting even if you are in my arms instead of me being in yours."
        the_sister "Alright, good night [the_sister.mc_title]."
        mc.name "Good night."
        if the_sister.love > 50:
            the_sister "..."
            "She seems to tense up, like she wants to say something more."
            the_sister "..."
            the_sister "I love you."
            "She mumbles, almost too quite to hear."
            menu:
                "Respond":
                    mc.name "I love you too."
                    "The tension bleeds out of her body as she relaxes back against you."
                    $ the_sister.change_stats(happiness = 5, love = 5)
                "Stay silent":
                    mc.name "..."
                    "You stay quite, the tension seems to grow a bit, but you deepen your breathing, like you somehow fell asleep already."
                    "It seems like she isn't going to make an issue of it, but she isn't happy."
                    $ the_sister.change_stats(happiness = -5, love = -5)
    $ old_location.lighting_conditions = old_lighting
    $ clear_scene()
    call advance_time_move_to_next_day() from _call_advance_time_move_to_next_day_lily_first_followup
    call lily_first_followup_morning() from _call_lily_first_followup_morning
    return "Advance Time"

label lily_first_followup_morning():
    $ mc.change_location(lily_bedroom)
    $ the_mom = mom
    $ the_sister = lily
    $ wear_pajamas(the_mom)
    $ wear_pajamas(the_sister)
    $ mom_slutty = False
    $ sis_slutty = False
    $ the_cousin = None
    if hall.has_person(aunt):
        $ the_cousin = cousin
        $ the_aunt = aunt
        $ wear_pajamas(the_cousin)
        $ wear_pajamas(the_aunt)
        $ aunt_slutty = False
        $ cousin_slutty = False
        if the_cousin.effective_sluttiness() > 60:
            $ cousin_slutty = True
        if the_aunt.effective_sluttiness() > 60:
            $ aunt_slutty = True
        if the_mom.effective_sluttiness() > 60:
            $ mom_slutty = True
        if the_sister.effective_sluttiness() > 60:
            $ sis_slutty = True
        $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], the_mom)
    else:
        $ the_group = GroupDisplayManager([the_mom, the_sister], the_mom)
        if the_mom.effective_sluttiness() > 40 or mc.business.event_triggers_dict.get("family_threesome", False) == True:
            $ mom_slutty = True
        if the_sister.effective_sluttiness() > 40 or mc.business.event_triggers_dict.get("family_threesome", False) == True:
            $ sis_slutty = True
    "When you wake up in the morning you are briefly disoriented until you remember where you are."
    "[the_sister.title]'s room is recognizable. You just aren't used to seeing it from her bed, especially after spending the night with her."
    "You were right about sleeping like a rock, you never even noticed [the_sister.possessive_title] getting out of bed this morning."
    if mc.event_triggers_dict.get("lily_comfort", None) == "sex":
        "Still naked from your late night activities you look to the thankfully closed door."
        "You get out of bed and get yourself dressed."
    elif mc.event_triggers_dict.get("lily_comfort", None) == "hand":
        "Thankfully the door is closed so you get out of bed and pull on your pants."
    elif mc.event_triggers_dict.get("lily_comfort", None) == "oral":
        "Fortunately you pulled your clothes back on last night, but you are still glad the door is closed."
        "You climb to your feet and strech out some kinks from the unfamiliar bed."
    "It seems like [the_sister.title] has already started her day, and you figure you should probably follow suit."
    if the_cousin:
        "Suddenly you remember that [the_cousin.title] has been sleeping in here. She was out last night but must have come home at some point. Did she see you and [the_sister.title] sleeping together?"
        "This could be bad... you better get out there and see if you need to do damage control."
        "You head to your bedroom first and are somewhat relieved to see that the bed was slept in. Hopefully [the_cousin.possessive_title] just took advantage of the free bed and doesn't care about the reason."
    "You head for the kitchen to see who is around."
    $ mc.change_location(kitchen)
    $ the_group.draw_group(position = "sitting", emotion = "happy")
    $ the_group.draw_person(the_mom, position = "walking_away")
    if mom_slutty:
        if the_mom.outfit.wearing_panties():
            "[the_mom.possessive_title] is just in her underwear in front of the stove, humming as she scrambles a pan full of eggs."
            $ mc.change_locked_clarity(5)
        else:
            "[the_mom.possessive_title] is in front of the stove naked, humming as she scrambles a pan full of eggs."
            $ mc.change_locked_clarity(10)
    else:
        "[the_mom.possessive_title] is at the stove and humming to herself as she scrambles a pan full of eggs."
    $ the_mom.update_outfit_taboos()
    $ the_group.draw_person(the_mom, position = "back_peek")
    the_mom "Good morning [the_mom.mc_title]. I'm almost ready to serve, have a seat."
    if sis_slutty:
        if the_sister.outfit.wearing_panties():
            "[the_sister.possessive_title] is sitting at the kitchen table wearing her underwear. She gives a dramatic yawn before nodding to you."
            $ mc.change_locked_clarity(5)
        else:
            "[the_sister.possessive_title] is sitting at the kitchen table naked. She gives a dramatic yawn before nodding to you."
            $ mc.change_locked_clarity(10)
    else:
        "[the_sister.possessive_title] is sitting at the kitchen table and gives a dramatic yawn before nodding to you."
    $ the_sister.update_outfit_taboos()
    the_sister "Good morning [the_sister.mc_title]."
    if the_cousin:
        if aunt_slutty:
            if the_aunt.outfit.wearing_panties():
                "[the_aunt.possessive_title] is also sitting at the kitchen table. You are a bit surprised she is just wearing her underwear."
                $ mc.change_locked_clarity(5)
            else:
                "[the_aunt.possessive_title] is also sitting at the kitchen table. Shockingly she is naked."
                $ mc.change_locked_clarity(10)
        else:
            "[the_aunt.possessive_title] is also sitting at the kitchen table."
        "There is no sign of [the_cousin.possessive_title], but you settle down at the table with the rest of your family."
    else:
        "You quickly take a seat next to [the_sister.title], leaning close to whisper in her ear."
        mc.name "Listen, about last night..."
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            "[the_sister.title] smiles up at you and then leans forward for a kiss."
            "As your lips connect you feel her hand running up your thigh."
            $ the_group.draw_person(the_mom, position = "walking_away")
            "Your mother takes the pan off the stove and begins to slide the contents off onto three plates."
            $ the_group.draw_person(the_mom)
            "She turns around and hands one plate to you and one plate to [the_sister.title]."
            $ the_group.draw_person(the_sister, position = "sitting")
            the_mom "Now, now you two. The table is for eating. I would have thought that last night was enough for you."
            the_sister "Sorry mom. We'll be good."
            mc.name "Yeah, sorry."
            the_mom "Don't worry, I understand. I just want to have a nice meal right now."
        elif mom_slutty and sis_slutty:
            "[the_sister.title] smiles up at you and then quickly glances at [the_mom.possessive_title]."
            "Her grin turns mischevious as she looks down and moves her hand to your leg, running it up your thigh."
            $ the_group.draw_person(the_mom, position = "walking_away")
            "Your mother takes the pan off the stove and begins to slide the contents off onto three plates."
            $ the_group.draw_person(the_mom)
            "She turns around and hands one plate to you and one plate to [the_sister.title]."
            $ the_group.draw_person(the_sister, position = "sitting")
        if mom_slutty and sis_slutty:
            if mom.lactation_sources > 0 and mom.tits_visible():
                mom "Want a little milk for your coffee, honey?"
                "[mom.title] gives you a quick wink."
                mc.name "Sure mom."
                "[mom.possessive_title] bends slightly over your coffee. She takes one of her breasts in her hand and starts to squeeze."
                "It takes a second, but soon a stream of her milk is pouring out into you coffee."
                mom "Just say when!"
                "You let her continue for a few more moments, until you can see the cream start to circulate around your hot coffee."
                $ mom.change_stats(happiness = 5, slut = 1, max_slut = 40)
                mc.name "That's good!"
                lily "Thanks Mom, you're the best!"
            elif lily.lactation_sources > 0 and lily.tits_visible():
                mom "Want some coffe, honey?"
                mc.name "Sure mom."
                mom "Here you go, maybe [lily.fname] could help you out with some milk."
                "[mom.title] gives you a quick wink."
                lily "Really, Mom?"
                mc.name "I mean... if you don't mind it would be nice."
                "[lily.possessive_title] gives an exasperated sigh, but then bends slightly over your coffee. She takes one of her breasts in her hand and starts to squeeze."
                "It takes a second, but soon a stream of her milk is pouring out into you coffee."
                lily "Let me know when you have enough."
                "You let her continue for a few more moments, until you can see the cream start to circulate around your hot coffee."
                $ lily.change_stats(happiness = 5, slut = 1, max_slut = 40)
                mc.name "That's good!"
            else:
                lily "Thanks Mom, you're the best!"
            $ the_group.draw_person(the_mom, position="sitting")
            the_mom "No problem, I'm just happy to spend my morning relaxing with my two favorite people!"
            $ mc.change_locked_clarity(10)
            $ lily.change_stats(love = 3)
            $ mom.change_stats(love = 3, happiness = 5)
            if mc.business.event_triggers_dict.get("family_threesome", False) == True:
                "You enjoy a relaxing breakfast bonding with your mother and sister. [the_mom.possessive_title] seems particularly happy she gets to spend time with you."
                "Neither [lily.title] or [mom.possessive_title] seem to think it's strange to relax in their underwear and [lily.title] manages to keep you going throughout the meal."
                "The combined stimulation is starting to take a toll on you."
                "You try to focus on something work related, but instead all you can focus on are [mom.possessive_title]'s heaving tits, across the table from you."
                mom "Honey? Are you feeling okay? You seem a little zoned out..."
                "Next to you, [lily.title] grasps your erection and speaks up."
                lily "I'm sure he's fine mom, but us dressing like this has him all worked up. He's hard as a rock!"
                mom "It doesn't help that you keep encouraging him. [lily.fname] honey, let's take care of him before the day gets going."
                lily "Good idea mom!"
                menu:
                    "Accept their help":
                        mc.name "Oh wow, that would be great!"
                        $ the_group.draw_person(mom, position = "stand2")
                        $ the_group.draw_person(lily, position = "blowjob")
                        "[mom.possessive_title] gets up and starts walking around the table, while [lily.title] gets on her knees and starts pulling off your pants and underwear."
                        "Your cock springs out of your clothes, nearly smacking [lily.possessive_title] in the face. [mom.title] gets on her knees next to [lily.title]."
                        call start_threesome(lily, mom, start_position = threesome_double_blowjob, position_locked = True) from _call_start_threesome_study_morning
                        $ the_report = _return
                        if the_report.get("guy orgasms", 0) > 0:
                            "You enjoy your post-orgasm bliss for a few moments while [mom.possessive_title] and [lily.possessive_title] get up."
                        else:
                            "Finished for now, you decide to put your cock away while [mom.possessive_title] and [lily.possessive_title] get up."
                        $ the_group.draw_person(mom, position="stand3", display_transform = character_center_flipped)
                        $ the_group.draw_person(lily, position = "stand4", display_transform = character_right)
                        mc.name "Mmm, thanks for breakfast mom!"
                        if the_report.get("guy orgasms", 0) > 0:
                            "[lily.title] laughs and jokes back."
                            lily "Thanks for breakfast, bro!"
                    "Refuse":
                        mc.name "That's okay, I have a ton of stuff to get done today. Maybe tonight after dinner?"
                        mom "Okay, if that's what you want [mom.mc_title]."
                        $ the_group.draw_person(mom, position="walking_away", display_transform = character_left_flipped)
                        "[mom.possessive_title] gets up and starts to do the dishes."
            else:
                "You enjoy a relaxing breakfast bonding with your mother and sister. [the_mom.possessive_title] seems particularly happy she gets to spend time with you."
                "Neither [lily.title] or [mom.possessive_title] seem to think it's strange to relax in their underwear and [lily.title] reaches over to stroke you occasionally."
                "It is difficult, but your head wins out and you are able to resist the urge to take thing further in front of [the_mom.possessive_title]."
            "When you're done you help [mom.possessive_title] put the dirty dishes away and get on with your day."
        elif sis_slutty:
            $ the_group.draw_person(the_sister, position = "sitting")
            "Before you can finish your sentence your mother turns around and gasps."
            $ the_group.draw_person(the_mom, emotion = "angry")
            the_mom "[the_sister.fname]! What are you wearing?"
            $ the_group.draw_person(the_sister, position = "sitting")
            the_sister "What do you mean? I just got up, I haven't had time to pick out an outfit yet."
            $ the_group.draw_person(the_mom, emotion = "angry")
            the_mom "You shouldn't be running around the house naked. Go put some clothes on young lady."
            $ the_group.draw_person(the_sister, position = "sitting", emotion = "angry")
            "[the_sister.possessive_title] scoffs and rolls her eyes."
            the_sister "Come on Mom, you're being ridiculous. This is my house too, I should be able to wear whatever I want!"
            "Your mother and sister lock eyes, engaged in a subtle battle of wills."
            if the_sister.obedience > the_mom.obedience:
                $ the_group.draw_person(the_mom, position = "walking_away")
                "Mom sighs loudly and turns back to the stove."
                the_mom "Fine! You're so stubborn [the_sister.title], I don't know how I survive around here!"
                $ the_sister.change_obedience(-2)
                $ the_sister.change_happiness(10)
                $ the_sister.change_slut(2, 50)
                $ the_mom.change_obedience(10)
                $ the_group.draw_person(the_sister, position = "sitting", emotion = "happy")
                "[the_sister.possessive_title] looks at you, obviously pleased with herself, and winks."
                "Breakfast proceeds, but there is a bit of tension at the table."
                "[the_sister.title] looks pleased with herself and from time to time she runs her hand along your thigh."
            else:
                "[the_sister.title] finally sighs loudly and looks away. She pushes her chair back and stands up in defeat."
                $ the_group.draw_person(the_sister, emotion = "angry")
                the_sister "Fine! I'll go put on some stupid clothes so my stupid mother doesn't keep worrying."
                $ the_group.draw_person(the_sister, position = "walking_away")
                "[the_sister.title] sulks out of the kitchen."
                $ the_group.draw_person(the_mom, )
                the_mom "I don't know how I manage to survive with you two around!"
                $ the_sister.apply_outfit(the_sister.planned_outfit)
                $ the_sister.change_obedience(10)
                $ the_sister.change_happiness(-5)
                $ the_mom.change_obedience(-2)
                $ the_group.draw_person(the_sister, position = "sitting")
                "[the_sister.possessive_title] is back by the time [the_mom.title] starts to plate breakfast. She sits down and starts to eat without saying a word."
                "The table is a bit tense, but breakfast proceeds somewhat normally."
                "About halfway through [the_sister.title] glances down at your pants and then proceeds to reach over and run her hand along your thigh. It is almost like she wants to be caught."
            "It seems that spending the night with her might have made her a bit more comfortable being bold around you."
            "When you're done you help Mom put the dirty dishes away and get on with your day."
        else:
            "[the_sister.title] flushes with embarassment and angrily cuts you off, while trying to keep her voice quiet."
            the_sister "Not now!"
            if mom_slutty:
                "She then turns away from you just as [the_mom.possessive_title] spins around."
                the_sister "Oh my god Mom, what are you wearing?"
                $ the_mom.draw_person(position = "back_peek")
                the_mom "What? It's the weekend and it's just the three of us. I didn't think anyone would mind if I was a little more casual."
                $ the_sister.draw_person(position = "sitting")
                if the_mom.vagina_visible():
                    the_sister "Mom, I don't think you know what casual means. Could you at least put on some panties or something?"
                elif the_mom.tits_visible():
                    the_sister "Mom, I don't think you know what casual means. I mean, couldn't you at least put a bra?"
                else:
                    the_sister "Mom, you're prancing around the kitchen in your underwear. In front of your son and daughter. That's weird."
                    "[the_sister.title] looks at you."
                    the_sister "Right [the_sister.mc_title], that's weird?"
                if the_mom.obedience > 115:
                    $ the_mom.draw_person(position = "back_peek")
                    the_mom "What do you think [the_mom.mc_title], do you think it's \"weird\" for your mother to want to be comfortable in her own house?"
                    $ mc.change_locked_clarity(5)
                    menu:
                        "Side with Mom":
                            mc.name "I think Mom's right [the_sister.title]. It's nothing we haven't seen before, she's just trying to relax on her days off."
                            $ the_mom.change_obedience(-5)
                            $ the_sister.change_obedience(5)
                            "[the_sister.title] looks at the two of you like you're crazy then sighs dramatically."
                            the_sister "Fine, but this is really weird, okay?"
                            $ the_mom.draw_person(position = "sitting")
                            "[the_mom.possessive_title] dishes out three portions and sits down at the table with you. [the_sister.title] eventually gets used to her mother's outfit and joins in on your conversation."
                            $ the_sister.change_slut(2, 30)
                            $ the_mom.change_happiness(10)
                        "Side with [the_sister.title]":
                            mc.name "I actually think [the_sister.title] is right, this is a little weird. Could you go put something on, for our sakes?"
                            $ the_sister.change_obedience(-2)
                            $ the_sister.change_slut(1, 30)
                            $ the_mom.change_obedience(5)
                            the_mom "Oh you two, you're so silly. Fine, I'll be back in a moment. [the_sister.title], could you watch the eggs?"
                            $ the_sister.draw_person(position = "walking_away")
                            "Your mother leaves to get dressed. [the_sister.possessive_title] ends up serving out breakfast for all three of you."
                            $ the_mom.apply_outfit(the_mom.planned_outfit)
                            the_sister "She's been so weird lately. I don't know what's going on with her..."
                            $ the_mom.draw_person(position = "sitting")
                            $ the_sister.change_happiness(5)
                            $ the_mom.change_happiness(5)
                            "When [the_mom.possessive_title] gets back she sits down at the table and the three of you enjoy your breakfast together."
                else:
                    $ the_mom.draw_person(position = "back_peek")
                    the_mom "Well luckily I'm your mother and it doesn't matter what you think. I'm going to wear what makes me comfortable."
                    "She takes the pan off the stove and slides the scrambled eggs out equally onto three plates."
                    the_mom "Now, would you like some breakfast or not?"
                    "[the_sister.title] sighs dramatically."
                    the_sister "Fine, but this is really weird, okay?"
                    $ the_sister.change_slut(1, 30)
                    $ the_mom.change_happiness(10)
                    $ the_mom.draw_person(position = "sitting")
                    "[the_mom.possessive_title] gives everyone a plate and sits down. [the_sister.title] eventually gets used to her mother's outfit and joins in on your conversation."
                    "When you're done you help Mom put the dirty dishes away and get on with your day."
            else:
                $ the_group.draw_person(the_sister, position = "sitting")
                the_sister "So what's the occasion Mom?"
                $ the_group.draw_person(the_mom)
                "[the_mom.possessive_title] takes the pan off the stove and scoops the scrambled eggs out equally onto three waiting plates."
                the_mom "Nothing special, I just thought we could have a nice quiet breakfast together."
                "She slides one plate in front of you and one plate in front of [the_sister.title], then turns around to get her own before sitting down to join you."
                $ the_group.draw_person(the_mom, position = "sitting")
                the_mom "Go ahead, eat up!"
                $ the_sister.change_love(3)
                $ the_mom.change_love(3)
                $ the_mom.change_happiness(5)
                "While the food is good [the_sister.possessive_title] seems tense. Still, [the_mom.possessive_title] seems particularly happy she gets to spend time with you."
                "When you're done you help [the_mom.title] put the dirty dishes away and get on with your day."
    $ clear_scene()
    return

label lily_second_best_friend(the_sister, the_person):
    the_person "So... did you talk to [the_sister.fname] about... things."
    "Oh shit, you completely forgot to actually talk to her last week."
    if the_person.event_triggers_dict.get("lily_comfort", None) == "sex":
        "To be fair, she did kind of jump you."
    elif the_person.event_triggers_dict.get("lily_comfort", None) == "oral":
        "To be fair, her mouth was a bit busy."
    elif the_person.event_triggers_dict.get("lily_comfort", None) == "hand":
        "To be fair, she did distract you a bit."
    else:
        "To be fair, she was more concerned with how you were doing."
    menu:
        "Tell the truth (mostly)":
            mc.name "Sorry, [the_person.title], I went to talk to her but it was a difficult topic to bring up."
            mc.name "We talked about you, she knows something was going on with us and that it ended."
            mc.name "From there the conversation kinda got away from me. I didn't see a good way to steer it back to you and her."
            if mc.event_triggers_dict.get("lily_comfort", None) == "sex":
                "Especially after she fucked you to exhaustion."
            elif the_person.event_triggers_dict.get("lily_comfort", None) == "oral":
                "Especially after she sucked you off."
            elif mc.event_triggers_dict.get("lily_comfort", None) == "hand":
                "Especially after she jerked you off."
            the_person "Okay, do you think you could talk to her again?"
            mc.name "Yeah, I will for sure."
        "Lie":
            mc.name "Yes, absolutely. We talked about you last week."
            "Your mind races as you scramble for an answer that will satisfy her and be relatively factual."
            menu:
                "She is curious":
                    mc.name "She is certainly curious. When I brought up the idea of her dating a girl she seemed intrigued."
                    mc.name "If I had to guess she has thought about it before, but probably liked boys enough to go with the flow."
                    mc.name "I think I could get her to ask you out if you give me a bit of time."
                    $ the_person.event_triggers_dict["lily_lie"] = 2
                "Give her time":
                    mc.name "She seemed a little surprised when I asked, sort of like she had never really thought about it before."
                    mc.name "When we finished talking it seemed like she was deep in thought."
                    mc.name "I think you need to give her some time, let her come around to the idea of seeing you as more than a friend."
                    mc.name "I'll be sure to bring it up again, see if I can help nudge her in the right direction."
                    $ the_person.event_triggers_dict["lily_lie"] = 1
                "Not going to happen":
                    mc.name "She likes you, she really does, but nothing is going to happen."
                    mc.name "I don't think she is ever going to return your feelings."
                    mc.name "I'll talk to her again, but I think you might need to look elsewhere."
                    $ the_person.event_triggers_dict["lily_lie"] = -1
            the_person "Well, that is good to know. At least I have some idea of what to expect."
            the_person "I guess no matter what I'm still gonna be hanging around. Maybe I'll be able to sway her a bit more while we are studying."
            mc.name "Sure, you never know what will happen."
            "You better make sure that your story checks out before [the_person.title] catches you in a lie."
            "Maybe your serums could help out. Can you convince [the_sister.title] that she wants to do what you already promised [the_person.title]?"
    the_person "Thanks again. I know this is kind of awkward and I really appreciate the help."
    if the_person.height < 0.9:
        "She steps forward goes up on her toes and kisses you on the cheek."
    else:
        "She steps forward and gives you a kiss on the cheek."
        $ lily_second_followup = Action("Lily First Followup", lily_followup_requirement, "lily_second_followup_label")
    $ mc.business.add_mandatory_crisis(lily_second_followup)
    $ clear_scene()
    return

label lily_second_followup_label():
    $ the_person = get_lab_partner()
    $ the_sister = lily
    "As you are getting ready for bed you decide there is no time like the present and make your way to [the_sister.possessive_title]'s room."
    $ mc.location = lily_bedroom
    $ the_sister.draw_person(position = "sitting")
    the_sister "Hey there, [the_sister.mc_title]. Should I get used to seeing you on Mondays?"
    if cousin.location == lily_bedroom:
        $ mc.location.move_person(cousin, downtown)
        mc.name "Hey, [the_sister.title], where is [cousin.fname]?"
        the_sister "Don't know, don't care. Just happy to have some alone time."
        mc.name "Oh, sorry, I can go."
        the_sister "No, wait! I meant from her, I like spending time with you."
        the_sister "You are always welcome to spend time with me."
    if mc.event_triggers_dict.get("lily_comfort", None) == "sex" or mc.event_triggers_dict.get("lily_comfort", None) == "hand" or mc.event_triggers_dict.get("lily_comfort", None) == "oral":
        "While it is tempting to try for a repeat of last time, you resolve to actually talk with her this time."
        "Maybe afterwards..."
        mc.name "I mean... I'm not gonna argue if you want me to come see you at night."
        "She smiles and starts to walk towards you before you hold out a hand to stop her."
        mc.name "Unfortunately that isn't why I'm here. I need to ask you some delicate questions."
    else:
        mc.name "I'd like that, but it's kinda going to depend on how you answer some delicate questsions."
    the_sister "Oh, what's going on?"
    mc.name "First, I want you to promise to take some time to think. This is a bit complicated and I don't want you to make any rash decisions."
    the_sister "Now I'm a little worried, is something wrong with you or mom?"
    mc.name "No, nothing like that. Nothing is wrong, it's just well... [the_person.fname] asked me something and I wasn't sure how to answer her."
    the_sister "[the_person.fname]? She was just here. What did she ask?"
    mc.name "Look, she is scared of messing up your friendship and that is the last thing she wants."
    mc.name "Can you just promise you'll think before you do anything major with this information."
    the_sister "...okay... I promise."
    if the_sister.has_role(girlfriend_role):
        "Well, no going back now. How are you going to ask your sister/girlfriend if she wants to start dating your ex?"
        mc.name "So you and I are dating, but obviously that relationship has some inherant difficulties."
        mc.name "[the_person.fname] and I hit it off after a few conversations, and started spending some time together too."
        the_sister "I know, and that is fine. I still don't understand where this is going."
        mc.name "I'm getting there, hang on."
        mc.name "So you know she kinda broke up with me, but niether of us have told you why."
        mc.name "The thing is that while she was getting closer to me she started to develop a crush on someone else..."
        mc.name "You."
        "Understanding dawns on [the_sister.possessive_title]'s face and you can tell that she is deep in thought, no doubt reexamining her recent interactions with [the_person.title]."
        mc.name "Obviously I can't blame her for picking you over me, I would do the same thing."
        "That earns you a faint smile, although she is still thinking."
        mc.name "And it would be pretty hypocritical of me to say you couldn't explore a relationship with her when I already have."
        mc.name "So she is scared to come out to you and wreck your freindship if you wouldn't be interested, but I couldn't exactly explain why she hasn't seen you flirting with boys at school."
    else:
        "Well, no going back now. How are you going to ask your sister if she wants to start dating your ex?"
        if not the_sister.has_taboo("vaginal_sex"):
            mc.name "So you and I have gotten very close, but I'm not sure what kind of future we really have."
        elif not the_sister.has_taboo("sucking_cock"):
            mc.name "Getting close to you has been lots of fun, but there are limits to what we should really do together."
        mc.name "[the_person.fname] and I hit it off after a few conversations, and started spending some time together too."
        the_sister "I know, and that is fine. I still don't understand where this is going."
        mc.name "I'm getting there, hang on."
        mc.name "So you know she kinda broke up with me, but niether of us have told you why."
        mc.name "The thing is that when we fooled around it was clear she wanted something else, and she was developing a crush on someone else..."
        mc.name "You."
        "Understanding dawns on [the_sister.possessive_title]'s face and you can tell that she is deep in thought, no doubt reexamining her recent interactions with [the_person.title]."
        mc.name "Obviously I can't blame her for picking you over me, I would do the same thing."
        "That earns you a faint smile, although she is still thinking."
        mc.name "And it would be pretty hypocritical of me to say you couldn't fool around with her when I already have."
        mc.name "So she is scared to come out to you and make unwelcome advances, but I couldn't exactly explain why she hasn't seen you hanging off any boys at school."
    the_sister "Wow... that is a lot. I want to say I'm surprised, but I guess I'm really not."
    the_sister "It is sort of like finally figuring out an optical illusion. Things make more sense now when I think about the way she behaves."
    the_sister "Plus I'm a little flattered but at the same time embarassed that she didn't think she could talk to me directly."
    mc.name "It can be a tough conversation to have, and I don't think she has really had it with too many people yet."
    the_sister "Oh god, do you think we are the only two people that know? Will it mess her up if I reject her?"
    mc.name "I don't know. Like I said, it is a delicate situation."
    the_sister "Yeah..."
    mc.name "Of course the real question is what you want to do. You can't guilt yourself into a relationship you don't want to make her happy."
    $ willing = lily_willing_threesome()
    if willing:
        the_sister "Well first things first, I obviously don't have a problem with being intimate with another girl."
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            the_sister "Even when you aren't around me and Mom have been getting pretty involved."
    else:
        the_sister "I'm not opposed to the idea, I just kinda always pictured myself with a man."
    mc.name "Okay, that is one aspect of this taken care of, what about the relationship aspect?"
    the_sister "I don't know, I hadn't really thought of her in that way, and it's gonna take some time for me to process."
    mc.name "That's good, but she will want to know what I found out about your sexuality. What should I tell her?"
    if willing:
        the_sister "Go ahead and tell her I have some experience with women, but don't be too specific."
        mc.name "Obviously."
    else:
        the_sister "Tell her the truth, I've never been with a woman but I don't think I'd have a problem if we had a good connection."
        mc.name "Okay."
    the_sister "Does she know you were going to out her to me?"
    mc.name "No, and I feel terrible about that, but I didn't see a way to ask you without telling you why."
    the_sister "Yeah... maybe I can try and set her up with a boy and see how she reacts. Or maybe I could call a girl hot and see what she does... I'll figure something out."
    mc.name "Then what? If she confesses and asks you out are you going to say yes?"
    the_sister "I guess. I mean if it is just a date it won't be too different than hanging out with my friend."
    the_sister "What do you think I should do?"
    menu:
        "Go for it" if willing:
            $ the_person.event_triggers_dict["lily_truth"] = 2
            mc.name "My vote is definitely that you go for it. The two of you would be so hot together."
            the_sister "You know I'm not gonna let you watch right?"
            mc.name "Don't worry, I can imagine it just fine."
            mc.name "But seriously, I think she could make you happy. You are only young once, might as well take advantage of the opportunity while you have it."
        "Take it slow":
            $ the_person.event_triggers_dict["lily_truth"] = 1
            mc.name "You can always take things slow too, no need to rush right into sex."
            if not the_sister.has_taboo("vaginal_sex"):
                the_sister "Really? Promoting abstinince while you fuck your sister is a bit disingenuous."
                mc.name "Well everyone is different. You don't need to model your sex life after mine."
            elif not the_sister.has_taboo("sucking_cock") or not the_sister.has_taboo("anal_sex"):
                the_sister "Really? The restraint speech from you sounds a bit hypocritical."
                mc.name "Hey, I'm just saying it is an option."
            else:
                the_sister "Yeah, wouldn't want to do anything we regret."
                mc.name "Exactly."
        "Don't do it":
            $ the_person.event_triggers_dict["lily_truth"] = -1
            mc.name "It's not a good idea. If something goes wrong what are you going to do the rest of the semester?"
            the_sister "I guess you're right."
    if willing or (the_sister.sluttiness + 10*the_sister.get_opinion_score("getting head")) > 60:
        if the_person.event_triggers_dict.get("lily_truth", 0) > 1:
            the_sister "I guess you're right. I mean she is hot."
            the_sister "I'm kind of excited about next week now."
        elif the_person.event_triggers_dict.get("lily_truth", 0) > 0:
            the_sister "Right, no harm no foul. She is kinda hot."
            the_sister "Maybe I'll just make the first move and see what happens."
        else:
            the_sister "It's a shame, she is pretty hot."
            the_sister "I'll just wait for her to make the first move."
        $ the_person.event_triggers_dict["lily_truth"] += 1
    else:
        if the_person.event_triggers_dict.get("lily_truth", 0) > 0:
            the_sister "Sounds like a plan. I'll just wait for her to make the first move."
        else:
            the_sister "I'll just think of it as a compliment and try to move past this."
    mc.name "I think that whatever happens and whatever you ultimatly decide she wants to keep your friendship strong."
    if the_person.event_triggers_dict.get("lily_truth", 0) > 0:
        the_sister "I know, and I do too, but if we could have something more that might be even better."
    else:
        the_sister "I know, I just hope she isn't too upset."
    $ clear_scene()
    return

label lily_second_followup_loop_label():
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ the_person.event_triggers_dict["friend_with_benefits"] = 2
    "As you are getting ready for bed you decide there is no time like the present and make your way to [the_sister.possessive_title]'s room."
    $ mc.location = lily_bedroom
    $ the_sister.draw_person(position = "sitting")
    the_sister "Hey there, [the_sister.mc_title]. Back again?"
    if cousin.location == lily_bedroom:
        $ mc.location.move_person(cousin, downtown)
        mc.name "Hey, [the_sister.title], where is [cousin.fname]?"
        the_sister "Don't know, don't care. Just happy to have some alone time."
        mc.name "Oh, sorry, I can go."
        the_sister "No, wait! Did you want to talk?"
    mc.name "Yeah, I seems like [the_person.fname] chickened out."
    the_sister "Yeah... There were a few times where it seemed like she wanted to ask me something, but she kept changing the topic when I asked."
    mc.name "Have you thought anymore about what you want to do?"
    $ willing = lily_willing_threesome()
    if the_person.event_triggers_dict.get("lily_truth", 0) < 0 and willing:
        the_sister "Well since last week things have changed a bit."
        the_sister "I obviously don't have a problem with being intimate with another girl."
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            the_sister "Even when you aren't around me and mom have been getting pretty involved."
    else:
        the_sister "Nothing has really changed for me. Did you change your mind about what I should do?"
    menu:
        "Go for it" if willing:
            $ the_person.event_triggers_dict["lily_truth"] = 2
            mc.name "In light of recent developments I think you should go for it."
            the_sister "You know I'm not gonna let you watch right?"
            mc.name "Don't worry, I can imagine it just fine."
            mc.name "But seriously, I think she could make you happy. You are only young once, might as well take advantage of the opportunity while you have it."
        "Take it slow":
            $ the_person.event_triggers_dict["lily_truth"] = 1
            mc.name "I've been thinking about it and you should give her a chance."
            mc.name "You can always take things slow too, no need to rush right into sex."
            if not the_sister.has_taboo("vaginal_sex"):
                the_sister "Really? Promoting abstinince while you fuck your sister is a bit disingenuous."
                mc.name "Well everyone is different. You don't need to model your sex life after mine."
            elif not the_sister.has_taboo("sucking_cock") or not the_sister.has_taboo("anal_sex"):
                the_sister "Really? The restraint speech from you sounds a bit hypocritical."
                mc.name "Hey, I'm just saying it is an option."
            else:
                the_sister "Yeah, wouldn't want to do anything we regret."
                mc.name "Exactly."
        "Don't do it":
            $ the_person.event_triggers_dict["lily_truth"] = -1
            mc.name "It's still not a good idea. If something goes wrong what are you going to do the rest of the semester?"
            the_sister "I guess you're right."
    if willing or (the_sister.sluttiness + 10*the_sister.get_opinion_score("getting head")) > 60:
        if the_person.event_triggers_dict.get("lily_truth", 0) > 1:
            the_sister "I guess you're right. I mean she is hot."
            the_sister "I'm kind of excited about next week now."
        elif the_person.event_triggers_dict.get("lily_truth", 0) > 0:
            the_sister "Right, no harm no foul. She is kinda hot."
            the_sister "Maybe I'll just make the first move and see what happens."
        else:
            the_sister "It's a shame, she is pretty hot."
            the_sister "I'll just wait for her to make the first move."
        $ the_person.event_triggers_dict["lily_truth"] += 1
    else:
        if the_person.event_triggers_dict.get("lily_truth", 0) > 0:
            the_sister "Sounds like a plan. I'll just wait for her to make the first move."
        else:
            the_sister "I'll just think of it as a compliment and try to move past this."
    mc.name "I think that whatever happens and whatever you ultimatly decide she wants to keep your friendship strong."
    if the_person.event_triggers_dict.get("lily_truth", 0) > 0:
        the_sister "I know, and I do too, but if we could have something more that might be even better."
    else:
        the_sister "I know, I just hope she isn't too upset."
    $ clear_scene()
    return

label lily_third_best_friend(the_sister, the_person):
    $ wait = False
    if the_person.event_triggers_dict.get("lily_truth", 0) > 2: # lily starts things
        "As it gets later and later it seems like [the_person.title] is not going to visit you today."
        "That makes sense, [the_sister.title] was pretty excited about initiating things after your talk last week."
        if the_person.event_triggers_dict.get("lily_lie", 0) < 1: # it is a surprise
            "[the_person.title] must have been incredibly surprised when she made the first move."
        else: # it is welcome
            "[the_person.title] must have been thrilled when she made the first move."
    elif the_person.event_triggers_dict.get("lily_lie", 0) <1: # wait for next week
        $ wait = True
        if the_person.event_triggers_dict.get("lily_lie", 0) <0: # doesn't want to be disappointed LOOP
            the_person "Hey, [the_person.mc_title]."
            mc.name "Hey, shouldn't you be talking with [the_sister.fname]?"
            the_person "I chickened out. I was hoping maybe you had talked with her again."
            the_person "If anything has changed in the last week it might give me the courage to talk to her."
            mc.name "As a matter of fact..."
        else: # first time answer
            the_person "Hey, [the_person.mc_title]. Sorry to sound like a broken record, but did you happen to talk to [the_sister.fname]?"
            mc.name "I did, we had a bit of a heart to heart, and she is a bit like you."
            mc.name "She is young and she isn't exactly sure what kind of relationships she will be okay with."
        "Now for the moment of truth. Your serums give you some control over [the_sister.possessive_title] so if you want to change her opinion you probably have that power."
        if the_person.event_triggers_dict.get("lily_truth", 0) < 0:
            "She is currently opposed to the idea, but you don't need to tell [the_person.title] that."
        else:
            "She would go along with it, but not too eagerly. That doesn't mean you have to tell [the_person.title] the truth."
        menu:
            "She loves you":
                $ the_person.event_triggers_dict["lily_lie"] = 2
                mc.name "Despite that I think she has a bit of a crush on you too."
                mc.name "When I brought up the idea of being with another girl she seemed to keep thinking of you as that girl."
                mc.name "So at the very least I can assure you she thinks you are hot. Combine that with your shared friendship and I think you'll be pleased with her response."
                the_person "Wow, that is great. I've got butterflies just thinking about this."
            "You have a shot":
                $ the_person.event_triggers_dict["lily_lie"] = 1
                mc.name "She is certainly curious. Maybe not as much as you are, but she definitely does not have a problem with the idea."
                mc.name "It seems like it hadn't really occured to her before, but now that I brought up the idea she is open to something."
                mc.name "She might still be a bit shocked when you come out to her, but you have a real shot of getting her to go out with you."
                the_person "That's good to know, takes some of the pressure off to not be scared of her reaction."
            "It's hopeless":
                $ the_person.event_triggers_dict["lily_lie"] = -1
                mc.name "Despite that I think you are going to have trouble convincing her to go out with you."
                mc.name "She still has some pretty strongly ingrained beliefs of what an appropriate relationship looks like."
                mc.name "Secretly I think she is curious but the social stigma she associates with the idea is going to make it hard to actually act on that curiosity."
                the_person "That is disappointing. I still think I need to take my shot, even if it doesn't work out."
        the_person "Alright, now I just need to work up the courage to tell her how I feel."
        mc.name "Give me another week to talk with her. I might be able to improve your odds."
        the_person "Yeah, of course. It is too late now anyway. I really hope we don't have too much homework next week."
        "With the conversation set for next week you have another chance to try and change [the_sister.title]'s opinion."
    else: # person starts things
        "As it gets later and later it seems like [the_person.title] is not going to visit you today."
        if the_person.event_triggers_dict.get("lily_lie", 0) > 1:
            "That makes sense, you already told her [the_sister.title] would definitely be interested."
        else:
            "That makes sense, you already told her you thought [the_sister.title] would come around eventually."
        if the_person.event_triggers_dict.get("lily_truth", 0) > 0: # it is welcome
            "Fortunately for her [the_sister.possessive_title] is going to eagerly accept."
        elif the_person.event_triggers_dict.get("lily_truth", 0) > -1: # it is acceptable
            "Luckily [the_sister.title] is not going to object too much to the idea."
        else: # it is not good
            "Unfortunately [the_sister.title] is going to reject her. [the_person.title] is going to be pissed."
            $ the_person.change_stats(happiness = -20, love = -20, obedience = -20)
            $ the_person.event_triggers_dict["anger"] = 2
    if wait:
        $ lily_second_followup_loop = Action("Lily Second Followup Loop", lily_followup_requirement, "lily_second_followup_loop_label")
        $ mc.business.add_mandatory_crisis(lily_second_followup_loop)
    else:
        "You'll have to check in with [the_sister.title] and see how things went."
        $ lily_third_followup = Action("Lily Third Followup", lily_followup_requirement, "lily_third_followup_label")
        $ mc.business.add_mandatory_crisis(lily_third_followup)
    $ clear_scene()
    return

label lily_third_followup_label():
    $ the_person = get_lab_partner()
    $ the_sister = lily
    if the_person.event_triggers_dict.get("lily_truth", 0) > 2: # she started
        $ the_sister.draw_person(emotion = "happy")
        "As you are getting ready for bed you hear a rapid knock at your door before [the_sister.title] pushes it open and lets herself in."
        "She is smiling widely and practically bubbling over with excitement."
        the_sister "Oh my god! [the_sister.mc_title] me and [the_person.fname] are dating!"
        the_sister "We were studying and I bascially propositioned her."
        $ the_sister.draw_person(position = "sitting")
        "She makes her way over to your bed and sits down next to you."
        if the_person.event_triggers_dict.get("lily_lie", 0) < 1: #surprise
            the_sister "At first she was a little surprised. Honestly I worried for a moment that you were lying to me about her feelings."
        else: # as expected
            the_sister "She was acting nervous all day and I figured I would just cut to the chase. She was so relieved and excited."
        the_sister "We had some work to do, but we are both eager to start spending more time together."
    elif the_person.event_triggers_dict.get("lily_truth", 0) > -1: # she accepted
        if the_person.event_triggers_dict.get("lily_truth", 0) > 0: # that is great
            $ the_sister.draw_person(emotion = "happy")
            "As you are getting ready for bed you hear a knock at your door before [the_sister.title] pushes it open and lets herself in."
            "She has a silly grin on her face. It is pretty clear something good happened tonight."
            the_sister "Hey [the_sister.mc_title], you'll never guess what happened today."
            "You grin back and put on a thoughtful expression."
            mc.name "You got a good score on a test?"
            the_sister "No, silly, [the_person.fname] worked up the courage to ask me out."
            mc.name "Really, what did you say?"
            the_sister "I said yes, just like you wanted. She was so relieved and excited."
        else: # you told her not to
            $ the_sister.draw_person(emotion = "sad")
            "As you are getting ready for bed you hear a hesitant knock at your door before [the_sister.title] pushes it open a crack."
            the_sister "Hey, [the_sister.mc_title] could I come in a talk to you?"
            mc.name "Yeah, sure. Is something wrong?"
            "She makes her way over to your bed and sits down next to you taking your hand in hers."
            $ the_sister.draw_person(position = "sitting", emotion = "sad")
            the_sister "Kind of, [the_person.fname] asked me out tonight. I know you said I should turn her down, but she looked so..."
            the_sister "I don't know exactly. It was like she was hanging all of her hopes on my answer."
            the_sister "I just couldn't say no to that face. I want to explore a relationship with her."
            if the_sister.obedience > 180:
                menu:
                    "Be understanding":
                        pass
                    "Break them up":
                        mc.name "[the_sister.title] that is completely unacceptable. I told you what to do."
                        mc.name "Now you are going to have to break up with her."
                        the_sister "What? No I couldn't... it will break her heart."
                        mc.name "I'll take some of the blame, I should have been more clear the first time. This is not a request it is an order."
                        mc.name "You WILL do this."
                        $ the_sister.change_stats(happiness = -20, love = -20, obedience = 20)
                        the_sister "Yes, sorry I will."
                        mc.name "What was that?"
                        the_sister "Yes Master. I live to serve you."
                        if the_person.obedience > 180:
                            $ the_person.change_stats(happiness = -20, love = -20, obedience = 20)
                        else:
                            $ the_person.change_stats(happiness = -20, love = -20, obedience = -20)
                        $ the_person.event_triggers_dict["anger"] = 2
                        "That was harder than it should have been. Now you are going to have to deal with [the_person.title] too."
                        $ clear_scene()
                        return
            mc.name "That's okay. I understand."
            mc.name "I should have expected this. You've been so adventurous I really can't fault you for wanting to experiment more."
            mc.name "After all, I am the one who has pushed you to keep going further."
            if the_sister.obedience > 180:
                the_sister "I'll try to be better Master. I want to serve you and make you happy."
                $ the_sister.change_stats(happiness = 10, love = 10, obedience = 20)
            else:
                the_sister "I'm sorry I let you down, thank you for understanding."
                $ the_sister.change_stats(happiness = 10, love = 10, obedience = -10)
            mc.name "What are you plans now?"
    else: # she rejected
        "As you are getting ready for bed your door suddenly slams open and an angry looking [the_sister.fname] storms in."
        $ the_sister.draw_person(emotion = "angry")
        the_sister "What the FUCK!?! Did you tell [the_person.fname] that I would go out with her?"
        the_sister "What were you thinking? You told me to turn her down and then sent her in there to get rejected."
        the_sister "She was so confident she just blurted it out and I had to tell her no. The look on her face broke my heart, it was like she couldn't even understand what I was saying."
        the_sister "Fuck, you are such an asshole [mc.name]."
        $ the_sister.draw_person(position = "walking_away")
        $ the_sister.change_stats(happiness = -20, love = -20, obedience = -20)
        "With that she spins and walks out, leaving your door standing open."
        $ clear_scene()
        "Maybe that was a mistake..."
        #mom comes to check on you maybe
        return
    the_sister "We are going to start doing our classwork on campus between classes so that we can come back here on Monday night."
    the_sister "She hasn't told her parents yet, and I don't really want mom to know so soon."
    if mc.business.event_triggers_dict.get("family_threesome", False) == True:
        the_sister "I don't think she would be jealous, but still better safe than sorry."
    elif lily.event_triggers_dict.get("vaginal_revisit_complete", False) or the_sister.is_girlfriend():
        the_sister "After all it isn't like I'm a lesbian. We are just fooling around a bit."
    else:
        the_sister "I'm not really sure how I would explain it. I'm not even sure how much I'm going to like girls."
    mc.name "Don't worry, your secret is safe with me. I am excellent at keeping secrets."
    the_sister "Thanks, I knew I could count on you."
    if the_sister.is_girlfriend():
        the_sister "This doesn't have to change anything between us."
        the_sister "Our relationship is still my highest priority, but I'm looking forward to exploring something with her too."
    elif the_sister.has_role(slave_role):
        the_sister "Of course you can still use me anytime you need."
        the_sister "I'll always be here for you [the_sister.mc_title], and maybe someday I can get her to be here for you too."
    elif lily.event_triggers_dict.get("vaginal_revisit_complete", False):
        the_sister "Don't worry you will still get to fuck me when you want."
        the_sister "I don't think I could give up real hot dick for her. Maybe I can even convince her to join us."
    elif lily.event_triggers_dict.get("anal_revisit_complete", False):
        the_sister "Don't worry, I'll still let you use my ass for relief."
        the_sister "We just have to be careful so she doesn't taste your cum if she eats me out."
    elif lily.event_triggers_dict.get("oral_revisit_complete", False):
        the_sister "I can still service you from time to time if you want."
        the_sister "But you better return the favor, [the_person.fname] might be better than you."
    else:
        the_sister "I'm sure you'll find someone too, maybe one of the girls at your office?"
    $ clear_scene()
    return

label lily_overnight_label():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ wear_pajamas(the_sister)
    $ the_sister.draw_person(emotion = "sad")
    "A few moments later your door opens slightly and [the_sister.possessive_title] quickly slips in and pushes it closed."
    if the_sister.event_triggers_dict.get("first_overnight", True):
        mc.name "Hey [the_sister.title]."
        the_sister "Shh... I don't want Mom to hear us."
        if mc.business.event_triggers_dict.get("family_threesome", False) == True:
            mc.name "You know she is fine with basically anything we do now right?"
            the_sister "I know, but I just want you to myself tonight."
        else:
            mc.name "Do you have something planned that she shouldn't find out about?"
            the_sister "It would be a bit embarrassing if she picked the wrong moment to walk in."
        mc.name "Really? What about [the_person.title]?"
        the_sister "Don't worry, she is gone for the night."
        mc.name "I heard the door, but what about the two of you?"
        the_sister "Don't worry, we are leaving things casual for now, she doesn't have to know."
    else:
        mc.name "Welcome back [the_sister.title]."
        mc.name "Another unsatisfying night with [the_person.title]?"
        the_sister "You could say that, she is trying but doesn't ever seem to be able to get me off like you."
        the_sister "Do you think you could help me out?"
        if mc.business.event_triggers_dict.get("family_threesome", False):
            menu:
                "Help her":
                    pass
                "Not tonight":
                    mc.name "I'm sorry [the_sister.title], as nice as it is to have you here I am just too tired."
                    mc.name "Why don't you go see if Mom can help you?"
                    the_sister "Oh... okay. Have a good night [the_sister.mc_title]."
                    $ the_sister.change_stats(love = -2, happiness = -2, obedience = 2)
                    call lesbian_sex(the_sister, mom, path = [finger1, finger1, finger1, oral1, oral1, oral1]) from _call_lesbian_sex_lily_overnight
                    $ clear_scene()
                    return
    mc.name "What did you have in mind?"
    $ the_sister.draw_person(emotion = "happy")

    "HERE IS WHERE YOU'RE CHOICES ARE LIMITED BY TABOOS"

    if not the_sister.has_taboo("vaginal_sex"):
        pass
    elif not the_sister.has_taboo("anal_sex"):
        pass
    elif not the_sister.has_taboo("touching_vagina"):
        pass
    elif not the_sister.has_taboo("touching_body"):
        pass
    else:
        pass
    call fuck_person(the_sister) from _call_fuck_person_lily_overnight_1

    if the_sister.event_triggers_dict.get("first_overnight", True) and the_person.event_triggers_dict.get("first_overnight", True):
        "Now that [the_sister.title] has come to you for help you wonder if there is any possibility of [the_person.title] needing you as well."
    elif not the_person.event_triggers_dict.get("first_overnight", True) and the_sister.event_triggers_dict.get("first_overnight", True):
        "Now that both [the_person.title] and [the_sister.title] have come looking for help you wonder what it would take to get them to to both join you at the same time."
    "You turn off the light by your bed and quickly sink into satisfied sleep."
    $ the_person.event_triggers_dict["first_overnight"] = False
    $ clear_scene()
    return

label best_friend_overnight_label():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    $ the_sister = lily
    $ the_person.apply_planned_outfit()
    "A few moments later there is a sound at your window. You are startled at first, but then you see [the_person.fname] standing just outside."
    if the_person.event_triggers_dict.get("first_overnight", True):
        $ scene_manager.add_actor(the_person, emotion = "sad")
        "You are a bit puzzled, but since she is gesturing for you to open the window you move to comply."
        mc.name "Yes?"
        the_person "We need to talk, can I come in?"
        mc.name "Um, yeah, you know you could have just walked down the hall."
        the_person "No, [the_sister.title] can't know I'm here. I had to leave and then sneak back."
        the_person "Can you give me a hand?"
        "You hold out a hand and help her through the window as quitely as you can, and then give her a moment to straighten herself out."
        mc.name "So.... how can I help you?"
        the_person "This is kind of awakward, you know since I broke up with you, but could we maybe..."
        "[the_person.title] stammers to a halt and blushes very red. Looking more closely it seems she is bit more flushed than climbing through your window would explain."
        mc.name "Wait, is this a booty call? After just getting done with my sister you come to see me too?"
        the_person "It's not like that. I'm not some sex crazed addict or anything. It's just... she got tired... and I didn't get to finish."
        mc.name "So you want to cheat on her with me?"
        the_person "Our relationship is still new, we are leaving it open for now and seeing how it works out."
        the_person "Plus, she already knows about us. We talked a bit and she doesn't care about what we've done."
        the_person "I figure as long as we keep it physical everything is fine. We're just taking care of one another's needs."
    else:
        $ scene_manager.add_actor(the_person, emotion = "happy")
        "It is pretty clear why she is back again so you quickly move to open the window."
        "You help her through the opening and then pull her into an embrace."
        mc.name "I feel a bit bad about you needing my help again, but I'd be lying if I said I wasn't looking forward to assisting you."
        the_person "Honestly I'm a bit excited too. It feels disloyal to say this, but you are so much better than [the_sister.fname] at this part."
    the_person "Why don't you get the window and I'll get ready for you."
    $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())
    "Once she is naked [the_person.title] drops back onto your bed, ready for you to take care of her."
    $ scene_manager.update_actor(the_person, position = "missionary", emotion = "happy")
    "You have to admit, the sight of her young aroused body has you ready as well and you qickly move into position."
    call fuck_person(the_person, private = True, start_object = make_bed(), skip_intro = False, girl_in_charge = False, hide_leave = False, affair_ask_after = False) from _call_fuck_person_best_friend_overnight
    $ the_report = _return
    if the_report.get("girl orgasms", 0) == 0:
        the_person "Seriously!? Neither one of you can get me off?"
        the_person "I'm gonna go. I guess I have to take care of this myself."
        $ the_person.change_stats(happiness = -10, love = -5, obedience = -5)
    else:
        the_person "God [the_person.mc_title] that was exactly what I needed."
        mc.name "Always happy to help you out."
        the_person "I'll keep that in mind if I'm ever in need again."
        if the_person.has_role(trance_role):
            call check_date_trance(the_person) from _call_check_date_trance_best_friend_overnight
    $ the_person.restore_all_clothing()
    $ scene_manager.update_actor(the_person, position = "walking_away")
    "With that [the_person.title] gets herself dressed and then heads to the door."
    if the_person.has_role(slave_role) and wakeup_duty_crisis not in mc.business.mandatory_morning_crises_list:
        $ slave_add_wakeup_duty_action(the_person)
        mc.name "You can't leave [the_person.title]."
        the_person "What?"
        mc.name "Well, first of all [the_sister.fname] could be out there and it would be hard to explain why you are coming out of my room."
        "She turns and starts to make her way to the window instead."
        mc.name "Also, I'm going to need you to return this favor in the morning. Find someplace comfortable on the floor and wake me up tomorrow."
        the_person "Right, yes [the_person.mc_title]."
    else:
        mc.name "Aren't you forgetting something?"
        "You catch her just as her hand is on the door and she turns to look back at you."
        $ scene_manager.update_actor(the_person, position = "back_peek")
        "With a smile you point towards the window she used to climb into your room."
        "She groans slightly, but does turn the rest of the way and make her way to the window."
        menu:
            "Help her out":
                $ the_person.change_love(2)
                "You get up and give her a hand getting out, earning you a quick kiss on the cheek before she leaves."
            "Just watch":
                $ the_person.change_obedience(2)
                "You just watch from your bed as she struggles her way out."

    if the_sister.event_triggers_dict.get("first_overnight", True) and the_person.event_triggers_dict.get("first_overnight", True):
        "Now that [the_person.title] has come to you for help you wonder if there is any possibility of [the_sister.title] needing you as well."
    elif not the_sister.event_triggers_dict.get("first_overnight", True) and the_person.event_triggers_dict.get("first_overnight", True):
        "Now that both [the_person.title] and [the_sister.title] have come looking for help you wonder what it would take to get them to to both join you at the same time."
    "You turn off the light by your bed and quickly sink into satisfied sleep."
    $ the_person.event_triggers_dict["first_overnight"] = False
    $ clear_scene()
    return

label best_friend_threesome_label():
    $ scene_manager = Scene()
    $ the_person = get_lab_partner()
    if the_person.arousal_perc > lily.arousal_perc:
        $ the_person = get_lab_partner()
        $ the_other_person = lily
    else:
        $ the_other_person = get_lab_partner()
        $ the_person = lily
    $ the_person.apply_planned_outfit()
    $ the_other_person.apply_planned_outfit()
    if the_person == lily:
        "A few moments later your door opens slightly and [the_person.possessive_title] quickly slips in and pushes it closed."
        $ scene_manager.add_actor(the_person, emotion = "sad")
        mc.name "Welcome back [the_person.title]."
        mc.name "Another unsatisfying night with [the_person.title]?"
        the_person "You could say that, she is trying but doesn't ever seem to be able to get me off like you."
        the_person "Do you think you could help me out?"
        $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())

    else:
        "A few moments later there is a sound at your window. You are startled at first, but then you see [the_person.fname] standing just outside."
        $ scene_manager.add_actor(the_person, emotion = "sad")
        "It is pretty clear why she is back again so you quickly move to open the window."
        "You help her through the opening and then pull her into an embrace."
        mc.name "I feel a bit bad about you needing my help again, but I'd be lying if I said I wasn't looking forward to assisting you."
        the_person "Honestly I'm a bit excited too. It feels disloyal to say this, but you are so much better than [the_other_person.fname] at this part."
        the_person "Why don't you get the window and I'll get ready for you."
        $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())
        "Once she is naked [the_person.title] drops back onto your bed, ready for you to take care of her."

    "HERE IS WHERE THE OTHER PERSON WALKS IN AND CATCHES YOU"

    $ scene_manager.update_actor(the_person, emotion = "sad")
    $ scene_manager.add_actor(the_other_person, display_transform = character_left_flipped, emotion = "sad")
    $ generalised_strip_description(the_other_person, the_person.outfit.get_full_strip_list())
    menu:
        "Start with [the_person.title]":
            call fuck_person(the_other_person) from _call_fuck_person_bf_threesome_1
            call fuck_person(the_person) from _call_fuck_person_bf_threesome_2
        "Start with [the_other_person.title]":
            call fuck_person(the_other_person) from _call_fuck_person_bf_threesome_3
            call fuck_person(the_person) from _call_fuck_person_bf_threesome_4

    "HERE IS WHERE THEY REACT BASED ON YOUR PERFORMANCE"

    $ clear_scene()
    return

label best_friend_test():
    $ the_sister = lily
    $ the_person = get_lab_partner()
    $ stop = False
    while not stop:
        if the_person.event_triggers_dict.get("anger", 1) > 0:
            call study_friend_transition(the_sister, the_person)
        elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 1:
            $ the_person.event_triggers_dict["friend_with_benefits"] = 1
            call lily_first_best_friend(the_sister, the_person)
            call lily_first_followup_label()
            call lily_first_followup_morning()
        elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 2:
            $ the_person.event_triggers_dict["friend_with_benefits"] = 2
            call lily_second_best_friend(the_sister, the_person)
            call lily_second_followup_label()
            call lily_second_followup_loop_label()
        elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 3:
            $ the_person.event_triggers_dict["friend_with_benefits"] = 3
            call lily_third_best_friend(the_sister, the_person)
            call lily_third_followup_label()
        else:
            "Unsurprisingly you do not get a visit during [the_sister.possessive_title]'s study time with [the_person.title]."
            if the_person.event_triggers_dict.get("friend_with_benefits", 0) < 50:
                call lily_offscreen_corruption(the_sister, the_person)
                "You do occasionally hear the murmur of them talking. Maybe you should try to find a way to spy on their dates in the future."
            elif the_person.event_triggers_dict.get("friend_with_benefits", 0) < 70:
                call lesbian_sex(the_sister, the_person)
                "You do occasionally hear what could be muffled moans. Some kind of spy camera is definitely sounding like a good invenstment."
            else:
                call lesbian_sex(the_sister, the_person)
                $ (sister_orgasm, person_orgasm) = _return
                "From time to time you hear a bed squeaking and once or twice it crashes into the wall. When it does there is some giggling followed by extreme silence."
                "You wonder if they really think their activities are going unnoticed, and once again wish you had picked up a camera."
            if (sister_orgasm + other_orgasm) < 1 and the_person.event_triggers_dict.get("friend_with_benefits", 0) > 80:
                $ best_friend_threesome = Action("Best Friend Threesome", lily_followup_requirement, "best_friend_threesome_label")
                $ mc.business.add_mandatory_crisis(best_friend_threesome)
            elif sister_orgasm < 1:
                $ lily_overnight = Action("Lily Overnight", lily_followup_requirement, "lily_overnight_label")
                $ mc.business.add_mandatory_crisis(lily_overnight)
            elif person_orgasm < 1:
                $ best_friend_overnight = Action("Best Friend Overnight", lily_followup_requirement, "best_friend_overnight_label")
                $ mc.business.add_mandatory_crisis(best_friend_overnight)
            $ the_person.event_triggers_dict["friend_with_benefits"] += (sister_orgasm + other_orgasm)*5
            $ the_other_person.event_triggers_dict["friend_with_benefits"] += (sister_orgasm + other_orgasm)*5
        menu:
            "Continue":
                pass
            "Stop":
                $ stop = True
    return
