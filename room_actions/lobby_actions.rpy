init 3 python:
    def daily_insult_requirement():
        if mc.business.is_open_for_business() and mc.business.get_employee_count() > 0:
            if mc.business.event_triggers_dict.get("daily_insult_employees", 0) < day:
                if count_employees_talk() > 0:
                    return True
                return "Already spoke with everyone"
            return "Only once per day"
        return False

    def daily_compliment_requirement():
        if mc.business.is_open_for_business() and mc.business.get_employee_count() > 0:
            if mc.business.event_triggers_dict.get("daily_compliment_employees", 0) < day:
                if count_employees_talk() > 0:
                    return True
                return "Already spoke with everyone"
            return "Only once per day"
        return False

    def count_employees_talk():
        count = 0
        for person in [x for x in mc.business.get_employee_list() if x.event_triggers_dict.get("day_last_employee_interaction", 0) < day]:
            count +=1
        return count

    def daily_insult_update_employee_stats():
        for person in [x for x in mc.business.get_employee_list() if x.event_triggers_dict.get("day_last_employee_interaction", 0) < day]:
            person.event_triggers_dict["day_last_employee_interaction"] = day
            person.change_obedience(mc.charisma)
            person.change_happiness(-5)
            person.change_love(-2)
        mc.business.event_triggers_dict["daily_talk_employees"] = day
        return

    def daily_compliment_update_employee_stats():
        for person in [x for x in mc.business.get_employee_list() if x.event_triggers_dict.get("day_last_employee_interaction", 0) < day]:
            person.event_triggers_dict["day_last_employee_interaction"] = day
            person.change_love(1)
            person.change_happiness(mc.charisma)
        mc.business.event_triggers_dict["daily_compliment_employees"] = day
        return

    def daily_insult_efficiency_initialization(self):
        lobby.add_action(self)
        return

    def daily_compliment_efficiency_initialization(self):
        lobby.add_action(self)
        return

    def company_breakfast_requirement():
        if mc.business.is_open_for_business() and mc.business.get_employee_count() > 0:
            if time_of_day == 1:
                if mc.business.event_triggers_dict.get("company_breakfast_employees", 0) < day:
                    if mc.business.funds > (10*mc.business.get_employee_count()):
                        return True
                    return "Requires more funds"
                return "Only once per week"
            return "Only in the morning"
        return "Business not open"

    def company_breakfast_initialization(self):
        lobby.add_action(self)
        return

    def company_lunch_requirement():
        if mc.business.is_open_for_business() and mc.business.get_employee_count() > 0:
            if time_of_day == 2:
                if mc.business.event_triggers_dict.get("company_lunch_employees", 0) < day:
                    if mc.business.funds > (10*mc.business.get_employee_count()):
                        return True
                    return "Requires more funds"
                return "Only once per week"
            return "Only in the afternoon"
        return "Business not open"

    def company_lunch_initialization(self):
        lobby.add_action(self)
        return

    def company_lunch_performance(meal_value = 0):
        count = 0
        number = 1
        for person in [x for x in mc.business.get_employee_list()]:
            count += 1
            if person in mc.business.research_team:
                ability = person.research_skill
                if renpy.random.randint(0,(ability)) == 0:
                    person.research_skill += 1
                    mc.log_event((person.title or person.name) + ": +" + str(number) + " Research Skill", "float_text_grey")
            elif person in mc.business.market_team:
                ability = person.market_skill
                if renpy.random.randint(0,(ability)) == 0:
                    person.market_skill += 1
                    mc.log_event((person.title or person.name) + ": +" + str(number) + " Market Skill", "float_text_grey")
            elif person in mc.business.supply_team:
                ability = person.supply_skill
                if renpy.random.randint(0,(ability)) == 0:
                    person.supply_skill += 1
                    mc.log_event((person.title or person.name) + ": +" + str(number) + " Supply Skill", "float_text_grey")
            elif person in mc.business.production_team:
                ability = person.production_skill
                if renpy.random.randint(0,(ability)) == 0:
                    person.production_skill += 1
                    mc.log_event((person.title or person.name) + ": +" + str(number) + " Production Skill", "float_text_grey")
            elif person in mc.business.hr_team:
                ability = person.hr_skill
                if renpy.random.randint(0,(ability)) == 0:
                    person.hr_skill += 1
                    mc.log_event((person.title or person.name) + ": +" + str(number) + " HR Skill", "float_text_grey")
            person.change_love(meal_value-4)
            person.change_happiness(meal_value-5)
        return count

    def company_lunch_slut(meal_value = 0):
        count = 0
        for person in [x for x in mc.business.get_employee_list()]:
            count += 1
            person.change_slut_temp(mc.charisma*2)
            person.change_love(meal_value-4)
            person.change_happiness(meal_value-5)
        return count

    def company_lunch_obey(meal_value = 0):
        count = 0
        for person in [x for x in mc.business.get_employee_list()]:
            count += 1
            person.change_obedience(mc.charisma)
            person.change_love(meal_value-4)
            person.change_happiness(meal_value-5)
        return count

    def company_lunch_love(meal_value = 0):
        count = 0
        for person in [x for x in mc.business.get_employee_list()]:
            count += 1
            person.change_love(2)
            person.change_happiness(meal_value)
        return count

    def company_serum_requirement():
        if mandatory_paid_serum_testing_policy.is_active():
            if mc.business.is_open_for_business() and mc.business.get_employee_count() > 0:
                return True
            return "Business not open"
        return "Serum testing inactive"

    def company_serum_initialization(self):
        lobby.add_action(self)
        return

    def company_serum_dose(the_serum):
        for person in mc.business.get_employee_list():
            if person.is_at_office():
                person.give_serum(copy.copy(the_serum), add_to_log = False)
        return

    daily_insult_efficiency_action = ActionMod("Insult all employees", daily_insult_requirement, "daily_insult_efficiency_employees", initialization = daily_insult_efficiency_initialization,
        menu_tooltip = "Insult workers at the cost of 1 efficiency per employee.", category = "Business Action")
    daily_compliment_efficiency_action = ActionMod("Compliment all employees", daily_compliment_requirement, "daily_compliment_efficiency_employees", initialization = daily_compliment_efficiency_initialization,
        menu_tooltip = "Compliment workers at the cost of 1 efficiency per employee.", category = "Business Action")
    company_breakfast_action = ActionMod("Buy the company breakfast {image=gui/heart/Time_Advance.png}", company_breakfast_requirement, "company_breakfast", initialization = company_breakfast_initialization,
        menu_tooltip = "Bring in breakfast for the company and gain a chance to influence your employees.", category = "Business Action")
    company_lunch_action = ActionMod("Buy the company lunch {image=gui/heart/Time_Advance.png}", company_lunch_requirement, "company_lunch", initialization = company_lunch_initialization,
        menu_tooltip = "Have lunch catered for the company and gain a chance to influence your employees.", category = "Business Action")
    company_serum_action = ActionMod("Give all employees serum", company_serum_requirement, "company_serum", initialization = company_serum_initialization,
        menu_tooltip = "Give the entire staff a dose of the same serum.", category = "Business Action")

