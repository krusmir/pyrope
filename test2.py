from pyrope import Replay
from pyrope.utils import reverse_bytewise
import bitstring

if __name__ == '__main__':
    replay = Replay("replays/crossplatform_party.replay")
    # netstream = bitstring.BitArray(b'<\x15\x8c\x82\x00\x00\x00\x00\x80\x0c\x00\x00\x00\x00\x04\x00\x00\x00\xc0')

    netstream = reverse_bytewise(replay._netstream_raw)

    frame_current_time = reverse_bytewise(netstream[0:32]).floatle
    frame_delta = reverse_bytewise(netstream[32:64]).floatle
    print("Current Time:", frame_current_time)
    print("Current Delta:", frame_delta)

    actor_present = netstream[64:65].bool  # 1 bit to signal we are replicating another actor
    print("Actor Present:", actor_present)

    actor_id = reverse_bytewise(
        netstream[65:75]).uintle  # compressed integer for the actor's network channel ID (max value is MaxChannels)
    print("Actor ID:", actor_id)

    channel = netstream[
              75:76].bool  # 1 bit to signal the channel is closing (actor was destroyed)` OR  - 1 bit to signal the channel is open
    print(channel)

    if channel:  # channel is open
        new_actor = netstream[76:77].bool  # - 1 bit to signal it is a new actor
        print(new_actor)
    else:
        eh = netstream[77:78].bool
        print(netstream[78:78 + 8 * 30])

        pass

    # channel = netstream[75:76].bool
    # print(channel)
    # is_new = netstream[76:77].bool
    # print(is_new)
    # x = 77
    # print(netstream[x:x+8*3].bytes)
    # print(netstream)
    # print(netstream[77:])
