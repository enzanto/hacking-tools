def read(filename: str, mode: str = "r") -> str | None:
    """
    Read the contents of a file.

    Args:
        filename (str): The path to the file to read.
        mode (str): The file mode (default: "r" for read).

    Returns:
        str | None: The file contents as a string, or None if the file is not found.

    Raises:
        Prints an error message if the file is not found or if an unexpected error occurs.
    """
    file = None
    try:
        file = open(filename, mode)
        data = file.read()
        return data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        data = None
        return data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        data = None
        return data
    finally:
        if file != None:
            file.close()


def read_list(filename: str, mode: str = "r") -> list[str] | None:
    """
    Read the contents of a file.

    Args:
        filename (str): The path to the file to read.
        mode (str): The file mode (default: "r" for read).

    Returns:
        list[str] | None: The file contents as a string, or None if the file is not found.

    Raises:
        Prints an error message if the file is not found or if an unexpected error occurs.
    """
    file = None
    try:
        file = open(filename, mode)
        data = file.read().split()
        return data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        data = None
        return data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        data = None
        return data
    finally:
        if file != None:
            file.close()


def write(data: str | list[str], filename: str, mode: str = "w") -> None:
    """
    Write data to a file.

    Args:
        data (str | list): The data to write. Can be a string or a list of strings.
            When a list is provided, each item is written on a separate line.
        filename (str): The path to the file to write to.
        mode (str): The file mode (default: "w" for write, "a" for append).

    Returns:
        None

    Raises:
        Prints an error message if the file is not found or an unexpected error occurs.
    """
    file = None
    try:
        file = open(filename, mode)
        if isinstance(data, str):
            file.write(data)
        elif isinstance(data, list):
            file.writelines([line + "\n" for line in data])
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if file != None:
            file.close()
