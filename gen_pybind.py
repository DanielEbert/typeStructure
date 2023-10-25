import json
import sys
import dataclasses
from dataclasses import dataclass

from pprint import pprint


@dataclass
class Member:
    member_name: str
    typename: str


@dataclass
class Struct:
    typename: str
    members: list[Member] = dataclasses.field(default_factory=list)


def get_structs() -> list[Struct]:
    with open(sys.argv[1]) as f:
        structs_dictlist = json.load(f)

    structs: list[Struct] = []

    for struct_dict in structs_dictlist:
        structs.append(Struct(struct_dict['typename'], [Member(
            m['member_name'], m['typename']) for m in struct_dict['members']]))

    return structs


def members_to_pybind_code(classname: str, members: list[Member]) -> str:
    ret = []

    for member in members:
        ret.append(
            f'        .def("{member.member_name}", &{classname}::{member.member_name})')

    return '\n'.join(ret)


def structs_to_pybind_code(structs: list[Struct]) -> str:
    struct_pybind_codes = []

    for struct in structs:
        struct_cpp = f"""\
    py::class_<{struct.typename}>(m, "{struct.typename}")
        .def(py::init<>())
{members_to_pybind_code(struct.typename, struct.members)}
        ;
"""
        struct_pybind_codes.append(struct_cpp)

    struct_pybind_codes_str = '\n'.join(struct_pybind_codes)

    code = f"""\
# include <pybind11/pybind11.h>

namespace py = pybind11

PYBIND11_MODULE(example, m) {{

{struct_pybind_codes_str}

}}
    """

    return code


def main() -> int:
    structs = get_structs()
    code = structs_to_pybind_code(structs)

    print(code)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
