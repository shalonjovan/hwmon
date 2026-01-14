from hwmon.state.state import get_system_state
import pprint


def main():
    state = get_system_state()
    pprint.pprint(state, sort_dicts=False)


if __name__ == "__main__":
    main()
