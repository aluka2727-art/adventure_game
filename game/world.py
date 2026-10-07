# All player-facing text from the original game. Do not rewrite these strings.

WOODEN_SWORD = "wooden sword"

UNRECOGNIZED = "Input not recognized, try again."

DEV_CHEAT_DEATH = "DEV CHEAT:\n{GAME OVER}"

READY_PROMPT = "Are you ready for an adventure?(yes/no)"
READY_YES = "Let the adventure begin!\n\n"
READY_NO = "Let me ask you again."

WAKE_UP = "You wake up in an empty dark room.\nThere are two doors in front of you."
DOOR_PROMPT = "Would you like to open the left or right door?(left/right)"
DOOR_RIGHT = "You open the door cautiously, revealing another room.\nIt is empty.\n Let's check the other door now."
DOOR_MIDDLE = "You bump into the wall."

DINO_INTRO = "You open the door slowly, revealing another room.\nIn the middle of the room, a red dinosaur-like creature is sound asleep.\nAt the other end of the room, there is another door."
DINO_PROMPT = "Fight the creature or sneak past it to the other door?(fight/sneak)"

FIGHT_START = "You see a wooden sword against the wall.\nYou run to the sword, your footsteps waking the creature.\nThere's no going back now!"
FIGHT_PROMPT = "(attack/surrender)"
FIGHT_SURRENDER = "You put two hands up in fear, but the creature roars!\nWith one mighty chomp, it eats you alive!\n{GAME OVER}"
FIGHT_FIRST_ATTACK = "You raise your sword up high.\nYou swing with all your might at the creature, but it just seems mildly annoyed."
FIGHT_AGAIN_PROMPT = "Attack again or run?(attack/run)"
FIGHT_RUN = 'You point behind the creature, asking, "what\'s that?"\nThe creature looks behind him, confused.\nAs the creature is distracted, you make a run for the next door and shut it tight behind you.'
FIGHT_SWORD_BREAKS = "You raise your sword up even higher.\nThe creature quickly grabs your sword and snaps it in half!"
FIGHT_UNARMED = "You try to fight without a weapon, but the creature overpowers you!\n{GAME OVER}"

SNEAK_START = "You quietly slip past the creature, but it suddenly wakes up!\nYou have no choice but to fight it!"
SNEAK_PROMPT = "(attack/mercy)"
SNEAK_MERCY = "You beg for mercy, but the creature just stares blankly.\nYou make a run for the next door and shut it tight behind you."

TTT_INTRO = "\n\nThe next room is identical to the last one, except instead of a creature, a tic-tac-toe board sits in the middle of them room."
TTT_PROMPT = "Examine the board or continue through the next door?(examine/continue)"
TTT_EXAMINE = "Upon closer inspection, the tic-tac-toe board seems like it's glowing."
TTT_CONTINUE = "You walk over to the door.\nAs you turn the knob, you realize the door is locked.\nYou hear a disembodied voice behind you.\nThe board is starting to brightly glow.\nVOICE: ...You can only pass if you beat me in one game of tic-tac-toe..."
TTT_PLAY_PROMPT = "(play/resign)"
TTT_LOSSES = [
    "You start playing, but the voice's skill is unmatched.\nYou lose!\nPlay again or admit your defeat?",
    "You start playing, but the voice cheats!\nYou lose!\nPlay again or admit your defeat?",
    "You start playing, but the game ends in a tie.\nVOICE: ...That doesn't count...\nYou lose!\nPlay again or admit your defeat?",
]
TTT_WIN_CHANCE = 0.05
TTT_WIN = "You start playing, and against all odds... you win."
TTT_RESIGN = "The door unlocks.\nVOICE: ...Wha-HEY! GET BACK HERE! WAIT!...\nYou walk into the next room, shutting the door tight behind you.\n\n"

APPLE = "apple"
VEND_INTRO = "This room is almost empty, except for a vending machine humming in the dark.\nIts display flickers: PRESS BUTTON... GET SNACK...\nA single apple sits behind the glass, glowing faintly."
VEND_PROMPT = "Press the button, kick the machine, or leave through the next door?(press/kick/leave)"
VEND_PRESS = "You press the button.\nThe machine gurgles, then an apple thuds into the tray.\nYou take it. The display now reads: THANK YOU FOR YOUR SOUL :)"
VEND_PRESS_AGAIN = "You press the button again.\nThe machine wheezes. Nothing comes out.\nThe display reads: YOU ALREADY PAID."
VEND_KICK_LIVE = "You kick the machine.\nIt rocks forward, then slams back into place.\nA low voice from inside whispers: ...don't."
VEND_KICK_DIE = "You kick the machine.\nIt rocks... and keeps rocking.\nThe whole thing tips over and crushes you.\nThe last thing you see is the display: HAVE A NICE DAY.\n{GAME OVER}"
VEND_KICK_DEATH_CHANCE = 0.25
VEND_LEAVE = "You walk past the machine toward the next door.\nIt beeps once, sadly, like it wanted a tip."

