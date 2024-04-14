# sliver

This is a set of [Mythic](https://docs.mythic-c2.net/) agents for interacting with [Sliver](https://sliver.sh/) C2 framework.

- `sliverapi`: for interacting with the sliver server (ie: start listeners, list sessions...etc)
- `sliverimplant`: for interacting with a sliver implant (ie: ps, netstat...etc)

The `sliverapi` payload doesn't build anything, but instead generates a "callback" within Mythic that allows you to interact with Sliver's API. This requires you to generate an [operator configuration file](https://sliver.sh/docs?name=Multi-player+Mode). This config file is the only build parameter, and once built, a callback will immediately appear and you can start tasking like normal.

A `sliverimplant` callback is instantiated when tasking a `use -id <sliver_implant_id>` from within the sliverapi callback. 

Checkout this [blog](./blog/blog.md) about my experience creating them.

### Quick Start

This assumes that sliver is installed and running.

```sh
# Generate Sliver Operator Config
sudo /root/sliver-server operator --name mythic --lhost <ip> --save mythic.cfg && sudo chown $USER:$USER mythic.cfg

# Install Agents into Mythic
cd /path/to/Mythic
# Ensure latest updates are there
git pull && sudo make && sudo ./mythic-cli start
# WARNING: This currently takes several minutes due to a grpc bug
sudo ./mythic-cli install github https://github.com/spenceradolph/sliver

# Browse to Mythic and Generate a Payload, select 'sliver' as the OS
# Upload the mythic.cfg file, continue through prompts and generate
```

## Future Plans / Ideas

- Mythic Supported UI
  - process browser ✅
    - task kill ✅
  - file browser 🐞 (buggy)
    - file download ✅
    - file upload ✅
    - file remove ✅
  - screenshots 🐞
  - artifacts
  - Interactive Tasking (shell) 🚧🐞 (buggy)
- Beacon checkin status
- Documentation-payload
- Build implants through Mythic ('generate' + UI)
- Sliver 3rd party integrations
- Stretch Goal: Ability to run the sliver server within mythic
- Stretch Goal: V2 everything in go💙 (match sliver official client code)

<details>
  <summary>Server Commands</summary>

    - clear
    - exit
    - help
    - monitor
    - wg-config
    - wg-portfwd
    - wg-socks
    - aliases
    - armory
    - background
    - beacons✅
    - builders
    - canaries
    - cursed
    - dns
    - env
    - generate
    - hosts
    - http
    - https
    - implants✅
    - jobs✅
    - licenses
    - loot
    - mtls✅
    - prelude-operator
    - profiles✅
    - reaction
    - regenerate
    - sessions✅
    - settings
    - stage-listener
    - tasks
    - update
    - use✅
    - version
    - websites
    - wg
    - operators
</details>

<details>
  <summary>Implant Commands</summary>

    - cat✅
    - cd✅
    - chmod
    - chown
    - chtimes
    - close
    - download✅
    - execute✅
    - execute-shellcode
    - extensions
    - getgid✅
    - getpid✅
    - getuid✅
    - ifconfig✅
    - info✅
    - interactive
    - kill
    - ls✅
    - memfiles
    - mkdir✅
    - msf
    - msf-inject
    - mv
    - netstat✅
    - ping✅ (session only)
    - pivots
    - portfwd
    - procdump
    - ps✅
    - pwd✅
    - reconfig (beacon only)
    - rename
    - rm✅
    - rportfwd
    - screenshot✅
    - shell✅ (session only)
    - shikata-ga-nai
    - sideload
    - socks5
    - ssh
    - tasks (beacon only)
    - terminate✅
    - upload✅
    - whoami✅
</details>

## How to install an agent in this format within Mythic

When it's time for you to test out your install or for another user to install your agent, it's pretty simple. Within Mythic is a `mythic-cli` binary you can use to install agents:

- `sudo ./mythic-cli install github https://github.com/user/repo` to install the main branch
- `sudo ./mythic-cli install github https://github.com/user/repo branchname` to install a specific branch of that repo

Now, you might be wondering _when_ should you or a user do this to properly add your agent to their Mythic instance. There's no wrong answer here, just depends on your preference. The three options are:

- Mythic is already up and going, then you can run the install script and just direct that agent's containers to start (i.e. `sudo ./mythic-cli payload start agentName` and if that agent has its own special C2 containers, you'll need to start them too via `sudo ./mythic-cli c2 start c2profileName`).
- Mythic is already up and going, but you want to minimize your steps, you can just install the agent and run `sudo ./mythic-cli mythic start`. That script will first _stop_ all of your containers, then start everything back up again. This will also bring in the new agent you just installed.
- Mythic isn't running, you can install the script and just run `sudo ./mythic-cli mythic start`.

## Local Development Notes

- VSCode devcontainer
  - If using vscode, it will prompt to auto build and attach to the Docker file
    - Warning: building the container takes a few minutes!
  - Auto adds the suggested extensions / settings
  - Use the debugger for breakpoints! (and easy restart of the main.py process)

- Required commands for local development against remote mythic

```bash
# In Mythic
sudo ./mythic-cli config set rabbitmq_bind_localhost_only false
sudo ./mythic-cli config set mythic_server_bind_localhost_only false
sudo ./mythic-cli restart

# get the RABBITMQ_PASSWORD from .env and paste into a rabbitmq_config.json
# In this repo
cd ./Payload_Type/sliverapi
cp rabbitmq_config.json.example rabbitmq_config.json
```

I am running both Mythic and Sliver in the same Ubuntu 22 VM, but running the Agent container externally in a docker container.

Once inside the container and rabbitmq set, this will run the agent side and update Mythic.

```bash
# or instead of running manually, hit the debug play button in vscode!
cd ./Payload_Type/sliverapi/
python3 main.py
```

Another note: the sliverimplant Dockerfile is built from the sliverapi .docker