label daily_insult_efficiency_employees():
    $ count = count_employees_talk()
    "Things have not been running as smoothly as you would like, and it is time to crack the whip."
    "Before settling down to work you send off an email asking each of your [count] employees to stop by today for a quick chat."
    "While this won't take much out of your day it will hinder their effectiveness somewhat."
    "It is also going to upset them, although the obedience gain should be worth it."
    $ daily_insult_update_employee_stats()
    $ mc.business.change_team_effectiveness(-count)
    return

label company_serum():
    $ count = len(mc.business.get_employee_list())
    $ money = count*100
    "You currently have [count] employees, that means to give them each a dose of serum you will need to have [count] doses in the production department."
    if not mandatory_unpaid_serum_testing_policy.is_active():
        "Unfortunately this is also going to cost you $[money] to accomplish."
        menu:
            "Proceed" if mc.business.funds > money:
                $ mc.business.change_funds(-money)
                "That is a small price to pay for what you can accomplish with the serums, so you decide to proceed."
            "Nevermind":
                "That is a bit pricey, so on second thought you decide to be a bit more selective and hand out individual doses instead."
                return
    $ finished = False
    "You just need to pick a serum for them to take."
    while not finished:
        "You quickly remind yourself you need at least [count]."
        call screen serum_inventory_select_ui(mc.business.inventory)
        if not _return == "None":
            $ the_serum = _return
            if mc.business.inventory.get_serum_count(the_serum) >= count:
                "After double checking the inventory you set aside [count] doses to be used by the staff."
                $ mc.business.inventory.change_serum(the_serum, -count)
                $ finished = True
            elif mc.business.inventory.get_serum_count(the_serum) < count:
                "Unfortunately you don't have enough of that serum to use."
        else:
            $ the_serum = None
            "You decide not to give a serum out after all."
            return
    "Before settling down to work you send off an email asking each of your [count] employees to swing by production for a special dose of serum."
    $ company_serum_dose(the_serum)
    return

