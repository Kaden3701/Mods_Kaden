init 3 python:
    def protein_shake_requirement():
        if not erica_protein_shake_is_unlocked():
            return False
        if time_of_day == 0:
            return "It is too early"
        if time_of_day == 4:
            return "It is too late"
        return True

    def protein_shake_initialization(self):
        gym.add_action(self)
        return

    protein_shake_action = ActionMod("Buy a protein shake for...\n{color=#ff0000}{size=18}Costs: $10{/size}{/color}", protein_shake_requirement, "protein_shake_label",
        initialization = protein_shake_initialization, menu_tooltip = "Bring a protein shake to someone in the gym.", category="Mall")

label protein_shake_label():
    if len(known_people_at_location(mc.location) + unknown_people_at_location(mc.location)) > 5:
        "There are a ton of people working out at the gym today. You could offer one of them a protein shake with some serum added."
    elif len(known_people_at_location(mc.location) + unknown_people_at_location(mc.location)) > 1:
        "There are a few people working out at the gym today. You could offer one of them a protein shake with some serum added."
    elif len(known_people_at_location(mc.location) + unknown_people_at_location(mc.location)) > 0:
        "There is only one person working out at the gym today. You could offer her a protein shake with some serum added."
    else:
        "There is no one working out at the gym today."
        return
    $ serum = None
    "You head over to the counter where they have the supplements. You order a couple of protein shakes, one for yourself and one to share."
    $ mc.business.change_funds(-10)
    "Once you are served, you have a moment with no one around. You can add a serum to the extra shake if you do it quickly!"
    menu:
        "Add a dose of serum to the shake" if mc.inventory.get_any_serum_count() > 0:
            call screen serum_inventory_select_ui(mc.inventory)
            if not _return == "None":
                $ serum = _return
                $ mc.inventory.change_serum(serum,-1)
                "You mix the serum into the protein shake."
            else:
                "You change your mind and leave the shake unaltered."
        "Add a dose of serum to the shake\n{color=#ff0000}{size=18}Requires: Serum{/size}{/color} (disabled)" if mc.inventory.get_any_serum_count() == 0:
            pass
        "Leave the shake alone":
            "You decide not dose one of the gym goers."
    "Now that you have a couple shakes it is time to find someone to share with."
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_at_location(mc.location) + unknown_people_at_location(mc.location), "Buy a shake for", ["Back"])]))
    $ the_person = _return
    if not the_person == "Back":
        if not the_person in known_people_at_location(mc.location):
            $ the_person.draw_person()
            "The girl that draws you eyes most is someone you haven't met before, but you figure that can be quickly remedied."
            "You decide to introduce yourself. You walk over to her and strike up a conversation."
            mc.name "Hello, I'm [mc.name], I don't think I've seen you around here before."
            $ the_person.set_mc_title(mc.name)
            the_person "Excuse me?"
            mc.name "I said hello, I wanted to come over and welcome you to the gym."
            "She looks you up and down, clearly a little confused why you would walk up to her out of the blue."
            if mc.charisma > 6:
                the_person "Oh wow! Thank you so much!"
                if serum:
                    "You hold out the dosed shake and she takes it with a smile."
                    $ the_person.give_serum(serum)
                else:
                    "You hold out the sake and she takes it with a smile."
                the_person "Wow, thanks again. This tastes great."
            elif mc.charisma > 4:
                the_person "Thanks, it is nice having some friendly people around to chat with."
                mc.name "Exactly, that is why I like this gym so much. As a matter of fact, I was getting myself a protein shake and thought maybe you could use one too."
                "She looks at it a bit skeptically."
                mc.name "I haven't tried either yet, so you can pick. The one on my right is blueberry and the other is strawberry."
                "She visibly relaxes at that."
                the_person "Thanks, blueberry sounds good."
                if serum:
                    if renpy.randint(0,1) > 0:
                        "Fortunately she picked the shake with the serum and takes a quick sip."
                        $ the_person.give_serum(serum)
                    else:
                        "Unfortunately she picks the wrong shake and you are left holding the one with, the now wasted, serum."
                else:
                    "You offer her the shake as you take a sip from the other."
            elif mc.charisma > 2:
                the_person "Thanks... do you work here?"
                mc.name "No, just a fellow gym goer, but if you need help with anything let me know."
                the_person "Actually, this guy just came up and started bothering me, do you think you could try and make him leave?"
                mc.name "Oh... right... sorry."
                "You beat a hasty retreat and find somewhere to dump out the extra shake."
                return
            else:
                $ the_person.draw_person(emotion = "angry")
                the_person "Get away creep, I just want to work out in peace."
                "That could have gone better, you back up and find a trash can to drop the extra shake in."
                return
            the_person "I'm [the_person.fname] by the way. Nice to meet you."
            $ the_person.set_title(the_person.name)
            $ the_person.set_possessive_title("Your gym girl")
            mc.name "Nice to meet you too."
        elif the_person.event_triggers_dict.get("protein_day", 0) == day:
            $ the_person.draw_person(emotion = "angry")
            the_person "What is wrong with you? You bought me a protein shake like an hour ago."
            the_person "What are you trying to say huh?"
            if the_person.body_type == "thin_body":
                the_person "Am I too skinny for you?"
            if the_person.body_type == "curvy_body":
                the_person "Am I too fat for you?"
            "Oh right... this was probably a mistake."
            mc.name "Sorry, I ju..."
            the_person "No, just no. I'm outta here."
            $ the_person.change_stats(love = -2, happiness = -2)
            return
        elif the_person.is_pregnant() and not the_person.knows_pregnant() and time_of_day == 1: #She has morning sickness
            mc.name "Care for a protein shake today, [the_person.title]?"
            $ the_person.draw_person(emotion = "sad")
            the_person "Oh... actually no. I'm not sure why, but I've been feeling nauseated all morning... sorry!"
            return
        elif the_person.love > 20:
            mc.name "Hey [the_person.title], looking good! I saw you over here and grabbed you a protein shake."
            "[the_person.possessive_title] looks at you and smiles wide."
            the_person "Oh! Hey [the_person.mc_title], that's great! I skipped the protein this morning..."
            if serum:
                "You hold out the dosed shake and she takes it with a smile."
                $ the_person.give_serum(serum)
            else:
                "You hold out the shake and she takes it with a smile."
        elif the_person.sluttiness > 40:
            mc.name "Hey [the_person.title]. I see you're working hard today, so I grabbed you a protein shake. Don't want you running out of energy."
            the_person "Hey! That's great! I need all the protein I can get."
            if not the_person.has_taboo("sucking_cock"):
                "She lowers her voice."
                the_person  "Especially from you... maybe after this we could..."
                mc.name "Mmm, that's a tempting offer. Let's see where the day takes us."
            if serum:
                "You hold out the dosed shake and she takes it with a smile."
                $ the_person.give_serum(serum)
            else:
                "You hold out the shake and she takes it with a smile."
        elif the_person.love < 0:
            mc.name "Damn, work it [the_person.title]. I've got a protein shake for you."
            $ the_person.draw_person(emotion = "sad")
            "She gives you a wary eye. It is clear she is skeptical of this sudden generosity."
            the_person "...did you spit in it or something?"
            mc.name "What? No, why would I do that."
            the_person "Worse then spit then? Did you really think I would take a drink from you?"
            if the_person.obedience > 160:
                mc.name "I did actually, go ahead take a sip before you upset me."
                if serum:
                    "You hold out the dosed shake and she takes it reluctantly."
                    $ the_person.give_serum(serum)
                else:
                    "You hold out the shake and she takes it reluctantly."
                $ the_person.change_stats(obedience = 2)
                "Although she is tense at first she can't taste anything wrong with the shake and seems to start enjoying it."
            else:
                mc.name "Sorry, no this was a mistake."
                $ the_person.change_stats(love = -2, happiness = -2)
                "She doesn't respond, just glaring at you until you turn and walk away."
            return
        else:
            mc.name "Hey [the_person.fname], I see you're working pretty hard today so I thought you could use a protein shake."
            "[the_person.possessive_title] looks at you and smiles."
            the_person "That sounds great!"
        "You chat for a bit as you both work on your shakes, but she wants to get back to her workout and you should probably do something too."
        mc.name "Well, I'm off to get my work out started. Have a good day."
        if the_person.love < 0:
            the_person "Um... okay..."
            "[the_person.possessive_title] is clearly still a bit skeptical."
        else:
            the_person "You too, and thanks again."
        $ the_person.change_stats(love = 2, happiness = 2)
        $ the_person.event_triggers_dict["protein_day"] = day
    return
