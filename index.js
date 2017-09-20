const spawn = require('child_process').spawn;
const watson = require('watson-developer-cloud');
const stream = require('stream');
const fs = require('fs');

const { sttConfig, channelTypes, DEBUG } = require('./constants');

let paused = false;
let restarting = false;
let process_this = false;

if (!fs.existsSync('logs')) {
	fs.mkdirSync('logs');
}

const channels = [];
const models = sttConfig.models;
const currentModel = 'generic';

const speech_to_text = watson.speech_to_text(sttConfig.auth);

const PythonShell = require('python-shell');

let deviceInterface;

switch (process.platform) {
	case 'darwin':
	deviceInterface = 'avfoundation';
	break;
	case 'win32':
	deviceInterface = 'dshow';
	break;
	default:
	deviceInterface = 'alsa';
	break;
}

function delayedRestart() {

	if(restarting)
		return;
	restarting = true;
	stopCapture();

	setTimeout(() => {
		startCapture();
		restarting = false;
	}, 1000);
};

function startCapture() {
	for (let i = 0; i < channelTypes.length; i++) {
		const p = spawn('ffmpeg', [
			'-v', 'error',
			'-f', deviceInterface,
			'-i', sttConfig.inputDevice || 'none:default',
			'-map_channel', `0.0.${i}`,
			'-acodec', 'pcm_s16le', '-ar', '16000',
			'-f', 'wav', '-'], { windowsVerbatimArguments: true });

		p.stderr.on('data', data => {
			console.error("FFMPEG ERROR");
			console.error(data.toString());
			process.exit(1);
		});

		let s;

		if (channelTypes[i] !== 'near') {

			const pausable = new stream.Transform();
			pausable._transform = function(chunk, encoding, callback) {
				if (!paused || DEBUG) {
					this.push(chunk);
				}
				callback();
			};

			s = p.stdout.pipe(pausable);
		} else {
			s = p.stdout;
		}

		if (channels[i]) {
			channels[i].process = p;
			channels[i].stream = s;
		} else {
			channels.push({process:p, stream:s});
		}
	}

	transcribe();
}

function stopCapture() {
	console.log('Stopping all channels.');
	for (let i = 0; i < channelTypes.length; i++) {
		if (channels[i].process) {
			channels[i].process.kill();
			channels[i].process = null;
		}
		channels[i].stream = null;
	}
}

function transcribe() {
	console.log(`Starting all channels with the ${currentModel} model.`);

	for (let i = 0; i < channelTypes.length; i++) {
		const sttStream = speech_to_text.createRecognizeStream({
			content_type: 'audio/l16; rate=16000; channels=1',
			model: models[currentModel],
			inactivity_timeout: -1,
			smart_formatting: true,
			'x-watson-learning-opt-out': true,
			interim_results: true,
			keywords: sttConfig.keywords,
			keywords_threshold: sttConfig.keywords_threshold,
			customization_id: "cc08b760-9e13-11e7-806a-99e03c64b58a"
		});

		sttStream.on('error', (err) => {
			console.error(err);
			console.info('An error occurred. Restarting capturing after 1 second.');
			delayedRestart();
		});

		sttStream.on('close', () => {
			console.error('websocket closed ---- not restarting')
			delayedRestart();
		})

		const textStream = channels[i].stream.pipe(sttStream);

		textStream.setEncoding('utf8');
		textStream.on('results', input => {
			const result = input.results[0];

			if (result) {
				const msg = { channel: i, result: result };
				if (result.final) {
					paused = true;
					console.info(JSON.stringify(msg));
					if (!process_this) {
						console.log("******************************");
						for (item of result.alternatives) {
							console.log(item);
							if (item.transcript.trim().toLowerCase().indexOf("watson") >= 0) {
								PythonShell.run('audiolib.py', err => {
									if (err) console.error(err);
									console.log('finished');
									process_this = true;
									paused = false;
								});
							} else {
								paused = false;
							}
						}
						console.log("******************************");
					} else {
						let result_data = [];
						console.log("******************************");
						for (item of result.alternatives) {
							console.log(item);
							if (item.transcript.trim().toLowerCase().length > 5 ) {
								result_data.push(item.transcript.trim().toLowerCase());	
							}
						}
						console.log("******************************");
						if (result_data.length > 0) {
							var options = {
								mode: 'text',
								args: [JSON.stringify(result_data)]
							};
							PythonShell.run('brain.py', options, (err, results) => {
								if (err) console.error(err);
								try {
									console.log('finished with results: ', results);
								} catch (e) {
									console.log(e);
								}
								process_this = false;
								paused = false;
							});
						} else {
							paused = false;
						}
					} 
				}
			}
		});
	}
}

startCapture();
