#include <pybind11/pybind11.h>
#include "c.hpp"

namespace py = pybind11;

PYBIND11_MODULE(TypeStructureLib, m) {
    py::class_<NestedStruct>(m, "NestedStruct")
        .def(py::init<>())
        .def_readwrite("nes", &NestedStruct::nes)
        ;

    py::class_<MyStruct>(m, "MyStruct")
        .def(py::init<>())
        .def_readwrite("a", &MyStruct::a)
        .def_readwrite("b", &MyStruct::b)
        .def_readwrite("nest", &MyStruct::nest)
        //.TODO_CUSTOM_HANDLING_NEEDED("arr", &MyStruct::arr)
        ;

}
    
