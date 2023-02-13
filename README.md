# Sublime commands #

This repo contains Sublime Text commands that can help you edit large Canopy bulk files.

To install a plugin, put it in a `Canopy` directory in the `Sublime Text/Packages` path. The directory must be at the top level. You can add keybindings like can be found in the sample file.

The included scripts are:

* **Extract Keys**: Select text that contains links like `[[Target|Display]]` and this command will copy to your clipboard a set of definitions for all the links in the selection. This can be helpful when you write a topic paragraph with many links to subtopics that don't exist yet, because you can select the paragraph, copy to clipboard and paste stub subtopic definitions for all the referenced subtopics.

* **Quick Jump**: This command opens the quick panel with entries for every topic and subtopic definition prefixed with category path. Selecting an option will jump your cursor to the given definition.

* **Category Select**: This command is similar to quick jump except that it only lists category paths and lets you pick which one to jump to.

* **Cycle References**: When your cursor is on a topic definition key or a reference, this command will send you to the next reference in the file that has that topic for a target. Running the command repeatedly will cycle through all such references in the bulk file.

* **Jump To Definition**: When your cursor is on a reference, this command will jump to the next topic definition that matches the reference. Running it multiple times should cycle.

* **Autocomplete**: Write `[[]]` and put your cursor in the middle and then run this command to populate the quick panel with all the topics and subtopics in the project. Selecting one will insert the name of the topic or subtopic into the square brackets.

* **Pick References**: Move your cursor over a topic or reference and invoke this command to get a drop down of other references to the same target that you can jump to.
