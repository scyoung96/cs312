colors = {  'blue': '027',      # blues
            'cyan': '045',
            'green': '048',     # greens
            'lime': '154',
            'yellow': '011',    # yellows
            'gold': '220',
            'orange': '202',    # oranges
            'red': '160',       # reds
            'maroon': '124',
            'magenta': '199',   # pinks
            'pink': '213',
            'violet': '129',    # purples
            'purple': '055',
            'indigo': '021',
            'black': '000',     # neutrals
            'white': '255',
            'brown': '130',
        }

def colorize(string, *args):
    '''Colorize a string. Arguments must be of type str or tuple. If tuple, the tuple must be of type (str, int), where str is a color and int is number of characters.'''
    
    string = str(string)

    typeCheck = checkArgs(args)

    if typeCheck == str:
        if len(args) == 1:
            return f'\033[38;5;{colors[args[0]]}m{string}\033[0;0m'

        else:
            strLen = len(string)
            splitLen = int(strLen / len(args))
            retStr = ''

            for i in args:
                retStr += f'\033[38;5;{colors[i]}m{string[:splitLen]}\033[0;0m'
                string = string[splitLen:]
            
            if splitLen * len(args) != strLen:
                retStr += f'\033[38;5;{colors[args[-1]]}m{string}\033[0;0m'

            return retStr

    elif typeCheck == tuple:
        retStr = ''

        for i in args:
            retStr += f'\033[38;5;{colors[i[0]]}m{string[:i[1]]}\033[0;0m'
            string = string[i[1]:]

        return retStr


def printc(string, *args):
    '''Print a string with color. Arguments must be of type str or tuple. If tuple, the tuple must be of type (str, int), where str is a color and int is number of characters.'''
   
    string = str(string)

    typeCheck = checkArgs(args)

    if typeCheck == str:
        if len(args) == 1:
            print(f'\033[38;5;{colors[args[0]]}m{string}\033[0;0m')

        else:
            strLen = len(string)
            splitLen = int(strLen / len(args))
            retStr = ''

            for i in args:
                retStr += f'\033[38;5;{colors[i]}m{string[:splitLen]}\033[0;0m'
                string = string[splitLen:]
            
            if splitLen * len(args) != strLen:
                retStr += f'\033[38;5;{colors[args[-1]]}m{string}\033[0;0m'

            print(retStr)

    elif typeCheck == tuple:
        retStr = ''

        for i in args:
            retStr += f'\033[38;5;{colors[i[0]]}m{string[:i[1]]}\033[0;0m'
            string = string[i[1]:]

        print(retStr)


def checkArgs(args):
    _type = None

    for i in args:
        if _type == None:
            _type = type(i)
        elif _type != type(i):
            raise TypeError("Arguments must be of the same type")
        
        if type(i) == tuple:
            if len(i) != 2:
                raise ValueError("Tuple arguments must have a length of 2")
            elif type(i[0]) != str or type(i[1]) != int:
                raise TypeError("Tuple arguments must be of type (str, int)")
        
        elif type(i) != str:
            raise TypeError("Arguments must be of type str or tuple")
        
        else:
            pass

    return _type
