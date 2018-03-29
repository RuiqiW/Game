"""
A helper function for str method
"""


def draw_hexagon(l: int, cells: list, ley_lines: list) -> str:
    """
    draw stone henge
    """
    n = (l+1) * 3
    result = ''

    # first two lines
    result += ' ' * 2 * (l + 2) + ley_lines[n - 1] + ' ' * 3 + ley_lines[n - 2]\
              + '\n'
    result += ' ' * (2 * (l + 2) - 1) + '/' + ' ' * 3 + '/' + '\n'
    index = 0

    # row 0 - l-1
    for i in range(l - 1):
        result += ' ' * 2 * (l - 1 - i) + ley_lines[i]
        for j in range(i + 2):
            result += ' - ' + cells[index]
            index += 1
        result += ' ' * 3 + ley_lines[n - i - 3] + '\n'
        result += ' ' * (2 * (l - i + 1) - 1)
        # edges
        for j in range(i + 2):
            result += '/ \\ '
        result += '/\n'
    result += ley_lines[l - 1]

    # row l
    for j in range(l + 1):
        result += ' - ' + cells[index]
        index += 1
    result += '\n' + ' ' * 5
    for j in range(l):
        result += '\\ / '
    result += '\\\n'

    # row l+1
    result += '  ' + ley_lines[l]
    for j in range(l):
        result += ' - ' + cells[index]
        index += 1
    result += ' ' * 3 + ley_lines[n - l - 2] + '\n'

    # last two lines
    result += ' ' * 4
    for j in range(l):
        result += ' ' * 3 + '\\'
    result += '\n'
    result += ' ' * 5
    for j in range(l):
        result += ' ' * 3 + ley_lines[l + 1 + j]
    result += '\n'
    return result


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
