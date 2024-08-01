import requests
import os
import time
import re

# List of image URLs
# Array[ Array[ str ] ] -> [template_id][N]
urls = [[
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/f/fe/IconPerks_aNursesCalling.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/ac/IconPerks_agitation.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/34/IconPerks_alienInstinct.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/97/IconPerks_awakenedAwareness.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/7/7a/IconPerks_bamboozle.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/51/IconPerks_barbecueAndChilli.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1c/IconPerks_batteriesIncluded.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/7/77/IconPerks_beastOfPrey.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/5a/IconPerks_bitterMurmur.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c3/IconPerks_bloodEcho.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/eb/IconPerks_bloodWarden.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/e0/IconPerks_bloodhound.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/3d/IconPerks_brutalStrength.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/3b/IconPerks_callOfBrine.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/10/IconPerks_corruptIntervention.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/45/IconPerks_coulrophobia.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/bd/IconPerks_coupDeGr%C3%A2ce.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c6/IconPerks_cruelLimits.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b1/IconPerks_darkArrogance.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/4f/IconPerks_darkDevotion.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/ed/IconPerks_darknessRevealed.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c3/IconPerks_deadMansSwitch.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/d3/IconPerks_deadlock.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/e7/IconPerks_deathbound.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/01/IconPerks_deerstalker.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/8/82/IconPerks_discordance.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1d/IconPerks_dissolution.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/94/IconPerks_distressing.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/f/ff/IconPerks_dragonsGrip.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/48/IconPerks_dyingLight.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/94/IconPerks_enduring.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/dd/IconPerks_eruption.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/5c/IconPerks_fireUp.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/4c/IconPerks_forcedHesitation.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1d/IconPerks_forcedPenance.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b2/IconPerks_franklinsDemise.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b3/IconPerks_friendsTilTheEnd.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/94/IconPerks_furtiveChase.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/53/IconPerks_gameAfoot.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/f/fd/IconPerks_gearhead.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6d/IconPerks_geneticLimits.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1c/IconPerks_grimEmbrace.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6b/IconPerks_hexBloodFavour.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/f/f1/IconPerks_hexCrowdControl.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c9/IconPerks_hexDevourHope.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/af/IconPerks_hexFaceTheDarkness.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c4/IconPerks_hexHauntedGround.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/11/IconPerks_hexHuntressLullaby.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/af/IconPerks_hexNoOneEscapesDeath.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/5d/IconPerks_hexPentimento.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/18/IconPerks_hexPlaything.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/ab/IconPerks_hexRetribution.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a2/IconPerks_hexRuin.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/36/IconPerks_hexTheThirdSeal.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/02/IconPerks_hexThrillOfTheHunt.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/64/IconPerks_hexTwoCanPlay.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/f/fe/IconPerks_hexUndying.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/2/23/IconPerks_hoarder.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/aa/IconPerks_hubris.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/3a/IconPerks_hysteria.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/e3/IconPerks_imAllEars.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6d/IconPerks_infectiousFright.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/40/IconPerks_insidious.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/14/IconPerks_ironGrasp.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b0/IconPerks_ironMaiden.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/52/IconPerks_knockOut.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a3/IconPerks_languidTouch.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/61/IconPerks_lethalPursuer.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c6/IconPerks_leverage.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/48/IconPerks_lightborn.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1c/IconPerks_blastMine.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/01/IconPerks_machineLearning.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/da/IconPerks_madGrit.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6b/IconPerks_makeYourChoice.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/36/IconPerks_mercilessStorm.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/0f/IconPerks_mindbreaker.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/60/IconPerks_monitorAndAbuse.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/33/IconPerks_nemesis.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/bb/IconPerks_noWayOut.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/2/29/IconPerks_nowhereToHide.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a1/IconPerks_oppression.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/c/c3/IconPerks_overcharge.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/9a/IconPerks_overwhelmingPresence.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/18/IconPerks_playWithYourFood.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/0f/IconPerks_popGoesTheWeasel.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/7/73/IconPerks_predator.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a2/IconPerks_rancor.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/d4/IconPerks_rapidBrutality.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/62/IconPerks_rememberMe.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6a/IconPerks_saveTheBestForLast.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/1c/IconPerks_scourgeHookFloodsOfRage.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/2/26/IconPerks_scourgeHookGiftOfPain.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/9a/IconPerks_scourgeHookHangmansTrick.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/91/IconPerks_scourgeHookMonstrousShrine.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/7/79/IconPerks_scourgeHookPainResonance.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/d8/IconPerks_septicTouch.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/ac/IconPerks_shadowborn.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/aa/IconPerks_shatteredHope.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/5a/IconPerks_sloppyButcher.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b1/IconPerks_spiesFromTheShadows.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a6/IconPerks_spiritFury.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/6/6e/IconPerks_starstruck.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/32/IconPerks_stridor.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/4a/IconPerks_superiorAnatomy.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/3/3b/IconPerks_surge.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/e/eb/IconPerks_surveillance.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/bb/IconPerks_thwack.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/4/4c/IconPerks_terminus.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/2/2a/IconPerks_territorialImperative.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a2/IconPerks_thanatophobia.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/b8/IconPerks_thrillingTremors.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/d9/IconPerks_tinkerer.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/94/IconPerks_trailOfTorment.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/8/8a/IconPerks_ultimateWeapon.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/9/91/IconPerks_unbound.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/1/11/IconPerks_undone.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/0/0c/IconPerks_unforeseen.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/a/a4/IconPerks_unnervingPresence.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/5/57/IconPerks_unrelenting.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/de/IconPerks_weaveAttunement.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/b/bb/IconPerks_whispers.png",
    "https://static.wikia.nocookie.net/deadbydaylight_gamepedia_en/images/d/d3/IconPerks_zanshinTactics.png"
]]

# Directory to save downloaded files
download_dir = '.\\images\\originals\\perks\\killers'

# Maximum number of retry attempts
max_retries = 10

def sanitize_filename(filename):
    # Remove or replace invalid characters for filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Function to download a single file with retry logic
count = 0

def download_file(url, dir, filename, attempt=1):
    global count

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        sanitized_filename = sanitize_filename(filename)
        filepath = os.path.join(dir, sanitized_filename)

        # Save the file
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        count = count + 1
        print(f'[{count}] Successfully downloaded {filename}')
    except requests.RequestException as e:
        print(f'Error downloading {filename}: {e}')
        if attempt < max_retries:
            print(f'Retrying ({attempt}/{max_retries})...')
            time.sleep(2)  # Wait before retrying
            download_file(url, filename, attempt + 1)  # Retry
        else:
            print(f'Failed to download {filename} after {max_retries} attempts.')

# Function to download all files from the array
def download_all_files():
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for ls in range(len(urls)):
        if not os.path.exists(f'{download_dir}\\template_{ls+1}'):
            os.makedirs(f'{download_dir}\\template_{ls+1}')

        for url in urls[ls]:
            filename = url.split('/')[7].split('.')[0]  # Extract the filename from the URL
            download_file(url, f'{download_dir}\\template_{ls+1}', f'{filename}.webp')

# Start the download process
if __name__ == '__main__':
    download_all_files()
