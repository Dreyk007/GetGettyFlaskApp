# Изобретённый заново велосипед. Но он, в своё время, помогал с простыми задачами.
class ReadWriteFile:
    """ Read and write text files with type detection. Version = 1.05 """

    def __init__(self, filename, sep=':*:'):
        # Separator for dicts
        self.sep = sep
        self.filename = filename

    def __file_read(self, one_row):
        """ Internal file read function. """
        with open(self.filename, 'r') as file:
            if one_row:
                return str(file.read()).strip()

            data = [row.strip() for row in file]
            # Check that the file is not empty
            if data:
                # Type detection
                if self.sep not in data[0]:
                    return data
                # Dict case
                else:
                    data_to_dict = dict()
                    for row_w_sep in data:
                        key, value = row_w_sep.split(self.sep)
                        data_to_dict[key] = value

                    return data_to_dict
            else:
                return None

    def __file_write(self, mode, data, clear=False):
        """ Internal file write function. """
        with open(self.filename, mode) as file:
            if clear:
                return None
            # Type detection and different actions for types
            if isinstance(data, list):
                for i in data:
                    file.write(f'{str(i)}\n')

            elif isinstance(data, (str, int, bool)) or data is None:
                file.write(f'{str(data)}\n')

            elif isinstance(data, dict):
                for key, value in data.items():
                    file.write(f'{str(key)}{self.sep}{str(value)}\n')

            else:
                raise ValueError('Wrong data type to write.')

    def read(self, one_row=False):
        """ Read the file. If one_row == True, file will be read in one line. """
        return self.__file_read(one_row)

    def write(self, data):
        """ Write the file. """
        self.__file_write('w', data)

    def append(self, data):
        """ Append data to the file without rewrite. """
        self.__file_write('a', data)

    def clear(self):
        """ Clear the file. """
        self.__file_write('w', data=None, clear=True)


if __name__ == '__main__':
    # Examples:
    list0 = [i for i in range(10)]
    list1 = [i + i for i in list0]
    dict0 = {key: value for key, value in zip(list0, list1)}
    list_w_dicts = [{'key': i} for i in list0]
    str0 = '123:*:\nsome_data321'

    # Write:
    ReadWriteFile('list.txt').write(list0)
    ReadWriteFile('dict.txt').write(dict0)
    ReadWriteFile('str.txt').write(str0)
    ReadWriteFile('list_w_dicts.txt').write(list_w_dicts)
    # Append:
    ReadWriteFile('appendlist.txt').append(list0)

    # Read:
    list_r = ReadWriteFile('list.txt').read()
    dict_r = ReadWriteFile('dict.txt').read()
    str_r = ReadWriteFile('str.txt').read(one_row=True)
    list_w_dicts_r = ReadWriteFile('list_w_dicts.txt').read()

    print(list_r)
    print(dict_r)
    print(str_r)
    print(list_w_dicts_r)

    # from MyFunc_OLD import RW_File
    #
    # RW_File(mode='w', filename='str.txt', linksl=str0, read_dict=0)
    # str_r = RW_File(mode='r', filename='str.txt', linksl=str0, read_dict=0)
    # RW_File(mode='w', filename='list_w_dicts.txt', linksl=list_w_dicts, read_dict=0)
    #
    # print(str_r)
