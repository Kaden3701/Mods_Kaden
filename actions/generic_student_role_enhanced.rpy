init 2 python:
    def student_intern_offer_requirement(the_person):
        if mc.business.college_interns_unlocked and not the_person in mc.business.get_intern_list():
            if the_person in [lily, erica, kaya, emily]:
                return False
            if not mc.business.has_funds(5000):
                return "$5000 scholarship fund"
            if not len(mc.business.get_intern_depts_with_openings()) > 0:
                return "No internship openings"
            if not the_person.location == university:
                return "Talk on campus"
            return True
        return False

    student_intern_offer_action = Action("Offer internship", student_intern_offer_requirement, "student_intern_offer_label",
        menu_tooltip = "Offer this student an internship with your company.")

init 5 python:
    add_label_hijack("normal_start", "activate_student_role_enhancement")
    add_label_hijack("after_load", "activate_student_role_enhancement")

label student_intern_offer_label(the_person):
    $ hated = []
    $ multiplier = 0
    $ the_person.draw_person(position = "sitting")
    "You probably shouldn't just come right out and offer [the_person.title] a $5000 internship, maybe a few questions first."
    mc.name "How is school going [the_person.title]?"
    the_person "It's going really good, I am learning so much."
    if the_person.get_opinion_score("supply work") > 0:
        if the_person.get_opinion_score("supply work") > 1:
            the_person "It is so interesting learning about all the levels of the supply chain and how interconnected everything really is."
        else:
            the_person "We've been practicing cold calls to suppliers and it is so fun playing the person getting the call."
    if the_person.get_opinion_score("HR work") > 0:
        if the_person.get_opinion_score("HR work") > 1:
            the_person "We've been looking at how human resource departments can set the culture of a whole company. It is so cool to think I could have such a big impact."
        else:
            the_person "I'm looking forward to being able to help people with their problems all day."
    if the_person.get_opinion_score("marketing work") > 0:
        if the_person.get_opinion_score("marketing work") > 1:
            the_person "We've been designing ad campaigns, and it is so much fun to really flex my creativity to make people think about a product in a whole new way."
        else:
            the_person "Today we were learning about how much of an impact discounts can have on helping sell a product."
    if the_person.get_opinion_score("production work") > 0:
        if the_person.get_opinion_score("production work") > 1:
            the_person "Learning is great, but I'm so excited to get out there and actually make things with my own hands. I really want to be able to point to something and say I made it."
        else:
            the_person "I'm glad production work is more than sitting at a desk. By the time school is done I'll be ready to stop sitting all day."
    if the_person.get_opinion_score("research work") > 0:
        if the_person.get_opinion_score("research work") > 1:
            the_person "When Professor [nora.last_name] talks about the things she researches I am so excited to get out there and make discoveries of my own."
        else:
            the_person "I'm ready to get out and pursue my own ideas instead of following in the footsteps of my professors."
    mc.name "Wow, that all sounds pretty incredible. I'm glad you are having such a good time in school."
    the_person "Well, to be honest is isn't all great."
    if the_person.get_opinion_score("supply work") < 0:
        the_person "Talking about buying supplies is so boring"
        $ hated.append("supply")
    if the_person.get_opinion_score("HR work") < 0:
        the_person "I'm independant and don't want to have to think about what other people need."
        $ hated.append("HR")
    if the_person.get_opinion_score("marketing work") < 0:
        the_person "I'm never sure what to say when we practice selling things to our classmates."
        $ hated.append("marketing")
    if the_person.get_opinion_score("production work") < 0:
        the_person "I don't really like how physical the production process can be."
        $ hated.append("production")
    if the_person.get_opinion_score("research work") < 0:
        the_person "Recording results of experiments is so boring, and then we repeat them to be safe."
        $ hated.append("research")
    mc.name "Well that is understanding. So you do all that every week?"
    the_person "Pretty much, but if I have to catch up on something I do have my weekends free."
    the_person "Luckily I only have to work during the summer as long as I am careful about how much I spend."
    the_person "Of course that does mean my weekends can be a bit boring, I can't go out partying without a steady income."
    mc.name "That is understandable. You know, if you were willing to sacrifice part of your weekend I might be able to help you afford to have more fun for part of it as well."
    the_person "Really?"
    mc.name "Yeah, I've been working with the university to offer an internship. You'll get some real life work experience and a hefty contribution towards your tuition."
    the_person "That sounds increadible. Is there a catch."
    mc.name "We need you there in the morning and afternoon every Saturday and Sunday, so you'll have to keep your partying from running too late."
    the_person "That's not too bad."
    mc.name "You'll also have to put up with me hanging around, I work most weekends to keep things going."
    the_person "Truly that is a great burden, but I think I'll be able to manage."
    the_person "What would I be doing exactly?"
    "That is a good question. You have five departments at the company but you'll need to find one that she likes and has openings."
    if len(hated) > 0:
        $ multiplier = len(hated)
        while multiplier > 0:
            $ the_dept = hated[multiplier-1]
            $ score = the_person.get_opinion_score("[the_dept] work")
            $ the_person.discover_opinion("[the_dept] work")
            if score == -2:
                "[the_person.title] hates [the_dept] work."
            else:
                "[the_person.title] doesn't like [the_dept] work."
            $ multiplier -=1
    menu:
        "Biology (Research)" if len(mc.business.college_interns_research) < mc.business.max_interns_by_division:
            $ the_dept = "Research"
        "Biology \n{color=#ff0000}{size=18}Research Team Full!{/size}{/color} (disabled)" if len(mc.business.college_interns_research) >= mc.business.max_interns_by_division:
            pass
        "Chemistry (Production)" if len(mc.business.college_interns_production) < mc.business.max_interns_by_division:
            $ the_dept = "Production"
        "Chemistry \n{color=#ff0000}{size=18}Production Team Full!{/size}{/color} (disabled)" if len(mc.business.college_interns_production) >= mc.business.max_interns_by_division:
            pass
        "Graphic Design (Marketing)" if len(mc.business.college_interns_market) < mc.business.max_interns_by_division and mc.business.college_market_interns_unlocked:
            $ the_dept = "Marketing"
        "Graphic Design (Marketing) (disabled)":    #In the future we may have opportunities to recruit interns for these programs.
            pass
        "Psychology (HR)" if len(mc.business.college_interns_HR) < mc.business.max_interns_by_division and mc.business.college_hr_interns_unlocked:
            $ the_dept = "HR"
        "Psychology (HR) (disabled)":
            pass
        "Business (Supply)" if len(mc.business.college_interns_supply) < mc.business.max_interns_by_division and mc.business.college_supply_interns_unlocked:
            $ the_dept = "Supply"
        "Business (Supply) (disabled)":
            pass
        "Never mind":
            $ the_dept = None
    if the_dept:
        mc.name "I've got an opening in the [the_dept] department of my business."
        if the_dept in hated:
            if the_person.get_opinion_score("[the_dept] work") < -1:
                $ multiplier = 2
                the_person "Weren't you listening, I said that I hate [the_dept] work."
            else:
                $ multiplier = 1
                the_person "Weren't you listening, I said that I don't like [the_dept] work."
            menu:
                "Do it for love" if the_person.love > 30+(15*multipler):
                    mc.name "I know, but that is my only opening at the moment. Please, would you do it for me?"
                    the_person "Well... okay, but only because I love you so much."
                    the_person "To be honest I am pretty excited about working with you, even if it means I have to do [the_dept] work."
                "Obey me" if the_person.obedience > 130+(15*multipler):
                    mc.name "Sorry, I misspoke. You are going to work in the [the_dept] department. This isn't a request."
                    the_person "Yes [the_person.mc_title]!"
                    mc.name "That's a good girl."
                    the_person "Of course, anything for you."
                "Do it for money" if mc.business.has_funds(5000*(1+multipler)):
                    mc.name "I know, but sadly that is all I have available at the moment."
                    mc.name "I know it isn't ideal, but would you be willing to do this if I gave you some extra money?"
                    if multiplier == 1:
                        the_person "Okay, but it is going to cost you another $5,000."
                    else:
                        the_person "Really... I guess if you were willing to give me extra $10,000 I would be able to deal with it."
                    menu:
                        "Okay":
                            mc.name "I can make that happen. Let me just wire you the extra money now."
                            "You pull out your phone and get the money transferred, she takes out hers to verify."
                            $ mc.business.change_funds(-5000*multipler)
                            the_person "Looks good."
                        "Never mind":
                            $ the_dept = None
                "Never mind":
                    $ the_dept = None
        else:
            $ the_person.discover_opinion("[the_dept] work")
            if the_person.get_opinion_score("[the_dept] work") < 1:
                the_person "Okay, that's fine."
            elif the_person.get_opinion_score("[the_dept] work") < 2:
                the_person "Great! That sounds like it could be fun."
            else:
                the_person "Really? That is awesome! It is exactly what I was hoping for."
    if the_dept:
        mc.name "Great, I'll get the paperwork all taken care of and then see you this weekend."
        $ mc.business.hire_college_intern(the_person, the_dept, add_to_location = False)
        $ mc.business.change_funds(-5000)
    else:
        mc.name "Sorry, this isn't going to work. I don't have anything that you will be happy with right now."
        the_person "Oh, well alright. I guess let me know if something changes."
    $ del score
    $ del multiplier
    $ del hated
    $ del the_dept
    $ clear_scene()
    return

label activate_student_role_enhancement(stack):
    python:
        generic_student_role.add_action(student_intern_offer_action)
        execute_hijack_call(stack)
    return
