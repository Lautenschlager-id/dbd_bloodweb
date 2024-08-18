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




