.. _member_intent:

The Member Intent
=================

Discord recently changed what you have to do for bots to be able to access server member informaiton, meaning that without changes, calling ``guild.members`` will return an empty list, which is no good!!

To fix this, we need to do two things:

1. Enable the *Privileged Gateway Intent* for Server Members.
    a. To do this. go to the `Discord developer portal <https://discord.com/developers/applications/>`_ and select your tester bot
    b. Select the bot tab
    c. Enable the ``SERVER MEMBERS INTENT`` and the ``PRESENCE INTENT``` sliders
2. Update distest! There are also changes that need to be made on our side. They have been made, but be sure you update to 0.4.9 or newer to get the changes!

Now, you should be good to go. Have fun testing!

Quick note - For some godforsaken reason, the :py:class:`on_member_update <discord.on_member_update>` event is just horribly slow and unreliable. I'm not really sure what to do about this, but be forewarned if you want to use it!