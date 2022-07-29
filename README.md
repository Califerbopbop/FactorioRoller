# FactorioRoller (MANDATORY SETUP INSTRUCTIONS INCLUDED)

For setup, you must go to https://www.factorio.com/download/archive/1.1.62 and download the windows .zip and extract the contents to a folder named "Factorio_x64_1.1.62" inside the distribution folder of your choice (exe is recommended so you don't have to also download python 3.10 for execution). Then cut and paste the "mods" folder downloaded in the distribution folder to the "Factorio_1.1.62" subfolder of "Factorio_x64_1.1.62". Then either execute the exe or open FactorioRoller.py with Python3.10 and the UI will open. More information on the distributions is below along with a description of how FactorioRoller works and how to use it.

FactorioRoller is an external tool written in Python + Cython for taking user specified criteria and automatically rerolling Factorio seeds until a good map is found for 100% speedrunning.

Two distributions are included in this repo, where one is the source files written in python and cython plus the compiled python extension file (pyd) that is imported and the other is an exe made from auto-py-to-exe from the python source distribution.

Included in the distributions is a Factorio mods folder with a mod that is derived from AntiElitz' "Clean Map Preview" mod which is used to generate previews of random seeds with specific RGB values for resources for efficient counting of resources. This also allows the user to have their normal instance of Factorio running while rolling maps with the tool without interference.

When executed (either through running the exe file in the exe distro or through runninng FactorioRoller.py in the python distro), a terminal window and a UI will open. The UI has a series of parameters the user can adjust to modify how FactorioRoller searches. Values are all in the form of in-game tiles (except for water and crude oil which behave differently for some reason).

The default values for the parameters are based on the current WR seed values tweaked around finding viable maps. Radius determines how many tiles away from the edges of the base blueprint FactorioRoller is allowed to search for resources, while the rest of the parameters are based on the footprint of blueprints. The default base and power plant parameters are based on the Nefrums/AntiElitz blueprints included in Nefrums' PB on Speedrun.com. The four rotations of the base and power plant are checked and the starting area is the rectangle between the power plant and the base in each orientation. I originally included support for mirroring the power plant, but it turns out to not really be worth the extra 4 checks vs how often it results in a map becoming good, so I commented out that feature.

The use of the batch generation feature is greatly encouraged as it allows the tool to generate multiple seeds without having to relaunch Factorio in headless mode for every single seed. On my PC it takes about 1 sec for Factorio to launch and 1 sec to generate each preview, so running with batches cuts the generation time in half. I'm sure results will vary a lot with processor, RAM, and SSD specs.

The default parameters find what FactorioRoller deems to be a "good map" about 0.8% of the time (~1 in every 125 maps). FactorioRoller generates the total batch size before running any analysis, so I would reccommend setting batch to something like 100-200 to keep from wasting time generating extra maps for a ~1 sec time cost per batch generation. If batch is set higher than max rerolls nothing bad happens, but you will waste time generating extra maps that will not get analyzed.

There's a folder included in each distribution with a series of seeds that FactorioRoller deemed good with the default parameters. I would appreciate review of these for feedback on if these are actually playable or if the default settings should be changed in future iterations. This is very much a work in progress that I'm looking for any kind of feedback on. The UI is certainly not pretty and is likely missing features that users will want, feedback here would be much appreciated.

The interface includes the ability to save your current input parameters as custom settings that will persist and can be loaded from the interface buttons. Note that this will override the previously saved custom settings.

This repository will be shared in the Steel Axe discord and I can be reached by my discord info there for feedback.

Here's a PayPal donation link for the generous who feel I saved them some time either playing 100% or watching someone play it: https://www.paypal.com/donate/?business=KEVFH97J37BPE&no_recurring=1&currency_code=USD
