from __future__ import annotations

import gdb

import os
from pprint import pprint

from dataclasses import dataclass
import dataclasses


@dataclass
class Member:
    member_name: str
    typename: str


@dataclass
class Struct:
    typename: str
    members: list[Member] = dataclasses.field(default_factory=list)


all_structs = {}


def get_types(target_type: gdb.Type):
    typename = target_type.name
    if typename in all_structs.keys():
        return

    struct = Struct(typename)

    for field in target_type.fields():
        fieldname = field.name
        fieldtype = field.type.strip_typedefs()
        fieldtype_name = fieldtype.name

        while fieldtype.code in [gdb.TYPE_CODE_ARRAY, gdb.TYPE_CODE_PTR]:
            if fieldtype.code == gdb.TYPE_CODE_ARRAY:
                fieldtype = fieldtype.target().strip_typedefs()
                fieldtype_name = f'array.{fieldtype.name}'

            if fieldtype.code == gdb.TYPE_CODE_PTR:
                fieldtype = fieldtype.target().strip_typedefs()
                fieldtype_name = f'pointer.{fieldtype.name}'

        if fieldtype.code == gdb.TYPE_CODE_STRUCT:
            get_types(fieldtype)
        elif fieldtype.code == gdb.TYPE_CODE_ENUM:
            # we probably want to cast to underlying type later
            print('TYPE_CODE_ENUM encountered, but not handeled yet.')
        elif fieldtype.code == gdb.TYPE_CODE_UNION:
            print('TYPE_CODE_UNION encountered, but not handeled yet.')

        struct.members.append(Member(fieldname, fieldtype_name))

    all_structs[typename] = struct


target_type = gdb.lookup_type(os.getenv('TARGET_TYPE'))
get_types(target_type)

pprint([dataclasses.asdict(struct) for struct in all_structs.values()])
