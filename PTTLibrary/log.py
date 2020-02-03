import sys
from time import strftime

try:
    from . import lib_util
    from . import i18n
except ModuleNotFoundError:
    import lib_util
    import i18n


class Level(object):

    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4

    MinValue = TRACE
    MaxValue = SILENT


def merge(config, msg) -> str:
    if isinstance(msg, list):
        if config.language == i18n.Language.Chinese:

            for i, element in enumerate(msg):
                if len(element) == 0:
                    continue
                if element[0].upper() != element[0].lower() and i != 0:
                    msg[i] = ' ' + element.lstrip()
                if (element[-1].upper() != element[-1].lower() and
                        i != len(msg) - 1):
                    msg[i] = element.lstrip() + ' '

            msg = ''.join(msg)
        else:
            msg = ' '.join(msg)
    msg = str(msg)
    msg = msg.replace('  ', ' ')

    return msg


def log(config, log_level, msg):

    if not lib_util.check_range(Level, log_level):
        raise ValueError('log_level', log_level)

    if config.log_level > log_level:
        return
    if len(msg) == 0:
        return
    msg = merge(config, msg)

    total_message = '[' + strftime('%m%d %H:%M:%S') + ']'
    if log_level == Level.DEBUG:
        total_message += '[' + i18n.Debug + '] ' + msg
    elif log_level == Level.INFO:
        total_message += '[' + i18n.Info + '] ' + msg

    try:
        print(total_message.encode(
            sys.stdin.encoding,
            'replace'
        ).decode(
            sys.stdin.encoding
        ))
    except Exception:
        print(total_message.encode('utf-8', "replace").decode('utf-8'))

    if config.log_handler is not None:
        config.log_handler(total_message)


LastValue = None


def show_value(config, log_level, msg, value):

    if not lib_util.check_range(Level, log_level):
        raise ValueError('log_level', log_level)

    if config.log_level > log_level:
        return
    global LastValue

    if isinstance(value, list):
        value = ''.join(value)

    check_ptt_msg = merge(config, [i18n.PTT, i18n.Msg])
    msg = merge(config, msg)
    value = merge(config, value)

    if len(msg) == 0:
        return
    # if len(Value) == 0:
    #     return

    if check_ptt_msg == msg and value == LastValue:
        return

    total_message = []
    total_message.append(msg)
    total_message.append(' [')
    total_message.append(value)
    total_message.append(']')

    log(config, log_level, ''.join(total_message))

    LastValue = value