
from .searchclient import *
from agent import StatespaceSearchAgent

from preprocessing.mapper import WallMap, GoalMap, goals_sets
from preprocessing.planner import Planner
from strategy import factory as strategy_factory
from heuristic.h_funct import *


def is_multi_agent(level):
    colors_re = re.compile(r'^[a-z]+:\s*[0-9A-Z](\s*,\s*[0-9A-Z])*\s*$')
    pos = level.tell()
    line = level.readline().rstrip()
    if colors_re.fullmatch(line) is not None:
        is_m = True
    else:
        is_m = False
    return is_m, line


def main(strategy, subgoals, debug, **extras):
    # Read server messages from stdin.
    server_messages = sys.stdin

    # Use stderr to print to console through server.
    print('SearchClient initializing. I am sending this using the error output stream.', file=sys.stderr, flush=True)

    # Choose if the level is multi or single agent
    is_multi, first_line = is_multi_agent(server_messages)
    if not is_multi:
        client = SearchClient(server_messages, first_line, debug)

        initial_state = client.initial_state
        w_map = WallMap(initial_state.walls)
        w_map.trim_map(initial_state.boxes, (initial_state.agent_row, initial_state.agent_col))
        #print(w_map.str_nodes(), file=sys.stderr, flush=True)
        #print(w_map.str_map(), file=sys.stderr, flush=True)
        g_map = GoalMap(initial_state.goals)
        planner = Planner()
        planner.floyd_warshall(initial_state.walls)
        strategy_ = strategy_factory(name=strategy,
                                     subgoals=subgoals,
                                     wall_map=w_map,
                                     goal_map=g_map,
                                     initial_state=initial_state,
                                     priority_function=goals_sets,
                                     planner=planner,
                                     heuristic_function=h_constant_reward,
                                     dist_function=planner.dist,
                                     weight_value=5)

        solution = client.search(strategy_)

        # Read level and create the initial state of the problem.
        if solution is None:
            print(strategy_.search_status(), file=sys.stderr, flush=True)
            print('Unable to solve level.', file=sys.stderr, flush=True)
            sys.exit(0)
        else:
            print('\nSummary for {}.'.format(strategy_), file=sys.stderr, flush=True)
            print('Found solution of length {}.'.format(len(solution)), file=sys.stderr, flush=True)
            print('{}.'.format(strategy_.search_status()), file=sys.stderr, flush=True)

            for state in solution:
                print("[" + str(state.action) + "]", flush=True)
                response = server_messages.readline().rstrip()
                if response == 'false':
                    print('Server responsed with "{}" to the action "{}" applied in:\n{}\n'.format(response,
                                                                                                   state.action,
                                                                                                   state),
                          file=sys.stderr, flush=True)
                    break
    else:
        # Read level and create the initial state of the problem.
        print("This is multi agent level!!!")