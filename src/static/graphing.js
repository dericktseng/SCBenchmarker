var benchmark_color = "#2abfa4";
var own_color = "#b12abf";

/**
 * clears the graph on the canvas
 * @param {HTMLCanvasElement} canvas - canvas to clear
 * @returns context of new canvas to draw on.
 */
function clearGraph(canvas) {
    var id = canvas.id;
    var canvasClass = canvas.classList;
    var container = canvas.parentElement;
    canvas.remove();

    var newCanvas = document.createElement("canvas");
    newCanvas.id = id;
    newCanvas.classList = canvasClass;
    container.appendChild(newCanvas);

    return newCanvas.getContext("2d");
}

/**
 * Generates a Graph with given parameters.
 * @param {Array[string]} timestamps - Array of strings representing timestamps
 * @param {Array[Number]} bench - first y values (bench values)
 * @param {Array[Number]} own - second y values (own values)
 * @param {string} title - title of graph
 * @param {HTMLCanvasElement} canvas - canvas to draw graph on.
 */
function generateGraph(timestamps, bench, own, title, canvas) {
    var ctx = clearGraph(canvas);

    // plots points and draws graph. Returns for further editing.
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [{
                    label: 'Benchmark ' + title,
                    data: bench,
                    fill: false,
                    borderColor: benchmark_color
                }, {
                    label: 'Own ' + title,
                    data: own,
                    fill: false,
                    borderColor: own_color
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            showTooltips: true,
            tooltips: {
                mode: 'index',
                intersect: false
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
}

function showMineralGraph(timestamps, bench, own) {
    var canvas = document.getElementById('mineralChart');
    generateGraph(
        timestamps,
        bench,
        own,
        "Mineral Rate",
        canvas);
}

function showGasGraph(timestamps, bench, own) {
    var canvas = document.getElementById('gasChart');
    generateGraph(
        timestamps,
        bench,
        own,
        "Gas Rate",
        canvas);
}

function showWorkersGraph(timestamps, bench, own) {
    var canvas = document.getElementById('workerChart');
    generateGraph(
        timestamps,
        bench,
        own,
        "Workers Created",
        canvas);
}

function showSupplyGraph(timestamps, bench, own) {
    var canvas = document.getElementById('supplyChart');
    generateGraph(
        timestamps,
        bench,
        own,
        "Supply",
        canvas);
}

/**
 * 
 * @param {HTMLElement} target target to display on.
 * @param {Array[string]} timestamps timestamps
 * @param {Array[Dict]} buildList list of buildings, units, upgrades at every time.
 */
function displayBuild(target, timestamps, buildList) {
    // clears the frame for drawing
    target.innerText = '';

    // dictionary of units, buildings, upgrades, entries at a timestamp
    var prevBuildListItem = {};
    for(i = 0; i < timestamps.length; i++) {
        // dictionary of units, buildings, upgrades, entries at a timestamp
        var currBuildListItem = buildList[i];
        
        // whether timestamp has something changing in the build
        var validTime = false;

        var buildBlock = document.createElement("div");
        buildBlock.className += 'buildBlock';

        for(buildEntry in currBuildListItem) {
            if (buildEntry in prevBuildListItem) {
                var diff = currBuildListItem[buildEntry] - prevBuildListItem[buildEntry];
                if (diff > 0) {
                    var buildElement = document.createElement("div");
                    buildElement.innerText = buildEntry + ": " + diff;
                    buildBlock.appendChild(buildElement);
                    validTime = true;
                }
            } else {
                var buildElement = document.createElement("div");
                buildElement.innerText = buildEntry + ": " + currBuildListItem[buildEntry];
                buildBlock.appendChild(buildElement);
                validTime = true;
            }
        }

        if (validTime) {
            var timestampElement = document.createElement("div");
            timestampElement.innerText = timestamps[i];
            target.appendChild(timestampElement);
            target.appendChild(buildBlock);
        }

        prevBuildListItem = currBuildListItem;
        validTime = false;
    }
}

function showBuild(timestamps, bench, own) {
    var benchElement = document.getElementById('benchmarkBuild');
    var ownElement = document.getElementById('ownBuild');

    // all of timestamp, bench, and own should have the same length:
    displayBuild(benchElement, timestamps, bench);
    displayBuild(ownElement, timestamps, own);
}