This file representes the development guidelines inside the whale
project.

PLUGINS
=======
Generally whale plugins can provide three kind of methods:
-generators
-converters

Generators are methods that returns a set of information, eg. a
system-utils plugin can have a generator that provides the list of
current logged-in users. 
A converter is a method that returns a set of information associated
to a list of informations, eg. a system-utils plugin can have a
converter method, that given a list of users, returns the used disk
space.
For a generator we call END, the kind of information it generates. The
previous example can have "User" as END.
Similarly a converter has a START and an END.
Plugins can be combined in a pipe so that one's END matches the START
of the next one. The first is a generator.

A metod is a plugin if its name is in the form START2END. It is a
generator if its name is _2END.

Whale should be made of:
-a language (describing possible conversion of information)
-an orchestrator, that takes care of connecting different plugins and
querying the system. Furthermore the orchestrator should be able to
allow some sort of configuration, eg. different behaviours for
different cases, like interactive use, or web use, should produce
informations using different formats (json, textual, xml, ...).
-the orchestrator should also provide a trace of the intermediate
steps used to perform the calculation.



USE CASES
=========
We give here some use-cases.

whale.convert("TypeStart","TypeEnd","StartObject") should return a
list of TypeEnd objects.
w should be a shortname of whale. 
c should be a shortname of convert.
So one should be able to do w.c("TypeStart","TypeEnd","StartObject").

Similarly the should be a shortname g for generator.
Eg.: w.g("Type")

Eg. w.c("TypeStart","TypeEnd",w.g("TypeStart"))
