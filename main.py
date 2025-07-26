# class Macro:
#     name: str
#     parameters: list[str]
#     default_parameter_values: dict[str, str]
#     ports: list[str]

#     def template(self, instance_name: str, parameter_values: dict[str, str] = {}, port_values: dict[str, str] = {}):
#         if set(port_values.keys()) != set(self.ports):
#             raise ValueError(f'Port values must be provided for excatly all ports listed: {self.ports}')
#         s = f'{self.name} {instance_name}('
#         s += ', '.join([f'.{k}({v})' for k, v in port_values.items()])
#         s += ');'
#         return s


from abc import ABC


class Macro(ABC):
    name: str
    ports: list[str]
    parameters: list[str]
    default_parameter_values: dict[str, str]

    def template(
        self,
        instance_name: str,
        parameter_values: dict[str, str] = {},
        port_values: dict[str, str] = {},
    ):
        if set(port_values.keys()) != set(self.ports):
            raise ValueError(
                f"Port values must be provided for excatly all ports listed: {self.ports}"
            )
        parameter_values_combined = {
            **self.default_parameter_values,
            **parameter_values,
        }
        s = f"{self.name} "
        if len(parameter_values_combined) > 0:
            s += "#(\n"
            s += ",\n".join(
                [f"    .{k}({v})" for k, v in parameter_values_combined.items()]
            )
            s += "\n)\n"
        s += f"{instance_name}(\n"
        s += ",\n".join([f"    .{k}({v})" for k, v in port_values.items()])
        s += "\n);"
        return s


class FDCE(Macro):
    name = "FDCE"
    parameters = ["INIT"]
    default_parameter_values = {"INIT": "0"}
    ports = ["D", "CE", "R", "Q", "QBAR"]


class BUFGCE_1(Macro):
    name = "BUFGCE_1"
    parameters = []
    default_parameter_values = {}
    ports = ["O", "CE", "I"]


class MUXF8_D(Macro):
    name = "MUXF8_D"
    parameters = []
    default_parameter_values = {}
    ports = ["O", "LO", "I0", "I1", "S"]


if __name__ == "__main__":
    m = FDCE()

    inst_str = m.template(
        instance_name="fdce0",
        port_values={
            "D": "wire_0",
            "CE": "wire_1",
            "R": "wire_2",
            "Q": "wire_3",
            "QBAR": "wire_4",
        },
    )

    print(inst_str)
