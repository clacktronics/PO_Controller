void sequence() {
  
  if(cuePos == 0){
    lineColor = 0;
  }
  
  else if(cuePos < 22){
    lineColor = 255;
     speed = 0.1;
     trail = 100;
     toggleDirection(0);
     circleSize = map(spatialData[3],0,360,250,300);
   }
   else if (cuePos < 33){
     lineColor = 0;
     //circleSize = 300;
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
   }
   else if (cuePos < 46) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-100,100);
     yModifier = map(spatialData[3],0,360,0,100);
     trail = 20;
     speed = 0.06;
     line = 7;
     toggleDirection(1);  
   }
      else if (cuePos < 47) {
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
     if(lastCue != cuePos){ circleSize -= 67;lastCue = cuePos; }  
   }
   
   else if (cuePos < 54) {
     lineColor = 0;
     trail = 40;
   }
     
   else if (cuePos < 62) {
     lineColor = 255;
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
   else if (cuePos < 80) {
     lineColor = 255;
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
   
      else if (cuePos < 120) {
     lineColor = 0;  
   } 
   
   else if (cuePos < 173) {
     lineColor = 255;
     xModifier = map(spatialData[1],0,360,-200,200);
     circleSize = map(spatialData[2],0,360,10,400);;
     trail = 10;
     speed = 0.04;      
   }
   else if (cuePos < 209) {
     lineColor = 255;
     circleSize = map(spatialData[3],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection(1);
     trail = 30;
     speed = 0.1;
     line = 7;     
   }
 
   else if (cuePos < 300) {
     lineColor = 0; 
     trail = 100;
   }
   
  
  
  
}