init 3 python:
    def electonic_shopping_requirement():
        if mc.business.is_open_for_business():
            return "WORK IN PROGRESS"
        return "Wait for business to open"


    def electonic_shopping_initialization(self):
        electronics_store.add_action(self)
        return

    electonic_shopping_action = ActionMod("Shop for electonics", electonic_shopping_requirement, "electonic_shopping_label", initialization = electonic_shopping_initialization,
        menu_tooltip = "See what is in stock at the electonics store.", category = "Mall")

label electonic_shopping_label():
    "YOU BROWSE THE STORE"
    "SPY CAMERA"
    "WATERPROFF SPY CAMERA"
    "HACK TO ENABLE COMPUTER CAMERA"
    "HACK TO DOWNLOAD PHONE PHOTOS"
    return
