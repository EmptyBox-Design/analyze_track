import processing.sound.*;
import java.io.File; 
import java.io.IOException; 
import java.io.FileWriter;
import java.util.Arrays;

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
String songName = "home";
String genre = "indie";
String activeSong = genre+"/"+songName+".mp3";
String fileHeader = "index,value,";
boolean fileHeaderFlag = false;
String filePath = "/Users/bamforion/Documents/Processing/analyze_track/songData/";
int bandCounter = 1;

public void setup() {
  //System.out.println(Math.abs(0.000043));
  //System.out.println(Math.round(1+Math.abs(0.000043)));=
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
public void saveToFile(String content) {
  FileWriter fw = null;
  File f = new File(filePath + songName+".csv");
  try {
    if (!f.exists()) {
      f.createNewFile();
    }
    fw = new FileWriter(f, true);
    if (fileHeaderFlag == false) {
      fw.write(fileHeader);
      fileHeaderFlag = true;
    }
    fw.write("\r\n");
    fw.write(content);
    fw.close();
  } 
  catch (IOException e) {
    // Error when writing to the file
    e.printStackTrace();
  }
}
public color colorSelector(int index) {
  double h = map(index, bands, 1, 6, 0);
  color[] colorArray = {color(#0cebeb), color(#20e3b2), color(#29ffc6), color(#ee0979), 
    color(#ff6a00), color(#ff4b1f), color(#ff9068)};
  int roundVal= (int) Math.round(h);
  return colorArray[roundVal];
}
// input is current max height of the line
// checks to see if every band has been drawn
// if so then incrament the height of the next line
public void checkHeight(float value) {
  if (value == bands-1) {
    maxHeight = maxHeight + 1;
    bandCounter = bandCounter +1;
  } else if (maxHeight >= height) {
    // when max height equals the total height of the 
    // canvas then reset and clear the screen
    // reset the height
    maxHeight = 1; 
    background(30, 30, 30);
  }
}
public float sortArray(float[] array, String type) {
  Arrays.sort(array);
  float val = 0;
  if (type == "max") {
    val =  array[511];
  } else if (type == "min") {
    val = array[0];
  }
  return val;
}

public void draw() {
  fft.analyze(spectrum);
  for (int i = 0; i < bands; i++) {
    // incraments height based on each band of sound input
    checkHeight(i);
    // convert values into strings for saving
    String val = Float.toString(spectrum[i]);
    String id = Float.toString(bandCounter);
    float min = sortArray(spectrum, "min");
    float max = sortArray(spectrum, "max");
    // save spectrum by index to file
    saveToFile(id+"-"+i+","+val+",");
    // line constructor
    float lineHeight = map(spectrum[i],min, max, maxHeight,maxHeight-2);
    // System.out.println("lineheght-----"+lineHeight);
    //System.out.print("STARRRRRT::::::"+lineHeight+":"+spectrum[0]+":"+spectrum[511]+":"+spectrum[i]+":::::END");
    line(i, maxHeight, i, lineHeight);
    strokeWeight(strokeWeight);
    // if there is not amplitude in the band paint black else
    // paint the stroke the given color based on even odd
    //if (maxHeight < (maxHeight - spectrum[i]*maxHeight*multiplier) + heightThreshold) {
    //if(lineHeight <= maxHeight+4){
    //  noStroke();
    //  noFill();
    //} else {
    int strokeColor = colorSelector(i);
    stroke(strokeColor, alpha);
    //}
  }
}
