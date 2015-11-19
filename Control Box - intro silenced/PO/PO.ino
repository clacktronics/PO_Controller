#include <avr/pgmspace.h>
//#include <Flash.h>
#include "sequence_data.h"

int pinmap[8] = {6,2,9,11,7,5,10,12}; // New pinmap reflects timers
int pin,sequence_length,sequence_loops,sequenceR;

void setup() {

Serial.begin(250000);
  
TCCR4B = TCCR4B & 0b11111000 | 0x04; //1&5
TCCR3B = TCCR3B & 0b11111000 | 0x05; //2&6
TCCR2B = TCCR2B & 0b11111000 | 0x04; //3&7
TCCR1B = TCCR1B & 0b11111000 | 0x03; //4&8

for (int i=0;i<8;i++){ pinMode(pinmap[i],OUTPUT);  }

pinMode(A0,INPUT);
digitalWrite(A0,HIGH);


}

void(* resetFunc) (void) = 0; //declare reset function @ address 0


void loop() {

sequence_length = sizeof(sequence)/9; // 9 bytes an array
sequence_loops = sizeof(loops)/6; // 3 * 2 bytes and array

int total_steps = 0;
long total_time = 0;

for(int x = 0; x < sequence_loops; x ++)
{

  // get amount of steps in 1 loop
  int lsteps = (loops[x][1] - loops[x][0]) + 1;
  // Multiply it about amount of loops
  lsteps *= loops[x][2];
  // add this to the total step count so far
  total_steps += lsteps;
  
  
  // get delay time for 1 loop by adding up the delay times.
  long ldelay = 0;
  for(int i = loops[x][0];i<=loops[x][1];i++) {ldelay += pgm_read_byte(&(sequence[i][8]));}
  Serial.print("Loop: ");Serial.print(x); Serial.print(" In one loop "); Serial.print(ldelay); Serial.print("0 mSeconds. So over ");  Serial.print(loops[x][2]); 
  // multiply this by number of loops
  ldelay *= loops[x][2];
  total_time += ldelay;
  Serial.print(" loops ");
  Serial.print(ldelay);
  Serial.println("0 mSeconds");
}
Serial.print("There are "); Serial.print(total_time);Serial.println("0 total mS.");
Serial.println(" ");

int total_s = total_time / 100;
float delay_seconds = float(delay_time)/1000;
int sequence_duration_mins = total_s/60;
int sequence_duration_seconds = total_s%60;

Serial.println("Paris Opera Sequencer");
Serial.println("---------------------");
Serial.println(" ");
Serial.print("There are ");Serial.print(sequence_loops);Serial.print(" loops and ");Serial.print(sequence_length);Serial.println(" steps.");
Serial.print("Total steps considering loops are ");Serial.print(total_steps);Serial.println(",");
Serial.print("so at ");Serial.print(total_time);Serial.print("0 milliseconds would run for approx ");Serial.print(sequence_duration_mins);Serial.print(':');Serial.print(sequence_duration_seconds);Serial.println(" minuties.");
Serial.println(" ");
Serial.println("'s' to start and 'x' to reset");
Serial.println(" ");



// wait for 's' over serial to start
while(Serial.read() != 's' && digitalRead(A0)) {}


for(int x = 0; x < sequence_loops; x ++)
{
  Serial.print("Sequence ");
  Serial.println(x+1);
  Serial.println("==========");
  for(int l = 0;l<loops[x][2];l++)
  {
    for(int i = loops[x][0]; i <= loops[x][1]; i++)
    {
    writeStep(i);
    delay(pgm_read_byte(&(sequence[i][8])) * 10);
    if(Serial.read() == 'x') {writeAll(0); Serial.println("RESET");Serial.println(" "); resetFunc();}
    }
  Serial.println(" ");
  }
}

Serial.println("END");


}



void writeStep(int m) {

  for (int i=0;i<8;i++){ 
    int pin = pinmap[i];
    int fromP = pgm_read_byte(&(sequence[m][i]));
    int value = map(fromP,0,3,0,255);
    Serial.print(fromP);
    analogWrite(pin,value) ;
    }
  Serial.println(" ");
  
}

void writeAll(int val) {
    for (int i=0;i<8;i++){ 
    int pin = pinmap[i];
    analogWrite(pin,val) ;
    }
}


