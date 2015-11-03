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
int cuePos, lastCue = 0;
boolean setDirection = true;
float xModifier,yModifier;
int trail = 140;
float circleSize = 300;
int line = 7;

void setup() {
  fullScreen(1);
  //size(1080, 720);
  centerx = width/2;  
  centery = height/2;
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
  stroke(255);
  strokeWeight(line);
  if(!(lastx ==0 || lasty == 0 || xpos == 0 || ypos ==0 )){line(lastx, lasty, xpos, ypos);}
  lastx = xpos;
  lasty = ypos;
  
  // inspect data graphically
  dataGraph();

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
   if (spat != null) {
     int source1 = int(spat[1]);
     int val = int(spat[2]);
     //println(source1," - ",val);
     spatialData[source1] = val;
   }
   
   if (cue != null){
     cuePos = int(cue[1]);
   }  
}

void dataGraph()
{
    textSize(32);
  text(cuePos, 100, 30); 
  fill(0, 102, 153);
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

void toggleDirection() {
  if(lastCue != cuePos){ 
         setDirection = !setDirection;
         lastCue = cuePos; }   
}