label daily_compliment_efficiency_employees():
    $ count = count_employees_talk()
    "Things have been going great, and it is about time that you recognize your employees."
    "Before settling down to work you send off an email asking each of your [count] employees to stop by today for a quick chat."
    "While this won't take much our of your day it will hinder their effectiveness somewhat."
    "They should be thrilled to hear from you."
    $ daily_compliment_update_employee_stats()
    $ mc.business.change_team_effectiveness(-count)
    return

label company_breakfast():
    $ department = all
    $ goal = None
    $ count = mc.business.get_employee_count()
    $ meal_value = 1
    "To help get the day off to the right start you decide to pick up breakfast for the company."
    if count < 10:
        "There are only [count] employees, feeding them shouldn't be a problem."
    elif count > 10:
        "You currently have [count] employees, feeding all of them could be expensive."
    "You pick up some assorted pastries and coffee."
    "Now you just need a plan for what you want to improve about your employees."
    menu:
        "Performance":
            "Work is the reason they are here, it would be nice if they were a bit better at their jobs. Although learning can be boring."
            $ count = company_lunch_performance(meal_value)
        "Sluttiness":
            "They could stand to be more free spirited. Although you'll have to push boundaries."
            $ count = company_lunch_slut(meal_value)
        "Obedience":
            "They could stand to be more obedient. Although you'll have to be mean."
            $ count = company_lunch_obey(meal_value)
        "Love":
            "They are already making you happy, and deserve to be happy in turn. They will appreciate the attention."
            $ count = company_lunch_love(meal_value)
    $ mc.business.change_funds(count*meal_value*-10)
    $ mc.business.event_triggers_dict["company_breakfast_employees"] = (day + 6)
    call advance_time from company_breakfast_advance
    return

label company_lunch():
    $ department = all
    $ goal = None
    $ count = mc.business.get_employee_count()
    $ meal_value = 1
    "You think that the company could use a catered lunch to reward them for their hard work."
    if count < 10:
        "There are only [count] employees, feeding them shouldn't be a problem."
    elif count > 10:
        "You currently have [count] employees, feeding all of them could be expensive."
    "There are a wide range of options for food. It all comes down to how much you want to pay, and how happy you want your employees to be."
    menu:
        "Pizza\n{color=#ff0000}{size=18}Costs: $10/each{/size}{/color}" if mc.business.funds > (10*count):
            "Free food is always good, surely they will be happy with something simple like pizza."
        "Sandwiches and sides\n{color=#ff0000}{size=18}Costs: $30/each{/size}{/color}" if mc.business.funds > (30*count):
            "Sandwiches are a good middle of the road option. Throw in some side dishes and they will be happy, right?"
            $ meal_value = 3
        "Lobster\n{color=#ff0000}{size=18}Costs: $50/each{/size}{/color}" if mc.business.funds > (50*count):
            "Only the best for your employees, money doesn't matter. This will make everyone happy."
            $ meal_value = 5
    "Now you just need a plan for what you want to improve about your employees."
    menu:
        "Performance":
            "Work is the reason they are here, it would be nice if they were a bit better at their jobs. Although learning can be boring."
            $ count = company_lunch_performance(meal_value)
        "Sluttiness":
            "They could stand to be more free spirited. Although you'll have to push boundaries."
            $ count = company_lunch_slut(meal_value)
        "Obedience":
            "They could stand to be more obedient. Although you'll have to be mean."
            $ count = company_lunch_obey(meal_value)
        "Love":
            "They are already making you happy, and deserve to be happy in turn. They will appreciate the attention."
            $ count = company_lunch_love(meal_value)
    $ mc.business.change_funds(count*meal_value*-10)
    $ mc.business.event_triggers_dict["company_lunch_employees"] = (day + 6)
    call advance_time from company_lunch_advance
    return
