DEFAULT_FILE_MODES = {
    "r", "r+", "rb", "rb+",
    "w", "w+", "wb", "wb+",
    "a", "a+", "ab", "ab+"
}


class FileManager:

    ####################### Initialization #######################

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file_object = None

    ###################### Getters and Setters ######################

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            raise TypeError("Filename must be a string")
        if not value.strip():
            raise ValueError("Filename must not be empty")
        self.__filename = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, str):
            raise TypeError("Mode must be a string")
        if not value.strip():
            raise ValueError("Mode must not be empty")
        if value.strip() not in DEFAULT_FILE_MODES:
            raise ValueError(f"Set incorrect mode: {value}")
        self.__mode = value.strip()

    ####################### Magic Methods #######################

    def __enter__(self):
        self.file_object = open(self.filename, self.mode)
        return self.file_object

    def __exit__(self, exc_type, exc, tb):
        if self.file_object:
            self.file_object.close()

        if exc_type:
            raise exc_type(f"{exc} (line {tb.tb_lineno})")

        return False

    ######################### String Representation #######################

    def __str__(self):
        return f"File manager: filename {self.filename}, mode {self.mode}"

    def __repr__(self):
        return f"FileManager( filename={self.filename!r} , mode={self.mode!r})"


# Write
with FileManager("test.txt", "w") as f:
    f.write("hello")

# Read
with FileManager("test.txt", "r") as f:
    print(f.read())

# Bad mode
try:
    FileManager("test.txt", "x")
except ValueError as e:
    print(e)
