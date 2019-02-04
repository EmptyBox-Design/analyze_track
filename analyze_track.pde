

import processing.sound.*; 
SoundFile file;
Amplitude amp;
AudioIn in;
FFT fft;
// GLOBALS
int bands = 512;
float[] spectrum = new float[bands];
float maxHeight = 1;
float heightThreshold = 1;
float alpha = 90;
float multiplier = 1.5;
float strokeWeight = 0.3f; 
String activeSong = "jar.mp3";

public color colorSelector(int index) {
  double h = map(index, bands, 1, 6, 0);
  color[] colorArray = {color(#0cebeb), color(#20e3b2), color(#29ffc6), color(#ee0979), 
    color(#ff6a00), color(#ff4b1f), color(#ff9068)};
  int roundVal= (int) Math.round(h);
  return colorArray[roundVal];
}

public void setup() {
  // size the canvas
  size(512, 800);
  // paint canvas black
  background(30, 30, 30);
  // Create an Input stream which is routed into the Amplitude analyzer
  fft = new FFT(this, bands);
  in = new AudioIn(this, 0);

  // start the Audio Input
  in.start();

  // patch the AudioIn
  fft.input(in);
  file = new SoundFile(this, activeSong);
  file.play();
}     
// input is current max height of the line
// checks to see if every band has been drawn
// if so then incrament the height of the next line
public void checkHeight(float value) {
  if (value == bands-1) {
    maxHeight = maxHeight + 1;
  } else if (maxHeight == height) {
    // when max height equals the total height of the 
    // canvas then reset and clear the screen
    // reset the height and draw axis
    maxHeight = 1; 
    background(30, 30, 30);
  }
}
public void draw() {
  fft.analyze(spectrum);
  for (int i = 0; i < bands; i++) {
    // incraments height based on each band of sound input
    checkHeight(i);
    // line constructor
    line(i, maxHeight, i, maxHeight - spectrum[i]*maxHeight*multiplier);
    strokeWeight(strokeWeight);
    // if there is not amplitude in the band paint black else
    // paint the stroke the given color based on even odd
    if (maxHeight < (maxHeight - spectrum[i]*maxHeight*multiplier) + heightThreshold) {
      noStroke();
      noFill();
    } else {
      int strokeColor = colorSelector(i);
      stroke(strokeColor, alpha);
    }
  }
} 
