import hypermedia.net.*;
//import com.hamoid.*;

//VideoExport videoExport;

int PORT_RX=7004;
String HOST_IP = "127.0.0.1";//IP Address of the PC in which this App is running
UDP udp;//Create UDP object for recieving
int position1, position2;
float xpos = 250;
float ypos = 0;
float speed = 0.05;
float xangle, yangle;
float lastx, lasty,pos2_float,pos2;
int centerx, centery;
String test;
int[] spatialData = {0,0,0,0,0,0,0};
int cuePos, lastCue, pitPos, lastPit = 0;
boolean setDirection = true;
float xModifier,yModifier;
int trail = 140;
float circleSize = 300;
int line = 7;
int lineColor = 255;

int momentColor = 255;
int momentx, momenty;

void setup() {
  //fullScreen(2);
  size(1080, 720);
  centerx = width/2;  
  centery = height/2 -50;
  udp= new UDP(this, PORT_RX, HOST_IP);
  //udp.log(true);
  udp.listen(true);
  noLoop();
  frameRate(60);
  background(0);
  loop();
  //videoExport = new VideoExport(this, "PO.mp4");
  
}

void draw() {
  
  // trail dimmer
  fill(0, trail);
  strokeWeight(0);
  stroke(0);
  rect(0, 0, width, height);
  fill(255);
  
  sequence(); 
  //println(spatialData);

  // draw the line
  stroke(lineColor);
  strokeWeight(line);
  if(!(lastx ==0 || lasty == 0 || xpos == 0 || ypos ==0 )){line(lastx, lasty, xpos, ypos);}
  lastx = xpos;
  lasty = ypos;
  
  //inspect data graphically
  dataGraph();
  
  // interlude line
  lineMoment();

  // Works out rotation from radians
  pos2 = map(pos2_float, 0.00, 360.00, -100.00, 100.00);
  ypos = centery + (sin(yangle) * circleSize) + yModifier;
  xpos = centerx + (cos(yangle) * circleSize) + xModifier;
  
 // println(xModifier + " - " + yModifier);
  rotationIncrementer(setDirection);
  //videoExport.saveFrame();
  
} 

void receive(byte[] data, String HOST_IP, int PORT_RX) {
  String value = new String(data);
  //println(value);
  String spat[] = match(value, "spat source ([0-9]) az -([0-9]*)");
  String cue[] = match(value, "cue ([0-9]*)");
  String pitch[] = match(value, "pitch ([0-9]*)");
  
   if (spat != null) {
     int source1 = int(spat[1]);
     int val = int(spat[2]);
     //println(source1," - ",val);
     spatialData[source1] = val;
   }
   
   else if (cue != null){
     cuePos = int(cue[1]);
   }  
   
   else if (pitch != null){
     pitPos = int(pitch[1]);
   }  
   
}

void lineMoment() {
  
  if(cuePos < 22) {
    momentColor = 0;
    momentx =0;
    momenty = 0;
  }
  
    else if(cuePos < 23) {
    momentColor = 255;
    momentx = 120;
    momenty = 70;
  }
  
 else if(cuePos < 78) {
    momentColor = 0;
    momentx = 120;
    momenty = 70;
  }
  
  else if(cuePos < 90) {
    momentColor = 255;
    momentx = centerx +200;
    momenty = height -20;
  }
  
 else if(cuePos < 200) {
    momentColor = 0;
  }
  
  fill(momentColor);
  textSize(32);
  text('_', momentx, momenty); 
}

void dataGraph()
{
  textSize(32);
  fill(255, 255, 255);
  text(cuePos, 120, 30); 
  if(cuePos >= 22 && cuePos <= 31 || cuePos >= 209) {fill(255, 255, 255);} else {fill(0, 0, 0);}
  text("Celing Lights on", 120, 60); 
  
    int spacer = 0;
  for(int i = 1; i <= 6; i++)
  {
    if(spatialData[i] != 0)
    {
    line(10+spacer,10,10+spacer,10+spatialData[i]);
    //println(spatialData[i]);
    }
    spacer += 10;
  }
  
  line(90,10,90,10+pitPos);
  
  
  
  
}


void rotationIncrementer(boolean direction){
    
    
    if(direction){
      xangle += speed;
      yangle += speed;
    }
    else
    {
      xangle -= speed;
      yangle -= speed;
    }
    
    if (xangle < 0) {xangle = TWO_PI;}
    else if (xangle > TWO_PI) {xangle = 0;}
    
    if (yangle < 0) {yangle = TWO_PI;}
    else if (yangle > TWO_PI) {yangle = 0;}
  
  
}

void toggleDirection(int a) {
  if (a == 1) {lastPit = pitPos;}
  if(lastCue != cuePos || pitPos != lastPit){ 
         setDirection = !setDirection;
         lastCue = cuePos;
         lastPit = pitPos;
       }
}