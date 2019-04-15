from collections import OrderedDict

from pyrope.netstream_property_parsing import read_property_value
from pyrope.utils import (reverse_bytewise, BOOL, read_serialized_vector,
                          read_byte_vector, read_serialized_int, read_uint32_max)
from pyrope.exceptions import FrameParsingError, PropertyParsingError


class Frame:
    _actor_alive = {}  # Map of ActorID:Archtype shared across Frames

    def __init__(self):
        self.current = None
        self.delta = None
        self.actors = None
        self.header = None
        self.major = 0
        self.minor = 0
        self.patch_version= 0
        self.maxchannels = None

    def parse_frame(self, netstream, objects, propertymapper, header, major, minor, patch_version):
        self.header = header
        self.maxchannels = header["MaxChannels"]
        self.major = major
        self.minor = minor
        self.patch_version= patch_version
        self.current = reverse_bytewise(netstream.read('bits:32')).floatle
        self.delta = reverse_bytewise(netstream.read('bits:32')).floatle
        # if self.current < 0.001 or self.delta < 0.001:
        #     raise FrameParsingError("Last Frame caused some offset. Nextbits: %s"
        #                             % netstream.read('bits:64').hex)
        self.actors = self._parse_actors(netstream, objects, propertymapper)

    def _parse_actors(self, netstream, objects, propertymapper):
        maxchannels = self.header["MaxChannels"]
        actors = OrderedDict()  # Ordered Dict to reflect order of appearance in json output
        while True:
            startpos = netstream.pos
            actor_present = netstream.read(BOOL)

            if not actor_present:
                break

            if int(self.major) > 868 or int(self.major) == 868 and int(self.minor) >= 14:
                pos = netstream.pos
                actorid = reverse_bytewise(netstream.read('bits:10')).uintle
                print("pos 1", netstream.pos)
                # netstream.pos = pos
                # actorid = read_uint32_max(netstream, maxchannels)
                unknown = netstream.read('bits:1').bool
                print("pos 2", netstream.pos)
            else:
                actorid = reverse_bytewise(netstream.read('bits:10')).uintle
            channel = netstream.read(BOOL)
            if not channel and self._actor_alive:
                try:
                    shorttype = str(actorid) + 'd' + '_'
                    shorttype += self._actor_alive[actorid].split('.')[-1].split(':')[-1]
                    actors[shorttype] = {'startpos': startpos,
                                         'actor_id': actorid,
                                         'actor_type': self._actor_alive[actorid],
                                         'open': channel}
                    del self._actor_alive[actorid]
                except KeyError:
                    raise FrameParsingError("Tried to delete non existent actor", actors)
                continue

            new = netstream.read(BOOL)
            try:
                if new:
                    type_name, data = self._parse_new_actor(netstream, objects)
                    self._actor_alive[actorid] = type_name
                else:
                    data = self._parse_existing_actor(netstream,
                                                      self._actor_alive[actorid],
                                                      objects, propertymapper)
            except (PropertyParsingError, KeyError) as e:
                e.args += ({'CurrFrameActors': actors},)
                try:
                    e.args += ({'ErrorActorType': self._actor_alive[actorid],
                                'ErrorActorId': actorid,
                                'ErrorActorData': data},)
                except KeyError:
                    pass
                raise e
            if new:
                shorttype = str(actorid) + 'n' + '_'
                shorttype += self._actor_alive[actorid].split('.')[-1].split(':')[-1]
            else:
                shorttype = str(actorid) + 'e' + '_'
                shorttype += self._actor_alive[actorid].split('.')[-1].split(':')[-1]
            actors[shorttype] = {
                'startpos': startpos,
                'actor_id': actorid,
                'actor_type': self._actor_alive[actorid],
                'new': new,
                'data': data}
        return actors

    # TODO: fix parse existing actor
    def _parse_existing_actor(self, netstream, actor_type, objects, propertymapper):
        properties = {}
        while netstream.read(BOOL):
            pos = netstream.pos
            property_id_0 = read_uint32_max(netstream, self.maxchannels)
            netstream.pos = pos
            property_id = read_serialized_int(netstream,
                                              propertymapper.get_property_max_id(actor_type))
            # print(property_id_0)
            # print(property_id)
            property_name_0 = objects[propertymapper.get_property_name(actor_type, property_id_0)]
            property_name = objects[propertymapper.get_property_name(actor_type, property_id)]

            # print(property_name_0)
            # print(property_name)
            try:
                if property_name == 'TAGame.RBActor_TA:ReplicatedRBState':
                    property_value = read_property_value(property_name, netstream, self.major, self.minor, self.patch_version)
                else:
                    property_value = read_property_value(property_name, netstream)
            except PropertyParsingError as e:
                e.args += ({"Props_till_err": properties},)
                raise e
            properties[property_name] = property_value
        return properties

    def _parse_new_actor(self, netstream, objects):
        actor = {}
        if int(self.major) > 868 or int(self.major) == 868 and int(self.minor) >= 14:
            actor['nameid'] = reverse_bytewise(netstream.read('bits:32')).uintle
            if actor['nameid'] == 38:
                print(actor)
        print(actor)
        actor['flag'] = netstream.read(BOOL)
        type_id = reverse_bytewise(netstream.read('bits:32')).uintle
        type_name = objects[type_id]
        if 'TheWorld' in type_name:  # World types are Vector Less
            return type_name, actor
        actor['vector'] = read_serialized_vector(netstream)
        if 'Archetypes.Ball' in type_name or 'Car_Default' in type_name:
            actor['rotation'] = read_byte_vector(netstream)
        return type_name, actor
