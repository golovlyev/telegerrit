
from telegerrit.gerrit.models import CommentsWriter, UserMap


class Option(object):
    """
    Defines option for setting
    """
    def __init__(self, title, value=None):
        """
        Options used to save one of the setting
        :param title: option title
        """
        assert title and isinstance(title, basestring)

        self.title = title
        self.value = value or title

    def __cmp__(self, other):
        return self.value == other


class Setting(object):
    """
    Aggregator for options
    """

    def __init__(self, name, callback, asking_text='Enter value',
                 options=None):
        super(Setting, self).__init__()
        assert callable(callback)

        self.name = name
        self.callback = callback
        self.text = asking_text
        self.__options = options or []

    def __unicode__(self):
        return self.name

    @property
    def options(self):
        return [op.value for op in self.__options]

    @property
    def keyboard_options(self):
        return [op.title for op in self.__options]

    def next_step(self, message):
        print 'next_step', message
        option = message.text
        if self.is_valid(option):
            return self.save_results(message)
        else:
            print 'invalid option', option

    def is_valid(self, option):
        result = True
        if self.options:
            print 'option in self.options', option in self.options
            result = option in self.options
        return result

    def save_results(self, message):
        return self.callback(message)

option_enable = Option('Enable')
option_disable = Option('Disable')


def notify_comment_saver(message):
    is_notified = 1 if message.text == option_enable else 0
    chat_id = message.chat.id
    return CommentsWriter.save(chat_id, is_notified)


def username_saver(message):
    chat_id = message.chat.id
    return UserMap.set(chat_id=chat_id, gerrit_username=message.text)


settings_list = [
    Setting('Set gerrit username', username_saver, 'Enter gerrit username'),
    Setting('Notify about new comments for changes', notify_comment_saver,
            options=(option_enable, option_disable)),
    # Setting('Notify about new change', new_change_saver,
    #         option_enable, ),
]
