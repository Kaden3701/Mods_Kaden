init 3 python:
    def mansion_threesome_requirement():
        if len(known_people_at_location(mc.location)) > 1:
            return True
        return "Not enough girls around the mansion"

    def mansion_threesome_initialization(self):
        harem_mansion.add_action(self)
        return

    def get_threesome_partners(person, partner_list = []):
        temp_list = []
        for other_person in partner_list:
            if not town_relationships.get_relationship(person, other_person):
                if other_person.home == harem_mansion:
                    town_relationships.begin_relationship(person, other_person)
            if town_relationships.get_relationship(person, other_person):
                temp_relationship = town_relationships.get_relationship(person, other_person).type_b
                temp_list.append([str(other_person.name) + " " + str(other_person.last_name) + " (" + temp_relationship + ")", other_person])
        temp_list.append(["Back", "Back"])
        return temp_list

    mansion_threesome_action = ActionMod("Start threesome", mansion_threesome_requirement, "mansion_threesome_label",
        initialization = mansion_threesome_initialization, menu_tooltip = "Start a threesome with two of your harem members.", category="Home")

label mansion_threesome_label():
    $ scene_manager = Scene()
    "You take a look around your mansion to see which girls are around."
    call screen enhanced_main_choice_display(build_menu_items([get_sorted_people_list(known_people_at_location(mc.location), "Start threesome with...", ["Back"])]))
    $ the_person = _return
    if not the_person == "Back":
        $ scene_manager.add_actor(the_person)
        mc.name "Hey [the_person.title], we should have a threesome."
        the_person "Sounds fun, who do you want to join us?"
        $ the_other_person = menu(get_threesome_partners(the_person, partner_list = (known_people_at_location(mc.location))))
        if not the_other_person == "Back":
            $ relationship = town_relationships.get_relationship(the_person, the_other_person).type_b
            mc.name "[the_other_person.fname]."
            if relationship in ["Mother", "Daughter", "Sister", "Aunt", "Cousin"]:
                if the_person.get_opinion_score("incest") > 0:
                    the_person "Kinky, you know I like hooking up with my [relationship!l]!"
                else:
                    the_person "Seriously? Isn't that a little weird?"
            elif relationship in ["Rival", "Nemesis"]:
                the_person "Really? You know we don't exactly get along right?"
            else:
                the_person "Great, we always have fun together."
            $ scene_manager.add_actor(the_other_person)

            call start_threesome(the_person, the_other_person) from _call_start_threesome_mansion
        else:
            mc.name "Nevermind, I don't know who else to pick."
            the_person "Oh, okay. Well if you change your mind let me know!"
            "She smiles at you and waits to see if you need something else."
    else:
        "None of them interest you enough to do anything right now."
    $ clear_scene()
    return
