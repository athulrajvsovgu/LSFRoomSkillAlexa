from gettext import gettext as _

WELCOME_MSG = _("Hello! Welcome to LSF Room Service. What can I do for you?")
WELCOME_REMPROMPT_MSG = _("You can say for example, find a free room in building twenty two.")
WELCOME_BACK_MSG = _("WWelcome back. You have a reservation for the room {} from {} till {}.")
HELP_MSG = _("You can tell me your date of birth and I'll take note. You can also just say, 'register my birthday' and I will guide you. Which one would you like to try?")
GOODBYE_MSG = _("Goodbye!")
ERROR_MSG = _("Sorry, I couldn't understand what you said. Can you reformulate?")
ERROR_TIMEZONE_MSG = _("I can't determine your timezone. Please check your device settings and make sure a timezone was selected. After that please reopen the skill and try again!")
RESULT_MSG = _("I have found {} room for you. It is: ")
RESULTS_MSG = _("I have found {} rooms for you. They are: ")
NO_RESULT_MSG = _("Sorry, I couldn't find any rooms.")
RESERVE_MSG = _("Do you want to reserve any rooms?")
YES_RESERVED_MSG = _("Ok. I have reserved the room {} for the specified amount of time.")
NO_RESERVED_MSG = _("Sorry. I could not reserve a room for you.")
TEST_MSG = _("Here are the results. You can reserve a room if needed.")
RESERVE_PROMPT_MSG = _("To reserve a room you can say for example, reserve a room in building twenty nine for two hours.")
TRY_AGAIN = _("Invalid option entry. Do you want to try again?")
INVALID_OPTION = _("Invalid option entry. There are only {} records. You need to enter a value less than or equal to the number of records.")
USER_CANNOT_BOOK = _("But you cannot resever a room. A reservation already exist in your name which expires only by {}.")
CANCEL_RESERVATION = _("Your reservation has been cancelled.")
NO_RESERVATION = _("Sorry, you donot have any reservations.")
ERROR_RESERVATION_CANCEL = _("Your reservation has been cancelled.")