void sequence() {
  
  if(cuePos == 0){
    lineColor = 255;
  }
  
  else if(cuePos < 22){
    lineColor = 255;
     speed = 0.1;
     trail = 100;
     toggleDirection(0);
     circleSize = map(spatialData[3],0,360,250,300);
   }
   else if (cuePos < 35){
     lineColor = 0;
     circleSize = 25;
     speed = 0.3;
     trail = 500;
     //xModifier = map(spatialData[1],0,360,-50,50);
     //yModifier = map(spatialData[3],0,360,-50,50);
     //trail = 50;
     //speed = 0.03;
   }
   
   else if (cuePos < 39) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-100,100);
     yModifier = map(spatialData[3],0,360,0,100);
     trail = 20;
     speed = 0.06;
     line = 7; 
     circleSize = 300;
   }
   else if (cuePos < 47) {
     lineColor = 0;
     xModifier = map(spatialData[1],0,360,-100,100);
     yModifier = map(spatialData[3],0,360,0,100);
     trail = 20;
     speed = 0.06;
     line = 7;
     toggleDirection(1);  
   }
      else if (cuePos < 48) {
      lineColor = 255;
     circleSize = 400;
   }
   else if (cuePos < 53) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-10,10);
     yModifier = map(spatialData[3],0,360,-10,10);
     trail = 5;
     speed = 0.07;
     line = 3;  
     if(lastCue != cuePos){ circleSize -= 100;lastCue = cuePos; }  
   }
   
   else if (cuePos < 54) {
     lineColor = 0;
     trail = 40;
   }
     
   else if (cuePos < 60) {
     lineColor = 0;
     xModifier = map(spatialData[2],0,360,0,100);
     yModifier = map(spatialData[2],0,360,0,100);
     trail = 20;
     speed = 0.05;
     circleSize = 300;
     toggleDirection(1);
   }
   else if(cuePos < 71){
     lineColor = 255;
     speed = 0.05;
     trail = 15;
     toggleDirection(1);
     circleSize = map(spatialData[3],0,360,50,300);
   }
   else if (cuePos < 75) {
     lineColor = 255;
     xModifier = map(spatialData[2],0,360,0,100);
     yModifier = map(spatialData[2],0,360,0,100);
     circleSize = 400;
     trail = 10;
     speed = 0.5;
   }
   else if (cuePos < 90) {
     lineColor = 0;
     xModifier = map(spatialData[1],0,360,-10,10);
     yModifier = map(spatialData[3],0,360,-10,10);
     trail = 40;
     speed = 0.07;
     line = 7;  
     if(lastCue != cuePos){ circleSize -= 30;lastCue = cuePos; }  
   }
   else if (cuePos < 96) {
     lineColor = 255;
     xModifier = map(spatialData[2],0,360,0,200);
     yModifier = map(spatialData[2],0,360,0,150);
     trail = 30;
     speed = 0.03;
     toggleDirection(1);     
   }
   else if (cuePos < 101) {
     lineColor = 255;
     circleSize = map(spatialData[2],0,360,-400,400);
     toggleDirection(1);
     trail = 30;
     speed = 0.6;      
   }
   else if (cuePos < 114) {
     lineColor = 255;
     toggleDirection(1);
     trail = 60;
     speed = 0.01; 
     circleSize = 300;
   }
   
   
      
   else if (cuePos < 117) {
     lineColor = 255;
     if(lastCue != cuePos){ circleSize -= 100; } 
     toggleDirection(1);
     trail = 30;
     speed = 0.05;
     
   } 
   
      else if (cuePos < 126) {
     lineColor = 0;  
   } 
   
   else if (cuePos < 140) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-200,200);
     circleSize = map(spatialData[2],0,360,10,400);;
     trail = 6;
     speed = 0.04;      
   }
   
      else if (cuePos < 161) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-200,200);
     circleSize = 0;//map(spatialData[2],0,360,10,400);;
     trail = 6;
     speed = 0.04;      
   }
   
  else if (cuePos < 173) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-200,200);
     circleSize = map(pitPos,50,100,-100,100);//map(spatialData[2],0,360,10,400);;
     trail = 6;
     speed = 0.04;      
   }
   
     else if (cuePos < 174) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
   else if (cuePos < 175) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
   else if (cuePos < 179) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     speed = 0.04;  
     trail = 6;
   }
   
   else if (cuePos < 180) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
   else if (cuePos < 185) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
   else if (cuePos < 186) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
   else if (cuePos < 189) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
   else if (cuePos < 190) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
  else if (cuePos < 192) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
  else if (cuePos < 193) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
   else if (cuePos < 194) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
   else if (cuePos < 195) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
      else if (cuePos < 197) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;      
   }
   
   else if (cuePos < 200) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 20;
     speed = 0.1;
     line = 7;     
   }
   
  else if (cuePos < 203) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 30;
     speed = 0.1;
     line = 7;     
   }
  
   
   
   else if (cuePos < 206) {
     lineColor = 255;
     circleSize = 100;//map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 30;
     speed = 0.1;
     line = 7;     
   }
   
   else if (cuePos < 207) {
     lineColor = 0;
     xModifier = 0;
     circleSize = 0;
     trail = 6;
     speed = 0.04;     
   }
   
      else if (cuePos < 209) {
     lineColor = 255;
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 10;
     speed = 0.025;
     line = 7;   
     circleSize = 100;
   }
 
   else if (cuePos < 210) {
     lineColor = 0; 
     trail = 5;
   }
   
    else if (cuePos < 300) {
     
     trail = 200;
   }
  
  
  
}