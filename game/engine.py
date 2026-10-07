"""Turn-based game engine (web API + CLI)."""

import copy
import random
import string
import sys

from game import world

WOODEN_STICK = "wooden stick"
DEMON_SWORD = "demon sword"

ROOM_ORDER = ["ready", "door", "dino", "ttt", "vend", "eat", "library", "boss1", "world2", "forest", "treehouse"]

ROOM_CHEATS = {
    "~ready": "ready",
    "~start": "ready",
    "~door": "door",
    "~dino": "dino",
    "~ttt": "ttt",
    "~vend": "vend",
    "~eat": "eat",
    "~library": "library",
    "~boss1": "boss1",
    "~world2": "world2",
    "~forest": "forest",
    "~treehouse": "treehouse",
}


def new_game():
    return {"inventory": [], "flags": {}}


def has_item(game, item):
    return item in game["inventory"]


def add_item(game, item):
    if item not in game["inventory"]:
        game["inventory"].append(item)


def remove_item(game, item):
    if item in game["inventory"]:
        game["inventory"].remove(item)


def random_babel_page():
    length = random.randint(40, 80)
    chars = string.ascii_letters + string.digits + " ,.;:!?"
    return "".join(random.choice(chars) for _ in range(length))


def random_babel_title():
    length = random.randint(12, 36)
    chars = string.ascii_letters + string.digits + " "
    title = "".join(random.choice(chars) for _ in range(length)).strip()
    return title if title else "xkcd"


def ensure_library_shelf(game):
    if "library_titles" in game:
        return
    real_index = (world.LIBRARY_BOOK_COUNT - 1) // 2
    titles = []
    for index in range(world.LIBRARY_BOOK_COUNT):
        if index == real_index:
            titles.append(world.TTT_REAL_BOOK_TITLE)
        else:
            titles.append(random_babel_title())
    game["library_titles"] = titles
    game["library_ttt_index"] = real_index


def resolve_book_choice(raw, game):
    ensure_library_shelf(game)
    titles = game["library_titles"]
    if raw.isdigit():
        index = int(raw) - 1
        if 0 <= index < len(titles):
            return index
        return None
    real_title = world.TTT_REAL_BOOK_TITLE.lower()
    if raw == real_title:
        return game["library_ttt_index"]
    for index, title in enumerate(titles):
        if raw == title.lower():
            return index
    return None


def is_ttt_book(index, game):
    ensure_library_shelf(game)
    return index == game["library_ttt_index"]


def initial_state():
    return {
        "game": new_game(),
        "room_idx": 0,
        "ctx": {"phase": "enter"},
        "ended": False,
        "complete": False,
    }


def _save_checkpoint(state):
    state["checkpoint"] = {
        "game": copy.deepcopy(state["game"]),
        "room_idx": state["room_idx"],
        "ctx": copy.deepcopy(state["ctx"]),
    }


def restore_checkpoint(state):
    """Return to the world 2 entrance saved after world 1."""
    snapshot = state.get("checkpoint")
    if not snapshot:
        return _response([], state, _prompt_for_state(state))
    state["game"] = copy.deepcopy(snapshot["game"])
    state["room_idx"] = snapshot["room_idx"]
    state["ctx"] = copy.deepcopy(snapshot["ctx"])
    state["ended"] = False
    state["complete"] = False
    state["clear_log"] = True
    return _response([world.WORLD_2_INTRO], state, world.WORLD_2_PROMPT)


def _room_name(state):
    return ROOM_ORDER[state["room_idx"]]


def _skip_to_room(state, room_name):
    state["room_idx"] = ROOM_ORDER.index(room_name)
    state["ctx"] = {"phase": "enter"}


def _apply_item_cheat(state, answer):
    game = state["game"]
    if answer == "~sword":
        add_item(game, world.WOODEN_SWORD)
        return True
    if answer == "~apple":
        add_item(game, world.APPLE)
        return True
    if answer == "~kit":
        add_item(game, world.WOODEN_SWORD)
        add_item(game, world.APPLE)
        return True
    return False


