init -1 python:
    def clothing_formatted_title(the_item):
        hexcode = Color(rgb = (the_item.colour[0], the_item.colour[1], the_item.colour[2]))
        formatted_title = "{color=" + hexcode.hexcode + "}" + the_item.name + "{/color}"
        return formatted_title

    def return_underwear(the_item):
        temp_list = []
        for key, list_of_values in mc.stolen_underwear.items():
            if the_item in list_of_values:
                temp_list = list_of_values
                temp_list.remove(the_item)
                del mc.stolen_underwear[key]
                if temp_list:
                    mc.stolen_underwear[key] = []
                    for clothing in temp_list:
                        mc.stolen_underwear[key].append(clothing)
        return

    def plural_display_name(clothing):
        if clothing in shoes_list or socks_list or pants_list or panties_list:
            if clothing not in [thong, tiny_g_string]:
                return True
        return False

    def home_residents():
        residents = []
        for person in [x for x in all_people_in_the_game() if x.home == mc.location]:
            residents.append(person)
        return residents

    def get_existing_rivals(self, person):
        return_list = []
        for relationship in self.get_relationship_type_list(person, types = ["Nemesis", "Rival"]):
            return_list.append(relationship[0])
        return return_list

    def get_existing_rival_count(self, person):
        return __builtin__.len(get_existing_rivals(self, person))

    def get_existing_friends(self, person):
        return_list = []
        for relationship in self.get_relationship_type_list(person, types = ["Friend", "Best Friend"]):
            return_list.append(relationship[0])
        return return_list

    def get_exisiting_friend_count(self, person):
        return __builtin__.len(get_existing_friends(self, person))

    def get_exisiting_family_count(self, person):
        return __builtin__.len(get_family_members(self, person))

    def pregnant_family(person):
        the_mothers = []
        if len(get_family_members(town_relationships, person)) > 0:
            for x in get_family_members(town_relationships, person):
                if x.event_triggers_dict.get("preg_knows", False):
                    if x.event_triggers_dict.get("preg_tits_date", 999) < day-5:
                        the_mothers.append(x)
        return the_mothers

    def pregnant_friends(person):
        the_mothers = []
        if len(get_existing_friends(town_relationships, person)) > 0:
            for x in get_existing_friends(town_relationships, person):
                if x.event_triggers_dict.get("preg_knows", False):
                    if x.event_triggers_dict.get("preg_tits_date", 999) < day-5:
                        the_mothers.append(x)
        return the_mothers

    def pregnant_enemies(person):
        the_mothers = []
        if len(get_existing_rivals(town_relationships, person)) > 0:
            for x in get_existing_rivals(town_relationships, person):
                if x.event_triggers_dict.get("preg_knows", False):
                    if x.event_triggers_dict.get("preg_tits_date", 999) < day-5:
                        the_mothers.append(x)
        return the_mothers

    def pregnant_people(person): #change to body type check?
        the_mothers = []
        if pregnant_family(person):
            the_mothers.extend(pregnant_family(person))
        if pregnant_friends(person):
            the_mothers.extend(pregnant_friends(person))
        if pregnant_enemies(person):
            the_mothers.extend(pregnant_enemies(person))
        return the_mothers
