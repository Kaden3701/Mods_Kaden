init -1 python:
    def get_person_bra_size(self):
        if not hasattr(self, "_bra_size"):
            self._bra_size = Person.rank_tits(self.tits)
        return self._bra_size

    def set_person_bra_size(self, value):
        self._bra_size = value
        return

    Person.bra_size = property(get_person_bra_size, set_person_bra_size, None, "The bra size of a person.")

    def crisis_bra_size_requirement():
        if mc.business.is_open_for_business():
            if mc.is_at_work():
                if crisis_bra_size_get_people():
                    return True
        return False

    def bra_count(person):
        count = 0
        for outfit in [x for x in person.wardrobe.outfits + person.wardrobe.underwear_sets if x.wearing_bra()]:
            count += 1
        if count < 1 and person.wearing_bra:
            count += 1
        return count

    def crisis_bra_size_get_people():
        temp_list = []
        for person in mc.business.get_employee_list():
            if not pregnant_role in person.special_role:
                if person.bra_size + 1 < Person.rank_tits(person.tits): #more than 1 size bigger
                    if bra_count(person) > 0:
                        temp_list.append(person)
                    elif person.bra_size + 2 < Person.rank_tits(person.tits):
                        temp_list.append(person)
                elif person.bra_size - 1 > Person.rank_tits(person.tits): #more than 1 size smaller
                    if bra_count(person) > 0:
                        temp_list.append(person)
            for person in temp_list:
                for serum in person.serum_effects:
                    if serum.has_trait(breast_enhancement) or serum.has_trait(breast_reduction) or serum.has_trait(lactation_hormones):
                        if person in temp_list:
                            temp_list.remove(person)
        return temp_list

init 3 python:
    crisis_bra_size_action = ActionMod("Bra Size", crisis_bra_size_requirement, "crisis_bra_size_label",
        menu_tooltip = "An employee lets you know their bras don't fit any more.", category = "Business Crisis", is_crisis = True, is_morning_crisis = False, priority = 5)