def _finish_room(state, messages):
    state["room_idx"] += 1
    state["ctx"] = {"phase": "enter"}
    if state["room_idx"] >= len(ROOM_ORDER):
        state["complete"] = True
        return None
    return _enter_room(state, messages)


def _enter_room(state, messages):
    room = _room_name(state)
    game = state["game"]
    ctx = state["ctx"]

    if room == "ready":
        ctx["phase"] = "ready"
        return world.READY_PROMPT
    if room == "door":
        messages.append(world.WAKE_UP)
        ctx["phase"] = "door"
        return world.DOOR_PROMPT
    if room == "dino":
        messages.append(world.DINO_INTRO)
        ctx["phase"] = "dino"
        return world.DINO_PROMPT
    if room == "ttt":
        messages.append(world.TTT_INTRO)
        ctx["phase"] = "ttt"
        return world.TTT_PROMPT
    if room == "vend":
        messages.append(world.VEND_INTRO)
        ctx["phase"] = "vend"
        return world.VEND_PROMPT
    if room == "eat":
        messages.append(world.EATING_INTRO)
        ctx["phase"] = "eating"
        ctx["sat_once"] = False
        ctx["examine_count"] = 0
        ctx["in_void"] = False
        ctx["void_fed"] = False
        ctx["offered_sword"] = False
        return world.EATING_PROMPT
    if room == "library":
        messages.append(world.LIBRARY_INTRO)
        ensure_library_shelf(game)
        ctx["phase"] = "library"
        return world.LIBRARY_PROMPT
    if room == "boss1":
        messages.append(world.BOSS1_INTRO)
        if game["flags"].get("ttt_won"):
            messages.append(world.BOSS1_INTRO_TTT_WON)
        ctx["phase"] = "boss"
        ctx["boss_losses"] = 0
        return world.BOSS1_PROMPT
    if room == "world2":
        messages.append(world.WORLD_2_INTRO)
        ctx["phase"] = "world_2"
        _save_checkpoint(state)
        state["clear_log"] = True
        return world.WORLD_2_PROMPT
    if room == "forest":
        messages.append(world.FOREST_INTRO)
        ctx["phase"] = "forest"
        return world.FOREST_PROMPT
    if room == "treehouse":
        messages.append(world.TREEHOUSE_INTRO)
        ctx["phase"] = "treehouse"
        ctx["fairy_talks"] = 0
        ctx["treehouse_looks"] = 0
        return world.TREEHOUSE_PROMPT
    return None


