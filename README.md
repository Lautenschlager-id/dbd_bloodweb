# Dead By Daylight's Automatic Bloodweb Grinder

Choose which addons, items, offerings, or even perks you'd like to grind from a specific character in Dead By Daylight and the Bloodweb Grinder will automatically grind the bloodwebs for you.
<br/><br/>
**Currently only works on resolution `1920x1080` and when the game's window is positioned at the left-most side of the screen.**
<br/><br/>
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

<table>
	<thead>
		<tr>
			<th>Setting</th>
			<th>Description</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<code>parameters</code>
			</td>
			<td>
				Should be an array with the default commands to be passed whenever you execute the project.
				<ul>
					<li><i>Example: [ "-r", "survivor" ]</i></li>
				</ul>
				Note that running a command through the terminal will expand, and may override, the ones in settings.
				<ul>
					<li>
						<i>Example:</i>
						<ul>
							<li>
								If the setting is <code>["-r", "survivor"]</code> and the terminal parameter is <code>-p 1</code>:
								<ul>
									<li>Final result will be equivalent to <code>-r survivor -p 1</code></li>
								</ul>
							</li>
							<li>
								If the setting is <code>["-r", "survivor"]</code> and the terminal parameter is <code>-r trapper -p 1</code>:
								<ul>
									<li>Final result will be equivalent to <code>-r trapper -p 1</code></li>
								</ul>
							</li>
						</ul>
					</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>default_matching_threshold</code>
			</td>
			<td>
				A number in the interval [0,1] that represents OpenCV's image matching threshold.
				<br/><br/>
				The higher this number is, the more identical images must be to be matched.
				<br/>
				This setting is used to identify which nodes must be clicked in the bloodweb. <sub>(match list)</sub>
				<ul>
					<li><i>Example: 0.75</i></li>
					<li>Default: 0.75</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>default_ignore_threshold</code>
			</td>
			<td>
				A number in the interval [0,1] that represents OpenCV's image matching threshold.
				<br/><br/>
				The higher this number is, the more identical images must be to be matched.
				<br/>
				This setting is used to identify which nodes must be ignored in the bloodweb. <sub>(ignore list)</sub>
				<ul>
					<li><i>Example: 0.78</i></li>
					<li>Default: 0.78</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>grind_strategy</code>
			</td>
			<td>
				A string that defines the strategy in which the bloodweb nodes will be grinded.
				<ul>
					<li>Default: <code>default</code></li>
				</ul>
				The options are:
				<table>
					<thead>
						<tr>
							<th>Strategy</th>
							<th>Description</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td><code>priority_then_closer_to_center</code> or <code>default</code></td>
							<td>
								Nodes are selected first based on their priority (determined by their order in the match list).
								<br/>
								Among nodes with the same priority, those closer to the center of the bloodweb are selected first.
								<details>
									<summary>Example</summary>
									Example grinding:
									<ol>
										<li>Syringes</li>
										<li>Green Batteries</li>
									</ol>
									<img src='https://i.imgur.com/Mpcu63g.png' height='500' alt='example' />
								</details>
							</td>
						</tr>
						<tr>
							<td><code>priority_then_further_to_center</code></td>
							<td>
								Nodes are selected first based on their priority (determined by their order in the match list).
								<br/>
								Among nodes with the same priority, those further from the center of the bloodweb are selected first.
								<details>
									<summary>Example</summary>
									Example grinding:
									<ol>
										<li>Syringes</li>
										<li>Green Batteries</li>
									</ol>
									<img src='https://i.imgur.com/df2bvL1.png' height='500' alt='example' />
								</details>
							</td>
						</tr>
						<tr>
							<td><code>distance_closer</code></td>
							<td>
								Nodes are selected based on their proximity to the center of the bloodweb, with those closer to the center selected first.
								<details>
									<summary>Example</summary>
									Example grinding:
									<ol>
										<li>Syringes</li>
										<li>Green Batteries</li>
									</ol>
									<img src='https://i.imgur.com/6DojKfa.png' height='500' alt='example' />
								</details>
							</td>
						</tr>
						<tr>
							<td><code>distance_further</code></td>
							<td>
								Nodes are selected based on their proximity to the center of the bloodweb, with those further from the center selected first.
								<details>
									<summary>Example</summary>
									Example grinding:
									<ol>
										<li>Syringes</li>
										<li>Green Batteries</li>
									</ol>
									<img src='https://i.imgur.com/7CfntNb.png' height='500' alt='example' />
								</details>
							</td>
						</tr>
						<tr>
							<td><code>priority</code></td>
							<td>
								Nodes are selected first based on their priority (determined by their order in the match list).
								<br/>
								Among nodes with the same priority, the selection does not follow a specific sequence.
								<details>
									<summary>Example</summary>
									Example grinding:
									<ol>
										<li>Syringes</li>
										<li>Green Batteries</li>
									</ol>
									<img src='https://i.imgur.com/df2bvL1.png' height='500' alt='example' />
								</details>
							</td>
						</tr>
					</tbody>
				</table>
			</td>
		</tr>
		<tr>
			<td>
				<code>use_bloodweb_level_controller</code>
			</td>
			<td>
				Whether the Bloodweb Level Controller should be used or not.
				<ul>
					<li>Default: true</li>
				</ul>
				When the Bloodweb Level Controller is on,
				<ul>
					<li>Levels 1 to 9, and 11, are skipped automatically;</li>
					<li>The command <code>-p</code> is allowed, defining a limit to how many prestiges the system will grind.</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>disable_addon_grinding</code>
			</td>
			<td>
				Whether all addon images should be ignored.
				<ul>
					<li>Default: false</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>disable_item_grinding</code>
			</td>
			<td>
				Whether all item images should be ignored.
				<ul>
					<li>Default: false</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>disable_offering_grinding</code>
			</td>
			<td>
				Whether all offering images should be ignored.
				<ul>
					<li>Default: false</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>disable_perk_grinding</code>
			</td>
			<td>
				Whether all perk images should be ignored.
				<ul>
					<li>Default: true</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<code>log_ignored_matches</code>
			</td>
			<td>
				Whether ignored matches should be logged in <code>log.txt</code>.
				<ul>
					<li>Default: false</li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

