from pyrope import Replay

if __name__ == '__main__':
    replay = Replay("replays/crossplatform_party.replay")
    replay.parse_netstream()

    # with open('outputs/crossplatform_party.replay.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.netstream_to_json())