label crisis_bra_size_label():
    $ the_person = get_random_from_list(crisis_bra_size_get_people())
    $ test_outfit = the_person.outfit.get_copy()
    $ the_bra = test_outfit.get_bra()
    if the_bra:
        $ test_outfit.remove_clothing(bra)
    if Person.rank_tits(the_person.tits) -1 > the_person.bra_size: #can't even fit in old tops
        $ top = test_outfit.get_upper_top_layer()
        while top:
            $ test_outfit.remove_clothing(top)
            $ top = test_outfit.get_upper_top_layer()
        $ test_outfit.add_upper(lab_coat.get_copy())
    $ the_person.apply_outfit(test_outfit)
    $ scene_manager = Scene()
    $ scene_manager.add_actor(the_person, position = "stand4", emotion = "sad")
    "As you are working one of your employees approaches, looking a little troubled."
    if Person.rank_tits(the_person.tits) -1 > the_person.bra_size:
        "You are a little surprised to see that she seems to be wearing a lab coat with no top on underneath."
    elif Person.rank_tits(the_person.tits) > the_person.bra_size:
        "It seems like she is not wearing a bra, and her breasts are straining to fit inside her top."
    if mc.location.get_person_count() > 1:
        "She steps close, lowering her voice so that no one else can hear."
    the_person "Excuse me, [the_person.mc_title] I'm having a problem and was hoping to get some advice from you."
    mc.name "Sure, [the_person.title], what can I do for you?"
    if mc.location.get_person_count() > 1:
        the_person "Could we go to your office so we can talk in private?"
        mc.name "Of course, lead the way."
        "You get up and follow her to your office, once there you take a seat and gesture for her to continue."
    the_person "This morning when I was getting dressed I was having some problems with my clothes."
    the_person "I tried a few different outfits, and it seems like nothing I have fits properly any more."
    mc.name "What do you mean they don't fit?"
    if Person.rank_tits(the_person.tits) > the_person.bra_size:
        the_person "It's my breasts, they have grown a ridiculous amount. They don't fit in my bras anymore. I can't even get them on."
        mc.name "That sounds terrible."
        if Person.rank_tits(the_person.tits) -1 > the_person.bra_size:
            the_person "It is, in fact it's so bad I couldn't even get my top on. I had to grab a lab coat to wear since nothing else worked."
    elif Person.rank_tits(the_person.tits) < the_person.bra_size:
        the_person "It's my breasts, they seem to be shrinking. It's like going back before puberty."
        the_person "Suddenly all of my clothes are really loose."
        the_person "I didn't even wear a bra, because it just felt weird having the cups half full."
    "It sounds like your serums have had a profound effect on [the_person.title]. You better help her deal with the fall out of their effects."
    mc.name "This is serious, what can I do to help you?"
    the_person "I think I need to buy new clothes so that I can be comfortable and properly dressed for work."
    the_person "The problem is that I just paid rent and I can't afford a whole new wardrobe until my next paycheck."
    the_person "I was hoping I could get an advance or something so that I can go shopping tonight."
    "This is at least partially your fault, you should probably take responsibility for the problem."
    mc.name "I should be able help you out."
    menu:
        "Give her an advance":
            mc.name "The company can certainly afford to pay you in advance. Your work is more than satisfactory."
            $ weeks_wages = the_person.salary*5
            $ the_person.draw_person(emotion = "happy")
            $ the_person.change_happiness(5 + mc.charisma)
            $ the_person.change_obedience(1 + mc.charisma)
            $ mc.business.funds -= weeks_wages
            $ the_person.change_salary(-the_person.salary)
            $ add_unpaid_intern_clear_punishment_action(the_person)
            "You pull out your wallet and start to pull out a few bills."
            "[the_person.title] takes the bills, then smiles broadly at you."
            the_person "That's very generous of you sir, thank you."
        "Give her a bonus":
            mc.name "In fact, you don't even need to consider it an advance."
            call employee_pay_cash_bonus(the_person) from _call_new_bra_bonus
    $ the_person.apply_outfit(test_outfit)
    $ scene_manager.update_actor(the_person)
    mc.name "Have you thought about what you want to buy when you go shopping?"
    the_person "I thought I would just buy the same clothes in a size that is more appropriate to my current situation."
    mc.name "That is one option, but why not take the opportunity to reassess your outfits. Are you happy with all of them the way they are?"
    the_person "I was so worried about getting something to wear I didn't consider that. Is there anything you think I should try and change?"
    $ alterations = 0
    if Person.rank_tits(the_person.tits) -1 > the_person.bra_size:
        mc.name "Well since it looks like you'll have to buy new shirts why don't we look at those first."
        the_person "Right, none of the ones I have fit right."
        menu:
            "Less conservative tops" if the_person.sluttiness > 30:
                mc.name "I think you could be a bit more daring. The clothes you have now are nice, but you might want to show off your new assets."
                the_person "You're right, it could be good to show off my body now that there is so much more to show."
                $ the_person.discover_opinion("skimpy outfits")
                $ alterations += smaller_shirts(the_person)
                if bra_count(the_person) == 1:
                    $ the_person.increase_opinion_score("skimpy outfits")
                if the_person.sluttiness > 50:
                    $ alterations += smaller_shirts(the_person)
                    if the_person.sluttiness > 70:
                        $ alterations += smaller_shirts(the_person)
                        if the_person.sluttiness > 90:
                            $ alterations += smaller_shirts(the_person)
            "The same tops":
                mc.name "I'm not sure if you'd be comfortable going with anything more daring that what you wear now."
                the_person "Yeah, I think that my current wardrobe is fine."
        mc.name "With that decided now we need to think about your bras."
    if Person.rank_tits(the_person.tits) > the_person.bra_size:
        mc.name "You will probably want some kind of support for your new breasts."
        if the_person.get_opinion_score("not wearing underwear") > 0:
            the_person "Actually, I don't seem to have any stretch marks from their rapid expansion. I've never been a big fan of underwear anyway."
        elif the_person.get_opinion_score("not wearing underwear") == 0:
            the_person "I suppose so, although I don't seem to have any stretch marks from their rapid expansion."
        else:
            the_person "Yes, I definitely want new bras, but surprisingly I don't seem to have any stretch marks to worry about."
    else:
        mc.name "Do you think you'll even want to wear bras, with tits that are so much smaller?"
        if the_person.get_opinion_score("not wearing underwear") > 0:
            the_person "I don't know, I certainly didn't always wear bras. I kind of miss how free I was back then."
        elif the_person.get_opinion_score("not wearing underwear") == 0:
            the_person "Maybe? I guess I just assumed I should wear bras, I've been doing it so long."
        else:
            the_person "Yes, I definitely want new bras, even if there isn't much to fill them."
    $ the_person.discover_opinion("not wearing underwear")
    "You think about her opinion, but since you are basically buying the clothes you might be able to push her outside of her comfort zone."
    menu:
        "No bras":
            mc.name "I want you to stop wearing bras."
            if the_person.get_opinion_score("not wearing underwear") < 0:
                the_person "I'm not sure I'm comfortable with that."
                if the_person.sluttiness > 50 or the_person.obedience > 150 or the_person.love > 50:
                    mc.name "Don't worry [the_person.title] I'm comfortable with it, and isn't that what really matters?"
                    the_person "I guess you're right. I won't buy any new bras"
                    if bra_count(the_person) == 1:
                        $ the_person.increase_opinion_score("not wearing underwear")
                    $ alterations += bra_removal(the_person)
                else:
                    mc.name "I understand, you're not really ready for that yet."
            elif the_person.get_opinion_score("not wearing underwear") == 0:
                the_person "Ok."
                if bra_count(the_person) == 1:
                    $ the_person.increase_opinion_score("not wearing underwear")
                $ alterations += bra_removal(the_person)
            else:
                if the_person.has_large_tits():
                    the_person "Oh, that sounds exciting, but my tits are so big."
                    mc.name "That's exactly why you should do it. Just imagine them swinging around all day for everyone to see."
                    the_person "That does sound pretty hot. I won't buy any new bras."
                elif the_person.tits in ["A", "AA"]:
                    the_person "That shouldn't be a problem. I hardly have anything to hold in them anyway."
                    mc.name "Exactly, and this way I'll be able to grab a little handful whenever I want."
                    the_person "I like the thought of that. I won't buy any new bras."
                else:
                    the_person "Ok."
                if bra_count(the_person) == 1:
                    $ the_person.increase_opinion_score("not wearing underwear")
                $ alterations += bra_removal(the_person)
        "Less conservative bras" if the_person.sluttiness > 30:
            mc.name "I want you to buy sexier bras."
            if the_person.get_opinion_score("not wearing underwear") == 2:
                the_person "That is something I could probably do, but why don't I just stop wearing them altogether?"
                $ the_person.discover_opinion("not wearing underwear")
                menu:
                    "Yes":
                        mc.name "That would be even better. I guess you don't need to buy any new bras after all."
                        the_person "Yes, [the_person.mc_title]."
                        if bra_count(the_person) == 1:
                            $ the_person.increase_opinion_score("not wearing underwear")
                        $ alterations += bra_removal(the_person)
                    "No":
                        mc.name "No, I like you wearing them, I just want them to be skimpy and sexy."
                        the_person "I'll take a look and see what I can do for you."
            else:
                if the_person.get_opinion_score("lingerie") > 0:
                    the_person "Well I do like having something sexy to show off when I take off my clothes."
                elif the_person.get_opinion_score("lingerie") == 0:
                    the_person "Ok."
                else:
                    the_person "Underwear is underwear, does it really matter what it looks like?"
                    mc.name "It does for me, I love seeing your body highlighted by sexy clothes."
                    the_person "Alright, I'll try to find something more daring while I'm shopping."
            $ the_person.discover_opinion("lingerie")
            if bra_count(the_person) == 1:
                $ the_person.increase_opinion_score("skimpy outfits")
            $ alterations += sexier_bras(the_person)
            if the_person.sluttiness > 50:
                $ alterations += sexier_bras(the_person)
                if the_person.sluttiness > 70:
                    $ alterations += sexier_bras(the_person)
                    if the_person.sluttiness > 90:
                        $ alterations += sexier_bras(the_person)
        "The same bras":
            mc.name "What you already had was nice. Why don't you just get a better fitting for your new body."
            the_person "Yes, that would probably be safest for now."
    if alterations > 10:
        the_person "You'll hardly recognize me with all the changes I'm making to my wardrobe."
        mc.name "I look forward to seeing the new you soon."
    elif alterations > 0 or bra_count(the_person) < 1:
        the_person "I guess I'll look a little different next time you see me."
        mc.name "I'm sure you'll look great in whatever you find."
    else:
        the_person "Thanks for the help, I can't wait to get back to my normal clothes."
        mc.name "Of course, let me know if you ever need more help in the future."
    if the_person.should_wear_uniform() and Person.rank_tits(the_person.tits) -1 > the_person.bra_size:
        "With her problem solved, at least for now, you remember that her situation has forced her out of uniform."
        mc.name "It is understandable that you couldn't get into your uniform today, but it is still a serious violation of company policy."
        mc.name "I'm afraid I'm going to have to punish you for your failure to properly prepare for the day."
        the_person "Oh, right, I understand. Thank you for being so helpful. I'll definitely be in uniform the next time you see me."
        $ the_person.add_infraction(Infraction.out_of_uniform_factory())
    $ the_person.bra_size = Person.rank_tits(the_person.tits)
    $ scene_manager.clear_scene()
    return
