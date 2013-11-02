class FileReader:

    @classmethod
    def read(cls, input_file):
        return open(input_file, 'r+').read()