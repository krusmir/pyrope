from pyrope import Replay
from pyrope.utils import reverse_bytewise, reverse_byte, read_byte_vector, read_uint32_max
import bitstring
import math


# def ReadUInt32Max(bs: bitstring):
#     print(bs.pos)
#     # print (bs)
#     maxValue = 2047
#     maxBits = math.floor(math.log10(maxValue) / math.log10(2) + 1)
#     print(maxBits)
#     i = 0
#     value = 0
#     shift_value = value + (1 << i)
#     print(shift_value)
#     while i < maxBits and shift_value < maxValue:
#         value = value + bs.read('bits:1') << i
#         i = i + 1
#     return reverse_bytewise(value).uintle


if __name__ == '__main__':
    replay = Replay("replays/crossplatform_party.replay")
    # netstream = bitstring.BitArray(b'<\x15\x8c\x82\x00\x00\x00\x00\x80\x0c\x00\x00\x00\x00\x04\x00\x00\x00\xc0')

    netstream = reverse_bytewise(replay._netstream_raw)

    frame_current_time = reverse_bytewise(netstream.read('bits:32')).floatle
    frame_delta = reverse_bytewise(netstream.read('bits:32')).floatle
    print("Current Time:", frame_current_time)
    print("Current Delta:", frame_delta)

    actor_present = netstream.read('bits:1').bool  # 1 bit to signal we are replicating another actor
    print("Actor Present:", actor_present)

    # actor deserialize

    actor_id = read_uint32_max(netstream, replay.header["MaxChannels"])
    # actor_id = reverse_bytewise(
    #     netstream[65:75]).uintle  # compressed integer for the actor's network channel ID (max value is MaxChannels)
    print("Actor ID:", actor_id)
    print(netstream.pos)
    channel = netstream.read('bits:1').bool
    print("spawned?", channel)
    is_new = netstream.read('bits:1').bool
    print("is new?", is_new)
    name_id = reverse_bytewise(netstream.read('bits:32')).uintle
    print(name_id)
    unknown1 = netstream.read('bits:1').bool
    print(unknown1)
    type_id = reverse_bytewise(netstream.read('bits:32')).uintle
    print(type_id)
    print(replay.objects[type_id])

    # channel = netstream[75: 76].bool  # 1 bit to signal the channel is closing (actor was destroyed)` OR  - 1 bit to signal the channel is open
    #
    # if channel:  # channel is open
    #     new_actor = netstream[76:77].bool  # - 1 bit to signal it is a new actor
    #     print("is new actor:", new_actor)
    # else:
    #     eh = netstream[77:78].bool
    #     print(netstream[78:78 + 8 * 30])

    # channel = netstream[75:76].bool
    # print(channel)
    # is_new = netstream[76:77].bool
    # print(is_new)
    # x = 77
    # print(netstream[x:x+8*3].bytes)
    # print(netstream)
    # print(netstream[77:])
