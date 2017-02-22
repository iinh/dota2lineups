window.onload = function(){
    fillMatches('wins'); // Default sorting
};

function fillMatches(sorting){
    var matchesShown = 20;
    var contentField;
    var number;
    var lineup;
    var wins;
    var losses;
    var winRate;
    var p_number;
    var p_lineup;
    var p_wins;
    var p_losses;
    var p_winRate;
    var lineup;
    var id;
    var matchesParsed;
    var p_matchesParsed;

    var xhttp = new XMLHttpRequest();
    var data = new FormData();
    data.append('sorting', sorting)
    var url = '/show_matches';
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            res = JSON.parse(this.responseText);
            console.log(res.success);
            console.log(res);

            if (res.success){
                for (var i = 0; i < matchesShown; i++){
                    contentField = document.createElement("div");
                    contentField.className = "content_field";

                    // add list index (1 to 20)
                    var id = (i+1).toString() + '.';
                    number = document.createElement("div");
                    number.className = "number";
                    p_number = document.createElement("p");
                    p_number.textContent = id;
                    p_number.className = "small_text";
                    number.appendChild(p_number);

                    // add lineup string
                    lineupstring = convertLineUp(res.data[i].lineup);
                    lineup = document.createElement("div");
                    lineup.className = "lineup";
                    p_lineup = document.createElement("p");
                    p_lineup.textContent = lineupstring;
                    p_lineup.className = "small_text";
                    lineup.append(p_lineup);

                    // add wins string
                    wins = document.createElement("div");
                    wins.className = "wins";
                    p_wins = document.createElement("p");
                    p_wins.textContent = res.data[i].wins;
                    p_wins.className = "small_text";
                    wins.appendChild(p_wins);

                    // add losses string
                    losses = document.createElement("div");
                    losses.className = "losses";
                    p_losses = document.createElement("p");
                    p_losses.textContent = res.data[i].losses;
                    p_losses.className = "small_text";
                    losses.appendChild(p_losses);

                    // add winrate string
                    winRate = document.createElement("div");
                    winRate.className = "winrate";
                    p_winRate = document.createElement("p");
                    p_winRate.textContent = res.data[i].win_rate;
                    p_winRate.className = "small_text";
                    winRate.appendChild(p_winRate);

                    // put them all in a single match div
                    contentField.appendChild(number);
                    contentField.appendChild(lineup);
                    contentField.appendChild(wins);
                    contentField.appendChild(losses);
                    contentField.appendChild(winRate);
                    document.getElementById("content_matches").appendChild(contentField);
                }

                    // add counter of matches parsed
                    matchesParsed = document.createElement("div");
                    matchesParsed.className = "lineup";
                    p_matchesParsed = document.createElement("p");
                    p_matchesParsed.textContent = res.matches_parsed + ' matches parsed.';
                    p_matchesParsed.className = "small_text";
                    matchesParsed.appendChild(p_matchesParsed);
                    document.getElementById("content_matches").appendChild(matchesParsed);
                }
                else{
                    // Hijack the lineup field to show an error message.
                    contentField = document.createElement("div");
                    contentField.className = "content_field";
                    lineup = document.createElement("div");
                    lineup.className = "lineup";
                    p_lineup = document.createElement("p");
                    p_lineup.textContent = res.message;
                    p_lineup.className = "small_text";
                    lineup.append(p_lineup);
                    contentField.appendChild(lineup)
                    document.getElementById("content_matches").appendChild(contentField);
                }
        }
    };
    xhttp.open('POST', url, true);
    xhttp.send(data);
}

/**
    Convert a lineup key to a string of hero names
    i.e '1.2.3.4.5' to 'Anti-Mage * Axe * Bane * Bloodseeker * Crystal Maiden
 */
function convertLineUp(lineup){

    var heroes = {
        1: "Anti-Mage",
        2: "Axe",
        3: "Bane",
        4: "Bloodseeker",
        5: "Crystal Maiden",
        6: "Drow Ranger",
        7: "Earthshaker",
        8: "Juggernaut",
        9: "Mirana",
        10: "Morphling",
        11:"Shadow Fiend",
        12: "Phantom Lancer",
        13: "Puck",
        14: "Pudge",
        15: "Razor",
        16: "Sand King",
        17: "Storm Spirit",
        18: "Sven",
        19: "Tiny",
        20: "Vengeful Spirit",
        21: "Windranger",
        22: "Zeus",
        23: "Kunkka",
        25: "Lina",
        26: "Lion",
        27: "Shadow Shaman",
        28: "Slardar",
        29: "Tidehunter",
        30: "Witch Doctor",
        31: "Lich",
        32: "Riki",
        33: "Enigma",
        34: "Tinker",
        35: "Sniper",
        36: "Necrophos",
        37: "Warlock",
        38: "Beastmaster",
        39: "Queen of Pain",
        40: "Venomancer",
        41: "Faceless Void",
        42: "Skeleton King",
        43: "Death Prophet",
        44: "Phantom Assassin",
        45: "Pugna",
        46: "Templar Assassin",
        47: "Viper",
        48: "Luna",
        49: "Dragon Knight",
        50: "Dazzle",
        51: "Clockwerk",
        52: "Leshrac",
        53: "Nature's Prophet",
        54: "Lifestealer",
        55: "Dark Seer",
        56: "Clinkz",
        57: "Omniknight",
        58: "Enchantress",
        59: "Huskar",
        60: "Night Stalker",
        61: "Broodmother",
        62: "Bounty Hunter",
        63: "Weaver",
        64: "Jakiro",
        65: "Batrider",
        66: "Chen",
        67: "Spectre",
        68: "Ancient Apparition",
        69: "Doom",
        70: "Ursa",
        71: "Spirit Breaker",
        72: "Gyrocopter",
        73: "Alchemist",
        74: "Invoker",
        75: "Silencer",
        76: "Outworld Devourer",
        77: "Lycanthrope",
        78: "Brewmaster",
        79: "Shadow Demon",
        80: "Lone Druid",
        81: "Chaos Knight",
        82: "Meepo",
        83: "Treant Protector",
        84: "Ogre Magi",
        85: "Undying",
        86: "Rubick",
        87: "Disruptor",
        88: "Nyx Assassin",
        89: "Naga Siren",
        90: "Keeper of the Light",
        91: "Wisp",
        92: "Visage",
        93: "Slark",
        94: "Medusa",
        95: "Troll Warlord",
        96: "Centaur Warrunner",
        97: "Magnus",
        98: "Timbersaw",
        99: "Bristleback",
        100: "Tusk",
        101: "Skywrath Mage",
        102: "Abaddon",
        103: "Elder Titan",
        104: "Legion Commander",
        105: "Techies",
        106: "Ember Spirit",
        107: "Earth Spirit",
        108: "Abyssal Underlord",
        109: "Terrorblade",
        110: "Phoenix",
        111: "Oracle",
        112: "Winter Wyvern",
        113: "Arc Warden",
        114: "Monkey King"
        }

    var res = '';
    var lineup = lineup.split(".");

    res = heroes[lineup[0]] + ' * ' + heroes[lineup[1]] + ' * ' + heroes[lineup[2]] + ' * ' + heroes[lineup[3]] + ' * ' + heroes[lineup[4]];
    return res;
}
