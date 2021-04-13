import re
from builder.Parser import Parser
import builder.BuildTopology


class Test:
    def clear_empty(self, line: list):
        return [string for string in line if string != '']

    def _hw_wrapper(self, data):
        idx = ''
        modules = []
        unit = []
        for line in data:
            name = line[0]
            unit_num = line[1]
            local_id = name + unit_num
            line = self.clear_empty(line[2:])
            local = [name, unit_num]
            if local_id == idx:
                unit.extend(line)
            else:
                idx = local_id
                unit = []
                unit.extend(local)
                unit.extend(line)
                modules.append(unit)
        return modules

    def get_hardware_data(self, data):
        modules = list(set([module[0] for module in data]))
        modules = {key: {} for key in modules}
        hardware = self._hw_wrapper(data)
        for unit in hardware:
            if unit.__len__() == 3:
                modules[unit[0]].update({unit[1]: {"PCB_version": unit[2]}})
            if unit.__len__() == 4:
                modules[unit[0]].update({unit[1]: {"Unit_version": unit[2],
                                           "PCB_version": unit[3]}})
            if unit[0] == "LPU":
                modules[unit[0]].update({unit[1]: {"LPU_version": unit[2],
                                                   "PCB_version": unit[3],
                                                   "NSE_version": unit[4],
                                                   unit[5]: {"PIC_version": unit[6],
                                                             "PCB_version": unit[7]
                                                             }
                                                   }})
            if unit[0] == "POWER":
                local = {}
                line = unit[2:]
                for index, item in enumerate(line):
                    if index % 2 == 0:
                        local[item] = line[index + 1]
                modules[unit[0]].update({unit[1]: local})
        return modules


if __name__ == '__main__':
    t = Test()
    template = "../templates/huawei/hw_info.template"
    with open(r'hu_out.txt') as file:
        text = file.read()
    parser = Parser()
    parser = parser.parse_data(template, text)
    #for i in parser:
    #    print(i)

    t.get_hardware_data(parser)