EATING_INTRO = "The next room is a small dining room.\nThere is a table with a chair in the middle of the room."
EATING_PROMPT = "Sit on the chair or examine the table?(sit/examine)"
EATING_SIT = "You sit on the chair.\nYou feel a little tickle on your rear end.\nYou immediately stand up."
EATING_SIT_AGAIN = "You sit on the chair again.\nYou hear a faint voice from the chair.\nVOICE: ...Don't sit on me...\nYou immediately stand up."
EATING_EXAMINE = "You examine the table.\nIt is made of wood and has a little bit of ketchup on it."
EATING_EXAMINE_AGAIN = "You examine the table again.\nUpon close inspection, the ketchup is actually a strawberry jam."
EATING_EXAMINE_AGAIN_AGAIN = "You examine the table again.\nUpon close inspection, the strawberry jam is actually a bloodstain."

VOID_INTRO = "You touch the bloodstain and it starts to glow faintly.\nThe bloodstain opens up into the void.\nVOID: ...Feed me..."
VOID_PROMPT = "Feed the void or leave?(feed/leave)"
VOID_FEED_SWORD = "You look in your pocket and pull out your wooden sword.\nYou throw the sword into the void.\nThe void regurgitates the sword back to you.\nVOID: ...No wood, I'm vegan..."
VOID_FEED_APPLE = "You look in your pocket and pull out an apple.\nYou throw the apple into the void.\nThe void seems to be satisfied."
VOID_FEED_NOTHING = "You look in your pocket, but it's empty.\nVOID: ...I'm still hungry..."
VOID_FEED_APPLE_NOTHING = "You look in your pocket, but you already fed the apple to the void.\nVOID: ...I'm full..."
VOID_LEAVE_LIVE = "You walk past the void and continue to the next room.\nThe void seems to be satisfied."
VOID_LEAVE_DIE = "You try to leave the void, but it grabs you and pulls you into it.\nYou are now part of the void.\n{GAME OVER}"

TTT_REAL_BOOK_TITLE = "How to Win at Tic-Tac-Toe"
TTT_BOSS_CHEAT_CODE = "three in a row"

LIBRARY_INTRO = "\n\nYou enter a vast library.\nEvery shelf stretches into darkness.\nWhispers say every book here is nonsense... except maybe one."
LIBRARY_PROMPT = "Search the shelf, read a book, or try the next door?(search/read/door)"
LIBRARY_SEARCH_HEADER = "Titles on this shelf (by number):"
LIBRARY_BOOK_COUNT = 12
LIBRARY_READ_WHICH = "Which book?(number or exact title)"
LIBRARY_READ_GIBBERISH_HEADER = "Page {page} of 10:"
LIBRARY_PAGE_PROMPT = "(next/close)"
LIBRARY_REAL_PAGE_PROMPT = "(next/close)"
LIBRARY_TTT_BOOK_PAGES = [
    "Page 1: Always let your opponent go first. They feel confident. You feel nothing.",
    "Page 2: The center square is powerful, unless the voice cheats. Then it is decorative.",
    "Page 3: Corners are safe. Unless they are not. This book is not responsible for outcomes.",
    "Page 4: If you see two in a row, block it. Unless the board is lying. Boards lie here.",
    "Page 5: Forks win games. Forks also win arguments. Carry a fork metaphorically.",
    "Page 6: Never play for a tie against a disembodied voice. Ties are lies.",
    "Page 7: Resigning unlocks doors sometimes. The voice hates that trick.",
    "Page 8: The voice cannot stand being outsmarted by reading material.",
    "Page 9: Advanced strategy: do not play fair. The voice never does.",
    "Page 10: HOW TO CHEAT: When the voice challenges you again, do not press play.\nType the secret phrase exactly:\nthree in a row\nThe voice will panic.\nYou will win.\nProbably.",
]

LIBRARY_DOOR_OPEN = "The door unlocks with a glow.\nYou step through."

