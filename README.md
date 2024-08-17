# Dead By Daylight's Automatic Bloodweb Grinder

Choose which addons, items, offerings, or even perks you'd like to grind from a specific character in Dead By Daylight and the Bloodweb Grinder will automatically grind the bloodwebs for you.
<br/>
<br/>
**Use at your own risk.**

## Installation

1. Clone the project into your local machine
```git
git clone https://github.com/Lautenschlager-id/dbd_bloodweb/
```

2. Install the requirements
```bash
$ cd bloodweb
$ pip install -r requirements.txt
```

3. Install [Tesseract's latest version](https://github.com/UB-Mannheim/tesseract/releases)


## Configuration

1. All settings are placed in `/src/config/settings.json`
	* Setting `parameters` should be an array with the default commands to be passed whenever you execute the project.
		* _Example: [ "-r", "survivor" ]_

	* Setting `default_matching_threshold` is a number in the interval [0,1] that represents OpenCV's image matching threshold.
		The higher this number is, the more identical images must be to be matched.
		This setting is used to identify which nodes must be clicked in the bloodweb. (match list)
		* _Example: 0.75_
		* Default: 0.75

	* Setting `default_ignore_threshold` is a number in the interval [0,1] that represents OpenCV's image matching threshold.
		The higher this number is, the more identical images must be to be matched.
		This setting is used to identify which nodes must be ignored in the bloodweb. (ignore list)

	* Setting `grind_strategy` defines the strategy in which the bloodweb will be grinded.
		The options are:
		* `priority_then_closer_to_center` or `default`: Nodes are selected first based on their priority (determined by their order in the match list). Among nodes with the same priority, those closer to the center of the bloodweb are selected first.
			* Example grinding:
				* #1 Syringes
				* #2 Green Batteries
			<img src='https://i.imgur.com/Mpcu63g.png' height='500' alt='example' />
		* `priority_then_further_to_center`: Nodes are selected first based on their priority (determined by their order in the match list). Among nodes with the same priority, those further from the center of the bloodweb are selected first.
			* Example grinding:
				* #1 Syringes
				* #2 Green Batteries
			<img src='https://i.imgur.com/df2bvL1.png' height='500' alt='example' />
		* `distance_closer`: Nodes are selected based on their proximity to the center of the bloodweb, with those closer to the center selected first.
			* Example grinding:
				* #1 Syringes
				* #2 Green Batteries
			<img src='https://i.imgur.com/6DojKfa.png' height='500' alt='example' />
		* `distance_further`: Nodes are selected based on their proximity to the center of the bloodweb, with those further from the center selected first.
			* Example grinding:
				* #1 Syringes
				* #2 Green Batteries
			<img src='https://i.imgur.com/7CfntNb.png' height='500' alt='example' />
		* `priority`: Nodes are selected first based on their priority (determined by their order in the match list). Among nodes with the same priority, the selection does not follow a specific sequence.
			* Example grinding:
				* #1 Syringes
				* #2 Green Batteries
			<img src='https://i.imgur.com/df2bvL1.png' height='500' alt='example' />




## How to use

1. Get to the folder `/src/`
```bash
$ cd bloodweb
$ cd src
```

2. Execute `main.py`
```bash
$ python main.py
```

## Collaborate

1. Fork the project

2. Create a new branch
```bash
$ cd bloodweb
$ git checkout master
$ git checkout -b feature_name
```

3. Open up a Pull Request


## Development details





# recall
template = 1 to 6, 1=brown, 6=event;
icon = main image, not the background
background = template image, e.g. template_1 = brown bg

_evaluate_custom_resource_icon_template = reuse originals from one specific template_ but keep generating for other templates too
e.g. for perks, images are in template_1, then it pulls the icon from template_1, but uses background etc from template_N


match_list matches
ignore_list also matches, but blocks that space from being matched on match_list items




