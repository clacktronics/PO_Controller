void sequence() {
  
 
  if(cuePos < 25){
     speed = 0.1;
     trail = 100;
     toggleDirection();
     circleSize = map(spatialData[3],0,360,250,300);
   }
   else if (cuePos < 34){
     circleSize = 300;
     xModifier = map(spatialData[1],0,360,-50,50);
     yModifier = map(spatialData[3],0,360,-50,50);
     trail = 50;
     speed = 0.03;
   }
   
   else if (cuePos < 39) {
     xModifier = map(spatialData[1],0,360,-100,100);
     yModifier = map(spatialData[3],0,360,0,100);
     trail = 20;
     speed = 0.06;
     line = 7;  
   }
   else if (cuePos < 46) {
     xModifier = map(spatialData[1],0,360,-100,100);
     yModifier = map(spatialData[3],0,360,0,100);
     trail = 20;
     speed = 0.06;
     line = 7;
     toggleDirection();  
   }
      else if (cuePos < 47) {
     circleSize = 400;
   }
   else if (cuePos < 53) {
     xModifier = map(spatialData[1],0,360,-10,10);
     yModifier = map(spatialData[3],0,360,-10,10);
     trail = 5;
     speed = 0.07;
     line = 3;  
     if(lastCue != cuePos){ circleSize -= 50;lastCue = cuePos; }  
   }
   else if (cuePos < 62) {
     xModifier = map(spatialData[1],0,360,0,100);
     yModifier = map(spatialData[1],0,360,0,100);
     trail = 20;
     speed = 0.05;
     circleSize = 300;
     toggleDirection();
   }
   else if(cuePos < 71){
     speed = 0.05;
     trail = 15;
     toggleDirection();
     circleSize = map(spatialData[3],0,360,50,300);
   }
   else if (cuePos < 75) {
     xModifier = map(spatialData[2],0,360,0,100);
     yModifier = map(spatialData[2],0,360,0,100);
     circleSize = 400;
     trail = 10;
     speed = 0.5;
   }
   else if (cuePos < 80) {
     xModifier = map(spatialData[1],0,360,-10,10);
     yModifier = map(spatialData[3],0,360,-10,10);
     trail = 40;
     speed = 0.07;
     line = 7;  
     if(lastCue != cuePos){ circleSize -= 30;lastCue = cuePos; }  
   }
   else if (cuePos < 96) {
     xModifier = map(spatialData[1],0,360,0,200);
     yModifier = map(spatialData[1],0,360,0,150);
     trail = 30;
     speed = 0.03;
     toggleDirection();     
   }
   else if (cuePos < 101) {
     circleSize = map(spatialData[2],0,360,-400,400);
     toggleDirection();
     trail = 30;
     speed = 0.6;      
   }
   else if (cuePos < 114) {
     toggleDirection();
     trail = 60;
     speed = 0.01;      
   }
   else if (cuePos < 122) {
     toggleDirection();
     trail = 30;
     speed = 0.05;     
   }   
   else if (cuePos < 173) {
     xModifier = map(spatialData[1],0,360,-200,200);
     circleSize = map(spatialData[2],0,360,10,400);;
     trail = 10;
     speed = 0.04;      
   }
   else if (cuePos < 210) {
     circleSize = map(spatialData[2],0,360,-400,400);
     xModifier = map(spatialData[4],0,360,-200,200);
     toggleDirection();
     trail = 30;
     speed = 0.1;
     line = 7;     
   }
   else if (cuePos < 300) {
     toggleDirection();
     circleSize = 350;
     trail = 50;
     speed = 0.01;
     line = 7;      
   }
   
  
  
  
}