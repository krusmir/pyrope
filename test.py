from pyrope import Replay

if __name__ == '__main__':
    replay = Replay("replays/crossplatform_party.replay")
    replay.parse_netstream()
    # with open('outputs/crossplatform_party.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())

    # replay = Replay("replays/1.replay")
    # replay.parse_netstream()
    # with open('outputs/1.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # with open('outputs/1.replay.netstream.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.netstream_to_json())
    #
    # replay = Replay("replays/2.replay")
    # with open('outputs/2.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # replay = Replay("replays/3.replay")
    # with open('outputs/3.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # replay = Replay("replays/4.replay")
    # with open('outputs/4.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # replay = Replay("replays/5.replay")
    # with open('outputs/5.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # replay = Replay("replays/6.replay")
    # with open('outputs/6.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    # replay = Replay("replays/7.replay")
    # with open('outputs/7.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
    #
    #     replay = Replay("replays/8.replay")
    # with open('outputs/8.replay.header.json', 'w', encoding='utf-8') as outfile:
    #     outfile.write(replay.header_to_json())
