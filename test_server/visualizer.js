let features;
let sound;
let idx = 0;
let windowDuration = 1024 / 44100;
let lastUpdate = 0;
let started = false;
const RING_POINTS = 200;

function preload() {
  features = loadJSON('features_normalized.json');
  sound = loadSound('test_audio.wav');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  angleMode(DEGREES);
  noFill();
  strokeCap(ROUND);
  textAlign(CENTER, CENTER);
  textSize(24);
  fill(200);
}

function draw() {
  background(17);

  if (!started) {
    text("Click to Start", width / 2, height / 2);
    return;
  }

  let currentTime = sound.currentTime();
  let frameIndex = Math.floor(currentTime / windowDuration);

  if (frameIndex >= features.length) {
    noLoop();
    return;
  }

  idx = frameIndex;
  let f = features[idx];
  if (!f || f.length < 7) return;

  drawVisualizer(f);
}

function drawVisualizer(f) {

  let [rms, centroid, pitch, bandwidth, interval, tempo, beat] = f;
  console.log("Current feature vector:", f);

  let t = millis() * 0.002;

  let baseRadius = map(rms, 0, 1, 150, min(width, height) * 0.35);
  let hueVal = map(centroid, 0, 1, 0, 360);
  let wobbleAmp = map(bandwidth, 0, 1, 10, 80);
  let beatGlow = map(beat, 0, 1, 50, 255);
  let rotationSpeed = map(interval, 0, 1, 0.2, 2);
  let tempoRadius = map(tempo, 0, 1, 20, 80);
  let pitchFreq = map(pitch, 0, 1, 2, 10);

  push();
  translate(width / 2, height / 2);
  rotate(frameCount * rotationSpeed);

  drawWobbleRing(baseRadius, rms, wobbleAmp, centroid, hueVal, beatGlow);
  drawTempoOrbs(baseRadius, tempoRadius, beat, hueVal);
  drawBeatBurst(beat, hueVal);

  pop();
}

function drawWobbleRing(baseRadius, rms, wobbleAmp, centroid, hueVal, beatGlow) {
  let t = millis() * 0.002;
  strokeWeight(2);
  colorMode(HSB);
  stroke(hueVal, 255, 255, beatGlow);
  noFill();

  beginShape();
  for (let i = 0; i < RING_POINTS; i++) {
    let angle = map(i, 0, RING_POINTS, 0, 360);

    let audioWiggle = sin(angle * 3 + t) * wobbleAmp * rms;
    let organicWiggle = noise(i * 0.05, t * 0.3) * 50 * rms * centroid;

    let r = baseRadius + audioWiggle + organicWiggle;
    let x = r * cos(angle);
    let y = r * sin(angle);
    curveVertex(x, y);
  }
  endShape(CLOSE);
}

function drawTempoOrbs(baseRadius, tempoRadius, beat, hueVal) {
  let orbCount = 8;
  for (let i = 0; i < orbCount; i++) {
    let angle = millis() * 0.05 + i * (360 / orbCount);
    let r = baseRadius + tempoRadius;
    let x = r * cos(angle);
    let y = r * sin(angle);
    fill(hueVal, 255, 255, 150);
    noStroke();
    ellipse(x, y, 6 + 4 * beat);
  }
}

function drawBeatBurst(beat, hueVal) {
  if (beat > 0.6) {
    for (let i = 0; i < 60; i++) {
      let angle = random(360);
      let r = random(30, 80);
      let x = r * cos(angle);
      let y = r * sin(angle);
      stroke(hueVal, 255, 255, 150);
      strokeWeight(random(1, 2));
      point(x, y);
    }
  }
}

function mousePressed() {
  if (!started) {
    userStartAudio();
    sound.play();
    started = true;
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
