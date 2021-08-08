var benchmark_color = "#2abfa4";
var own_color = "#b12abf";
var workerUnits = ['Probe', 'SCV', 'Drone'];
var workerClass = 'worker'

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

function addTagIfWorker(element, buildEntry) {
    // tag classname as worker if worker unit. This is to hide if checkbox is ticked.
    if (workerUnits.includes(buildEntry)) {
        element.className += workerClass;
    }
}

function to_MM_SS(timestamp) {
	var minutes = Math.floor(timestamp / 60);
	var seconds = timestamp - minutes * 60;
	if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
	return minutes + ":" + seconds
}

/**
 * 
 * @param {HTMLElement} target target to display on.
 * @param {Array[int]} timestamps timestamps
 * @param {Dict} build list of buildings, units, upgrades at every time.
 */
function displayBuild(target, build) {
    // clears the frame for drawing
    target.innerText = '';

    for(timestamp in build) {
		var time = to_MM_SS(timestamp);
        var buildBlock = document.createElement("div");
		var timestampElement = document.createElement("div");

        buildBlock.classList.add('buildBlock');
        buildBlock.classList.add(time);
		timestampElement.classList.add('timestamp');
		timestampElement.innerText = time;

        var buildEntryCount = 0;

        for(let buildEntry in build[timestamp]) {
			var buildElement = document.createElement("div");
			buildElement.innerText = buildEntry + ": " + build[timestamp][buildEntry]
			addTagIfWorker(buildElement, buildEntry);
			buildBlock.appendChild(buildElement);
			buildEntryCount += 1;
        }

		target.appendChild(timestampElement);
		target.appendChild(buildBlock);

		if (buildEntryCount == 1 && buildBlock.children[0].className == workerClass) {
			buildBlock.classList.add(workerClass);
			timestampElement.classList.add(workerClass);
		}
    }
}

function showBuild(bench, own) {
    var benchElement = document.getElementById('benchmarkBuild');
    var ownElement = document.getElementById('ownBuild');

    // all of timestamp, bench, and own should have the same length:
    displayBuild(benchElement, bench);
    displayBuild(ownElement, own);
}

function toggleWorkers(checkboxElement) {
    var workerElements = document.getElementsByClassName(workerClass);

    // show workers if checked, else hide them. Hidden by default
    for (workerElement of workerElements) {
        if (checkboxElement.checked) {
            workerElement.style.display = "flex";
        } else {
            workerElement.style.display = "none";
        }
    }
}