2. All presets are placed in `/src/config/presets.json`
<ul>
	<li>A preset is an object with  addons, items, offerings, and/or perks you expect the system to grind for you.</li>
	<li>By default, there should be a preset named <code>survivor</code> that targets all survivors, and presets named after each killer targeting them and possibly their exclusive addons.</li>
	<li>Preset names must be simple texts with letters or underscores (_):
		<ul>
			<li><i>Example:</i> <code>ghost_face</code>, <code>trapper</code>, ...</li>
		</ul>
		You can also create custom presets that are not named after any survivor or killer, facilitating grinding different items depending on your needs:
		<ul>
			<li><i>Example:</i> <code>basement</code> aiming basement addons for trapper, <code>flashlight</code> aiming flashlights and batteries, ...</li>
		</ul>
	</li>
	<li>A preset is expected to have the field <code>match</code>, holding the items that must be grinded in the bloodweb.</li>
	<li>
		A preset optionally may include the field <code>ignore</code>, holding the items that must be ignored in the bloodweb.
		<br/>
		This is only useful when you notice some unexpected items are being selected because the system recognizes it as one of the items that should be grinded,
		usually because of the similarity between the images.
	</li>
	<li>
		A preset optionally may include the field <code>match_exception</code>, holding the items that must not be matched during the file filtering.
		<br/>
		This is only useful when to add exceptions to star identifiers from either <code>match</code> or <code>ignore</code>.
		<br/>
		For example, if one of them includes the record <code>offer: *</code>, that is going to include all offerings. Let's say you want <u>all but one</u>. This <u>one</u> goes in <code>match_exception</code>.
		<br/>
		That is, <code>match</code> = <code>offer: *</code>, <code>match_exception</code> = <code>offer: reagent</code>, will match all offerings, except reagents (those won't even be included in the filterable filenames).
	</li>
	<li>
		The items of a preset should be denoted as case-insensitive strings following one of the formats below:
		<ul>
			<li>
				<code>color</code> <code>object</code>: <code>identifier</code>
			</li>
			<li>
				<code>object</code>: <code>identifier</code>
			</li>
		</ul>
		<table>
			<tr>
				<td>
					<table>
						<thead>
							<tr><th>Color</th></tr>
						</thead>
						<tbody>
							<tr><td>brown</td></tr>
							<tr><td>yellow</td></tr>
							<tr><td>green</td></tr>
							<tr><td>purple</td></tr>
							<tr><td>red</td></tr>
							<tr><td>orange</td></tr>
						</tbody>
					</table>
				</td>
				<td>
					<table>
						<thead>
							<tr><th>Object</th></tr>
						</thead>
						<tbody>
							<tr><td>addon</td></tr>
							<tr><td>item</td></tr>
							<tr><td>offer</td><td>offering</td></tr>
							<tr><td>perk</td></tr>
							<tr><td>map</td><td>realm</td><td>level</td></tr>
						</tbody>
					</table>
				</td>
			</tr>
		</table>
		<ul>
			<li>
				<i>Example:</i>
				<table>
					<thead>
						<tr>
							<th>Indentifier</th>
							<th>What matches?</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td><code>red offer: ebony memento mori</code></td>
							<td>Matches the red offering 'ebony memento mori'</td>
						</tr>
						<tr>
							<td><code>red offering: ebony*mori</code></td>
							<td>Matches the red offering 'ebony memento mori'</td>
						</tr>
						<tr>
							<td><code>red offer: mori</code></td>
							<td>Matches the red offering 'ebony memento mori'</td>
						</tr>
						<tr>
							<td><code>offering: mori</code></td>
							<td>Matches all offerings with the text 'mori'</td>
						</tr>
						<tr>
							<td><code>addon: *</code></td>
							<td>Matches all addons</td>
						</tr>
					</tbody>
				</table>
			</li>
		</ul>
		If the specified identifier requires a custom threshold, that's also possible by making the value a list of two values:
			the first being the identifier string,
			and the second being the custom threshold:
		<ul>
			<li><code>"red offer: mori",</code></li>
			<li><code>[ "red offer: mori", 0.67 ],</code></li>
		</ul>
	</li>
</ul>

## Commands

### [cmd] Grind Bloodweb

Identifies and grinds bloodweb nodes displayed in the screen.

<table>
	<thead>
		<tr>
			<th>Command</th>
			<th>Syntax</th>
			<th>Usage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<li><code>--run</code></li>
				<li><code>-r</code></li>
			</td>
			<td>
				<li><code>--run</code> <code>survivor|killer_name</code></li>
                <li><code>--run</code> <code>survivor|killer_name</code> <code>custom_preset_name</code></li>
			</td>
			<td>
				<li><code>--run survivor</code></li>
                <li><code>--run trapper</code></li>
                <li><code>--run trapper custom_basement_preset</code></li>
            </td>
		</tr>
	</tbody>
</table>

#### [sub-cmd] Limit Grinding Level

Limits how many levels the system will attempt to grind.
<li>Levels are detected when the system clicks the bloodweb's center node.</li>

<table>
	<thead>
		<tr>
			<th>Command</th>
			<th>Syntax</th>
			<th>Usage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<li><code>-l</code></li>
			</td>
			<td>
				<li><code>-l</code> <code>levels</code></li>
			</td>
			<td>
                <li><code>-l 50</code></li>
            </td>
		</tr>
	</tbody>
</table>

#### [sub-cmd] Limit Grinding Prestige

Limits how many prestiges the system will attempt to grind.
<li>Prestiges are detected after the system clicks the bloodweb's center node in level 50.</li>
<li>This command requires the setting <code>use_bloodweb_level_controller</code> to be on.</li>

<table>
	<thead>
		<tr>
			<th>Command</th>
			<th>Syntax</th>
			<th>Usage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<li><code>-p</code></li>
			</td>
			<td>
				<li><code>-p</code> <code>prestiges</code></li>
			</td>
			<td>
                <li><code>-p 1</code></li>
            </td>
		</tr>
	</tbody>
</table>

### [cmd] Image Processing

Processes raw images to be used in the grinding system.
<br/>
If you are not trying to change resolutions, then probably you should not be using this command as long as `/image/processed/` is populated.

<table>
	<thead>
		<tr>
			<th>Command</th>
			<th>Syntax</th>
			<th>Usage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<li><code>--image</code></li>
				<li><code>-i</code></li>
			</td>
			<td>
				<li><code>--image</code> <code>type</code></li>
                <li><code>--image</code> <code>type</code> <code>target</code></li>
                <li><code>--image</code> <code>type</code> <code>target</code> <code>killer_name</code></li>
			</td>
			<td>
				<li><code>--image addon killer</code></li>
                <li><code>--image addon killer trapper</code></li>
                <li><code>--image perk survivor</code></li>
                <li><code>--image all</code></li>
            </td>
		</tr>
	</tbody>
</table>

<table>
	<tr>
		<td>
			<table>
				<thead>
					<tr>
						<th>Type</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<tr>
							<td><code>all</code></td>
							<td>Process all images</td>
						</tr>
						<tr>
							<td><code>addon</code></td>
							<td>Process addon images</td>
						</tr>
						<tr>
							<td><code>item</code></td>
							<td>Process item images</td>
						</tr>
						<tr>
							<td><code>offering</code></td>
							<td>Process offer images</td>
						</tr>
						<tr>
							<td><code>perk</code></td>
							<td>Process perk images</td>
						</tr>
					</tr>
				</tbody>
			</table>
		</td>
		<td>
			<table>
				<thead>
					<tr>
						<th>Target</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<tr>
							<td><code>all</code></td>
							<td>Process for all killers and survivors</td>
						</tr>
						<tr>
							<td><code>killer</code></td>
							<td>Process for all killers or specified killer</td>
						</tr>
						<tr>
							<td><code>survivor</code></td>
							<td>Process for survivors</td>
						</tr>
					</tr>
				</tbody>
			</table>
		</td>
	</tr>
</table>

### [cmd] Download content from new survivor / killer

Downloads perks and addons from a new survivor/killer.
<br/>
The content is pulled from the Dead By Daylight's Fandom Wiki.

<table>
	<thead>
		<tr>
			<th>Command</th>
			<th>Syntax</th>
			<th>Usage</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>
				<li><code>--download</code></li>
				<li><code>-d</code></li>
			</td>
			<td>
                <li><code>--download</code> <code>survivor_name|killer_name</code></li>
			</td>
			<td>
				<li><code>--download ace visconti</code></li>
                <li><code>--download the skull merchant</code></li>
                <li><code>--download skull merchant</code></li>
            </td>
		</tr>
	</tbody>
</table>

## How to use

1. Get to the folder `/src/`
```bash
$ cd bloodweb
$ cd src
```

2. Execute `main.py` with the desired command
```bash
$ python main.py -r survivor
```

### When a new survivor or killer is introduced to the game

1. Get to the folder `/src/`
```bash
$ cd bloodweb
$ cd src
```

2. Execute `main.py` with the following commands
```bash
$ python main.py -d new_survivor_name
$ python main.py -d new_killer_name
$ python main.py -i perk survivor
$ python main.py -i perk killer
$ python main.py -i addon killer new_killer_name
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