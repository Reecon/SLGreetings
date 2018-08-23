# Greetings

A simple queue that shows you a list of people saying hi to you.

## Installation

* Donwload zip
* Import zip into bot
* Right-click script and select `Insert API Key`

## Usage

Edit the sttings to your liking and click the `Open Queue` button.

The HTML site is a simple list that shows the user name and the message.

### Filter

You can limit the messages shown in the list by filtering for keywords or emotes. Only the first message of anyone in chat matching the criteria will be shown in the queue.

__Note:__ If someone gets purged / timed out / banned their message will be removed from the queue as well.

__Note:__ Messages matching either or both filters will be shown.

#### Keyword Filter

If the checkbox is checked, the space separated list of keywords defined in the `Keywords` field will be used to filter messages before showing them in the queue. The keyword filter is __not__ case sensitive.

#### Emote Filter

If the checkbox is checked, the space separated list of emote-codes defined in the `Emotes` fiels will be used to filter messages before showing them in the queue. The emote filter __is__ case sensitive.

### Permission

You can also limit the users who show up in the queue to Moderators, Subscribers, (Bot) Editors or individual users by setting the permission level to the desired value.
