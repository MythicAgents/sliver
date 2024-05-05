# Some planning thoughts and high-level TODOs

- need to auto instantiate sessions and beacons on startup
    - should be easy, except for searching in Mythic

- would be cool that beacon results if tasked through sliver were picked up in Mythic
    - already possible by looking at Events!
    - probably won't do, will likely just use 'tasks' or something like that...

- Need a lot more work to correctly handle task results from windows implants
    - some things simply print
    - file system paths
    - should setup a testing framework
        - or a checklist for QC

- Building an implant using the GUI in Mythic might still be possible
    - optionally send an Implant config from the task
    - builder can either use the implant config, or the other build parameters?
        - don't mess with 'generate' or 'regenerate' or 'profile generate' stuff

- artifacts from spawning processes should be auto noted

- Beacon checkin status?

- 'clear' can cancel issued tasks not yet picked up by beaconers