def _handle_turn(state, answer, messages):
    game = state["game"]
    ctx = state["ctx"]
    phase = ctx.get("phase")

    if phase == "enter":
        return _enter_room(state, messages)

    if phase == "ready":
        if answer == "yes":
            messages.append(world.READY_YES)
            return _finish_room(state, messages)
        if answer == "no":
            messages.append(world.READY_NO)
            return world.READY_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.READY_PROMPT

    if phase == "door":
        if answer == "right":
            messages.append(world.DOOR_RIGHT)
            return world.DOOR_PROMPT
        if answer == "middle":
            messages.append(world.DOOR_MIDDLE)
            return world.DOOR_PROMPT
        if answer == "left":
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.DOOR_PROMPT

    if phase == "dino":
        if answer == "fight":
            ctx["phase"] = "fight"
            messages.append(world.FIGHT_START)
            add_item(game, world.WOODEN_SWORD)
            return world.FIGHT_PROMPT
        if answer == "sneak":
            ctx["phase"] = "sneak"
            messages.append(world.SNEAK_START)
            return world.SNEAK_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.DINO_PROMPT

    if phase == "fight":
        if answer == "surrender":
            messages.append(world.FIGHT_SURRENDER)
            state["ended"] = True
            return None
        if answer == "attack":
            messages.append(world.FIGHT_FIRST_ATTACK)
            ctx["phase"] = "fight_after_hit"
            return world.FIGHT_AGAIN_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.FIGHT_PROMPT

    if phase == "fight_after_hit":
        if answer == "run":
            messages.append(world.FIGHT_RUN)
            return _finish_room(state, messages)
        if answer == "attack":
            messages.append(world.FIGHT_SWORD_BREAKS)
            remove_item(game, world.WOODEN_SWORD)
            ctx["phase"] = "fight_broken"
            return world.FIGHT_AGAIN_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.FIGHT_AGAIN_PROMPT

    if phase == "fight_broken":
        if answer == "attack":
            messages.append(world.FIGHT_UNARMED)
            state["ended"] = True
            return None
        if answer == "run":
            messages.append(world.FIGHT_RUN)
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.FIGHT_AGAIN_PROMPT

    if phase == "sneak":
        if answer == "attack":
            messages.append(world.FIGHT_UNARMED)
            state["ended"] = True
            return None
        if answer == "mercy":
            messages.append(world.SNEAK_MERCY)
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.SNEAK_PROMPT

    if phase == "ttt":
        if answer == "examine":
            messages.append(world.TTT_EXAMINE)
            return world.TTT_PROMPT
        if answer == "continue":
            messages.append(world.TTT_CONTINUE)
            ctx["phase"] = "ttt_play"
            return world.TTT_PLAY_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.TTT_PROMPT

    if phase == "ttt_play":
        if answer == "play":
            if random.random() < world.TTT_WIN_CHANCE:
                messages.append(world.TTT_WIN)
                game["flags"]["ttt_won"] = True
                messages.append(world.TTT_RESIGN)
                return _finish_room(state, messages)
            messages.append(random.choice(world.TTT_LOSSES))
            return world.TTT_PLAY_PROMPT
        if answer == "resign":
            messages.append(world.TTT_RESIGN)
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.TTT_PLAY_PROMPT

    if phase == "vend":
        if answer == "press":
            if has_item(game, world.APPLE):
                messages.append(world.VEND_PRESS_AGAIN)
            else:
                messages.append(world.VEND_PRESS)
                add_item(game, world.APPLE)
            return world.VEND_PROMPT
        if answer == "kick":
            if random.random() < world.VEND_KICK_DEATH_CHANCE:
                messages.append(world.VEND_KICK_DIE)
                state["ended"] = True
                return None
            messages.append(world.VEND_KICK_LIVE)
            return world.VEND_PROMPT
        if answer == "leave":
            messages.append(world.VEND_LEAVE)
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.VEND_PROMPT

    if phase == "eating":
        if answer == "sit":
            if not ctx["sat_once"]:
                messages.append(world.EATING_SIT)
                ctx["sat_once"] = True
            else:
                messages.append(world.EATING_SIT_AGAIN)
            return world.EATING_PROMPT
        if answer == "examine":
            ctx["examine_count"] += 1
            count = ctx["examine_count"]
            if count == 1:
                messages.append(world.EATING_EXAMINE)
            elif count == 2:
                messages.append(world.EATING_EXAMINE_AGAIN)
            elif count == 3:
                messages.append(world.EATING_EXAMINE_AGAIN_AGAIN)
            else:
                messages.append(world.VOID_INTRO)
                ctx["phase"] = "void"
                return world.VOID_PROMPT
            return world.EATING_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.EATING_PROMPT

    if phase == "void":
        if answer == "feed":
            if ctx["void_fed"]:
                messages.append(world.VOID_FEED_APPLE_NOTHING)
            elif has_item(game, world.WOODEN_SWORD) and not ctx["offered_sword"]:
                messages.append(world.VOID_FEED_SWORD)
                ctx["offered_sword"] = True
            elif has_item(game, world.APPLE):
                messages.append(world.VOID_FEED_APPLE)
                remove_item(game, world.APPLE)
                ctx["void_fed"] = True
            elif has_item(game, world.WOODEN_SWORD):
                messages.append(world.VOID_FEED_SWORD)
            else:
                messages.append(world.VOID_FEED_NOTHING)
            return world.VOID_PROMPT
        if answer == "leave":
            if ctx["void_fed"]:
                messages.append(world.VOID_LEAVE_LIVE)
                return _finish_room(state, messages)
            messages.append(world.VOID_LEAVE_DIE)
            state["ended"] = True
            return None
        messages.append(world.UNRECOGNIZED)
        return world.VOID_PROMPT

    if phase == "library":
        if answer == "search":
            listing = [world.LIBRARY_SEARCH_HEADER]
            for number, title in enumerate(game["library_titles"], start=1):
                listing.append(f"{number}. {title}")
            messages.append("\n".join(listing))
            return world.LIBRARY_PROMPT
        if answer == "read":
            ctx["phase"] = "library_pick"
            return world.LIBRARY_READ_WHICH
        if answer == "door":
            messages.append(world.LIBRARY_DOOR_OPEN)
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.LIBRARY_PROMPT

    if phase == "library_pick":
        index = resolve_book_choice(answer, game)
        if index is None:
            messages.append(world.UNRECOGNIZED)
            ctx["phase"] = "library"
            return world.LIBRARY_PROMPT
        if is_ttt_book(index, game):
            ctx["phase"] = "ttt_book"
            ctx["book_page"] = 0
            messages.append(world.LIBRARY_TTT_BOOK_PAGES[0])
            return world.LIBRARY_REAL_PAGE_PROMPT
        ctx["phase"] = "gibberish_book"
        ctx["book_page"] = 1
        messages.append(world.LIBRARY_READ_GIBBERISH_HEADER.format(page=1))
        messages.append(random_babel_page())
        return world.LIBRARY_PAGE_PROMPT

    if phase == "gibberish_book":
        page = ctx["book_page"]
        if answer == "close":
            ctx["phase"] = "library"
            return world.LIBRARY_PROMPT
        if answer == "next":
            if page >= 10:
                page = 10
                ctx["book_page"] = page
                messages.append(world.LIBRARY_READ_GIBBERISH_HEADER.format(page=page))
                messages.append(random_babel_page())
                return world.LIBRARY_PAGE_PROMPT
            page += 1
            ctx["book_page"] = page
            messages.append(world.LIBRARY_READ_GIBBERISH_HEADER.format(page=page))
            messages.append(random_babel_page())
            return world.LIBRARY_PAGE_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.LIBRARY_PAGE_PROMPT

    if phase == "ttt_book":
        last_page = len(world.LIBRARY_TTT_BOOK_PAGES) - 1
        page = ctx["book_page"]
        if answer == "close":
            ctx["phase"] = "library"
            return world.LIBRARY_PROMPT
        if answer == "next":
            if page < last_page:
                page += 1
                ctx["book_page"] = page
            messages.append(world.LIBRARY_TTT_BOOK_PAGES[page])
            return world.LIBRARY_REAL_PAGE_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.LIBRARY_REAL_PAGE_PROMPT

    if phase == "boss":
        if answer == "play":
            ctx["boss_losses"] += 1
            if ctx["boss_losses"] >= world.BOSS1_MAX_LOSSES:
                messages.append(world.BOSS1_TOO_MANY_LOSSES)
                state["ended"] = True
                return None
            messages.append(random.choice(world.BOSS1_LOSSES))
            return world.BOSS1_PROMPT
        if answer == "resign":
            messages.append(world.BOSS1_RESIGN_END)
            state["ended"] = True
            return None
        if answer == world.TTT_BOSS_CHEAT_CODE:
            messages.append(world.BOSS1_CHEAT_WIN)
            ctx["phase"] = "boss_win"
            return world.BOSS1_FINISHED
        messages.append(world.BOSS1_CHEAT_UNKNOWN)
        return world.BOSS1_PROMPT

    if phase == "boss_win":
        if answer == "continue":
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.BOSS1_FINISHED

    if phase == "world_2":
        if answer == "forest":
            return _finish_room(state, messages)
        if answer == "back":
            messages.append(world.WORLD_2_BACK)
            add_item(game, world.APPLE)
            ctx["phase"] = "world_2_continue"
            return world.WORLD_2_BACK_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.WORLD_2_PROMPT

    if phase == "world_2_continue":
        if answer == "continue":
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.WORLD_2_BACK_PROMPT

    if phase == "forest":
        if answer == "explore":
            if random.random() < 0.25:
                messages.append(world.FOREST_EXPLORE_DEATH)
                state["ended"] = True
                return None
            messages.append(random.choice(world.FOREST_EXPLORE))
            return world.FOREST_PROMPT
        if answer == "path":
            messages.append(world.FOREST_PATH)
            ctx["phase"] = "forest_path"
            return world.FOREST_PATH_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.FOREST_PROMPT

    if phase == "forest_path":
        if answer == "continue":
            return _continue_along_path(state, messages)
        if answer == "enter":
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.FOREST_PATH_PROMPT

    if phase == "forest_path_onward":
        if answer == "continue":
            return _continue_along_path(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.FOREST_PATH_CONTINUE_PROMPT

    if phase == "treehouse":
        if answer == "talk":
            ctx["fairy_talks"] += 1
            talks = ctx["fairy_talks"]
            if talks == 1:
                messages.append(world.TREEHOUSE_TALK)
                return world.TREEHOUSE_PROMPT
            if talks == 2:
                messages.append(world.TREEHOUSE_TALK_AGAIN)
                return world.TREEHOUSE_PROMPT
            messages.append(world.TREEHOUSE_TALK_AGAIN_AGAIN)
            ctx["phase"] = "treehouse_problem"
            return world.TREEHOUSE_FAIRY_PROBLEM_PROMPT
        if answer == "examine":
            looks = world.TREEHOUSE_EXAMINE
            messages.append(looks[ctx["treehouse_looks"] % len(looks)])
            ctx["treehouse_looks"] += 1
            return world.TREEHOUSE_PROMPT
        messages.append(world.UNRECOGNIZED)
        return world.TREEHOUSE_PROMPT

    if phase == "treehouse_problem":
        if answer == "ask":
            messages.append(world.TREEHOUSE_FAIRY_PROBLEM_ASK)
            ctx["phase"] = "treehouse_help"
            return world.TREEHOUSE_FAIRY_HELP_PROMPT
        if answer == "leave":
            messages.append(world.TREEHOUSE_FAIRY_PROBLEM_LEAVE)
            state["ended"] = True
            return None
        messages.append(world.UNRECOGNIZED)
        return world.TREEHOUSE_FAIRY_PROBLEM_PROMPT

    if phase == "treehouse_help":
        if answer == "help":
            messages.append(world.TREEHOUSE_FAIRY_HELP_HELP)
            ctx["phase"] = "fairy_follow"
            ctx["fairy_follows"] = 0
            return world.FAIRY_FOLLOW_PROMPT
        if answer == "leave":
            messages.append(world.TREEHOUSE_FAIRY_HELP_LEAVE)
            state["ended"] = True
            return None
        messages.append(world.UNRECOGNIZED)
        return world.TREEHOUSE_FAIRY_HELP_PROMPT

    if phase == "fairy_follow":
        if answer == "follow":
            return _follow_fairy(state, messages)
        if answer == "leave":
            messages.append(world.FAIRY_FOLLOW_LEAVE)
            ctx["phase"] = "forest_end"
            return world.FOREST_END_PROMPT
        messages.append(world.UNRECOGNIZED)
        return _prompt_for_state(state)

    if phase == "demon_battle":
        if answer == "fight":
            if has_item(game, world.WOODEN_SWORD):
                messages.append(world.DEMON_BATTLE_FIGHT_SWORD)
            else:
                messages.append(world.DEMON_BATTLE_FIGHT_NO_SWORD)
                add_item(game, WOODEN_STICK)
            ctx["phase"] = "demon_defend"
            ctx["weapon_broken"] = False
            return world.DEMON_BATTLE_DEFEND_PROMPT
        if answer == "run":
            return _flee_demon(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.DEMON_BATTLE_PROMPT

    if phase == "demon_defend":
        if answer == "defend":
            if random.random() < 0.5:
                messages.append(world.DEMON_BATTLE_DEFEND_BLOCK)
                ctx["weapon_broken"] = False
            else:
                messages.append(world.DEMON_BATTLE_DEFEND_BLOCK_FAIL)
                ctx["weapon_broken"] = True
                remove_item(game, world.WOODEN_SWORD)
                remove_item(game, WOODEN_STICK)
            ctx["phase"] = "demon_attack"
            return world.DEMON_BATTLE_ATTACK_AGAIN_PROMPT
        if answer == "run":
            return _flee_demon(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.DEMON_BATTLE_DEFEND_PROMPT

    if phase == "demon_attack":
        if answer == "attack":
            if ctx.get("weapon_broken"):
                messages.append(world.DEMON_BATTLE_ATTACK_AGAIN_DEATH)
                state["ended"] = True
                return None
            if has_item(game, world.WOODEN_SWORD):
                messages.append(world.DEMON_BATTLE_ATTACK_AGAIN_SUCCES_WOODEN_SWORD)
                remove_item(game, world.WOODEN_SWORD)
                add_item(game, DEMON_SWORD)
                ctx["phase"] = "forest_end"
                return world.FOREST_END_PROMPT
            if has_item(game, WOODEN_STICK):
                messages.append(world.DEMON_BATTLE_ATTACK_AGAIN_SUCCES_STICK)
                remove_item(game, WOODEN_STICK)
                add_item(game, DEMON_SWORD)
                ctx["phase"] = "forest_end"
                return world.FOREST_END_PROMPT
            messages.append(world.DEMON_BATTLE_ATTACK_AGAIN_WEAPONLESS)
            state["ended"] = True
            return None
        if answer == "run":
            return _flee_demon(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.DEMON_BATTLE_ATTACK_AGAIN_PROMPT

    if phase == "forest_end":
        if answer == "continue":
            return _finish_room(state, messages)
        messages.append(world.UNRECOGNIZED)
        return world.FOREST_END_PROMPT

    messages.append(world.UNRECOGNIZED)
    return _prompt_for_state(state)


def _prompt_for_state(state):
    phase = state["ctx"].get("phase")
    prompts = {
        "ready": world.READY_PROMPT,
        "door": world.DOOR_PROMPT,
        "dino": world.DINO_PROMPT,
        "fight": world.FIGHT_PROMPT,
        "fight_after_hit": world.FIGHT_AGAIN_PROMPT,
        "fight_broken": world.FIGHT_AGAIN_PROMPT,
        "sneak": world.SNEAK_PROMPT,
        "ttt": world.TTT_PROMPT,
        "ttt_play": world.TTT_PLAY_PROMPT,
        "vend": world.VEND_PROMPT,
        "eating": world.EATING_PROMPT,
        "void": world.VOID_PROMPT,
        "library": world.LIBRARY_PROMPT,
        "library_pick": world.LIBRARY_READ_WHICH,
        "gibberish_book": world.LIBRARY_PAGE_PROMPT,
        "ttt_book": world.LIBRARY_REAL_PAGE_PROMPT,
        "boss": world.BOSS1_PROMPT,
        "boss_win": world.BOSS1_FINISHED,
        "world_2": world.WORLD_2_PROMPT,
        "world_2_continue": world.WORLD_2_BACK_PROMPT,
        "forest": world.FOREST_PROMPT,
        "forest_path": world.FOREST_PATH_PROMPT,
        "forest_path_onward": world.FOREST_PATH_CONTINUE_PROMPT,
        "treehouse": world.TREEHOUSE_PROMPT,
        "treehouse_problem": world.TREEHOUSE_FAIRY_PROBLEM_PROMPT,
        "treehouse_help": world.TREEHOUSE_FAIRY_HELP_PROMPT,
        "demon_battle": world.DEMON_BATTLE_PROMPT,
        "demon_defend": world.DEMON_BATTLE_DEFEND_PROMPT,
        "demon_attack": world.DEMON_BATTLE_ATTACK_AGAIN_PROMPT,
        "forest_end": world.FOREST_END_PROMPT,
    }
    if phase == "fairy_follow":
        if state["ctx"].get("fairy_follows"):
            return world.FAIRYFOLLOW_AGAIN_PROMPT
        return world.FAIRY_FOLLOW_PROMPT
    return prompts.get(phase)


def _follow_fairy(state, messages):
    ctx = state["ctx"]
    follows = ctx.get("fairy_follows", 0)
    if follows == 0:
        messages.append(world.FAIRY_FOLLOW_FOLLOW)
        ctx["fairy_follows"] = 1
        return world.FAIRYFOLLOW_AGAIN_PROMPT
    if follows == 1:
        messages.append(world.FAIRY_FOLLOW_FOLLOW_AGAIN)
        ctx["fairy_follows"] = 2
        return world.FAIRYFOLLOW_AGAIN_PROMPT
    messages.append(world.FAIRY_FOLLOW_FOLLOW_AGAIN_AGAIN)
    ctx["phase"] = "demon_battle"
    ctx["weapon_broken"] = False
    return world.DEMON_BATTLE_PROMPT


def _flee_demon(state, messages):
    messages.append(world.DEMON_BATTLE_RUN)
    state["ctx"]["phase"] = "forest_end"
    return world.FOREST_END_PROMPT


def _continue_along_path(state, messages):
    ctx = state["ctx"]
    if "path_limit" not in ctx:
        ctx["path_limit"] = random.randint(3, 5)
        ctx["path_steps"] = 0
    if ctx["path_steps"] >= ctx["path_limit"]:
        messages.append(world.FOREST_PATH_DEATH)
        state["ended"] = True
        return None
    messages.append(random.choice(world.FOREST_PATH_CONTINUE))
    ctx["path_steps"] += 1
    ctx["phase"] = "forest_path_onward"
    return world.FOREST_PATH_CONTINUE_PROMPT


def process_turn(state, user_input):
    """Start (state=None) or advance the game with one line of input."""
    messages = []

    if state is None:
        state = initial_state()
        prompt = _enter_room(state, messages)
        return _response(messages, state, prompt)

    if state.get("ended") or state.get("complete"):
        return _response(messages, state, None)

    answer = (user_input or "").strip().lower()

    if answer == "~die":
        messages.append(world.DEV_CHEAT_DEATH)
        state["ended"] = True
        return _response(messages, state, None)

    if answer in ROOM_CHEATS:
        _skip_to_room(state, ROOM_CHEATS[answer])
        prompt = _enter_room(state, messages)
        return _response(messages, state, prompt)

    if _apply_item_cheat(state, answer):
        return _response(messages, state, _prompt_for_state(state))

    prompt = _handle_turn(state, answer, messages)
    return _response(messages, state, prompt)


def _response(messages, state, prompt):
    ended = state.get("ended", False) or state.get("complete", False)
    clear_log = bool(state.pop("clear_log", False))
    return {
        "messages": messages,
        "prompt": prompt,
        "state": state,
        "inventory": list(state["game"]["inventory"]),
        "ended": ended,
        "complete": state.get("complete", False),
        "clear_log": clear_log,
    }


def play_game():
    """Terminal CLI."""
    state = None
    prompt = None
    while True:
        if state is None:
            result = process_turn(None, None)
        else:
            if prompt:
                print(prompt)
            result = process_turn(state, input())

        state = result["state"]
        for line in result["messages"]:
            print(line)

        if result["ended"]:
            sys.exit(0)

        prompt = result["prompt"]