BOSS1_INTRO = "\n\nThe voice returns, louder than before.\nThe tic-tac-toe board covers the entire wall.\nVOICE: ...Rematch. No running. No tom foolery. Play..."
BOSS1_INTRO_TTT_WON = "VOICE: ...You beat me once. That didn't count. This time I am serious..."
BOSS1_PROMPT = "(play/resign)"
BOSS1_LOSSES = [
    "You play. The voice moves before you finish thinking.\nYou lose!\nVOICE: ...Still bad...",
    "You play. The board rearranges itself.\nYou lose!\nVOICE: ...I didn't cheat. The board cheated for me...",
    "You play. It is a tie.\nVOICE: ...That doesn't count...\nYou lose anyway.",
]

BOSS1_MAX_LOSSES = 5
BOSS1_TOO_MANY_LOSSES = "You play again.\nThe voice is done humoring you.\nThe board flashes red.\nVOICE: ...Five strikes. You're out...\nThe walls close in.\n{GAME OVER}"
BOSS1_RESIGN_END = "You resign.\nVOICE: ...Good. Stay a loser forever...\n{GAME OVER}"
BOSS1_CHEAT_UNKNOWN = "You shout a phrase, but it sounds made up.\nVOICE: ...Nice try. Play for real..."
BOSS1_CHEAT_WIN = "You whisper the phrase from page ten.\nThe board flickers.\nVOICE: ...WHERE DID YOU— THAT'S NOT—...\nThe wall cracks.\nLight pours in."
BOSS1_FINISHED = "CONGRATULATIONS!\nYOU HAVE BEATEN THE FIRST BOSS!\n(continue)"



WORLD_2_INTRO = "\n\nYou step through the crack in the wall and find yourself outside.\nYour eyes adjust to the bright light and you see a large forest ahead of you."
WORLD_2_PROMPT = "Head into the forest or go back through the crack in the wall?(forest/back)"
WORLD_2_BACK = "You go back through the crack in the wall and find yourself back in the small dining room.\nOn the table, there is an apple glowing faintly.\nYou pick it up and put it in your pocket.\nAs you step out of the crack, you think you hear a faint voice in your head asking to be fed.\nYou continue into the forest."
WORLD_2_BACK_PROMPT = "(continue)"

FOREST_INTRO = "You head into the forest.\nThe trees are tall and the leaves are dense.\nYou can hear the sound of birds chirping in the distance."
FOREST_PROMPT = "Explore the forest or go along the path?(explore/path)"
FOREST_EXPLORE = [
    "You explore the forest.\nYou see a bear in the distance.",
    "You explore the forest.\nYou hear a noise in the distance.\nIt sounds like the voice from the void.",
    "You explore the forest.\nYou see a large tree in the distance.",
]
FOREST_EXPLORE_DEATH = "You explore the forest.\nYou fall into a hole.\nYou are now stuck in the hole.\n{GAME OVER}"
FOREST_PATH = "You go along the path.\nYou see a large tree in the distance.\nYou walk towards the tree.\nYou reach the tree and see a door in it."
FOREST_PATH_PROMPT = "Enter the tree or continue along the path?(enter/continue)"
FOREST_PATH_CONTINUE = [
    "You continue along the path.\nThe forest gets darker and darker.\nYou are scared.",
    "You continue along the path.\nYou hear a noise in the distance.\nYou are scared.",
    "You continue along the path.\nThe path gets narrower and narrower.\nYou are scared.",
]
FOREST_PATH_CONTINUE_PROMPT = "Continue along the path?(continue)"
FOREST_PATH_DEATH = "You continue along the path.\nThe forest gets darker and darker.\nThe path disappears.\nYour vision fades to black.\nYou are now part of the forest.\n{GAME OVER}"

