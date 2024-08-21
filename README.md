# README

This project contains the Python files needed for reading and writing HUUM models.
It is being used so that models can be defined in data, not in code.
The main model includes code which converts a model in form of a HUUM_io object into a HUUM_model memory object.

It has _not_ been uploaded to the Python Package Index, so a manual install via pip is necessary.

The documentation of the elements, field meanings and their possible interactions, can be found in the thesis _Agent Based Modelling of city-wide Water Demand_ (not yet published).

Created by Sven Berendsen as part of his PhD project at Newcastle University, (C) 2023.
Licenced under the terms of the Apache License 2.0.


## ToDo

- Professionalise Code: Currently the code is "clean prototype" level, i.e. has little in-code documentation (but very sensible function and object names).
- Use separators to make the blocks more easily visible.
- Agents: Group habit listings by appliance, when outputting.
- Implement messaging via logger everywhere.
- Extract the common x&y table parts of translator.py, usage_pattern.py & usage_template.py.
- For generating the parameter values from the optimisation vector, only pass on what's needed.
- Use traceback package for better error messages.
- Start using "classmethod" decorators for a more concise, yet more legible code.
- Remove the need for the whole sub-paths. This also enforces internal model structure
- Review which fields are actually necessary and which ones are not. E.g. agents aren't really needed in a consumer unit.
- Find a way to elegantly define variable length output time series.
- Implement internal consistency and data checks, e.g. for duplicate item names within a node and similar.


