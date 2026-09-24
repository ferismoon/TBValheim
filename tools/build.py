"""Regenerate static pages from the shipped pack archive; standard library only."""
from pathlib import Path
import re, json, zipfile, html, sys
ROOT = Path(__file__).resolve().parents[1]
DISCORD = 'https://discord.com/channels/659137486332887071/1054946454545907762'
def esc(value): return html.escape(str(value), quote=True)
def page(file, title, body, hero=False):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if file==url else '')+f'>{name}</a>' for url,name in [('index.html','Overview'),('install.html','Install'),('mods.html','Mods'),('changelog.html','Changelog')])
    markup = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="True Bastards Valheim: a survival mod pack for friends. Installation, included mods and release notes."><title>{esc(title)} · True Bastards Valheim</title><link rel="stylesheet" href="assets/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="topbar"><a class="brand" href="index.html">TRUE BASTARDS <span>/ VALHEIM</span></a><nav aria-label="Main navigation">{nav}<a href="{DISCORD}">Discord ↗</a></nav></header>
{body if hero else '<main id="main">'+body+'</main>'}
<footer><p>True Bastards · Valheim pack 1.0</p><p><a href="{DISCORD}">Downloads &amp; server details on Discord ↗</a></p></footer>
{'<script src="assets/mods.js"></script>' if file=='mods.html' else ''}</body></html>'''
    (ROOT/file).write_text(markup,encoding='utf-8')

page('index.html','Overview',f'''<div class="hero"><div class="eyebrow">A Valheim survival pack · Version 1.0</div><h1>A place to build.<br>A reason to venture out.</h1><p>Familiar survival, more equipment to discover, and fewer fiddly chores. Built for the True Bastards crew.</p><div class="actions"><a class="button" href="install.html">Get ready to join →</a><a class="button secondary" href="mods.html">Explore the mods</a></div></div>
<main id="main"><div class="eyebrow">Our kind of Valheim</div><h2>Keep the adventure. Smooth the rough edges.</h2><p class="intro">Gather supplies, haul them home, build something worth defending and head out together. This pack stays close to the rhythm of Valheim, with extra loot, weapons and quality-of-life features along the way.</p>
<div class="grid"><section class="card"><span class="number">01 / EXPLORE</span><h3>Make the journey count.</h3><p>Backpacks, a hip lantern and travel improvements help on longer trips. Gathering resources and getting them home still matter.</p></section><section class="card"><span class="number">02 / FIGHT</span><h3>Find your next favourite.</h3><p>Epic Loot, new weapons and armour, and enemies with extra stars and modifiers give you more to discover and prepare for.</p></section><section class="card"><span class="number">03 / SETTLE</span><h3>Build a proper home.</h3><p>Better building controls, easier repairs, planting tools and clearer item information make the everyday work more comfortable.</p></section></div>
<div class="split"><section><h2>Progress at your own pace.</h2><p class="muted">Boss progression is tracked per character. Someone else defeating a boss does not automatically give your character the same unlocks. Some equipment and activities stay locked until you earn the required progress.</p><p class="muted">Joining with an older character? Tell us in Discord if you have already beaten bosses but your gear is being rejected.</p></section><section class="card"><div class="eyebrow">Before you sail</div><h3>One shared pack.</h3><p>Use the version posted in our Valheim Discord channel so your mods and settings match the server.</p><a href="{DISCORD}">Open the Valheim channel ↗</a></section></div>
<section class="band"><h2>First release · 1.0</h2><p>The starting pack brings together equipment, progression and practical quality-of-life changes.</p><a href="changelog.html">Read the release notes →</a></section></main>''',True)

page('install.html','Installation',f'''<div class="eyebrow">Join the crew</div><h1 class="page-title">Ready for the next voyage?</h1><p class="intro">The pack download and server address are in our <a href="{DISCORD}">Valheim Discord channel</a>. You must already have access to the True Bastards Discord to open the channel.</p>
<section class="band"><strong>Windows / Steam · Pack 1.0</strong><p>This guide is for the supplied <code>ValheimModPack_1.0.zip</code>. Use the whole pack so you get our settings and included compatibility patch.</p></section>
<div class="split"><section><h2>Install the supplied ZIP</h2><ol class="steps"><li><strong>Install and launch Valheim once.</strong><p>Close the game before adding the pack.</p></li><li><strong>Download the pack from Discord.</strong><p>Get the current ZIP from the Valheim channel and extract it somewhere easy to find.</p></li><li><strong>Open your Valheim game folder.</strong><p>In Steam, right-click Valheim → Manage → Browse local files. This is the folder containing <code>valheim.exe</code>.</p></li><li><strong>Copy the extracted contents into that folder.</strong><p>The <code>BepInEx</code> folder, <code>winhttp.dll</code> and <code>doorstop_config.ini</code> belong beside <code>valheim.exe</code>, not inside another pack folder. Merge folders and replace the pack’s matching files when asked.</p></li><li><strong>Launch Valheim through Steam.</strong><p>Let the first modded launch finish. Find the server address and joining details in Discord, then connect.</p></li></ol></section>
<aside><section class="card"><h3>Already using mods?</h3><p>Use a clean installation or a separate profile. Adding the pack over unrelated mods can leave extras behind.</p><p>If you use Thunderstore Mod Manager, create a dedicated Valheim profile, open its folder through Settings → Browse profile folder, copy the bundle contents there, and use <strong>Start modded</strong>.</p><p>This ZIP is a folder bundle, not a profile-code export. Don’t use “Import local mod” for it.</p></section><section class="card"><h3>Updating the pack</h3><p>Check Discord and the changelog before updating. Follow any removal instructions; copying new files alone does not remove old mods.</p><p>Keep your version aligned with the server rather than updating individual mods separately.</p></section></aside></div>
<h2>A few useful controls</h2><table><thead><tr><th>Action</th><th>Pack binding</th></tr></thead><tbody><tr><td>Lantern light</td><td>K</td></tr><tr><td>Lantern heat</td><td>Alt + K</td></tr><tr><td>Backpack wisplight</td><td>L</td></tr><tr><td>Open backpack</td><td>I</td></tr><tr><td>Mod configuration</td><td>F1</td></tr></tbody></table>
<section class="band"><h2>Something isn’t right?</h2><p>Post in the Valheim channel with what happened, your pack version and any error message. If “The Gods Reject You” appears on an older character, mention which bosses you already defeated.</p><a href="{DISCORD}">Get help in Discord ↗</a></section>''')

descriptions = {
'PlantEverything':('Building & home','Plant Everything','More planting options for gardens and the land around your base.'),
'SeedBed':('Building & home','Seed Bed','Adds seed beds for your farming setup.'),
'VikingsDoSwim':('Travel & utility','Vikings Do Swim','Expands swimming controls, including diving.'),
'SearsCatalog':('Building & home','Sears Catalog','Makes larger building menus easier to browse.'),
'Pathfinder':('Travel & utility','Pathfinder','Adjusts exploration and map discovery.'),
'Better_Wisps':('Travel & utility','Better Wisps','Improves the usefulness of wisps in the mist.'),
'Digitalroots_Slope_Combat_Assistance':('Combat & equipment','Slope Combat Assistance','Helps melee attacks connect when fighting on slopes.'),
'Max_Dungeon_Rooms':('Combat & equipment','Max Dungeon Rooms','Changes dungeon room limits for dungeon generation.'),
'Blacksmiths_tools':('Libraries & support','Blacksmith’s Tools','Support tools used by Jude’s equipment mods.'),
'Judes_Equipment':('Combat & equipment','Jude’s Equipment','Adds more equipment to discover and craft.'),
'ValheimArmory':('Combat & equipment','Valheim Armory','More weapon choices across your adventure.'),
'EpicLoot':('Combat & equipment','Epic Loot','Adds magical equipment, enchantments and loot to hunt for.'),
'HipLantern':('Travel & utility','Hip Lantern','A wearable light with a separate heat mode.'),
'TradersExtended':('Travel & utility','Traders Extended','Expands trader interactions, including equipment repairs.'),
'AdventureBackpacks':('Travel & utility','Adventure Backpacks','Adds wearable backpacks and associated utility features.'),
'Venture_Area_Repair':('Building & home','Venture Area Repair','Makes repairing nearby building pieces less repetitive.'),
'Venture_Farm_Grid':('Building & home','Venture Farm Grid','Helps arrange crops with consistent spacing.'),
'Venture_Floating_Items':('Travel & utility','Venture Floating Items','Makes dropped items float so they are easier to recover from water.'),
'Venture_Logout_Tweaks':('Travel & utility','Venture Logout Tweaks','Adjusts logout behaviour.'),
'Daywheel':('Travel & utility','Daywheel','Adds an at-a-glance display of the day’s progress.'),
'Reely_Good_Rod':('Travel & utility','Reely Good Rod','Quality-of-life adjustments for fishing.'),
'Warm_Torches':('Travel & utility','Warm Torches','Adds warmth to carried torches.'),
'EpicLoot_ProgressionFix':('Progression','Epic Loot Progression Fix','Compatibility fixes for Epic Loot progression.'),
'World_Advancement_Progression':('Progression','World Advancement Progression','Tracks individual progress and gates equipment and activities behind boss kills.'),
'Need_For_Speed':('Travel & utility','Need for Speed','Makes travel along prepared paths more useful.'),
'AdvancedPortals':('Travel & utility','Advanced Portals','Adds portal tiers with different transport capabilities.'),
'StarLevelSystem':('Combat & equipment','Star Level System','Adds configurable creature stars, modifiers and raids.'),
'ZenSign':('Building & home','ZenSign','More useful signs for organising your base.'),
'ZenHoverItem':('Travel & utility','ZenHoverItem','Clearer information about items, containers and fuel when you look at them.'),
'ZenDistributor':('Building & home','ZenDistributor','Cart and distribution conveniences. The pack does not use its cart weight assistance.'),
'ZenBeehive':('Building & home','ZenBeehive','Easier manual collection from beehives.'),
'ZenRedecorate':('Building & home','ZenRedecorate','Move placed objects when rearranging your base.'),
'ZenConstruction':('Building & home','ZenConstruction','Building controls and nearby-container conveniences, with vanilla structural rules retained.'),
'BepInExPack_Valheim':('Libraries & support','BepInExPack Valheim','The loader that runs the pack’s mods.'),
'Jotunn':('Libraries & support','Jötunn','Shared support for custom items, building pieces and other mod features.'),
'JsonDotNET':('Libraries & support','Json.NET','A shared data library required by other mods.'),
'YamlDotNet':('Libraries & support','YamlDotNet','A shared configuration library required by other mods.'),
'ConditionalConfigSync':('Libraries & support','Conditional Config Sync','Supports synchronising mod settings.'),
'ConfigurationManager':('Libraries & support','Configuration Manager','An in-game interface for changing mod settings.'),
'Zen_ModLib':('Libraries & support','Zen ModLib','Shared support for the installed Zen mods.')}

if len(sys.argv)>1:
    archive=Path(sys.argv[1])
    with zipfile.ZipFile(archive) as z:
        raw=z.read('mods.yml').decode('utf-8-sig')
        mods=[]
        for block in re.split(r'^- manifestVersion:',raw,flags=re.M)[1:]:
            if not re.search(r'^  enabled: true$',block,re.M): continue
            full=re.search(r'^  name: (.+)$',block,re.M)[1].strip()
            author,name=full.split('-',1)
            cat,label,desc=descriptions[name]
            version='.'.join(re.search(r'^    '+part+r': (\d+)$',block,re.M)[1] for part in ['major','minor','patch'])
            mods.append(dict(name=label,category=cat,description=desc,version=version,url=f'https://thunderstore.io/c/valheim/p/{author}/{name}/'))
        assert any('TrueBastards.ProgressionBridge.dll' in n for n in z.namelist())
    (ROOT/'mods.json').write_text(json.dumps(mods,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
else:
    mods=json.loads((ROOT/'mods.json').read_text(encoding='utf-8'))
cards=''
for mod in sorted(mods,key=lambda x:(x['category'],x['name'].lower())):
    cards+=f'''<article class="card mod" data-mod data-category="{esc(mod['category'])}"><div class="meta">{esc(mod['category'])} · {esc(mod['version'])}</div><h2>{esc(mod['name'])}</h2><p>{esc(mod['description'])}</p><a href="{esc(mod['url'])}">View on Thunderstore ↗</a></article>'''
categories=''.join(f'<option>{esc(c)}</option>' for c in sorted({m['category'] for m in mods}))
page('mods.html','Included mods',f'''<div class="eyebrow">The pack, piece by piece</div><h1 class="page-title">What’s on board.</h1><p class="intro">The mods included in pack 1.0, with links to their own pages. Our pack settings may differ from a mod’s defaults. Use the Discord download to get the complete setup.</p><div class="filters"><label>Search mods<input id="search" type="search" placeholder="Try building, loot or backpacks…"></label><label>Category<select id="category"><option value="">All categories</option>{categories}</select></label></div><p id="count" class="muted" role="status">{len(mods)} mods</p><p id="empty" hidden>No matches. Try another search or category.</p><div class="mod-grid">{cards}</div><section class="band"><h2>Included pack compatibility patch</h2><p><strong>TrueBastards Progression Bridge 0.1.0</strong> connects Star Level System’s raid checks with individual World Advancement Progression keys. It comes with the pack and has no public Thunderstore page.</p></section>''')

page('changelog.html','Changelog','''<div class="eyebrow">The captain’s log</div><h1 class="page-title">What’s changed.</h1><p class="intro">Pack releases and the changes that matter when you play. Download the current version from our Valheim Discord channel.</p><article class="release" id="release-1-0"><div class="eyebrow">24 September 2026 · Initial release</div><h2>1.0 — Ready to set sail</h2><ul><li>Added Epic Loot, Valheim Armory and Jude’s Equipment for more loot and equipment choices.</li><li>Added Star Level System for creature stars, modifiers and raids.</li><li>Introduced individual boss progression through World Advancement Progression, with the pack’s progression bridge included.</li><li>Added building, farming, repair, storage and travel conveniences, including backpacks and a hip lantern.</li><li>Kept vanilla building support rules and removed ZenDistributor’s cart weight assistance.</li><li>Kept trader repairs available and set the hip lantern controls to K for light and Alt + K for heat.</li><li>Tuned the troll raid down: fewer trolls, no extra stars or modifiers, and an Elder progression requirement.</li></ul><p><a href="mods.html">Browse the complete mod list →</a></p></article><section class="band"><h2>Keeping everyone together</h2><p>Use the pack version announced in Discord. Any future update that needs extra installation steps will be called out here.</p></section>''')
print(f'Built four pages with {len(mods)} Thunderstore entries and one pack compatibility patch.')
