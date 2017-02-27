window.onload = function(){
    fillMatches('weighted_sort'); // Default sorting
};

/**
    Display meesage when lineups are loading
*/
function displayLoadingMessage(){
    var loadMsg;
    var loadIcon;
    matchesWrapper = document.getElementById("matches_wrapper");
    matchesWrapper.innerHTML = "";

    loadIcon = document.createElement("i");
    loadIcon.className = "fa fa-circle-o-notch fa-spin";

    loadMsg = document.createElement("p");
    loadMsg.className = "small_text";
    loadMsg.appendChild(loadIcon);
    loadMsg.id = "load_msg";
    loadMsg.textContent = "Loading matches, please wait a few seconds...";

    matchesWrapper.appendChild(loadMsg);
}

/**
    Remove old sorting arrow and move to correct, new column
*/
function updateSortArrow(sorting){
    var sort_description;
    var wins_arrow;
    var losses_arrow;
    var win_rate_arrow;
    var score_arrow;
    var child;
    var parent;

     // remove old sorting arrows
    var sorting_boxes = ["description_text_wins", "description_text_losses", "description_text_win_rate", "description_text_score" ];
    var sorting_arrows = ["wins_arrow", "losses_arrow", "win_rate_arrow", "score_arrow"];
    for (var i = 0; i < sorting_boxes.length; i++) {
        parent = document.getElementById(sorting_boxes[i]);
        child = document.getElementById(sorting_arrows[i]);
        if(child != null){
            parent.removeChild(child);
         }
    }

    // Add the correct arrow
    switch(sorting){
        case 'weighted_sort':
            sort_description = document.getElementById("description_text_score");
            score_arrow = document.createElement("i");
            score_arrow.className = "fa fa-caret-down";
            score_arrow.id = "score_arrow";
            sort_description.appendChild(score_arrow);
            break;
        case 'wins':
            sort_description = document.getElementById("description_text_wins");
            wins_arrow = document.createElement("i");
            wins_arrow.className = "fa fa-caret-down";
            wins_arrow.id = "wins_arrow";
            sort_description.appendChild(wins_arrow);
            break;
        case 'losses':
            sort_description = document.getElementById("description_text_losses");
            losses_arrow = document.createElement("i");
            losses_arrow.className = "fa fa-caret-down";
            losses_arrow.id = "losses_arrow";
            sort_description.appendChild(losses_arrow);
            break;
        case 'win_rate':
            sort_description = document.getElementById("description_text_win_rate");
            win_rate_arrow = document.createElement("i");
            win_rate_arrow.className = "fa fa-caret-down";
            win_rate_arrow.id = "win_rate_arrow";
            sort_description.appendChild(win_rate_arrow);
            break;
        default:
            break;
    }
}

/**
    Fill matches with given sorting.
    First, remove everything in the div "matches_wrapper",
    then create a new div for each lineup.

    If successful, lineups will be shown. If not, show error message.

*/
function fillMatches(sorting){



    var matchesShown = 20;
    var contentField;
    var number;
    var lineup;
    var wins;
    var losses;
    var winRate;
    var score;
    var infoText;
    var p_number;
    var p_wins;
    var p_losses;
    var p_winRate;
    var p_score;
    var a_lineup;
    var lineup_text;
    var id;
    var p_infoText;

    updateSortArrow(sorting); // Add sorting arrow
    displayLoadingMessage();  // Remove whatever is showing and replace with loading msg


    // Overload return call from xhttp request
    var xhttp = new XMLHttpRequest();
    var data = new FormData();
    data.append('sorting', sorting)
    var url = '/show_matches';
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            // return object here
            res = JSON.parse(this.responseText);

            // remove loading text
            var childDiv = document.getElementById("load_msg");
            var parentDiv = document.getElementById("matches_wrapper");
            if (childDiv != null){
                parentDiv.removeChild(childDiv);
            }

            // Success, fill with lineups
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
                    lineupstring = convertLineUp(res.data[i].lineup_key);
                    lineup = document.createElement("div");
                    lineup.className = "lineup";
                    a_lineup = document.createElement("a");
                    a_lineup.className = "link";
                    lineup_text = document.createTextNode(lineupstring);
                    lineup_text.className = "link";
                    a_lineup.appendChild(lineup_text);
                    a_lineup.title = lineupstring;
                    a_lineup.href = "/lineup/" + res.data[i].lineup_key;
                    lineup.appendChild(a_lineup);

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
                    p_winRate.textContent = (res.data[i].win_rate*100).toFixed(2) + ' %'; // Get rate in percentage with 2 decimals
                    p_winRate.className = "small_text";
                    winRate.appendChild(p_winRate);

                     // add score string
                    score = document.createElement("div");
                    score.className = "score";
                    p_score = document.createElement("p");
                    p_score.textContent = (res.data[i].weighted_sort).toFixed(2); // fix 2 decimals
                    p_score.className = "small_text";
                    score.appendChild(p_score);

                    // put them all in a single match div
                    contentField.appendChild(number);
                    contentField.appendChild(lineup);
                    contentField.appendChild(wins);
                    contentField.appendChild(losses);
                    contentField.appendChild(winRate);
                    contentField.appendChild(score);
                    document.getElementById("matches_wrapper").appendChild(contentField);
                }

                    // add counter of matches parsed
                    infoText = document.createElement("div");
                    infoText.className = "info_text";
                    p_infoText = document.createElement("p");
                    p_infoText.style.whiteSpace = "pre";
                    p_infoText.textContent = res.matches_parsed + ' matches parsed. \r\n \r\n';
                    p_infoText.textContent += 'Score is calculated with the following function: score = win rate * ln(matches played). \r\n';
                    p_infoText.textContent += 'Sorting only shows matches with more than 20 wins/losses, depending on chosen sorting. \r\n\r\n';
                    p_infoText.textContent += 'Click on a lineup to get the match ids.';


                    p_infoText.className = "info_text";
                    infoText.appendChild(p_infoText);
                    document.getElementById("matches_wrapper").appendChild(infoText);


                }

                // else, hijack the lineup field to show an error message.
                else{

                    contentField = document.createElement("div");
                    contentField.className = "content_field";
                    lineup = document.createElement("div");
                    lineup.className = "lineup";
                    p_lineup = document.createElement("p");
                    p_lineup.textContent = res.message;
                    p_lineup.className = "small_text";
                    lineup.appendChild(p_lineup);
                    contentField.appendChild(lineup)
                    document.getElementById("matches_wrapper").appendChild(contentField);
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
