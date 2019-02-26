import processing.sound.*;
import java.io.File; 
import java.io.IOException; 
import java.io.FileWriter;
import java.util.Arrays;

SoundFile file;
Amplitude amp;
AudioIn in;

String songName = "house";
String genre = "raggae";
String activeSong = genre+"/"+songName+".mp3";
String fileHeader = "index,value,";
boolean fileHeaderFlag = false;
String filePath = "/Users/bamforion/Documents/Processing/analyze_track/songData/";
int bandCounter = 0;
int doneCounter = 0;
public void setup() {
  // size the canvas
  size(512, 800);
  // paint canvas black
  background(30, 30, 30);

  amp = new Amplitude(this);
  in = new AudioIn(this, 0);
  in.start();
  amp.input(in);

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

public void draw() {
  bandCounter = bandCounter + 1;
  String val = Float.toString(amp.analyze());
  String id = Float.toString(bandCounter);
  // save spectrum by index to file
  saveToFile(id+","+val+",");
}