TREEHOUSE_INTRO = "You open the door and enter the tree.\nThe inside of the tree is a small room with a small, pretty fairy pacing back and forth in the middle of the room."
TREEHOUSE_PROMPT = "Talk to the fairy or examine the room?(talk/examine)"
TREEHOUSE_TALK = "You talk to the fairy.\nFAIRY: ...Don't talk to me..."
TREEHOUSE_TALK_AGAIN = "You talk to the fairy again.\nFAIRY: ...Didn't I tell you not to talk to me?..."
TREEHOUSE_TALK_AGAIN_AGAIN = "You talk to the fairy again.\nFAIRY: ...Fine. Since you won't stop trying to talk to me, I guess you could help me out..."
TREEHOUSE_EXAMINE = [
    "You examine the room.\nYou see a small table with mushrooms in a basket on it.\nThis is probably what the fairy eats.",
    "You examine the room.\nAgainst the wall, there is a large bookshelf with a lot of books on it.\nThe books are all written in a language you've never seen before, but they look like fantasy romances.",
    "You examine the room.\nIn a corner, there is a small bed with a blanket on it.\nThe blanket is made of a soft, warm fabric.",
    "You examine the room.\nOn the wall, there is a poster depicting a large bear.\nThe text is written in a language you've never seen before.",
]
TREEHOUSE_FAIRY_PROBLEM_PROMPT = "Ask the fairy what's wrong??(ask/leave)"
TREEHOUSE_FAIRY_PROBLEM_ASK = "You ask the fairy what's wrong.\nFAIRY: ...I'm stuck in this tree. Could you open the door for me?..."
TREEHOUSE_FAIRY_PROBLEM_LEAVE = "You leave the fairy. It gets mad.\nFAIRY: ...You want to talk to me so much, but now you want to leave? Not going to happen...\nWith a snap of her fingers, she deletes you.\n{GAME OVER}"
TREEHOUSE_FAIRY_HELP_PROMPT = "Help the fairy or leave?(help/leave)"
TREEHOUSE_FAIRY_HELP_HELP = "You help the fairy.\nFAIRY: ...Thank you! I'm so glad you're here! To thank you, I'll show you the way out of this forest..."
TREEHOUSE_FAIRY_HELP_LEAVE = "You leave the fairy. It gets mad.\nFAIRY: ...You want to help me so much, but now you want to leave? Not going to happen...\nWith a snap of her fingers, she deletes you.\n{GAME OVER}"

FAIRY_FOLLOW_PROMPT = "Follow the fairy or leave?(follow/leave)"
FAIRY_FOLLOW_FOLLOW = "You follow the fairy.\nFAIRY: ...And another right turn..."
FAIRYFOLLOW_AGAIN_PROMPT = "Keep following the fairy or leave?(follow/leave)"
FAIRY_FOLLOW_FOLLOW_AGAIN = "You keep following the fairy.\nFAIRY: ...We're almost there..."
FAIRY_FOLLOW_FOLLOW_AGAIN_AGAIN = "You keep following the fairy.\nThe fairy leads you to a small clearing in the forest.\nFAIRY: ...There's the door!...\nFAIRY: ...TO HELL...\nThe fairy turns into a demon and charges at you."
FAIRY_FOLLOW_LEAVE = "You think the fairy is a bit suspicious, so you leave. \nFAIRY: ...Okay then, goodbye..."

DEMON_BATTLE_PROMPT = "Fight the demon or run?(fight/run)"
DEMON_BATTLE_FIGHT_SWORD = "You pull out the wooden sword from earlier and charge at the demon.\nThe demon pulls out his own sword and charges at you."
DEMON_BATTLE_FIGHT_NO_SWORD = "You look around for a weapon, and you find a sturdy stick.\nYou charge at the demon with the stick.\nThe demon pulls out his own sword and charges at you."
DEMON_BATTLE_RUN = "You turn and run away from the demon.\nThe demon chases you through the forest.\nYou hear the demon's laughter in the distance."

DEMON_BATTLE_DEFEND_PROMPT = "Defend yourself or run?(defend/run)"
DEMON_BATTLE_DEFEND_BLOCK = "You raise your weapon to defend yourself.\nThe demon swings his sword at you.\nYou block the sword with your weapon."
DEMON_BATTLE_DEFEND_BLOCK_FAIL = "You raise your weapon to defend yourself.\nThe demon swings his sword at you.\nYou fail to block the sword and it breaks."

DEMON_BATTLE_ATTACK_AGAIN_PROMPT = "Attack the demon back or run?(attack/run)"
DEMON_BATTLE_ATTACK_AGAIN_SUCCES_WOODEN_SWORD = "You attack the demon back.\nThe demon becomes tired and starts to run away. With one swift swing, you cut the demon in half.\nThe demon disappears into a puff of smoke.\nThe demon's sword floats into your hand, merging with your wooden sword."
DEMON_BATTLE_ATTACK_AGAIN_SUCCES_STICK = "You attack the demon back.\nThe demon becomes tired and starts to run away. With one swift swing, you cut the demon in half.\nThe demon disappears into a puff of smoke.\nThe demon's sword floats into your hand, replacing your stick."
DEMON_BATTLE_ATTACK_AGAIN_DEATH = "You attack the demon back.\nThe demon is done playing around and charges at you.\nYou are now dead.\n{GAME OVER}"
DEMON_BATTLE_ATTACK_AGAIN_WEAPONLESS = "You try to fight without a weapon, but the demon overpowers you!\n{GAME OVER}"

FOREST_END_PROMPT = "Continue? (continue)"