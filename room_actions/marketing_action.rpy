init 3 python:
    def weekly_redesign_requirement():
        if mc.business.is_open_for_business():
            if mc.business.event_triggers_dict.get("weekly_redesign", -7) < day - 7:
                if mc.business.funds > 500:
                    return True
                return "Requires $500"
            return "Only once per week"
        return "Wait for business to open"

    def weekly_distraction_requirement():
        if mc.business.is_open_for_business():
            if mc.business.event_triggers_dict.get("weekly_distraction", -7) < day - 7:
                return True
            return "Only once per week"
        return "Wait for business to open"

    def weekly_redesign_function():
        mc.business.attention -= __builtin__.int((3*mc.charisma) + (mc.focus) + (2*mc.market_skill))
        mc.business.change_funds(-500)
        mc.business.event_triggers_dict["weekly_redesign"] = day
        return

    def weekly_distraction_function():
        mc.business.attention -= __builtin__.int((3*mc.charisma) + (mc.focus) + (2*mc.int))
        mc.business.event_triggers_dict["weekly_distraction"] = day
        return

    def weekly_redesign_initialization(self):
        m_division.add_action(self)
        return

    def weekly_distraction_initialization(self):
        m_division.add_action(self)
        return

    weekly_redesign_action = ActionMod("Redesign logo {image=gui/heart/Time_Advance.png}\n{color=#ff0000}{size=18}Costs: $500{/size}{/color}", weekly_redesign_requirement, "weekly_redesign_label", initialization = weekly_redesign_initialization,
        menu_tooltip = "Spend time redesigning your packaging to confuse regulators.", category = "Business Action")
    weekly_distraction_action = ActionMod("Distract regulators {image=gui/heart/Time_Advance.png}", weekly_distraction_requirement, "weekly_distraction_label", initialization = weekly_distraction_initialization,
        menu_tooltip = "Call in false complaints about a competitor so regulators are too busy to bother you.", category = "Business Action")

label weekly_redesign_label():
    "Looking at the recent sales reports in the marketing department have you a bit concerned."
    if mc.business.attention > mc.business.max_attention:
        "You've been getting a lot of attention lately and it's a little surprising the regulators haven't been here yet."
    elif mc.business.attention > mc.business.max_attention*0.75:
        "You have a ton of attention at the moment. It is so bad that your next sale could be the one that draws the regulators ire."
    elif mc.business.attention > mc.business.max_attention*0.5:
        "You have a bit of attention at the moment, and if you want to keep selling serums you probably need to do something about it."
    else:
        "You thankfully don't really have any attention at the moment, but you could still decrease it for safety before your next sale."
    "The unique packaging that signifies [b_name] products has helped you grow brand recognition, but in this situation that can be a double edged sword."
    "If you were to work on a redesign of the logo it might dilute the regulators focus if the products don't look connected."
    "Since you slap on labels as part of the production process it shouldn't be too hard to get some new ones printed out, but it will be a bit expensive."
    menu:
        "Contine\n{color=#ff0000}{size=18}Costs: $500{/size}{/color}":
            "It's worth it."
            "You get to work and after a bit of time you have something you are happy with."
            "You send the files to the industrial printer in the production department along with an email to alert them about the new packaging."
            $ weekly_redesign_function()
            call advance_time from _call_advance_time_attention_drop
        "Never mind":
            "Actually, maybe it isn't worth it. You'll have to reconsider."
    return

label weekly_distraction_label():
    "Looking at the recent sales reports in the marketing department have you a bit concerned."
    if mc.business.attention > mc.business.max_attention:
        "You've been getting a lot of attention lately and it's a little surprising the regulators haven't been here yet."
    elif mc.business.attention > mc.business.max_attention*0.75:
        "You have a ton of attention at the moment. It is so bad that your next sale could be the one that draws the regulators ire."
    elif mc.business.attention > mc.business.max_attention*0.5:
        "You have a bit of attention at the moment, and if you want to keep selling serums you probably need to do something about it."
    else:
        "You thankfully don't really have any attention at the moment, but you could still decrease it for safety before your next sale."
    "You've been capturing more and more market share from your competitors, but that can be a double edged sword."
    "As one of the leading companies in your industry you have more customers, but also draw more attention."
    "If you were to point the regulators towards one of your competitors they might be distracted enough to give you some breathing room."
    "You settle on a target, break out a few fake accents and get to work calling in complaints about their products."
    "By the time you are wrapping up your last call the agent on the other line assures you that they will send an investigator to check on them."
    $ weekly_distraction_function()
    call advance_time from _call_advance_time_attention_drop2
    return
